/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Optional y-websocket server URL, for example ws://localhost:1234. Unset means local only. */
  readonly VITE_SYNC_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
