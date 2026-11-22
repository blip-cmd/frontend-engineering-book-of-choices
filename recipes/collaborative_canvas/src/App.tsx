import { useEffect, useRef, useState } from 'react';
import * as Y from 'yjs';
import { IndexeddbPersistence } from 'y-indexeddb';
import { WebsocketProvider } from 'y-websocket';

type Shape = { x: number; y: number; w: number; h: number; color: string };

const ROOM = 'collaborative-canvas-starter';
const WIDTH = 800;
const HEIGHT = 500;
const COLORS = ['#e4572e', '#29335c', '#f3a712', '#669bbc', '#4c956c'];

// One shared document for the page. Each shape is a key in a Y.Map, so
// concurrent edits to different shapes merge; concurrent writes to the same
// key keep only one value.
const doc = new Y.Doc();
const shapes = doc.getMap<Shape>('shapes');

function draw(ctx: CanvasRenderingContext2D) {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);
  shapes.forEach((s) => {
    ctx.fillStyle = s.color;
    ctx.fillRect(s.x, s.y, s.w, s.h);
  });
}

export function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [loaded, setLoaded] = useState(false);
  const [status, setStatus] = useState('local only');
  const [count, setCount] = useState(0);

  // Local persistence first, then optional network sync.
  useEffect(() => {
    const local = new IndexeddbPersistence(ROOM, doc);
    local.on('synced', () => setLoaded(true));

    const url = import.meta.env.VITE_SYNC_URL;
    let remote: WebsocketProvider | undefined;
    if (url) {
      remote = new WebsocketProvider(url, ROOM, doc);
      remote.on('status', (e: { status: string }) => setStatus(e.status));
    }
    return () => {
      remote?.destroy();
      void local.destroy();
    };
  }, []);

  // Redraw whenever the shared map changes, locally or from a peer.
  useEffect(() => {
    const ctx = canvasRef.current?.getContext('2d');
    if (!ctx) return;
    const render = () => {
      draw(ctx);
      setCount(shapes.size);
    };
    render();
    shapes.observe(render);
    return () => shapes.unobserve(render);
  }, []);

  const addShape = () => {
    const w = 40 + Math.random() * 80;
    const h = 40 + Math.random() * 80;
    shapes.set(crypto.randomUUID(), {
      x: Math.random() * (WIDTH - w),
      y: Math.random() * (HEIGHT - h),
      w,
      h,
      color: COLORS[Math.floor(Math.random() * COLORS.length)] ?? '#000',
    });
  };

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: 16 }}>
      <h1>Collaborative Canvas Starter</h1>
      <p>
        <button type="button" onClick={addShape} disabled={!loaded}>
          Add shape
        </button>{' '}
        {count} shapes. Sync: {status}.
      </p>
      <canvas
        ref={canvasRef}
        width={WIDTH}
        height={HEIGHT}
        role="img"
        aria-label={`Canvas with ${count} shapes`}
        style={{ border: '1px solid #ccc' }}
      />
    </main>
  );
}
