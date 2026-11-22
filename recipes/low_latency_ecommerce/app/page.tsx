import Link from 'next/link';
import { formatPrice, getProducts } from '../lib/products';

// ISR: serve the cached page and regenerate it in the background at most once an hour.
export const revalidate = 3600;

export default async function Home() {
  const products = await getProducts();
  return (
    <main>
      <h1 className="mb-4 text-2xl font-bold">Products</h1>
      <ul className="space-y-2">
        {products.map((p) => (
          <li key={p.id}>
            <Link href={`/product/${p.id}`} className="underline">
              {p.name}
            </Link>{' '}
            <span>{formatPrice(p.priceCents)}</span>
          </li>
        ))}
      </ul>
    </main>
  );
}
