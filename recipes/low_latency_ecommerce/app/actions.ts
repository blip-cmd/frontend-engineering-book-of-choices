'use server';

import { cookies } from 'next/headers';
import { getProduct } from '../lib/products';

type CartResult = { ok: true; quantity: number } | { ok: false; error: string };

// Server Function: re-checks stock on the server and keeps the cart in a cookie.
export async function addToCart(productId: string): Promise<CartResult> {
  const product = await getProduct(productId);
  if (!product) return { ok: false, error: 'Unknown product' };
  const jar = await cookies();
  const cart = readCart(jar.get('cart')?.value);
  const quantity = (cart[productId] ?? 0) + 1;
  if (quantity > product.stock) return { ok: false, error: 'Out of stock' };
  cart[productId] = quantity;
  jar.set('cart', JSON.stringify(cart), { httpOnly: true, sameSite: 'lax', path: '/' });
  return { ok: true, quantity };
}

function readCart(raw: string | undefined): Record<string, number> {
  try {
    return raw ? (JSON.parse(raw) as Record<string, number>) : {};
  } catch {
    return {};
  }
}
