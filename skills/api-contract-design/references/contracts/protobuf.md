# Protobuf Contract

## Contents

- Scope
- Edition Rules
- File Layout
- Naming
- Fields
- Enums
- Services
- Constraints
- Compatibility Rules
- Anti-Patterns
- Checklist
- Sources

## Scope

- Authoring rules for `.proto` files describing gRPC services and message types.
- Baseline Edition 2024; fallback proto3. Messages also serve as payload schemas for binary messaging when the project uses Protobuf there.

## Edition Rules

- `edition = "2024";` replaces `syntax = "proto3";`; the wire format is unchanged by editions.
- Behaviors are controlled by features:

| Feature                              | Values                                                  | Controls                             |
| ------------------------------------ | ------------------------------------------------------- | ------------------------------------ |
| `features.field_presence`            | `EXPLICIT`, `IMPLICIT`, `LEGACY_REQUIRED`               | Whether unset differs from default   |
| `features.enum_type`                 | `OPEN`, `CLOSED`                                        | Handling of unknown enum numbers     |
| `features.repeated_field_encoding`   | `PACKED`, `EXPANDED`                                    | Wire encoding of repeated scalars    |
| `features.utf8_validation`           | `VERIFY`, `NONE`                                        | UTF-8 checking of strings            |
| `features.message_encoding`          | `LENGTH_PREFIXED`, `DELIMITED`                          | Encoding of sub-messages             |
| `features.json_format`               | `ALLOW`, `LEGACY_BEST_EFFORT`                           | JSON mapping strictness              |
| `features.enforce_naming_style`      | `STYLE2024`, `STYLE_LEGACY`                             | Naming-style enforcement             |
| `features.default_symbol_visibility` | `EXPORT_ALL`, `EXPORT_TOP_LEVEL`, `LOCAL_ALL`, `STRICT` | Which symbols other files may import |

- Features are set at file level and overridden at message, field, enum, or other levels.
- Edition 2024 grammar:
  - No `required` label; use `LEGACY_REQUIRED` only for legacy compatibility.
  - No `optional` label needed; explicit presence is the default.
  - `reserved` names are unquoted identifiers.
  - No `import weak`; `import option` imports custom options only.
  - `export` and `local` keywords control symbol visibility.
  - No `ctype` field option.
- Mixed projects may import proto2 and proto3 files from editions files and the reverse.
- Use proto3 only when the project toolchain does not support editions; then `syntax = "proto3";`, explicit `optional` for presence, and quoted `reserved` names.

## File Layout

- One file per cohesive set of messages and services; file name `lower_snake_case.proto`.
- Package with major version: `company.domain.v1`; directory structure mirrors the package.
- Order: edition/syntax, package, imports, file options, then definitions.
- Header notes as a leading comment block.
- Import only what is used; avoid cyclic imports.

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

Example: removing a field safely.

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
- Each RPC has unique request and response messages.
- Comment each RPC with behavior, idempotency, error codes, and deadline expectations.

## Constraints

- Core Protobuf has no min, max, or pattern keywords.
- Value constraints use Protovalidate (`buf.validate`) annotations:
  - Standard rules per field type: string length and pattern, numeric ranges, repeated size limits, required fields.
  - Custom rules written in CEL.
- Import the Protovalidate definitions and annotate fields; state in the header notes that Protovalidate is a Buf ecosystem convention, not a Protobuf standard.
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

- Compatible: add fields with new numbers; add enum values; add RPCs and services; add new messages.
- Breaking: remove or renumber fields; change a field's type to an incompatible one; change field presence semantics; reuse numbers or names; rename a package, service, or RPC; change an RPC's streaming shape.
- Removing a field: `reserved` its number and name.
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
- [ ] Constraints expressed by annotations or comments.
- [ ] RPC comments list errors, idempotency, and deadlines.
- [ ] Header notes present.

## Sources

- Protobuf Editions overview and feature settings (https://protobuf.dev/editions/overview/, https://protobuf.dev/editions/features/).
- Protocol Buffers style guide and language guide (editions).
- Protovalidate documentation (https://buf.build/docs/protovalidate).
