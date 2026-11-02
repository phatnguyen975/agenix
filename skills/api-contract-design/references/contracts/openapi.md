# OpenAPI Contract

## Contents

- Scope
- Version Rules
- Document Structure
- Operations
- Parameters
- Request Bodies and Media Types
- Responses
- Components
- Security Schemes
- Webhooks and Callbacks
- Streaming (SSE)
- Tags, Examples, Discriminator
- Authoring Rules
- Anti-Patterns
- Checklist
- Sources

## Scope

- Authoring rules for OpenAPI documents describing REST, SSE, and webhooks.
- Baseline 3.2.1; fallback 3.1.2. Fields marked (3.2) exist only in 3.2.x documents.
- Field types and constraints inside schemas follow the schema-modeling rules.

## Version Rules

- `openapi: 3.2.1` for new documents; keep the project's version for existing documents.
- Patch versions fix errors and clarify text; tooling treats all 3.2.x documents as the same feature set.
- Upgrading 3.1 to 3.2 is a version change plus optional adoption of new fields; the Schema Object stays a superset of JSON Schema 2020-12.
- `info.version` is the API contract version, not the OpenAPI version.
- Under 3.1, `query`, `additionalOperations`, `in: querystring`, `itemSchema`, `$self`, and the device authorization flow are unavailable; use the alternatives noted below.

## Document Structure

| Field               | Required                                 | Use                                                                                                          |
| ------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `openapi`           | Yes                                      | Specification version                                                                                        |
| `$self` (3.2)       | No                                       | Base URI of the document for relative references                                                             |
| `info`              | Yes                                      | `title`, `version` required; `summary`, `description` (header notes), `termsOfService`, `contact`, `license` |
| `jsonSchemaDialect` | No                                       | Default `$schema` for Schema Objects; omit to use the OAS dialect                                            |
| `servers`           | No                                       | Base URLs, with `variables`; (3.2) `name`                                                                    |
| `paths`             | One of `paths`, `components`, `webhooks` | Path items                                                                                                   |
| `webhooks`          | No                                       | Provider-initiated requests                                                                                  |
| `components`        | No                                       | Reusable objects                                                                                             |
| `security`          | No                                       | Default security requirements                                                                                |
| `tags`              | No                                       | Tag metadata and grouping                                                                                    |
| `externalDocs`      | No                                       | Link to further documentation                                                                                |

## Operations

- Path item methods: `get`, `put`, `post`, `delete`, `options`, `head`, `patch`, `trace`; (3.2) `query`; (3.2) `additionalOperations` for other HTTP methods.
- Operation fields: `tags`, `summary`, `description`, `externalDocs`, `operationId`, `parameters`, `requestBody`, `responses` (required), `callbacks`, `deprecated`, `security`, `servers`.
- `operationId`: unique across the document, stable, `camelCase`; code generators use it, so renaming is breaking for generated clients.
- `summary` is one line; `description` states behavior, preconditions, side effects, and idempotency.
- Mark deprecated operations with `deprecated: true` and name the replacement in the description.
- Under 3.1, describe a body-bearing read as `post` and state in the description that it is safe.

| Good `operationId`                                     | Bad                            |
| ------------------------------------------------------ | ------------------------------ |
| `listOrders`, `getOrder`, `createOrder`, `cancelOrder` | `orders_get`, `Order1`, `doIt` |

## Parameters

- Fields: `name`, `in` (`query`, `header`, `path`, `cookie`; (3.2) `querystring`), `description`, `required`, `deprecated`, `allowEmptyValue`, `style`, `explode`, `allowReserved`, `schema` or `content`, `example`/`examples`.
- Path parameters are always `required: true`.
- Every parameter has a schema with type and bounds; set defaults and maximums for paging parameters.
- Reuse shared parameters through `components.parameters`.
- (3.2) `in: querystring` describes the whole query string as one schema through `content`; do not mix it with `in: query` in one operation.
- Header parameters named `Content-Type`, `Accept`, and `Authorization` are not declared as parameters; use `requestBody` media types and `security`.

```yaml
parameters:
  - name: limit
    in: query
    description: Page size; default 20, maximum 100.
    schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
  - name: orderId
    in: path
    required: true
    schema: { type: string, maxLength: 64 }
```

## Request Bodies and Media Types

- `requestBody`: `description`, `content` (required), `required`.
- Media type object: `schema`, (3.2) `itemSchema`, `example`/`examples`, `encoding`, (3.2) `prefixEncoding`, `itemEncoding`.
- Declare every accepted media type; JSON default `application/json`; PATCH formats `application/merge-patch+json` or `application/json-patch+json`.
- Binary content: schema with `contentMediaType` (and `contentEncoding` for base64); multipart: `multipart/form-data` with `encoding` per part.
- Create, update, and read schemas are separate components when their fields differ.

## Responses

- `responses` is a map of status codes (`200`, `4XX` ranges, `default`); list every status the operation can return.
- Response fields: (3.2) `summary`; `description` (required in 3.1, optional in 3.2; always write it); `headers`; `content`; `links`.
- Declare response headers that clients rely on: `Location`, `ETag`, `Retry-After`, `RateLimit`, `RateLimit-Policy`, `Deprecation`, `Sunset`, `Link`.
- Error responses reference one shared Problem Details schema with media type `application/problem+json`.
- `default` covers unexpected errors only; it does not replace explicit statuses.

