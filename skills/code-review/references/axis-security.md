# Axis: security

## Purpose

Identify vulnerabilities introduced by or materially exposed by the change. Apply security controls to the actual trust boundaries and attack surface; do not assume every project is a web application or that every checklist item applies.

## Method

1. **Establish context and threat model.** Identify assets (credentials, personal/sensitive data, money, privileged operations, availability, intellectual property), actors, entry points, trust boundaries, principals, and data flows changed.
2. For each relevant boundary, consider appropriate STRIDE threats: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege. Write a plausible abuse path: attacker, controlled input/capability, vulnerable behavior, and impact.
3. Inspect the complete changed surface for credentials, secrets, permission changes, unsafe data flow, and new execution/network/file-system capabilities. Do not reproduce secrets in the report; redact them and recommend rotation when exposed.
4. Apply the OWASP Top 10:2025 taxonomy to relevant web/application changes and the OWASP Top 10 for LLM Applications:2026 taxonomy to LLM integrations. Apply other conditional lists only when the changed system meets their scope. Treat taxonomy as a coverage aid, not a claim that every control applies to every project.
5. Follow untrusted data from source to sink, including user input, files, webhooks, external APIs, model output, retrieved content, memory, inter-agent messages, environment data, and build inputs.
6. Verify each finding with a realistic attack path and evidence. Theoretical weaknesses without a plausible path or impact belong in Questions (Low confidence), not confirmed findings. Do not provide working exploit code.

## OWASP Top 10:2025

### A01 — Broken Access Control

- Is authentication required for every protected operation and authorization checked on the server/trusted boundary?
- Is object-level authorization enforced for every resource identifier, including nested resources and cross-tenant access?
- Are function/administrative operations guarded by role/permission checks with deny-by-default behavior?
- Are property-level reads and writes allowlisted so clients cannot read or mass-assign privileged fields (owner, role, tenant, price, status)?
- Are authorization decisions enforced on every request and relevant background/job path, not only in UI/client routing?
- Are service accounts, API keys, tokens, and delegated permissions scoped to the minimum required resources/actions?
- Are direct object references, alternate endpoints, bulk operations, exports, and batch jobs subject to the same authorization model?
- Are user-influenced file paths, redirect targets, resource identifiers, and server-side destinations validated against a policy? For network destinations, see SSRF controls under API/cross-cutting.

### A02 — Security Misconfiguration

- Are debug, verbose errors, test endpoints, default credentials, sample accounts, permissive ACLs, and unnecessary services/features disabled in production?
- Are identities, service accounts, storage, network, containers, and cloud permissions least-privileged?
- Are browser security headers configured for the actual response/content model? Consider CSP (nonce/hash/source policy), HSTS (only when HTTPS/subdomain rollout is safe), `X-Content-Type-Options`, framing controls (`frame-ancestors`/appropriate header), `Referrer-Policy`, and `Permissions-Policy`. Do not force a same-origin-only CSP if the application has justified sources.
- Is CORS limited to required origins, methods, and headers? Do not combine credentialed requests with wildcard origins. A public, non-credentialed resource may legitimately use `*`; validate the actual exposure.
- Are XML parsers configured to prevent unsafe external entity/schema resolution where XML is accepted?
- Are cloud storage buckets, object ACLs, debug/admin interfaces, error pages, and deployment defaults appropriately restricted?
- Are secrets absent from example/config files and supplied through approved secret-management mechanisms?

### A03 — Software Supply Chain Failures

- Dependency manifests, lockfiles, package provenance, package-manager behavior, and install-time scripts are owned by `dependencies`.
- Review here when the change itself downloads, loads, evaluates, or executes untrusted code/data outside the normal dependency-management boundary (for example remote scripts, dynamic plugin loading, model artifacts, or runtime code fetch).

### A04 — Cryptographic Failures

