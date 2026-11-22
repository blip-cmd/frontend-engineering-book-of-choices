import { notFound } from 'next/navigation';
import { formatPrice, getProduct, getProducts } from '../../../lib/products';
import { AddToCart } from './add-to-cart';

export const revalidate = 3600;

// Prerender every known product at build time; unknown ids render on demand.
export async function generateStaticParams() {
  const products = await getProducts();
  return products.map((p) => ({ id: p.id }));
}

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);
  if (!product) notFound();
  return (
    <main>
      <h1 className="text-2xl font-bold">{product.name}</h1>
      <p className="my-2">{formatPrice(product.priceCents)}</p>
      <AddToCart productId={product.id} />
    </main>
  );
}
