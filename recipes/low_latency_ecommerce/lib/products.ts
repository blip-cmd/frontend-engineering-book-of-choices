// Local mock catalog: no network calls, so the recipe builds offline.
export type Product = { id: string; name: string; priceCents: number; stock: number };

const products: Product[] = [
  { id: '1', name: 'Canvas tote', priceCents: 2400, stock: 12 },
  { id: '2', name: 'Ceramic mug', priceCents: 1800, stock: 0 },
  { id: '3', name: 'Linen apron', priceCents: 3900, stock: 5 },
];

export async function getProducts(): Promise<Product[]> {
  return products;
}

export async function getProduct(id: string): Promise<Product | undefined> {
  return products.find((p) => p.id === id);
}

export const formatPrice = (cents: number) => `$${(cents / 100).toFixed(2)}`;
