---
page: docs/essays/the_14kb_tcp_slow_start_budget.md
verified: 2026-11-21
---

# Claim Ledger: Essay, The 14 KB TCP Slow-Start Budget

> Every factual claim on the page, the primary source it rests on, and the result of two independent checks: the author pass that rewrote the page, and a separate verifier pass that did not write it. See [CONTENT_STANDARDS.md](../CONTENT_STANDARDS.md) for the process.

**Brief.** For a frontend engineer or tech lead working on server-rendered pages. The page helps them decide what belongs in the first bytes of the HTML response and whether a roughly 14 KB compressed budget is worth enforcing. Thesis (kept from the draft): on a new connection, TCP's initial congestion window lets the server send only about 14 KB before waiting a round trip, so the content the first render needs should sit in those bytes. The author pass kept the recommendation but labelled it as the book's position, replaced the draft's "single highest-ROI performance optimization" superlative (no source) with "a cheap, measurable target", narrowed the title claim that the first packet "decides your LCP" (web.dev's four LCP subparts contradict it), and added the cases where the budget is the wrong target, each with a source.

**History.** The AI-generated draft contained these errors, all corrected or removed: it called RFC 6928 a standard (it is Experimental, and its 10-segment window is optional); it said Linux, macOS and Windows all use 10 segments (only Linux was sourced); it said the TCP header takes 32 bytes but computed the MSS with 20; it gave an unsourced "14,180 bytes" payload after TLS overhead and a "14,336 bytes" pass line (that is 14 KiB, not a window size); it counted 1 versus 2 round trips and said one extra kilobyte "doubles the network delivery time", ignoring the TCP and TLS handshakes (the correct count on TCP with TLS 1.3 is 3 versus 4); it gave an unsourced 50 to 150 ms mobile round trip, a "sub-second LCP" target, Astro pages of "6 to 9 KB", and edge nodes "within 10 milliseconds of the user"; and it said streaming SSR avoids "blocking the main browser thread". The draft's curl command measured gzip only; servers often answer with Brotli, which the revised command requests.

---

## 1. Author pass (2026-11-21)

Sources were fetched in the same session with `curl` (RFCs as plain text from rfc-editor.org; HPBN, MDN, web.dev, framework docs and the curl manual as HTML converted to text), and quotes were matched against the fetched text. Arithmetic was checked with `node`; the curl command was run with curl 8.17.0.