- Is sensitive data protected in transit and at rest according to its classification, threat model, and applicable policy?
- Are current, approved cryptographic libraries and protocols used instead of custom algorithms or deprecated modes?
- Are passwords stored with an adaptive password-hashing scheme (prefer Argon2id where supported; use scrypt/bcrypt/PBKDF2 only with parameters appropriate to current guidance and runtime constraints)? Do not use a fixed work factor as a universal rule.
- Are security tokens, reset secrets, and non-guessable identifiers generated with a cryptographically secure random source?
- Are secret/token comparisons constant-time where timing leakage is relevant?
- Are keys, certificates, salts, peppers, and encryption contexts managed with access control, rotation, revocation, and backup/recovery as required?
- Are authenticated encryption/integrity protections used where tampering must be detected? Are nonces/IVs unique or generated according to the algorithm requirements?

### A05 — Injection

- Are SQL/NoSQL, LDAP, shell/OS commands, search queries, templates, expressions, and other interpreter inputs parameterized or safely constructed rather than concatenated from untrusted data?
- Is output encoded for its exact sink context (HTML text, attribute, script, URL, CSS, terminal, logs) using platform-safe mechanisms?
- Are dangerous HTML/script/markdown rendering and sanitization bypasses justified and constrained?
- Does untrusted input reach dynamic evaluation, deserialization, template compilation, command execution, or unsafe reflection?
- Are file names, archive entries, and structured input protected from traversal, parser confusion, and injection into downstream tools?

### A06 — Insecure Design

- Do plausible abuse cases have controls proportionate to impact (authorization, workflow state, quotas, limits, confirmation, rate controls, fraud/abuse detection)?
- Are trust boundaries and security invariants explicit and enforced in code, not only in prompts or client UI?
- Are multi-step privileged or financial actions authorized against current state and made atomic/idempotent where necessary?
- Are security controls fail-safe and designed for degraded dependencies, partial failures, retries, and concurrency?
- Are privacy/security requirements captured in applicable specs or policies and tested at the enforcing boundary?

### A07 — Authentication Failures

- Are credentials protected against brute force, credential stuffing, enumeration, and abuse without creating trivial account-lockout denial of service?
- Are MFA/passkeys or step-up authentication used for sensitive operations where the threat model/product policy requires them?
- Are sessions rotated after authentication/privilege changes, time-bounded, revocable, and invalidated on logout or credential reset as appropriate?
- For cookie sessions, are `Secure`, `HttpOnly`, and suitable `SameSite`/scope attributes set, with CSRF protection where required?
- Are password-reset, recovery, and verification tokens unpredictable, purpose-bound, short-lived, single-use, and safely delivered?
- Are OAuth/OIDC flows validated as applicable (state, nonce, PKCE, issuer/audience, redirect URI, token signature/expiry, allowed algorithms, key rotation)?
- Are JWT/API tokens validated for the expected issuer, audience, expiry/not-before, signature, key, and algorithm; are token scopes and revocation/rotation appropriate?

### A08 — Software or Data Integrity Failures

- Is deserialization of untrusted data avoided or restricted to safe schemas/types? Are unsafe native object formats/loaders (for example untrusted pickle-like formats) rejected?
- Are updates, artifacts, downloaded code, model/tool files, and deployment bundles authenticated and integrity-checked before use?
- Are webhooks and signed callbacks authenticated, timestamp/replay checked, and bound to the expected event/resource?
- Are archive extraction and file import protected against path traversal, symlink escape, decompression bombs, and overwrite of protected files?
- Are client-supplied prices, roles, ownership, state, and other authoritative values recomputed or verified server-side?
- Are idempotency keys, sequence numbers, and replay protections used where repeated messages/actions could duplicate effects?

### A09 — Security Logging and Alerting Failures

- Are authentication events, authorization denials, privilege changes, secret/key changes, high-impact actions, and relevant security failures recorded?
- Are events attributable to an actor, time, target, outcome, and correlation/request ID without logging secrets or unnecessary sensitive data?
- Is untrusted log content safely encoded/structured to prevent log injection and control-character spoofing?
- Are security logs access-controlled, retained, monitored, and protected against unauthorized alteration/deletion where required?

