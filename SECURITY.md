# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Mutual Dissent, please report it responsibly.

**Preferred:** Use [GitHub Private Vulnerability Reporting](https://github.com/q-uestionable-AI/mutual-dissent/security/advisories/new) — click "Report a vulnerability" in the Security tab. This keeps coordination on-platform and follows the [OpenSSF Vulnerability Disclosure Guide](https://github.com/ossf/oss-vulnerability-guide).

**Alternative:** Email **security@q-uestionable.ai** with a description of the vulnerability, steps to reproduce, and potential impact assessment.

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Allow up to 72 hours for initial response
3. We will coordinate disclosure timeline with you

## Scope

Mutual Dissent is a multi-model debate engine. Vulnerabilities in the tool itself are in scope:

- API key leakage in transcripts, logs, or web UI
- Command injection in CLI argument handling
- Prompt injection via web UI inputs
- Unsafe deserialization of transcript data
- Dependency vulnerabilities with exploitable paths

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