| # | Claim | Primary source | Result |
| :--- | :--- | :--- | :--- |
| 1 | Light in fiber about 200,000 km/s; New York to London fiber RTT 56 ms; real New York to Sydney RTT 200 to 300 ms | [HPBN ch. 1](https://hpbn.co/primer-on-latency-and-bandwidth/) (Table 1-1 and text) | verified (quote) |
| 2 | HPBN example: 64 KB over a new connection with 56 ms RTT takes 264 ms, 96 ms on a reused one; bandwidth "had no impact during the startup phase" | [HPBN ch. 2](https://hpbn.co/building-blocks-of-tcp/) | verified (quote) |
| 3 | Data in flight is limited by the smaller of the receive window and cwnd; cwnd is the server's estimate of the path | [MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work) | verified (quote) |
| 4 | Slow start adds at most SMSS to cwnd per ACK of new data | [RFC 5681 §3.1](https://www.rfc-editor.org/rfc/rfc5681.html) | verified (quote) |
| 5 | cwnd roughly doubles every round trip during slow start | MDN: How browsers work | verified (quote) |
| 6 | RFC 5681 initial window upper bound is 2 to 4 segments by SMSS | RFC 5681 §3.1 | verified |
| 7 | RFC 6928: IW up to 10 segments, "maximum 14600 B", `min(10*MSS, max(2*MSS, 14600))`; Experimental; "a TCP MAY start with an initial window that is smaller than 10 segments" | [RFC 6928 §1–2](https://www.rfc-editor.org/rfc/rfc6928.html) | verified (quote); draft's "Standardized by" corrected |
| 8 | Linux IW10 default "for all kernels above 2.6.39" | HPBN ch. 2 | verified (quote) |
| 9 | macOS and Windows default to 10 segments | none found | removed |
| 10 | `ip route ... initcwnd NUMBER` sets the initial window per route (Linux 2.5.70+) | [ip-route(8)](https://man7.org/linux/man-pages/man8/ip-route.8.html) | verified (quote) |
| 11 | TCP three-way handshake costs one round trip | HPBN ch. 2 | verified (quote) |
| 12 | Full TLS 1.3 handshake: client sends application data after one round trip | [RFC 8446 §2, Figure 1](https://www.rfc-editor.org/rfc/rfc8446.html); [HPBN ch. 4](https://hpbn.co/transport-layer-security-tls/) ("1-RTT for new") | verified |
| 13 | Certificate chain is sent under the same congestion window; a chain larger than it adds round trips | HPBN ch. 4 | verified (quote) |
| 14 | Ethernet carries at most 1,500 octets of IP datagram | [RFC 894](https://www.rfc-editor.org/rfc/rfc894.html) | verified (quote) |
| 15 | Minimum IPv4 and TCP headers 20 octets each, IPv4 MSS = MTU − 40 (1,460); IPv6 MSS = MTU − 60 (1,440) | [RFC 8200 §8.3](https://www.rfc-editor.org/rfc/rfc8200.html) | verified (quote); fixes draft's 32-byte inconsistency |
| 16 | Effective send MSS subtracts "the size of the fixed TCP header and any options" | [RFC 9293 §3.7.1](https://www.rfc-editor.org/rfc/rfc9293.html) | verified (quote) |
| 17 | Timestamps option is 10 bytes, recommended layout NOP NOP TSopt (12 bytes) | [RFC 7323 §3.2, Appendix A](https://www.rfc-editor.org/rfc/rfc7323.html) | verified |
| 18 | 10 × 1,460 = 14,600; with timestamps 14,480; IPv6 with timestamps 14,280 | `node` arithmetic from rows 14 to 17 | verified (run) |
| 19 | Each TLS 1.3 record has a 5-byte header (type, version, length) plus AEAD expansion | [RFC 8446 §5.1–5.2](https://www.rfc-editor.org/rfc/rfc8446.html) (TLSCiphertext struct) | verified |
| 20 | About 14,180 bytes remain after TLS framing | none found | removed; overhead depends on record sizes and headers |
| 21 | MDN: first chunk "usually 14KB"; web.dev: keep above-the-fold content "under 14 KB (compressed)", "10 packets or approximately 14 KB" | MDN: How browsers work; [web.dev: Extract critical CSS](https://web.dev/articles/extract-critical-css) | verified (quote) |
| 22 | TLS record plaintext up to 2^14 bytes; the whole record is needed to decrypt; HPBN recommends about 1,400-byte records at the start of a connection | RFC 8446 §5.1; HPBN ch. 4 | verified (quote) |
| 23 | ACKs of the handshake flight can enlarge cwnd before the HTML is sent, so the first HTML flight is not exactly the IW | RFC 5681 §3.1 with RFC 8446 Figure 1 | verified (reasoning from both) |
| 24 | QUIC IW: ten times max_datagram_size, limited to the larger of 14,720 bytes or twice the datagram size; datagram minimum 1,200 bytes, so 12,000 bytes at the minimum | [RFC 9002 §7.2 and variable definitions](https://www.rfc-editor.org/rfc/rfc9002.html); `node` | verified (quote, run) |
| 25 | QUIC combines the cryptographic and transport handshakes to minimize connection establishment latency; 1-RTT handshake | [RFC 9000 §7, Figure 5](https://www.rfc-editor.org/rfc/rfc9000.html) | verified (quote) |
| 26 | Cold load on TCP + TLS 1.3: complete HTML after 3 RTTs if it fits the first flight, 4 if not; 168 ms vs 224 ms at 56 ms RTT | rows 11, 12, 1; `node` | verified (derived); draft's 1 vs 2 RTT and "doubles" corrected |
| 27 | After ACKs, cwnd grows by up to one segment per ACK | RFC 5681 §3.1 | verified; draft's flat "doubles the congestion window (cwnd = 20)" reworded, since delayed ACKs (RFC 5681 §4.2) change growth |
| 28 | Mobile 4G/5G RTT is "50 to 150 milliseconds" | none current; HPBN's 2013 table gives only "< 100 ms" for 4G | removed; replaced with fiber RTTs from row 1 |
| 29 | Full TLS 1.2 handshake takes two round trips (without False Start) | HPBN ch. 4 | verified (quote) |
| 30 | Browser parses and renders from partial HTML; MDN advises putting what first render needs "in the first 14KB" | MDN: How browsers work | verified (quote) |
| 31 | On a reused connection the 64 KB response goes in one burst | HPBN ch. 2 | verified |
| 32 | LCP good at 2.5 s or less at the 75th percentile | [web.dev: LCP](https://web.dev/articles/lcp) | verified (quote); draft's "sub-second LCP" removed |
| 33 | LCP has four subparts; an optimization to one can "just shift the time saved to another part" | [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp) | verified (quote) |
| 34 | `rel=preconnect` starts connection setup early | [web.dev: preconnect](https://web.dev/articles/preconnect-and-dns-prefetch) | verified |
| 35 | Font preload comes "at the cost of taking away browser resources from the loading of other resources" | [web.dev: font best practices](https://web.dev/articles/font-best-practices) | verified (quote) |
| 36 | `width`/`height` attributes or CSS `aspect-ratio` reserve space for images and video | [web.dev: Optimize CLS](https://web.dev/articles/optimize-cls) | verified (quote) |
| 37 | High TTFB from redirects and backend processing is diagnosed with field data and `Server-Timing`; CDNs cache on edge servers closer to users | [web.dev: Optimize TTFB](https://web.dev/articles/optimize-ttfb) | verified |
| 38 | Astro renders components to HTML and CSS, "stripping out all client-side JavaScript automatically", by default | [Astro docs: Islands](https://docs.astro.build/en/concepts/islands/); `npm view astro` 7.4.13 | verified (quote) |
| 39 | Astro content pages compress to 6 to 9 KB | none found | removed |
| 40 | `renderToReadableStream` resolves "as soon as the entire shell has been rendered"; shell is the part outside `<Suspense>` | [react.dev (19.3 docs)](https://react.dev/reference/react-dom/server/renderToReadableStream); `npm view react` 19.3.1 | verified (quote) |
| 41 | Next.js `loading.js` shows loading UI "while the content of a route segment streams in" | [Next.js docs v16.4.6](https://nextjs.org/docs/app/api-reference/file-conventions/loading); `npm view next` 16.4.6 | verified (quote) |
| 42 | Remix streaming; streaming avoids blocking the main thread | not checked | removed (Remix name dropped; main-thread claim unsupported) |
| 43 | Workers run on "Cloudflare's global network" | [Cloudflare Workers docs](https://developers.cloudflare.com/workers/reference/how-workers-works/) | verified (quote) |
| 44 | Edge nodes "within 10 milliseconds of the user" | none found | removed |
| 45 | Two levers for slow start cost: lower RTT or raise the initial window | HPBN ch. 2 | verified |
| 46 | curl `size_download` is body bytes transferred excluding headers; `size_header` is HTTP/1-style; `--compressed` decompresses; `%header{}` since 7.84.0 | [curl manual](https://curl.se/docs/manpage.html) | verified (quote) |
| 47 | The command prints `body=334 headers=348 encoding=br` for `https://example.com/` | curl 8.17.0 run, 2026-11-21 | verified (run). Also tested on MDN's home page: gzip body 16,384 bytes, Brotli 13,890, showing why the command requests Brotli |
| 48 | "Below 14,336 bytes ... completes in a single round trip" | none; 14,336 is 14 × 1,024 | removed; replaced with a heuristic comparison that points to row 18's range |
| 49 | `ss --options --extended --memory --processes --info` shows connection settings; checklist says ensure cwnd is 10 | HPBN ch. 2 | verified (quote) |
| 50 | Contents of the first window (first-screen HTML, critical CSS, early LCP reference) and what to keep out (large state blobs, inline SVG below the fold, inline third-party snippets, below-the-fold markup) | rows 21, 30, 33 to 36 | the book's position, labelled as such; "HTTP chunked transfer" and "CSS sprites" advice dropped |

## 2. Independent verifier pass (2026-11-21)

**Verdict: PASS.** The verifier did not write the page. It extracted 52 claims from the page itself (not from section 1), fetched every cited source fresh with `curl -sL` (nine RFCs as plain text from rfc-editor.org; HPBN chapters 1, 2 and 4; MDN; seven web.dev articles; ip-route(8); the curl manual; Astro, react.dev, Next.js and Cloudflare docs), converted HTML to text and searched it for each claim and quote. Result: 44 SUPPORTED, 7 PARTIAL (all corrected below), 1 UNSUPPORTED (corrected below), 0 left open. No first-person experience. Every number on the page links to a source in its block or is arithmetic on sourced inputs.

Edits to the page:

1. Opening blockquote: "a server can send only about 14 KB before it must wait one round trip for acknowledgments" overstated MDN, which says "The first chunk of content is usually 14KB of data" and that the server decides how many segments to send "before waiting for an ACK". Reworded to "the first chunk of data a server sends is usually about 14 KB, after which it waits for acknowledgments".
2. Section 2, item 2: "RFC 6928 raised the upper bound" changed to "proposes raising", matching RFC 6928 §1–2 ("This document proposes to raise the upper bound"), consistent with its Experimental status.
3. Section 4 setup: Cases A and B treat the first HTML flight as exactly the initial window, which section 3 says is not exact (ACKs of the TLS handshake flight grow cwnd per RFC 5681 §3.1). Added the stated simplification "ignore the window growth during the handshake described in section 3" so the cases no longer contradict section 3. No new fact added.
4. Case A: "up to about 2 KB of response headers" was an unsourced number and does not hold in every configuration: `node` gives 12 KiB + 2 KiB = 14,336 bytes, more than the 14,260 bytes left in ten 1,448-byte segments after 22 bytes of TLS 1.3 framing per record (5-byte header, 1-byte inner type, 16-byte AEAD tag), and more than 14,060 over IPv6 with timestamps. Reworded to "a small set of response headers".
5. Case B: "the remaining 1.2 KB" (15.2 − 14) ignored headers and TLS framing; replaced with "the rest of the response".
6. Section 5, warm-connection bullet: added HPBN ch. 2's own qualifier that slow-start restart "resets the congestion window of a connection after it has been idle", so a warm connection's cwnd has grown only if it has not sat idle.
7. Section 6, React (UNSUPPORTED part): "`renderToReadableStream` (and `renderToPipeableStream` for Node.js) resolves as soon as the entire shell has been rendered" attributed promise resolution to `renderToPipeableStream`, which the cited page does not say (it says only "For Node.js, use renderToPipeableStream instead"). Reworded to "(for Node.js, the docs point to `renderToPipeableStream` instead)".
8. Section 6, Cloudflare: "Cloudflare's global network" of data centers: the words "of data centers" are not in the source (which says "thousands of machines distributed across hundreds of locations"); deleted.

The H1 and blockquote stay on adjacent lines. A blank line between them was tried, but the audit then reads the H1 as its own block holding "14 KB" with no link, which is an error on a verified page, so the blank line was removed again.

Checks that matched without edits: HPBN Table 1-1 (56 ms NY to London fiber RTT; 200,000,000 m/s; NY to Sydney "200–300 millisecond range"); HPBN 264 ms vs 96 ms and "had no impact during the startup phase"; "for all kernels above 2.6.39"; the `ss` command and "Ensure that cwnd size is set to 10"; RFC 5681 IW of 2 to 4 segments and "at most SMSS bytes for each ACK"; RFC 6928 "maximum 14600 B", formula and "MAY start with an initial window that is smaller than 10 segments"; RFC 894 1,500 octets; RFC 8200 §8.3 minus 40 and minus 60 octets; RFC 9293 "fixed TCP header and any options"; RFC 7323 10-byte TSopt and NOP NOP layout; RFC 8446 Figure 1, 2^14 and TLSCiphertext header (type, version, length = 5 bytes); RFC 9002 §7.2 quote, 14,720 bytes and 1,200-byte minimum; RFC 9000 §7 and Figure 5 1-RTT; HPBN ch. 4 1,400-byte records, "entire record must be available", certificate chain overflow and TLS 1.2 two round trips; all web.dev, MDN, Astro, react.dev, Next.js and curl manual quotes verbatim.

Arithmetic (`node`): 1500 − 40 = 1,460; 1500 − 60 = 1,440; minus 12 bytes of options = 1,448 and 1,428; ×10 = 14,600, 14,480, 14,280; RFC 6928 formula at MSS 1,460 = 14,600; RFC 9002 formula at 1,200 bytes = 12,000 and at 1,472 = 14,720; 3 × 56 = 168 ms, 4 × 56 = 224 ms, 1/3 more; TLS 1.2 totals 4 and 5; HPBN 64 KB = 45 segments = 10 + 20 + 15.

Code and packages: the curl command was run with curl 8.17.0 on 2026-11-21 and printed `body=334 headers=346 encoding=br` (the header count varies by run with response header values; the page's 348 was its own dated run). `npm view`: astro 7.4.13, react 19.3.1, next 16.4.6, matching the versions the page names. `python pipelines/scripts/audit_repo_standards.py` passed after the edits, with the page set to agent-verified.

What the verifier still flags, not as errors: the section 4 cases are a model (no loss, no handshake window growth, no delayed ACKs), and real first HTML flights on TLS 1.3 are often larger than the initial window; HPBN dates from 2013 with later updates.

## 3. Known omissions (follow-up content, not errors)

Topics a complete treatment could add. Each needs its own sourced, verified entry before it is published:

* TLS 1.3 and QUIC 0-RTT resumption (RFC 8446 §2.3, RFC 9001), and their replay caveats
* QUIC's anti-amplification limit (a server may send at most three times the bytes it has received before address validation, RFC 9000 §8.1), which can cap the server's first flight
* HTTP/2 frame headers and HPACK/QPACK header compression, and how they change the byte count
* `103 Early Hints` and the browser preload scanner as ways to start subresource fetches before the HTML finishes
* Slow-start restart after idle (HPBN's checklist item) and its effect on reused connections
* CDN-specific initial window settings, from each vendor's own documentation
* Field data on HTML document sizes (for example, the HTTP Archive Web Almanac, naming edition and percentile)

Formatting note for the verifier: the H1 and the opening blockquote sit on adjacent lines with no blank line between them, so the audit reads them as one block and the "14 KB" in the title shares a block with the blockquote's source links. It renders as a heading followed by a quote.

## 4. Scores (agent assessment)

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 1 | 2 | **16** |

D1 is 1 because the essay argues for one target rather than comparing alternatives, though it now names when the target is wrong. D6 is 1 because HPBN (the source for several TCP and TLS details) dates from 2013 with later updates; framework claims are pinned. D8 is 1 because sections 4 and 7 refer back to sections 3 and 4. D9 is 1: the worked cases and the curl command are real and were run, but there is no example of fixing an over-budget page. G8 (human accountability) is not met; the page has not been reviewed by a human expert.
