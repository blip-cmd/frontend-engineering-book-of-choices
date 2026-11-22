import type { NextConfig } from 'next';

// Playbook 5: keep the default Node.js runtime so ISR works, and put a CDN in
// front for the public catalog HTML. Personalised responses (the cart) set
// Cache-Control: private in their own route handler, not in this shared config.
const nextConfig: NextConfig = {
  poweredByHeader: false,
  images: {
    formats: ['image/avif', 'image/webp'],
  },
  headers: async () => [
    {
      source: '/:path*',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      ],
    },
  ],
};

export default nextConfig;
