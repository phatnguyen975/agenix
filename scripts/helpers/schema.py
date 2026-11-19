"""Evaluate the Draft 2020-12 vocabulary used by bundled schemas."""

import re
from datetime import datetime
from urllib.parse import unquote, urlsplit

from .core import Invalid, contained, https, read_json

DRAFT = "https://json-schema.org/draft/2020-12/schema"
KEYWORDS = {
    "$schema",
    "$id",
    "$defs",
    "$ref",
    "title",
    "description",
    "default",
    "examples",
    "type",
    "enum",
    "const",
    "pattern",
    "format",
    "minLength",
    "minItems",
    "minimum",
    "uniqueItems",
    "items",
    "contains",
    "properties",
    "required",
    "additionalProperties",
    "dependentRequired",
    "allOf",
    "anyOf",
    "oneOf",
    "not",
    "if",
    "then",
    "else",
}


def equal(left, right):
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            equal(left[k], right[k]) for k in left
        )
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(equal(a, b) for a, b in zip(left, right))
    return left == right


def typed(value, name):
    if name == "integer":
        return type(value) is int or type(value) is float and value.is_integer()
    types = {
        "object": (dict,),
        "array": (list,),
        "string": (str,),
        "number": (int, float),
        "boolean": (bool,),
        "null": (type(None),),
    }
    if name not in types:
        raise Invalid(f"Unsupported schema type: {name}")
    return type(value) in types[name]


class Schemas:
    def __init__(self, root):
        self.root = root.resolve()
        self.documents = {}

    def load(self, path):
        if path not in self.documents:
            document = read_json(path)
            if not isinstance(document, dict) or document.get("$schema") != DRAFT:
                raise Invalid("Expected a bundled Draft 2020-12 schema")
            self.inspect(document)
            self.documents[path] = document
        return self.documents[path]

    def inspect(self, node):
        if isinstance(node, bool):
            return
        if not isinstance(node, dict):
            raise Invalid("Expected a schema object")
        if unknown := node.keys() - KEYWORDS:
            raise Invalid(f"Unsupported schema keyword: {min(unknown)}")
        for key in ("$defs", "properties"):
            for child in node.get(key, {}).values():
                self.inspect(child)
        for key in ("allOf", "anyOf", "oneOf"):
            for child in node.get(key, []):
                self.inspect(child)
        for key in (
            "items",
            "contains",
            "additionalProperties",
            "not",
            "if",
            "then",
            "else",
        ):
            if key in node:
                self.inspect(node[key])

    def reference(self, document, reference):
        uri = urlsplit(reference)
        if uri.scheme or uri.netloc or uri.query or uri.path.startswith("/"):
            raise Invalid("Schema references must stay within the installed bundle")
        if uri.path:
            # Schema includes such as ../evidence are allowed inside the bundle.
            document = (document.parent / unquote(uri.path)).resolve()
            if not document.is_relative_to(self.root):
                raise Invalid("Schema reference escapes the bundle")
        target = self.load(document)
        fragment = unquote(uri.fragment)
        if fragment and not fragment.startswith("/"):
            raise Invalid("Expected a JSON Pointer schema reference")
        for segment in fragment.split("/")[1:]:
            try:
                target = target[segment.replace("~1", "/").replace("~0", "~")]
            except (KeyError, TypeError) as exc:
                raise Invalid("Unresolved schema reference") from exc
        return document, target

    def validate(self, path, value, pointer=""):
        document = contained(self.root, path)
        schema_path, schema = self.reference(document, "#" + pointer)
        if error := self.check(schema_path, schema, value, "$"):
            raise Invalid(error)

    def check(self, document, node, value, location, depth=0):
        if depth > 128:
            raise Invalid("Schema evaluation depth exceeded")
        if isinstance(node, bool):
            return None if node else f"{location}: rejected by schema"

        def check(schema, instance=value, path=location, source=document):
            return self.check(source, schema, instance, path, depth + 1)

        def require(condition, message):
            return None if condition else f"{location}: {message}"

        if "$ref" in node:
            source, target = self.reference(document, node["$ref"])
            if error := check(target, source=source):
                return error
        if "type" in node:
            names = node["type"]
            if not any(
                typed(value, name)
                for name in ([names] if isinstance(names, str) else names)
            ):
                return require(False, f"expected {names}")
        if "const" in node and not equal(value, node["const"]):
            return require(False, "unexpected constant")
        if "enum" in node and not any(equal(value, choice) for choice in node["enum"]):
            return require(False, "value outside allowed set")
        for key in ("allOf", "anyOf", "oneOf"):
            if key in node:
                results = [check(choice) for choice in node[key]]
                matches = results.count(None)
                if key == "allOf" and matches != len(results):
                    return next(error for error in results if error)
                if key == "anyOf" and not matches or key == "oneOf" and matches != 1:
                    return require(False, f"value does not satisfy {key}")
        if "not" in node and check(node["not"]) is None:
            return require(False, "value matches excluded shape")
        if "if" in node:
            branch = "then" if check(node["if"]) is None else "else"
            if branch in node and (error := check(node[branch])):
                return error
        if isinstance(value, str):
            if len(value) < node.get("minLength", 0):
                return require(False, "value too short")
            if "pattern" in node and not re.search(node["pattern"], value):
                return require(False, "invalid pattern")
            if "format" in node and not valid_format(node["format"], value):
                return require(False, f"invalid {node['format']}")
        if (
            type(value) in (int, float)
            and "minimum" in node
            and value < node["minimum"]
        ):
            return require(False, "value below minimum")
        if isinstance(value, list):
            if len(value) < node.get("minItems", 0):
                return require(False, "too few items")
            if node.get("uniqueItems") and any(
                equal(a, b) for i, a in enumerate(value) for b in value[:i]
            ):
                return require(False, "duplicate array item")
            if "contains" in node and not any(
                check(node["contains"], item) is None for item in value
            ):
                return require(False, "required array member is missing")
            for index, item in enumerate(value):
                if error := check(
                    node.get("items", True), item, f"{location}[{index}]"
                ):
                    return error
        if isinstance(value, dict):
            required = set(node.get("required", []))
            for key in value:
                required.update(node.get("dependentRequired", {}).get(key, []))
            if missing := required - value.keys():
                return require(False, f"missing {', '.join(sorted(missing))}")
            properties = node.get("properties", {})
            for key, item in value.items():
                if error := check(
                    properties.get(key, node.get("additionalProperties", True)),
                    item,
                    f"{location}.{key}",
                ):
                    return error
        return None


def valid_format(name, value):
    if name == "uri":
        return https(value)
    if name == "date-time":
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z",
            value,
        ):
            return False
        try:
            datetime.fromisoformat(value)
            return True
        except ValueError:
            return False
    raise Invalid(f"Unsupported schema format: {name}")