### A10 — Mishandling of Exceptional Conditions

- Do authorization, validation, signature, and policy failures fail closed rather than grant access or continue with unsafe defaults?
- Do external errors avoid disclosing secrets, stack traces, queries, internal paths, or sensitive configuration to untrusted callers?
- Are security-relevant exceptions surfaced/handled rather than swallowed?
- Are partial failures, cleanup, transaction rollback, and resource release safe when security checks or side effects fail midway?
- Can error handling, fallback, retry, or recovery paths bypass controls that exist on the normal path?

## Cross-cutting Controls

### Input, Parsing, and Resource Limits

- Validate at trust boundaries using schema/type/range/length constraints and canonical parsers. Prefer allowlisted values where the domain has a closed set; do not assume denylist-only validation is sufficient.
- Normalize/validate before authorization decisions where equivalent encodings or identifiers exist; avoid validation/use on different canonical forms.
- Bound request body size, nesting/depth, decompressed size, processing time, batch size, pagination, upload count, and concurrent work.
- Verify uploads by content as well as declared type/extension; store outside executable web roots, use safe names, and apply malware/content scanning where the threat model requires it.

### SSRF and Outbound Requests

- For user/model-controlled URLs or destinations, allowlist scheme/host/port where possible; block loopback, link-local, private, reserved, and metadata destinations when not explicitly required.
- Resolve and validate every address actually connected to; account for DNS rebinding, redirects, IPv4/IPv6 representations, alternate encodings, proxies, and redirects to disallowed destinations.
- Restrict egress at the network/runtime boundary; do not rely only on string checks in application code.
- Apply outbound timeouts, response-size limits, content-type validation, and redirect limits.

### Filesystem and Destructive Path Operations

- Treat a user/model-supplied path as a candidate, never as authorization. Constrain operations to an explicit allowed root and reject root/parent escape.
- Resolve/canonicalize paths and account for symlinks, hard links, mount points, case normalization, and platform-specific separators.
- Close check/use races where an attacker can mutate the path hierarchy; use safe directory/file-handle APIs or equivalent beneath-root/no-follow semantics when available.
- Prove resource ownership and authorization from trusted state; a marker file writable by an attacker is not proof of ownership.
- Make delete/move/overwrite operations narrow, auditable, recoverable, and protected against unintended target selection.

### Secrets and Privacy

- Are secrets absent from source, build output, logs, fixtures, snapshots, and version control? If a real secret is exposed, recommend rotation/revocation, not merely deletion from the diff.
- Are local environment/key files excluded according to repository policy, while example files use unmistakable placeholders?
- Are sensitive fields minimized in prompts, telemetry, API responses, logs, analytics, and crash reports?
- Is personal data collected for a defined purpose, retained only as needed, and deleted across primary stores, backups, caches, indexes, and downstream processors where applicable?
- Are export/deletion/consent and third-party processing controls implemented where required by product policy or law? Do not infer jurisdictional requirements from code alone.

## Conditional Security Profiles

Apply only when the changed component meets the profile scope. Do not re-report an issue already covered by a base category; cross-reference it instead.

### API Security Top 10:2023

Apply when the change exposes or consumes an API.

