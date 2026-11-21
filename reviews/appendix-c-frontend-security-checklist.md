---
page: book/10_appendices/frontend_security_checklist.md
status_granted: agent-verified
verified: 2026-11-21
review_by: 2027-05
---

# Claim Ledger: Appendix C, Production Frontend Security Hardening Checklist

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a developer or tech lead preparing a web app for production. The page helps them decide which browser-side protections to ship before launch. Thesis: most frontend security is a short list of explicit settings (cookies, CSRF, headers, sanitizing, dependencies), each backed by OWASP, MDN or the framework's own docs.

**History.** [Pull request #1](https://github.com/blip-cmd/frontend-engineering-book-of-choices/pull/1) rewrote the AI-generated draft. Among other errors, the draft claimed that Partytown stops third-party scripts from reading form fields; Partytown's own docs say worker code accesses the DOM synchronously.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session and quotes matched against the live page text.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | `HttpOnly` forbids JavaScript from reading the cookie | [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie) | verified (quote) |
| 2 | Do not store session identifiers in localStorage; avoid tokens in IndexedDB | [OWASP HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html) | verified (quote) |
| 3 | Recommended cookie `__Host-SessionID=...; Secure; HttpOnly; SameSite=Strict; Path=/` | [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | verified (quote) |
| 4 | Set SameSite explicitly (Strict preferred); the default "varies across browsers and versions" | OWASP Session Management | verified (quote) |
| 5 | Strict vs Lax behaviour | OWASP Session Management; MDN Set-Cookie | verified |
| 6 | `__Host-` requires Secure, HTTPS origin, `Path=/`, no `Domain` | MDN Set-Cookie | verified (quote) |
| 7 | SameSite "is useful as a defense-in-depth control but it does not replace a proper CSRF defense" | [OWASP CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | verified (quote) |
| 8 | CSRF defense order: framework, tokens (synchronizer or signed double-submit), Fetch Metadata with an origin fallback | OWASP CSRF Prevention | verified (quote) |
| 9 | Clear-Site-Data `"storage"` clears Web Storage and IndexedDB, and unregisters service workers | [MDN Clear-Site-Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data) | verified (quote) |
| 10 | Baseline widely available "since September 2023"; secure contexts only | MDN Clear-Site-Data | verified (quote) |
| 11 | `"cookies"` affects the entire registered domain, including subdomains | MDN Clear-Site-Data | verified (quote) |
| 12 | Cache API not listed under `"storage"`; keep sensitive responses out of it | MDN Clear-Site-Data; OWASP HTML5 | verified |
| 13 | `NEXT_PUBLIC_` variables are inlined into browser JavaScript | [Next.js docs](https://nextjs.org/docs/app/guides/environment-variables) | verified (quote) |
| 14 | `VITE_` variables are exposed to client code and must not hold API keys | [Vite docs](https://vite.dev/guide/env-and-mode) | verified (quote) |
| 15 | Strict CSP policy text; per-response nonce; hash-based CSP for static pages; report-only mode | [web.dev: strict CSP](https://web.dev/articles/strict-csp) | verified (quote) |
| 16 | `frame-ancestors 'none'` similar to `X-Frame-Options: DENY`; not supported in `<meta>` | [MDN frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors) | verified (quote) |
| 17 | Use more than one clickjacking mechanism; X-Frame-Options meta tags "DO NOT WORK" | [OWASP Clickjacking Defense](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html) | verified (quote) |
| 18 | `nosniff` blocks scripts and styles with the wrong MIME type | [MDN X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options) | verified (quote) |
| 19 | HSTS purpose; one-year example; preload needs `max-age` of at least `31536000` plus `includeSubDomains`; preload "not part of the HSTS specification" | [MDN Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security) | verified (quote) |
| 20 | Default Referrer-Policy is `strict-origin-when-cross-origin` | [MDN Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy) | verified (quote) |
| 21 | Untrusted HTML in `dangerouslySetInnerHTML` risks XSS | [react.dev](https://react.dev/reference/react-dom/components/common) | verified (quote) |
| 22 | DOMPurify usage; do not modify output after sanitizing; jsdom on the server; happy-dom "not considered safe" | [DOMPurify README](https://github.com/cure53/DOMPurify) | verified (quote) |
| 23 | React 19 blocks `javascript:` URLs, "but this does not replace application-specific URL validation" | [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | verified (quote) |
| 24 | `safeHttpUrl` rejects dangerous schemes | Node 24 test run | verified (run) |
| 25 | Packages exist: `dompurify` 3.4.18, `zod` 4.6.7, `valibot` 1.5.0, `jsdom` 31.0.1 | `npm view` | verified |
| 26 | Code models invent package names (at least 5.2% commercial, 21.7% open) | [Spracklen et al., USENIX Security 2025](https://arxiv.org/abs/2406.10279v3) | verified |
| 27 | SRI hash prefixes; cross-origin SRI needs CORS; `no-cors` "will always fail" | [MDN SRI](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) | verified (quote) |
| 28 | Partytown gives worker code synchronous DOM access through proxies | [Partytown: How it works](https://partytown.qwik.dev/how-does-partytown-work) | verified (quote) |
| 29 | `allow-scripts` + `allow-same-origin` on same-origin content defeats the sandbox | [MDN iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe) | verified (quote) |
| 30 | Tokens in URLs leak through history and logs; third-party scripts run with page privileges; secret-requiring calls belong on the server; lockfiles pin versions | none | explanatory background, no source |

## 2. Independent verifier pass (2026-11-21)

A separate agent that did not write the page downloaded all 21 cited sources, extracted 43 claims and checked each one.

* **Verdict: PASS.** No unsupported claims; every quote appears verbatim (allowing for typographic quotes and line breaks).
* **Two partial findings, both fixed before this status was granted:**
  1. Clear-Site-Data: "only works over HTTPS" was reworded to MDN's "secure contexts (HTTPS) in some or all supporting browsers".
  2. Partytown: the Sandboxing page describes API allow/deny controls, but the [configuration reference](https://partytown.qwik.dev/configuration/) documents no such option. The page now says to treat that control as unavailable.
* **Minor wording fixed:** "attackers register those names" became "attackers can register those names", since the paper models the threat rather than reporting observed attacks.
* **Code:** `safeHttpUrl` was re-run against mixed-case, whitespace, tab, NUL-prefixed, `data:`, `vbscript:`, `blob:`, `file:`, protocol-relative and relative inputs; all were handled correctly. The JSX example matches the DOMPurify README. Header syntax matches MDN.

## 3. Known omissions (follow-up content, not errors)

The verifier listed topics a complete production checklist could add. Each needs its own sourced, verified entry before it is published:

* CSP browser-compatibility fallbacks web.dev mentions; Trusted Types (`require-trusted-types-for 'script'`); `form-action`; CSP reporting endpoints
* `__Http-` and `__Host-Http-` cookie prefixes now listed on MDN
* `Integrity-Policy` headers on MDN's SRI page
* Cross-Origin-Opener-Policy and Permissions-Policy
* `Cache-Control: no-store` for authenticated pages
* `postMessage` origin checks and open-redirect validation
* Production source maps
* Supply-chain hardening: `npm ci`, disabling install scripts, provenance and trusted publishing, delaying new releases

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | **17** |

All gates pass except G8 (human accountability), which the `agent-verified` status discloses instead: the page tells readers it has not yet been reviewed by a human expert.
