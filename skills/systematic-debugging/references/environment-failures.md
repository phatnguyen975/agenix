# Environment-Specific Failures

**Pattern:** works in one environment, fails in another.

## Method

1. Define the two environments: working and failing.
2. Capture the same fingerprint in both, with identical commands.
3. Diff the fingerprints.
4. In a safe, controlled copy, change or transfer one difference at a time toward the failing conditions until the failure moves. Do not modify production or shared state for this experiment without explicit approval.
5. The last difference moved is the candidate cause; confirm it as any other hypothesis (`diagnosis.md`).

## Fingerprint checklist

- Operating system, version, architecture; path separators and case sensitivity; line endings; locale, encoding, timezone, clock.
- Runtime and tool versions; dependency versions actually installed, not only declared.
- Environment variables and configuration files in effect; default values.
- Data and state: database contents and schema version, files, caches, feature flags.
- Permissions, users, network access, proxies, DNS, ports.
- Resources: memory, CPU, disk, file descriptors, time limits.
- Build and deploy: build flags, debug against release, bundled against source.

## Rules

- Run the feedback loop inside the failing environment (container, remote shell with permission); do not reason from the working one.
- Do not special-case code per environment unless the root cause shows the environment-dependent behavior is legitimately required.