- **API1 Broken Object Level Authorization:** every operation using a client-controlled object/resource ID checks access to that object.
- **API2 Broken Authentication:** authentication tokens and credential flows resist compromise, forgery, replay, and misuse.
- **API3 Broken Object Property Level Authorization:** responses expose only authorized fields; writes allow only authorized properties (includes excessive data exposure/mass assignment concerns).
- **API4 Unrestricted Resource Consumption:** cap request rates, payloads, batch/page sizes, execution time, concurrency, and paid third-party spend per relevant identity/tenant.
- **API5 Broken Function Level Authorization:** privileged functions/operations require explicit server-side permissions.
- **API6 Unrestricted Access to Sensitive Business Flows:** protect flows vulnerable to automation/abuse at scale (purchases, sign-ups, bookings, inventory claims) with proportionate business controls.
- **API7 Server-Side Request Forgery:** apply outbound destination and egress controls above.
- **API8 Security Misconfiguration:** review API gateway, CORS, debug/documentation endpoints, transports, error handling, and deployment defaults.
- **API9 Improper Inventory Management:** maintain an accurate inventory of hosts, API versions, environments, and data exposure; retire or protect deprecated/debug interfaces.
- **API10 Unsafe Consumption of APIs:** validate third-party API data as untrusted, enforce timeouts/size/type constraints, and handle redirects/errors safely.

### LLM Top 10:2026

Apply when the change sends data to, receives data from, or otherwise integrates a large language model.

- **LLM01 Prompt Injection:** treat direct and indirect user input, retrieved documents, websites, files, tool output, multimodal content, and persistent memory as untrusted data. Do not rely on prompt wording or input filtering alone to enforce authorization; constrain what model output can reach and what actions it can trigger.
- **LLM02 Sensitive Information Disclosure:** prevent unauthorized disclosure of secrets, personal data, private prompts/context, training or retrieval data, and cross-user/tenant information through model output, context assembly, logs, and downstream channels.
- **LLM03 Excessive Agency:** limit model-enabled functionality, permissions, autonomy, tool scope, action count, and side-effect impact. Enforce authorization and critical invariants in deterministic application code; require approval where impact warrants it.
- **LLM04 Supply Chain:** review provenance, integrity, versioning, licensing, and access controls for models, datasets, adapters, plugins, tool servers, model-serving components, and model artifacts. Package-manager manifests, lockfiles, and install scripts remain owned by `dependencies`; assess runtime trust and model/artifact integrity here.
- **LLM05 Data and Model Poisoning:** protect training, fine-tuning, evaluation, feedback, retrieval, and indexing pipelines against malicious or low-integrity data; preserve provenance, validation, review, and rollback capability.
- **LLM06 Unbounded Consumption:** bound tokens, context size, model calls, tool calls, loops, retries, concurrency, execution time, payload sizes, and provider spend by relevant user, tenant, and task.
- **LLM07 Misinformation:** validate model claims used for consequential decisions or actions against appropriate authoritative sources; preserve provenance, communicate uncertainty, and require human review when the impact requires it.
- **LLM08 Hidden Context Exposure:** prevent unintended disclosure of system/developer instructions, hidden context, internal reasoning or other non-user-facing context, retrieved private content, and operational details. Do not store secrets in prompts or rely on prompt secrecy as an access control.
- **LLM09 Vector and Embedding Weaknesses:** enforce tenant- and permission-aware retrieval; control ingestion, indexing, provenance, poisoning, isolation, update/deletion propagation, and retrieval relevance; do not treat vector similarity as authorization.
- **LLM10 Improper Output Handling:** treat model output as untrusted before using it in HTML, SQL, shell, code execution, file paths, URLs, templates, or downstream APIs. Validate, encode, constrain, and authorize at the receiving sink; do not assume model-generated code is safe.

### Agentic Applications Top 10:2026

Apply when the changed component can plan across steps, retain/use memory, call tools, coordinate agents, or act on behalf of a user/system.

