---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Appendix C: Production Frontend Security Hardening Checklist

> A comprehensive pre-flight verification checklist for securing client applications against XSS, token exfiltration, CSRF, and supply-chain attacks.

---

## 1. Authentication & Session Security
* [ ] **HttpOnly Cookies for Session Tokens:** All JWTs and session identifiers are stored in cookies flagged with `HttpOnly; Secure; SameSite=Lax`.
* [ ] **Zero Secrets in Client Code:** No database credentials, private API keys, or cloud signing keys exist in frontend source files or environment variables prefixed for client bundling (e.g., `NEXT_PUBLIC_` or `VITE_`).
* [ ] **Post-Logout Storage Cleanup:** Explicitly clear ephemeral memory stores, IndexedDB caches, and service worker caches upon user logout.

---

## 2. Content Security Policy (CSP) & HTTP Headers
* [ ] **Strict Nonce-Based CSP Deployed:** Enforce a Content Security Policy header on HTML responses with random per-request nonces:
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none';
  ```
* [ ] **Frame Embedding Protection:** Protect against clickjacking by setting `frame-ancestors 'none'` in CSP or `X-Frame-Options: DENY`.
* [ ] **MIME-Type Sniffing Protection:** Enforce `X-Content-Type-Options: nosniff`.
* [ ] **Referrer Policy Configured:** Enforce `Referrer-Policy: strict-origin-when-cross-origin` to prevent leaking private URL query parameters to third parties.

---

## 3. Input Handling & DOM Sanitization
* [ ] **HTML Sanitization on Rich Content:** Any dynamic HTML string passed to `dangerouslySetInnerHTML` is sanitized via `DOMPurify.sanitize(dirtyHtml)`.
* [ ] **URL Scheme Validation:** User-provided links (e.g., profile website links) are validated to reject dangerous schemes like `javascript:alert(1)` or `data:text/html`. Only `http://` and `https://` schemes are permitted.
* [ ] **Runtime Schema Validation on Network Payloads:** Incoming backend API responses are validated with `zod` or `valibot` schemas before critical business logic processes them.

---

## 4. Third-Party Dependencies & Supply Chain
* [ ] **Automated Lockfile Auditing:** CI pipeline runs automated dependency vulnerability scans (e.g., Snyk, Socket, or npm audit) on every pull request.
* [ ] **Subresource Integrity (SRI) on External CDNs:** Any external script loaded from public CDNs includes cryptographic SRI hashes (`integrity="sha384-..." crossorigin="anonymous"`).
* [ ] **Isolated Third-Party Tracking:** Marketing and analytics trackers are executed in isolated Web Workers via `Partytown` to prevent untrusted third-party scripts from reading DOM input fields.
