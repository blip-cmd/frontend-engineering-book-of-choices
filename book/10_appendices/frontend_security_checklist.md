---
status: draft
ai_involvement: drafted
last_verified:
verified_against:
review_by:
reviewers:
---

# Appendix C: Production Frontend Security Hardening Checklist

> A pre-launch checklist for the browser side of a web application: sessions, secrets, response headers, untrusted HTML and URLs, dependencies and third-party scripts. Each item links to the primary source that justifies it.

**Who this is for:** a developer or tech lead preparing a web application for production. The checklist covers what the frontend and its HTTP responses control. It does not replace server-side input validation, authorization checks, or a threat model for your own application.

---

## 1. Sessions, Cookies and CSRF

* [ ] **Keep session tokens in `HttpOnly` cookies, never in Web Storage.** `HttpOnly` forbids JavaScript from reading the cookie ([MDN: Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)), so a cross-site scripting (XSS) bug cannot copy the token out. OWASP: "Do not store session identifiers in local storage as the data is always accessible by JavaScript", and avoid storing session tokens or other secrets in IndexedDB ([OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)).

* [ ] **Set every security attribute explicitly.** OWASP's recommended session cookie ([Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)):

  ```http
  Set-Cookie: __Host-SessionID=<value>; Secure; HttpOnly; SameSite=Strict; Path=/
  ```

  * `SameSite`: set `Strict` (preferred) or `Lax` explicitly. Do not rely on the browser default, which "varies across browsers and versions" (OWASP). `Strict` excludes all cross-site requests; `Lax` still sends the cookie on top-level cross-site navigations that use safe methods, such as following a link.
  * `__Host-` prefix: the browser rejects the cookie unless it is `Secure`, set from an HTTPS origin, has `Path=/` and has no `Domain` attribute ([MDN: Set-Cookie, cookie prefixes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)). This stops a subdomain from overwriting your session cookie.

* [ ] **Protect state-changing requests against CSRF; `SameSite` alone is not enough.** OWASP: "SameSite is useful as a defense-in-depth control but it does not replace a proper CSRF defense in most deployments." Its primary defenses, in order ([CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)):
  1. Use your framework's built-in CSRF protection if it has one.
  2. Otherwise add CSRF tokens to all state-changing requests: the synchronizer token pattern for stateful servers, signed double-submit cookies for stateless ones.
  3. If you target only modern browsers, you may rely on Fetch Metadata headers (`Sec-Fetch-Site`), with a fallback to checking the standard origin headers.

* [ ] **Clear browser-side data on logout.** End the session on the server, then send [`Clear-Site-Data`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data) on the logout response:

  ```http
  Clear-Site-Data: "cache", "cookies", "storage"
  ```

  * `"storage"` clears localStorage, sessionStorage and IndexedDB, and unregisters service workers (MDN). MDN marks the header Baseline widely available, "available across browsers since September 2023", and it only works over HTTPS.
  * **Caution:** `"cookies"` "affects the entire registered domain, including subdomains" (MDN), so it can also sign users out of sibling apps on other subdomains. Drop that directive if your subdomains share a registered domain but not a session.
  * MDN's description of `"storage"` does not list the Cache API. Do not put responses containing sensitive data into the Cache API in the first place ([OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)).

---

## 2. Secrets