- **ASI01 Agent Goal Hijack:** trusted goals/policies are separated from untrusted content; malicious instructions in external artifacts/tool outputs cannot redirect the agent's objective or plan.
- **ASI02 Tool Misuse and Exploitation:** tools are explicitly allowlisted, inputs/schemas validated, outputs treated as untrusted, and side effects constrained.
- **ASI03 Identity and Privilege Abuse:** agents use least-privilege identities or appropriately scoped delegated user identities, short-lived credentials, and action-level authorization; never inherit broader rights than required.
- **ASI04 Agentic Supply Chain Vulnerabilities:** review agent frameworks, tool servers, MCP/connectors, plugins, skills, models, and artifacts for provenance, integrity, identity, and granted capabilities. Package-manager lockfiles and install scripts remain owned by `dependencies`; this profile focuses on the runtime agent/tool trust boundary.
- **ASI05 Unexpected Code Execution (RCE):** generated code/commands are not executed directly from model output; execution is sandboxed with least privilege, resource/network limits, and disposable workspaces where feasible.
- **ASI06 Memory & Context Poisoning:** persistent memory, summaries, retrieved context, and cross-session state have provenance, integrity, scope, expiry/deletion, and tenant/user isolation.
- **ASI07 Insecure Inter-Agent Communication:** agent messages are authenticated, integrity-protected, scoped, replay-resistant, and validated as data rather than trusted instructions.
- **ASI08 Cascading Failures:** bound agent loops, delegation depth, retries, fan-out, tool spend, and deadlines; use checkpoints, cancellation, circuit breakers, and recovery controls.
- **ASI09 Human-Agent Trust Exploitation:** users can distinguish generated/verified content; show source/action details and obtain meaningful confirmation before high-impact actions.
- **ASI10 Rogue Agents:** constrain autonomy and behavior, log attributable actions, monitor deviations, and provide a reliable stop/revoke/containment mechanism.

### Agent Control Standard (ACS)

Use as an optional, implementation-level reference when a changed agent platform exposes lifecycle hooks or a separate policy/guardian layer. ACS is not a replacement for threat modeling, application authorization, or the Agentic Top 10; do not require adoption where the runtime cannot support it.

- Are consequential tool/action requests intercepted before execution at the platform's available pre-action hook, rather than relying only on post-action logging?
- Are policy decisions enforced outside the model's own untrusted reasoning, with deterministic checks for identity, scope, resource, action, and risk where feasible?
- Does the integration make the decision semantics explicit (for example allow, deny, modify, ask for approval, or defer), and are modified arguments revalidated before execution?
- Is the policy/guardian communication authenticated and integrity-protected, with replay protection and bounded timeouts appropriate to the threat model?
- Is the failure posture explicit for guardian timeout, crash, unavailable policy, malformed decision, and transport failure? High-impact actions should not silently proceed when required authorization cannot be obtained; lower-risk fallback behavior must be deliberate and documented.
- Can an auditor reconstruct which agent/session requested an action, what target and arguments were evaluated, which policy decided, the disposition, and the final outcome without exposing secrets?
- Is the runtime inventory of agent identity, models, tools, and dependencies available or discoverable where the deployment needs it? Treat inventory claims as evidence only when the implementation actually emits and maintains them.
- Are hooks and controls tested at the enforcement boundary, including bypass attempts and guardian/policy unavailability?

### Mobile Top 10:2024

Apply when native or hybrid mobile code, SDK integration, local storage, deep links, or inter-process communication changes.

- **M1 Improper Credential Usage:** no embedded secrets; use platform-protected credential storage and short-lived tokens.
- **M2 Inadequate Supply Chain Security:** vet SDKs, libraries, build tools, and update channels.
- **M3 Insecure Authentication/Authorization:** enforce authorization server-side; do not trust client-only checks.
- **M4 Insufficient Input/Output Validation:** validate deep links, intents, IPC, notifications, files, and responses.
- **M5 Insecure Communication:** use authenticated encrypted transport; do not silently downgrade or disable certificate validation.
- **M6 Inadequate Privacy Controls:** minimize collection, permissions, analytics, and sensitive logs.
- **M7 Insufficient Binary Protections:** apply tamper/debugging/reverse-engineering protections when justified by the threat model; do not require obfuscation as a substitute for server-side controls.
- **M8 Security Misconfiguration:** review debug/release flags, exported components, backup policies, WebViews, and platform permissions.
- **M9 Insecure Data Storage:** protect local databases, files, caches, notifications, screenshots, backups, and app-switcher snapshots.
- **M10 Insufficient Cryptography:** use approved algorithms/APIs and platform key management; avoid custom or obsolete cryptography.

