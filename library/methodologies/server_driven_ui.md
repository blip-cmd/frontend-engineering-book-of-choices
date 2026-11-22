# Architectural Methodology: Server-Driven UI (SDUI)

> **Unverified background notes.** This file is an AI-generated research summary from the book's first draft. It has not been checked against the [content standards](../../CONTENT_STANDARDS.md) and is not part of the book. The verified chapters in `book/` cite primary sources directly; rely on those instead.

* **Identifier:** `server-driven-ui`
* **Pioneers & Key Implementers:** Airbnb (GhostPlatform / Epoxy), Lyft, Spotify, DoorDash, Uber
* **Core Mechanisms:** JSON-defined component trees, client-side rendering engines, dynamic layout orchestration, app-store update bypass

---

## 1. Mechanics and Mental Model

In traditional web and mobile development, the client owns the layout structure, rendering logic, and component placement; the backend simply delivers raw domain entities (e.g., `{ title: "Shoes", price: 99 }`). Any change to screen order, new promotional banners, or experimentation flows requires client code changes, testing, and deployment.

In **Server-Driven UI (SDUI)**, the roles invert:
1. **The Contract:** The server responds with a hierarchical description of the UI components to render, including their types, props, nested children, and action handlers:
   ```json
   {
     "type": "VerticalContainer",
     "children": [
       { "type": "HeroBanner", "props": { "title": "Winter Sale", "image": "..." } },
       { "type": "ProductCarousel", "props": { "category": "footwear" } }
     ]
   }
   ```
2. **The Client Component Registry:** The client maintains a catalog of battle-tested, pre-compiled primitive components mapped to string identifiers (`"HeroBanner" -> <HeroBanner />`).
3. **Dynamic Assembly:** The client parses the JSON tree and instantiates the matching components dynamically.

---

## 2. Comparative Trade-offs

### What You Gain:
* **Instantaneous UI Experimentation & Updates:** Layouts, promotional feeds, and screen flows update globally in seconds via server configuration without shipping client code.
* **Unified Cross-Platform Parity:** Web, iOS, and Android clients receive the identical JSON layout payload, ensuring consistent user experiences across platforms.
* **Simplified Client Logic:** The client becomes a lightweight rendering shell, shedding business rule validations and conditional display trees.

### What You Forfeit:
* **Large Network Payloads:** Verbose JSON layout representations consume significantly more bandwidth than clean entity REST/GraphQL responses.
* **Versioning & Backward Compatibility Fragility:** The server must continuously support older client component registries that lack newly released component types.
* **Compromised Interactive Performance:** Complex client-side animations, physics gestures, and micro-interactions are difficult to express in static JSON descriptors without custom domain-specific languages (DSLs).

---

## 3. Decision Bounds: When to Choose and Avoid

### Choose Server-Driven UI When:
* Operating large e-commerce feeds, travel booking screens, food delivery apps, or streaming home screens where layouts mutate weekly based on marketing campaigns or A/B testing.
* Maintaining unified experiences across Web, iOS, and Android where app store review cycles delay urgent feature rollouts.

### Avoid Server-Driven UI When:
* Building dense productivity workspaces, dashboards, data grids, or creative software where complex user-driven mutations, drag-and-drop operations, and fine-grained state manipulation dominate.
* The team lacks the bandwidth to engineer and maintain a robust schema validation and backward-compatibility governance pipeline.

---

## 4. Enabling Ecosystem & Tooling
* **Protocols & Formats:** JSON Schema, Protocol Buffers, FlatBuffers.
* **Open Source Engines:** DivKit (Yandex), Judo, Hyperview, Epoxy (Airbnb legacy).