* [ ] **Ship nothing secret to the browser.** Everything in a client bundle can be read by anyone who loads the page. Framework environment variables with a public prefix are copied into that bundle at build time:
  * Next.js: variables prefixed `NEXT_PUBLIC_` are inlined "into any JavaScript sent to the browser"; other variables stay on the server ([Next.js: Environment Variables](https://nextjs.org/docs/app/guides/environment-variables)).
  * Vite: variables prefixed `VITE_` "will be exposed in client-side source code", and "should not contain sensitive information such as API keys" ([Vite: Env Variables and Modes](https://vite.dev/guide/env-and-mode)).

  Calls that need a secret (payment APIs, database credentials, signing keys) belong on the server.

---

## 3. Response Headers

* [ ] **Deploy a strict Content Security Policy (CSP).** A strict CSP limits which scripts can run, so an injected `<script>` tag or inline handler does not execute. The nonce-based policy recommended by [web.dev: Mitigate XSS with a strict CSP](https://web.dev/articles/strict-csp):

  ```http
  Content-Security-Policy: script-src 'nonce-{RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none';
  ```

  * Replace `{RANDOM}` with a random nonce "regenerated on every server response", and add the same nonce to each `<script>` tag you serve. `'strict-dynamic'` lets scripts that a trusted script loads run too, so you do not maintain a list of allowed URLs.
  * For static or cached HTML, where a per-response nonce is impossible, web.dev recommends a hash-based CSP instead.
  * To test a policy without breaking the site, send it as `Content-Security-Policy-Report-Only` first, then switch to `Content-Security-Policy` (both modes are described by web.dev).

* [ ] **Prevent clickjacking.** Stop other sites from framing your pages with the CSP directive `frame-ancestors 'none'`. MDN describes it as similar to `X-Frame-Options: DENY`, "which is also supported in older browsers" ([MDN: frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors)). OWASP recommends implementing more than one mechanism for defense in depth, so send both ([OWASP Clickjacking Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html)).
  * **Both must be HTTP headers.** `frame-ancestors` "is not supported in the `<meta>` element" (MDN), and `X-Frame-Options` meta tags "DO NOT WORK" (OWASP).
  * **When not to use `'none'`:** if your pages are meant to be embedded (widgets, embeds), list the allowed parent origins in `frame-ancestors` instead.

* [ ] **Send `X-Content-Type-Options: nosniff`.** With it, the browser refuses to run a script or apply a stylesheet whose response has the wrong MIME type, and stops guessing content types for other responses ([MDN: X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options)).

* [ ] **Enforce HTTPS with HSTS.** `Strict-Transport-Security` "informs browsers that the host should only be accessed using HTTPS" ([MDN: Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)). MDN's one-year example:

  ```http
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  ```

  * `includeSubDomains` forces HTTPS on every present and future subdomain, so check that they all serve HTTPS before adding it.
  * To join the browser preload list, `max-age` must be at least `31536000` (one year) and `includeSubDomains` must be present. The preload list is a separate service from Google and "not part of the HSTS specification" (MDN).

* [ ] **Keep secrets out of URLs, and know your `Referrer-Policy`.** Browsers already default to `strict-origin-when-cross-origin`: full URL (including the query string) on same-origin requests, origin only on cross-origin requests, nothing when going from HTTPS to HTTP ([MDN: Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy)). Setting it explicitly documents your intent. If even your origin should not leak from certain pages, choose a stricter value from MDN's list. Tokens in URLs can also leak through browser history and server logs; send them in headers or request bodies instead.

---

## 4. Untrusted HTML, URLs and Data

* [ ] **Sanitize any HTML you inject.** React's `dangerouslySetInnerHTML` inserts a raw HTML string, and "if the HTML inside isn't trusted (for example, if it's based on user data), you risk introducing an XSS vulnerability" ([react.dev: common components](https://react.dev/reference/react-dom/components/common)). Sanitize it first with [DOMPurify](https://github.com/cure53/DOMPurify):

  ```jsx
  import DOMPurify from 'dompurify';

  export function Comment({ html }) {
    // Sanitize at render time, and do not modify the output afterwards.
    return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }} />;
  }
  ```

  * DOMPurify warns that if you sanitize HTML "and then modify it afterwards, you might easily void the effects of sanitization".
  * On the server, DOMPurify needs a DOM implementation: its README strongly recommends the latest version of `jsdom`, and says alternatives such as `happy-dom` "are not considered safe" yet.

* [ ] **Validate user-supplied URLs by scheme.** A link like `javascript:...` runs code when clicked. React 19 blocks `javascript:` URLs in `src` and `href`, "but this does not replace application-specific URL validation" ([OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)). Allow only the schemes you expect:

  ```js
  export function safeHttpUrl(input) {
    try {
      const url = new URL(input);
      return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : null;
    } catch {
      return null; // not an absolute URL
    }
  }
  ```

* [ ] **Treat API responses as untrusted input.** Validate the shape of data from the network before your code relies on it, for example with a schema library such as [Zod](https://www.npmjs.com/package/zod) or [Valibot](https://www.npmjs.com/package/valibot). This is defense in depth and a robustness measure: it turns a malformed or unexpected response into a handled error instead of corrupted state. It does not replace validation on the server.

---

## 5. Dependencies and Third-Party Scripts

* [ ] **Scan dependencies on every pull request.** Run a vulnerability scanner in CI (for example `npm audit`, GitHub Dependabot, Socket or Snyk) and commit your lockfile so every install resolves the same versions.

* [ ] **Check that a package is real before installing it, especially if an AI tool suggested it.** Code models invent package names (at least 5.2% of suggestions from commercial models and 21.7% from open models in one study), and attackers register those names ([Spracklen et al., USENIX Security 2025](https://arxiv.org/abs/2406.10279v3)). Confirm the name, owner and download history with `npm view <name>` or on npmjs.com.

* [ ] **Pin CDN scripts with Subresource Integrity (SRI).** Add an `integrity` hash (`sha256`, `sha384` or `sha512`) to any script or stylesheet loaded from another origin, plus `crossorigin="anonymous"`: cross-origin SRI requires CORS, and a `no-cors` request with an integrity check "will always fail" ([MDN: Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)).

  ```html
  <script src="https://cdn.example.com/lib.js"
          integrity="sha384-<base64 hash of the exact file>"
          crossorigin="anonymous"></script>
  ```

* [ ] **Assume every third-party script can read the whole page.** Analytics, tag managers and chat widgets run with your page's privileges, including access to form fields.
  * **Partytown is not a security boundary.** It moves third-party scripts into a web worker for performance, but by design it "allows code executed from the web worker to access DOM synchronously", forwarding calls to the main thread through JavaScript proxies ([Partytown: How does it work?](https://partytown.qwik.dev/how-does-partytown-work)). Its sandboxing options let you restrict which APIs a script may call ([Partytown: Sandboxing](https://partytown.qwik.dev/sandboxing)), but the documentation makes no security guarantee.
  * **Our recommendation:** load as few third-party scripts as possible, keep them off sensitive pages (sign-in, payment, account settings), and let your CSP define where scripts may come from.
  * For untrusted embedded content, use an `<iframe>` with the `sandbox` attribute, served from a different origin. MDN warns that combining `allow-scripts` and `allow-same-origin` for same-origin content lets the embedded document remove the sandbox, "making it no more secure than not using the sandbox attribute at all" ([MDN: iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)).
