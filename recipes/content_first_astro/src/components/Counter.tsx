import { useState } from 'preact/hooks';

export default function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button
      type="button"
      class="rounded bg-blue-700 px-4 py-2 font-medium text-white hover:bg-blue-800"
      onClick={() => setCount((c) => c + 1)}
    >
      Clicked {count} {count === 1 ? 'time' : 'times'}
    </button>
  );
}
