# Protobuf Contract

## Scope

- Authoring rules for `.proto` files describing gRPC services and message types.
- Baseline Edition 2026; fallback Edition 2024, then proto3 only for legacy toolchains. Messages also serve as payload schemas for binary messaging when the project uses Protobuf there.

## Edition Rules

- `edition = "2026";` is the current baseline and replaces `syntax = "proto3";`; editions preserve Protobuf wire-format compatibility when the same field numbers and types are used. Edition 2026 requires `protoc` 36.0 or later; Edition 2024 requires 32.0 or later. Confirm runtime and generated-code support too.
- Behaviors are controlled by features:
  | Feature                              | Values                                                  | Controls                                        |
  | ------------------------------------ | ------------------------------------------------------- | ----------------------------------------------- |
  | `features.field_presence`            | `EXPLICIT`, `IMPLICIT`, `LEGACY_REQUIRED`               | Whether unset differs from default              |
  | `features.enum_type`                 | `OPEN`, `CLOSED`                                        | Handling of unknown enum numbers                |
  | `features.repeated_field_encoding`   | `PACKED`, `EXPANDED`                                    | Wire encoding of repeated scalars               |
  | `features.utf8_validation`           | `VERIFY`, `NONE`                                        | UTF-8 checking of strings                       |
  | `features.message_encoding`          | `LENGTH_PREFIXED`, `DELIMITED`                          | Encoding of sub-messages                        |
  | `features.json_format`               | `ALLOW`, `LEGACY_BEST_EFFORT`                           | JSON mapping strictness                         |
  | `features.enforce_naming_style`      | `STYLE2026`, `STYLE2024`, `STYLE_LEGACY`                | Naming-style enforcement                        |
  | `features.enforce_proto_limits`      | `PROTO_LIMITS2026`, `LEGACY_NO_EXPLICIT_LIMITS`         | Compiler limits for messages, oneofs, and enums |
  | `features.default_symbol_visibility` | `EXPORT_ALL`, `EXPORT_TOP_LEVEL`, `LOCAL_ALL`, `STRICT` | Which symbols other files may import            |
- Edition 2026 changes defaults, including `STYLE2026` naming, strict symbol visibility, and `PROTO_LIMITS2026`; do not assume Edition 2024 defaults. Features can be set at the allowed scope and overridden at narrower scopes. Check the feature's allowed scope before setting it explicitly; `enforce_proto_limits` is not a file-level option.
- Edition 2026 supports custom ProtoJSON strings for enum values through `(pb.enumvalue.json).string`. This changes JSON representation, not the numeric Protobuf wire value. Use it only when every relevant parser, serializer, generated-code runtime, and gateway supports the option; treat the chosen JSON string as a compatibility-sensitive contract value.
- Edition grammar (verify against the selected edition):
  - No `required` label; use `LEGACY_REQUIRED` only for legacy compatibility.
  - No `optional` label needed; explicit presence is the default.
  - `reserved` names are unquoted identifiers.
  - No `import weak`; `import option` imports custom options only.
  - `export` and `local` keywords control symbol visibility. Under Edition 2026 `STRICT`, messages and enums are local by default; export only top-level types intentionally imported by other `.proto` files. Keep service-specific request/response and helper messages local when they are used only in the service file. Service declarations themselves are not importable message/enum types and cannot be marked `export`.
  - No `ctype` field option.
- Mixed projects may import proto2 and proto3 files from editions files and the reverse.
- Use Edition 2024 when the compiler/runtime does not support Edition 2026. Use proto3 only when the project toolchain does not support editions; then `syntax = "proto3";`, explicit `optional` for scalar presence where needed, and quoted `reserved` names.

## File Layout

- Preserve the project's `.proto` package, module, and import layout; file name `lower_snake_case.proto`.
- Package names normally carry a major API version (for example `company.domain.v1`); use the project's established package policy.
- Within a file, order declarations consistently: edition/syntax, package, imports, file options, then definitions.
- Use comments on services, RPCs, messages, and fields to describe the element they accompany. Keep cross-cutting transport, authentication, and operational policies in maintained API documentation when they cannot be expressed at the relevant declaration.
- Import only what is used; avoid cyclic imports. Keep imported definitions stable and available to the generated-code toolchain.

## Naming

| Element                     | Style                                           |
| --------------------------- | ----------------------------------------------- |
| Message, enum, service, RPC | `PascalCase`                                    |
| Field, oneof                | `lower_snake_case`                              |
| Enum value                  | `UPPER_SNAKE_CASE`, prefixed with the enum name |
| Package                     | lowercase dotted                                |

- Repeated field names are plural.
- Service names end in `Service`; request and response messages end in `Request` and `Response`.

## Fields

