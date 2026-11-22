# Collaborative Canvas Starter

A minimal local-first canvas: a Yjs document holds a `Y.Map` of shapes, y-indexeddb stores it in the browser, and a plain Canvas 2D context draws it. Network sync through y-websocket is optional.

It implements the [Collaborative Canvas and Document Workspaces playbook](../../book/09_decision_playbooks/collaborative_canvas_workspace.md). For larger scenes, the playbook suggests PixiJS 8 with its WebGL renderer (not the experimental WebGPU renderer) or Konva in place of the plain Canvas 2D drawing used here.

## Run

```bash
npm install
npm run dev        # http://localhost:3000
npm run typecheck
npm run build
npm run preview
```

Shapes persist in IndexedDB across reloads with no server.

To sync between browsers, run a y-websocket server you control and set its URL before starting:

```bash
VITE_SYNC_URL=ws://localhost:1234 npm run dev
```

If `VITE_SYNC_URL` is unset, the app never opens a network connection. There is no default server and no secret in this recipe.

## Caveat

A CRDT makes every replica converge, but it does not keep every edit. Two concurrent writes to the same property keep only one visible value; Yjs keeps one value for the key. Each shape here is its own map key, so concurrent edits to different shapes both survive. If a lost concurrent value matters, model the edits so they land on different keys, or surface the conflict in the UI.

## Versions

Built and type-checked on 2026-11-22 with Node 24.18.1 and:

| Package | Version |
| :--- | :--- |
| vite | 8.3.8 |
| @vitejs/plugin-react | 6.3.0 |
| react, react-dom | 19.3.1 |
| yjs | 13.6.33 |
| y-indexeddb | 9.0.12 |
| y-websocket | 3.1.0 |
| typescript | 7.0.2 |

## License

MIT, like everything under `recipes/`.