```yaml
responses:
  "404":
    description: Order not found.
    content:
      application/problem+json:
        schema: { $ref: "#/components/schemas/Problem" }
        examples:
          missing:
            summary: Unknown identifier
            value:
              type: https://example.com/problems/not-found
              title: Order not found
              status: 404
              detail: No order with identifier ord_01HZX.
              instance: /requests/9f2c
```

## Components

- Maps: `schemas`, `responses`, `parameters`, `examples`, `requestBodies`, `headers`, `securitySchemes`, `links`, `callbacks`, `pathItems`, (3.2) `mediaTypes`.
- Component names match `^[a-zA-Z0-9._-]+$`; use `PascalCase` for schemas.
- Define each reusable thing once and reference with `$ref`; never copy definitions between operations.
- Shared building blocks to define: `Problem`, `Error` extensions, pagination parameters, rate-limit headers, idempotency header, common responses (`Unauthorized`, `Forbidden`, `NotFound`, `TooManyRequests`).

## Security Schemes

| `type`          | Fields                                                                                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `apiKey`        | `name`, `in` (`query`, `header`, `cookie`)                                                                                                                         |
| `http`          | `scheme` (`basic`, `bearer`, ...), `bearerFormat`                                                                                                                  |
| `mutualTLS`     | none                                                                                                                                                               |
| `oauth2`        | `flows`: `implicit`, `password`, `clientCredentials`, `authorizationCode`, (3.2) `deviceAuthorization`; each flow has URLs and `scopes`; (3.2) `oauth2MetadataUrl` |
| `openIdConnect` | `openIdConnectUrl`                                                                                                                                                 |

- Common field: `description`; (3.2) `deprecated`.
- Security requirement semantics: array items are alternatives (OR); keys inside one object are combined (AND).
- Declare default `security` at the root; override per operation; `security: []` marks a deliberately public operation.
- List scopes per operation.
- Avoid declaring `implicit` and `password` flows in new contracts (current OAuth security guidance discourages them).

```yaml
# Alternatives (OR): either credential is accepted.
security:
  - OAuth2: [orders:read]
  - ApiKeyAuth: []
# Combined (AND): both credentials are required in one requirement object.
security:
  - OAuth2: [orders:read]
    ApiKeyAuth: []
# Public operation:
security: []
```

## Webhooks and Callbacks

- `webhooks`: map of names to path items describing requests the provider sends to consumers (event delivery).
- `callbacks` on an operation: requests the provider sends to a URL supplied in that operation's request, using runtime expressions such as `{$request.body#/callbackUrl}`.
- Describe the signature and delivery headers as header parameters on the webhook operation.
- Subscription management is a normal REST path set in `paths`.

```yaml
webhooks:
  orderPaid:
    post:
      operationId: orderPaidWebhook
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/OrderEvent" }
      responses:
        "2XX": { description: Event acknowledged. }
```

## Streaming (SSE)

- (3.2) `text/event-stream` response with `itemSchema` describing one event; use `data` with `contentMediaType` and `contentSchema` for JSON payloads.
- Other sequential types are described with `itemSchema` as well (for example JSON Lines or `multipart/mixed`).
- Under 3.1: media type `text/event-stream` with a string schema and the event format in the description.

## Tags, Examples, Discriminator

- Tag object: `name`, `description`, `externalDocs`; (3.2) `summary`, `parent`, `kind`.
- Example object: `summary`, `description`, `value`, `externalValue`; (3.2) `dataValue`, `serializedValue`.
- Every request and response media type has at least one example that validates against its schema; mutually exclusive variants use `examples`.
- Discriminator: `propertyName`, `mapping`; (3.2) `defaultMapping`. Use with `oneOf` for polymorphic payloads.

## Authoring Rules

- Header notes go in `info.description` as the first section.
- Every operation has `operationId`, `summary`, `tags`, `security`, `responses`.
- Reuse over repetition: schemas, parameters, responses, and headers live in `components`.
- Nullable values use type arrays (`type: [string, "null"]`), not `nullable`.
- Unused components are removed.
- Server URLs contain no real hosts or credentials; use documented placeholders and `variables`.
- Order: `info`, `servers`, `security`, `tags`, `paths`, `webhooks`, `components`.

## Anti-Patterns

- Duplicate schema definitions per operation.
- Missing error responses; only `200`.
- `additionalProperties: true` on request schemas by accident.
- Unbounded strings, arrays, and numbers.
- Inline anonymous schemas that generators name unpredictably.
- `operationId` omitted or renamed casually.
- Examples that do not validate.
- Real tokens or customer data in examples.

## Checklist

- [ ] `openapi` version is baseline or recorded fallback.
- [ ] Header notes in `info.description`.
- [ ] Every operation: unique `operationId`, `security`, all statuses, examples.
- [ ] Shared Problem Details schema used by every error response.
- [ ] Paging, idempotency, rate-limit, and caching headers declared where relevant.
- [ ] All reusable objects in `components` and referenced.
- [ ] 3.2-only fields appear only in 3.2.x documents.

## Sources

- OpenAPI Specification 3.2.1 and 3.1.2 (https://spec.openapis.org/oas/latest.html).
- OpenAPI Initiative release announcement for 3.2.
