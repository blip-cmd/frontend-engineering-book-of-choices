import { cookies } from 'next/headers';

// Personalised response: `private` keeps it out of shared CDN caches.
export async function GET() {
  const jar = await cookies();
  return new Response(jar.get('cart')?.value ?? '{}', {
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'private, no-store' },
  });
}
