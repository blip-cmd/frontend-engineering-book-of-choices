# Appendix C: Production Frontend Security Hardening Checklist

**Status:** not posted
**Page:** https://blip-cmd.github.io/frontend-engineering-book-of-choices/appendices/frontend-security-checklist/
**Ledger (sources for every claim):** https://github.com/blip-cmd/frontend-engineering-book-of-choices/blob/main/reviews/appendix-c-frontend-security-checklist.md

Every fact below is on the page with its source. Re-check the page before posting if it has changed since 2026-11.

---

## LinkedIn

Five frontend security settings I see misunderstood, each checked against OWASP, MDN or web.dev:

1️⃣ SameSite cookies are not CSRF protection on their own. OWASP: SameSite "is useful as a defense-in-depth control but it does not replace a proper CSRF defense". Use your framework's CSRF protection or tokens.

2️⃣ React 19 blocks javascript: URLs in src and href, but OWASP says this "does not replace application-specific URL validation". Allow only http: and https: for user links.

3️⃣ Clear-Site-Data on logout is useful, but its "cookies" directive affects the whole registered domain, including subdomains (MDN). That can sign users out of your other apps.

4️⃣ A strict CSP needs a nonce that is regenerated on every response (web.dev). Static or cached pages should use a hash-based CSP instead.

5️⃣ Moving third-party scripts into a web worker (for example with Partytown) is a performance move, not a security boundary: Partytown's docs say worker code can still access the DOM synchronously.

The full checklist covers sessions, CSRF, headers, HSTS, sanitizing HTML, SRI and supply chain, with a link to the primary source for every item:
https://blip-cmd.github.io/frontend-engineering-book-of-choices/appendices/frontend-security-checklist/

It's part of a free, open frontend reference that I'm verifying page by page in public.

#websecurity #frontend #javascript #react

---

## X (thread)

1/ 5 frontend security settings that are easy to get wrong, each checked against OWASP, MDN or web.dev 🧵

https://blip-cmd.github.io/frontend-engineering-book-of-choices/appendices/frontend-security-checklist/

2/ SameSite cookies are not CSRF protection by themselves. OWASP calls SameSite "a defense-in-depth control" that "does not replace a proper CSRF defense". Use your framework's CSRF protection or tokens.

3/ React 19 blocks javascript: URLs in src/href. OWASP: that "does not replace application-specific URL validation". Parse with new URL() and allow only http: and https:.

4/ Clear-Site-Data: "cookies" on logout clears cookies for the entire registered domain, subdomains included (MDN). Great for one app, surprising for a family of apps.

5/ Partytown moves third-party scripts into a worker for performance. It is not a sandbox for your form fields: its docs say worker code accesses the DOM synchronously.

6/ The full checklist links a primary source for every item, and the claim ledger is public. Corrections welcome.

---

## dev.to / Hashnode

**Title:** A frontend security checklist where every item links to its source
**Tags:** security, webdev, frontend, javascript
**Canonical URL:** https://blip-cmd.github.io/frontend-engineering-book-of-choices/appendices/frontend-security-checklist/

Republish the page (you hold the copyright, so the CC BY-NC-ND license does not restrict you). Add a short intro: why sourced checklists matter, and the Partytown correction found during verification. End with a link to the ledger and an invitation to send corrections. Set the canonical URL so the book's site gets search credit.

---

## Reddit (r/webdev or r/Frontend; check the rules, and HOLD until more pages are verified)

**Title:** Frontend security checklist with a primary source for every item. What's missing?

Lead with the "what's missing" question. The ledger already lists known omissions (Trusted Types, COOP, supply-chain hardening); mention that you're planning those and ask what else people would add.
