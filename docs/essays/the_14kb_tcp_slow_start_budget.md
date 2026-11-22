---
status: agent-verified
ai_involvement: drafted
last_verified: 2026-11
verified_against: RFC 5681, 6928, 894, 8200, 9293, 7323, 8446, 9000, 9002; HPBN ch. 1, 2, 4; MDN How browsers work; web.dev (LCP, Optimize LCP, critical CSS, preconnect, fonts, CLS, TTFB); ip-route(8); curl manual (curl 8.17.0); astro 7.4.13; react 19.3.1; next 16.4.6; Cloudflare Workers docs
review_by: 2027-11
reviewers:
ledger: reviews/the-14kb-tcp-slow-start-budget.md
---

# The 14 KB TCP Slow-Start Budget: What the First Round Trip of HTML Can Carry
> An essay for a frontend engineer or tech lead working on server-rendered pages who is deciding what belongs at the start of the HTML response. Its position: on a new connection, the first chunk of data a server sends is usually about 14 KB, after which it waits for acknowledgments ([MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)), so putting what the first render needs into those bytes is a cheap, measurable target. The figure is a heuristic derived from TCP's initial congestion window ([RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html)), not a hard limit, and this essay shows where it bends.

---

## 1. Why a fast connection still waits on round trips

Bandwidth says how many bytes per second a link can carry; latency says how long each byte takes to arrive. Light in optical fiber travels at roughly 200,000 km per second, so a New York to London round trip takes at least 56 ms over fiber, and a real New York to Sydney round trip is in the 200 to 300 ms range once routing and queuing are added ([High Performance Browser Networking (HPBN), ch. 1](https://hpbn.co/primer-on-latency-and-bandwidth/)).

A new TCP connection cannot use the full link at once. In HPBN's worked example, a 64 KB file fetched from London to New York over a new connection with a 56 ms round trip takes 264 ms, and the same request on an already-open connection takes 96 ms; the 5 Mbps of available bandwidth "had no impact during the startup phase" ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/)). Round trips and the congestion window set the cost, not the advertised speed of the connection.

---

## 2. How slow start caps the first flight of data (initcwnd)

A TCP sender limits unacknowledged data in flight to the smaller of two windows: the receive window, which the client advertises, and the congestion window (cwnd), which is the server's own estimate of what the path can carry without loss ([MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)). At the start of a connection the server knows nothing about the path, so cwnd starts small.

Slow start then grows the window as acknowledgments arrive. RFC 5681 lets a sender add at most one sender maximum segment size (SMSS) to cwnd for each ACK that acknowledges new data ([RFC 5681, Section 3.1](https://www.rfc-editor.org/rfc/rfc5681.html)), which roughly doubles the window every round trip until loss or the slow-start threshold ([MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)).

The starting value is the initial window (IW, set as `initcwnd` on Linux):

1. RFC 5681 set the upper bound at 2 to 4 segments, depending on segment size ([RFC 5681, Section 3.1](https://www.rfc-editor.org/rfc/rfc5681.html)).
2. RFC 6928 proposes raising the upper bound to 10 segments, "maximum 14600 B", using the formula `min(10*MSS, max(2*MSS, 14600))`. It is an Experimental RFC, not a Standards Track one, and the increase is optional: "a TCP MAY start with an initial window that is smaller than 10 segments" ([RFC 6928, Section 2](https://www.rfc-editor.org/rfc/rfc6928.html)).
3. On Linux, IW10 is the default "for all kernels above 2.6.39" ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/)). Operators can override it per route with `ip route ... initcwnd NUMBER` ([ip-route(8)](https://man7.org/linux/man-pages/man8/ip-route.8.html)), so a given server or CDN may use a different value.

On an HTTPS connection the HTML is not the first thing the server sends. The TCP three-way handshake costs one round trip ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/)), and a full TLS 1.3 handshake costs one more before the client sends its request ([RFC 8446, Section 2](https://www.rfc-editor.org/rfc/rfc8446.html)). The server's certificate chain travels in that handshake under the same congestion window, and a chain larger than the initial window adds round trips of its own ([HPBN, ch. 4](https://hpbn.co/transport-layer-security-tls/)).

---

## 3. Where the budget's size comes from, and why it varies

The 14 KB figure is the 10-segment initial window of [RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html) multiplied by a typical segment payload. Each input has a source and a range:

* Ethernet carries at most 1,500 octets of IP datagram per frame ([RFC 894](https://www.rfc-editor.org/rfc/rfc894.html)).
* The minimum IPv4 header is 20 octets and the minimum TCP header is 20 octets, so the IPv4 MSS on a 1,500-byte path is 1,460 bytes; IPv6's header is 20 octets longer, giving 1,440 bytes ([RFC 8200, Section 8.3](https://www.rfc-editor.org/rfc/rfc8200.html)).
* TCP options reduce the payload of every segment, because the effective send MSS subtracts "the size of the fixed TCP header and any options" ([RFC 9293, Section 3.7.1](https://www.rfc-editor.org/rfc/rfc9293.html)). The timestamps option is 10 bytes, laid out as 12 with two padding bytes ([RFC 7323, Section 3.2 and Appendix A](https://www.rfc-editor.org/rfc/rfc7323.html)), which leaves 1,448 bytes per IPv4 segment.

$$10 \times 1{,}460\text{ bytes} = 14{,}600\text{ bytes}$$

That product equals RFC 6928's cap of 14,600 bytes ([RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html)). With timestamps the same ten segments carry 14,480 bytes; over IPv6 with timestamps, 14,280 bytes. Those bytes also carry the HTTP response headers and, under HTTPS, a 5-byte header on every TLS record plus the cipher's authentication data ([RFC 8446, Section 5.2](https://www.rfc-editor.org/rfc/rfc8446.html)). There is no single exact HTML budget; "14 KB" is the rounded figure that [MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work) and [web.dev](https://web.dev/articles/extract-critical-css) use, and it counts compressed bytes on the wire.

Three effects move the real number:

* **TLS record size.** A TLS record holds up to 2^14 bytes of plaintext ([RFC 8446, Section 5.1](https://www.rfc-editor.org/rfc/rfc8446.html)), and the browser cannot decrypt any of a record until all of it has arrived. A server that sends 16 KB records on a new connection makes the client wait for the second flight before it can read the first. HPBN recommends records of about 1,400 bytes at the start of a connection, growing later ([HPBN, ch. 4](https://hpbn.co/transport-layer-security-tls/)).
* **Window growth during the handshake.** Each ACK of new data can add up to one SMSS to cwnd ([RFC 5681](https://www.rfc-editor.org/rfc/rfc5681.html)), so the client's acknowledgments of the TLS handshake flight can enlarge the window before the HTML is sent. The first HTML flight is therefore not exactly the initial window.
* **HTTP/3 over QUIC.** QUIC endpoints "SHOULD use an initial congestion window of ten times the maximum datagram size", limited to the larger of 14,720 bytes or twice the datagram size ([RFC 9002, Section 7.2](https://www.rfc-editor.org/rfc/rfc9002.html)). The datagram size is at least 1,200 bytes, so a connection still at that minimum starts at 12,000 bytes. QUIC combines the transport and TLS handshakes to reduce connection establishment latency, in one round trip ([RFC 9000, Section 7](https://www.rfc-editor.org/rfc/rfc9000.html)).

---

## 4. What one more kilobyte costs: one more round trip, not double the time

Take a new HTTPS connection over TCP with TLS 1.3, no packet loss, and an initial window of 10 segments ([RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html)), and, as a simplification, ignore the window growth during the handshake described in section 3. The TCP handshake takes one round trip and the TLS 1.3 handshake another ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/); [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html)). The request and the first flight of the response take a third.

### Case A: a 12 KB compressed document
1. The document plus a small set of response headers fits in the first flight of 10 segments ([RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html)).
2. The browser has the complete HTML after **3 round trips**: 168 ms at the 56 ms New York to London fiber round trip ([HPBN, ch. 1](https://hpbn.co/primer-on-latency-and-bandwidth/)), plus server time.

### Case B: a 15.2 KB compressed document
1. The first flight carries about 14 KB, then the server must wait for ACKs ([MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)).
2. Each ACK lets cwnd grow by up to one segment ([RFC 5681](https://www.rfc-editor.org/rfc/rfc5681.html)), and the server sends the rest of the response in the second flight.
3. The browser has the complete HTML after **4 round trips**: 224 ms at the same 56 ms round trip.

Crossing the window adds one round trip to a load that already needed three, about a third more network time, not double: the handshakes are part of every cold load. Over TLS 1.2, a full handshake without False Start needs two round trips instead of one ([HPBN, ch. 4](https://hpbn.co/transport-layer-security-tls/)), so the totals become four and five.

Case B does not mean the screen stays blank until the fourth round trip. The browser parses and renders from the bytes it has, which is why MDN advises putting "everything the browser needs to start rendering a page, or at least the HTML and CSS template for the basic page structure, in the first 14KB" ([MDN: How browsers work](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)). What the second flight delays is whatever sits in the bytes after the first window: content, and the discovery of any resource referenced there.

The cost applies to cold connections. On a connection that has already grown its window, the same 64 KB response in HPBN's example goes out in one burst ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/)).

---

## 5. What to put in the first window, and when the budget is the wrong target

Largest Contentful Paint (LCP) is good at 2.5 seconds or less, measured at the 75th percentile of page loads ([web.dev: LCP](https://web.dev/articles/lcp)). web.dev splits LCP into four subparts: time to first byte, resource load delay, resource load duration and element render delay ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)). The 14 KB budget acts on the later subparts: bytes that land in the second flight arrive a round trip later, and so does any resource the browser can only discover in them.

The book's position is that the first window of a server-rendered page should carry:

* The HTML for the first screen, in source order, with the LCP element or the reference to its image as early as possible.
* Critical CSS inlined in a `<style>` tag in the `<head>`; web.dev advises keeping above-the-fold content "under 14 KB (compressed)" ([web.dev: Extract critical CSS](https://web.dev/articles/extract-critical-css)).
* `<link rel="preconnect">` for third-party origins the page needs early ([web.dev: preconnect](https://web.dev/articles/preconnect-and-dns-prefetch)), and a font preload only for the primary typeface, since web.dev warns that a font preload comes "at the cost of taking away browser resources from the loading of other resources" ([web.dev: font best practices](https://web.dev/articles/font-best-practices)).
* `width` and `height` attributes, or CSS `aspect-ratio`, on images and video so the browser reserves their space ([web.dev: Optimize CLS](https://web.dev/articles/optimize-cls)).

And it should keep out of those first bytes anything that is not needed to draw the first screen: large serialized state objects (`window.__INITIAL_STATE__ = { ... }`) placed before the content, inline SVG illustrations for lower parts of the page, inline third-party snippets, and below-the-fold markup that can be streamed later in the same response.

The budget is the wrong target when:

* the LCP element is a large image whose load duration dominates; web.dev notes that an optimization to one subpart can "just shift the time saved to another part" ([web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp));
* the page is reached over an already-warm connection, as with client-side navigation in a single-page app, where cwnd has already grown, unless slow-start restart has reset it after the connection sat idle ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/));
* time to first byte is dominated by redirects or backend processing, which web.dev diagnoses separately with field data and the `Server-Timing` header ([web.dev: Optimize TTFB](https://web.dev/articles/optimize-ttfb)).

---

## 6. How Astro, React 19 streaming and edge hosting change what lands in the first window

* **Astro.** "By default, Astro will automatically render every UI component to just HTML & CSS, stripping out all client-side JavaScript automatically" ([Astro docs: Islands](https://docs.astro.build/en/concepts/islands/), checked against Astro 7.4). That removes script bytes, not HTML or inline CSS bytes, so an Astro page still needs measuring against the budget.
* **Streaming SSR in React 19 and Next.js 16.** React's `renderToReadableStream` (for Node.js, the docs point to `renderToPipeableStream` instead) resolves "as soon as the entire shell has been rendered", where the shell is "the part of your app outside of any `<Suspense>` boundaries" ([react.dev, React 19.3 docs](https://react.dev/reference/react-dom/server/renderToReadableStream)). Next.js's `loading.js` convention shows a loading state "while the content of a route segment streams in" ([Next.js 16 docs: loading.js](https://nextjs.org/docs/app/api-reference/file-conventions/loading)). Streaming changes the order and timing of bytes, not the size of the window: the shell is what should fit in the first flight.
* **Edge hosting (for example Cloudflare Workers).** Workers run on "Cloudflare's global network" ([Cloudflare Workers docs](https://developers.cloudflare.com/workers/reference/how-workers-works/)). Moving the server closer to the user shortens each round trip, which is one of the two levers HPBN names for slow start ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/)). The gain applies to HTML rendered or cached at the edge; web.dev notes that CDNs cache resources on edge servers physically closer to users ([web.dev: Optimize TTFB](https://web.dev/articles/optimize-ttfb)), and a response the edge must fetch from a distant origin still pays the origin round trip.

---

## 7. How to measure a page's first response against the budget

Measure the compressed body size and the header size of the HTML response:

```bash
# Compressed body bytes as transferred, plus headers and the encoding the server chose
curl -s -H "Accept-Encoding: br, gzip" -o /dev/null \
  -w "body=%{size_download} headers=%{size_header} encoding=%header{content-encoding}\n" \
  https://example.com/
```

`size_download` is "the size of the body/data that was transferred, excluding headers"; because the command does not pass `--compressed`, curl leaves the body compressed, so the figure is the bytes on the wire. `size_header` counts headers "as represented in HTTP/1-style header format", so on HTTP/2 and HTTP/3, where headers are compressed, it overstates their wire size ([curl manual](https://curl.se/docs/manpage.html)). `%header{}` needs curl 7.84.0 or later ([curl manual](https://curl.se/docs/manpage.html)). Run with curl 8.17.0 against `https://example.com/` on 2026-11-21, the command printed `body=334 headers=348 encoding=br`.

Compare the sum with roughly 14 KB, remembering from section 3 that the real first-flight size depends on MSS, TCP options, TLS record size and the server's `initcwnd` ([RFC 6928](https://www.rfc-editor.org/rfc/rfc6928.html)). On a Linux server you control, HPBN suggests `ss --options --extended --memory --processes --info` to see each peer's connection settings, and its checklist says to ensure cwnd is set to 10 ([HPBN, ch. 2](https://hpbn.co/building-blocks-of-tcp/)). A response a little over the line costs one round trip on a cold connection, as section 4 shows; a response far over it is a sign that content the first screen does not need is arriving ahead of content it does.
