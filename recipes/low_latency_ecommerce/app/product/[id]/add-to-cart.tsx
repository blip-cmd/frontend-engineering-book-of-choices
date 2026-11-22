'use client';

import { startTransition, useOptimistic, useState } from 'react';
import { addToCart } from '../../actions';

export function AddToCart({ productId }: { productId: string }) {
  const [count, setCount] = useState(0);
  const [optimisticCount, addOptimistic] = useOptimistic(count, (c: number, n: number) => c + n);
  const [error, setError] = useState<string | null>(null);

  function onAdd() {
    setError(null);
    startTransition(async () => {
      addOptimistic(1);
      // The server stays the authority on stock; when the Action ends, the
      // optimistic value is replaced by the confirmed count.
      const result = await addToCart(productId);
      startTransition(() => {
        if (result.ok) setCount(result.quantity);
        else setError(result.error);
      });
    });
  }

  return (
    <div>
      <button onClick={onAdd} className="rounded bg-black px-4 py-2 text-white">
        Add to cart
      </button>
      <p aria-live="polite" className="mt-2">
        In cart: {optimisticCount}
        {error && <span className="ml-2 text-red-700">{error}</span>}
      </p>
    </div>
  );
}
