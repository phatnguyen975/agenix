# API Contract Design Evaluation

Two read-only [scenarios](scenarios.json) passed semantic assessment in fresh contexts using inherited model settings. Give the raw request and the runtime skill path, keep the rubric private, and assess the actual response against the expected and prohibited behaviors.

## Coverage

- `external-query-compatibility` kept the caller's sections, provider revision and ownership. It identified the breaking method change and the difference between wire and toolchain support.
- `publisher-perspective-with-open-binding` proposed a send-only AsyncAPI outline with stable event identity. It left unselected broker and lifecycle choices open and distinguished manual reasoning from validation.

Static maintainer checks cover metadata, routing, YAML duplicate keys and local references, plus basic checks of selected example values. The behavioral cases use explicit skill selection and supplied context. They do not establish automatic routing, full format conformance, compiler compatibility or runtime behavior. Final editorial and reference updates received static review. No runner or inference dependency was added.