### CI/CD Security Risks

Apply when workflows, pipeline definitions, runners, build/release automation, artifact handling, or deployment credentials change.

- **CICD-SEC-1 Insufficient Flow Control Mechanisms:** preserve required reviews, branch protections, approval gates, and deployment separation.
- **CICD-SEC-2 Inadequate Identity and Access Management:** use individual/workload identities and least privilege; avoid shared long-lived accounts.
- **CICD-SEC-3 Dependency Chain Abuse:** pin and verify pipeline dependencies and external actions/plugins.
- **CICD-SEC-4 Poisoned Pipeline Execution:** prevent attacker-controlled branch names, titles, PR content, filenames, and artifacts from becoming executed commands or trusted pipeline instructions.
- **CICD-SEC-5 Insufficient Pipeline-Based Access Controls:** grant each job only the permissions, secrets, and environments it needs.
- **CICD-SEC-6 Insufficient Credential Hygiene:** use scoped, short-lived credentials; keep secrets out of logs/artifacts and rotate exposed credentials.
- **CICD-SEC-7 Insecure System Configuration:** isolate, harden, and preferably make runners ephemeral; separate untrusted PR execution from protected deployment secrets.
- **CICD-SEC-8 Ungoverned Usage of 3rd Party Services:** vet third-party integrations and pin immutable versions where possible.
- **CICD-SEC-9 Improper Artifact Integrity Validation:** sign/attest and verify build artifacts before promotion/deployment.
- **CICD-SEC-10 Insufficient Logging and Visibility:** audit pipeline, identity, approval, artifact, and deployment activity.

## Severity Guidance

- **Critical:** a realistic, evidenced path to severe data compromise, broad unauthorized privileged action, remote code execution with material impact, committed usable production secrets, or catastrophic integrity/availability loss.
- **High:** a plausible vulnerability with serious impact, including meaningful authorization bypass, sensitive data exposure, or privilege escalation under realistic preconditions.
- **Medium:** exploitable only under constrained conditions or a material defense-in-depth gap with a credible impact path.
- **Low:** limited security hygiene gap with low impact; do not use for theoretical risks without a plausible path.

Severity is impact plus likelihood in the changed context; do not assign it from OWASP category number alone. Confidence is assessed separately.

## Boundaries

- Vulnerable/malicious packages, lockfiles, package provenance, and package install scripts belong to dependencies; vulnerabilities in code/data handling belong here.
- General operational logging/health/alerts belong to compatibility-operability; security event logging and sensitive-data exposure belong here.
- Ordinary input-domain and failure correctness belongs to correctness; exploitability of untrusted input belongs here.
- Performance-only capacity issues belong to performance unless attacker-exploitable resource exhaustion is demonstrated.

## References

- [OWASP Top 10:2025](https://top10.owasp.org/2025/)
- [OWASP Application Security Verification Standard (ASVS) 5.0.0](https://asvs.owasp.org/)
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x00-header/)
- [OWASP Top 10 for LLM Applications:2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Agent Control Standard (ACS)](https://genai.owasp.org/resource/agent-control-standard-acs/) and [ACS Repository](https://github.com/GenAI-Security-Project/agent-control-standard)
- [OWASP Mobile Top 10:2024](https://owasp.org/www-project-mobile-top-10/)
- [OWASP MASVS 2.1.0](https://mas.owasp.org/MASVS/), [MASWE 1.0.0](https://mas.owasp.org/MASWE/), and [MASTG 2.0.0](https://mas.owasp.org/MASTG/)
- [OWASP Top 10 CI/CD Security Risks](https://owasp.org/projects/top-10-cicd-security-risks)