- Field numbers 1–15 use one tag byte; reserve them for frequent fields.
- Never change or reuse a field number; the number identifies the field on the wire.
- Scalar types: choose `int64`/`uint64`/`sint64` by value range and sign pattern; `string` for UTF-8 text; `bytes` for binary.
- Time: `google.protobuf.Timestamp`; durations: `google.protobuf.Duration`; masks: `google.protobuf.FieldMask`; flexible structures only when unavoidable: `google.protobuf.Struct`/`Any`.
- Presence: explicit presence distinguishes unset from default; use it for values where "unset" matters (partial updates, optional filters). Implicit presence only where the default value is meaningless as a distinct state.
- `oneof` for mutually exclusive fields; adding a field to an existing `oneof` is compatible, moving existing fields into one is not.
- `map<K, V>` for dictionaries; keys are integral or string types.
- Mark deprecated fields `[deprecated = true]`.
- Document each field in a comment: meaning, units, bounds, and whether it is output-only.

**Example:** removing a field safely.

```proto
// Before
message Order {
  string id = 1;
  OrderStatus status = 2;
  string coupon_code = 3;
}

// After: number and name are reserved, never reused.
message Order {
  string id = 1;
  OrderStatus status = 2;
  reserved 3;
  reserved coupon_code;
  string note = 4;
}
```

## Enums

- First value is the zero value and is named `<ENUM>_UNSPECIFIED`.
- Value names are prefixed with the enum name.
- Open enums (default in editions) preserve unknown numbers; consumers handle unknown values.
- Never reuse a number; `reserved` removed numbers and names.

```proto
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_PAID = 2;
}
```

## Services

- One service per capability; RPCs follow the gRPC reference (shapes, naming, errors).
- Prefer dedicated request and response types per RPC so each method can evolve independently. Reuse a message only when its direction, semantics, and constraints are genuinely identical (for example, a symmetric bidirectional-stream frame). Keep service-specific request/response types local by default under Edition 2026 `STRICT`; export a type only when another `.proto` file must import it.
- Comment each RPC with behavior, idempotency, error codes, and deadline expectations.

## Constraints

- Core Protobuf has no min, max, or pattern keywords.
- Value constraints use Protovalidate (`buf.validate`) annotations:
  - Standard rules per field type: string length and pattern, numeric ranges, repeated size limits, required fields.
  - Custom rules written in CEL.
- Import Protovalidate definitions and annotate fields only when the project declares and supports the dependency. Identify Protovalidate accurately as a Buf ecosystem project, not a Protobuf language feature; pin compatible plugin/runtime versions in project configuration.
- When the project does not use Protovalidate, state constraints in field comments.

```proto
import "buf/validate/validate.proto";

message CreateOrderRequest {
  string request_id = 1 [(buf.validate.field).string.uuid = true];
  string note = 2 [(buf.validate.field).string.max_len = 500];
  repeated string tags = 3 [(buf.validate.field).repeated.max_items = 20];
}

message DateRange {
  option (buf.validate.message).cel = {
    id: "date_range.order"
    message: "end must not be before start"
    expression: "this.end >= this.start"
  };
  google.protobuf.Timestamp start = 1;
  google.protobuf.Timestamp end = 2;
}
```

## Compatibility Rules

- **Compatible:** add fields with new numbers; add enum values; add RPCs and services; add new messages.
- **Breaking:** remove or renumber fields; change a field's type to an incompatible one; change field presence semantics; reuse numbers or names; rename a package, service, or RPC; change an RPC's streaming shape.
- When removing a field, `reserved` its number and name.
- Changing between wire-compatible scalar types is possible only within documented compatible groups; treat it as breaking unless the Protobuf documentation lists it as compatible.
- Breaking changes require a new package version.

## Anti-Patterns

- Reusing field numbers.
- Enum without a zero `_UNSPECIFIED` value.
- Sharing one message across unrelated RPCs.
- `Any` or `Struct` for data with a known shape.
- Constraints undocumented because the format cannot express them.
- Unversioned packages.

## Checklist

- [ ] `edition` (or `syntax`) declared; package versioned.
- [ ] Naming follows the table; enum zero values named `_UNSPECIFIED`.
- [ ] Field numbers never reused; removed ones reserved.
- [ ] Presence semantics chosen per field.
- [ ] Edition-specific features and ProtoJSON enum strings are supported by the complete compiler/runtime/toolchain; JSON representation changes are reviewed for compatibility.
- [ ] Constraints expressed by annotations or comments.
- [ ] RPC comments list errors, idempotency, and deadlines.
- [ ] Public services, RPCs, messages, and fields have useful element-level comments where needed; transport and runtime policies are documented and enforced separately.
- [ ] Under Edition 2026 `STRICT`, only reusable cross-file message/enum entry points are exported; service-local request/response and helper types remain local unless cross-file reuse is required.
