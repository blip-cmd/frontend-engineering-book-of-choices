// @ts-check
// SPDX-License-Identifier: AGPL-3.0-only
// Copyright (C) 2026 blip-cmd and contributors
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { sync } from './scripts/sync-content.mjs';

const SITE = 'https://blip-cmd.github.io';
const BASE = '/frontend-engineering-book-of-choices';
const REPO_URL = 'https://github.com/blip-cmd/frontend-engineering-book-of-choices';
const TITLE = 'Frontend Engineering as a Book of Choices';
const DESCRIPTION =
	'A free, open reference for frontend architecture decisions: rendering, reactivity, state, APIs, styling, delivery and offline, with the trade-offs behind each choice.';
const OG_IMAGE = `${SITE}${BASE}/og/default.png`;

// Generate the docs pages from ../book before Astro reads its content collection.
sync();

export default defineConfig({
	site: SITE,
	base: BASE,
	trailingSlash: 'always',
	integrations: [
		starlight({
			title: TITLE,
			description: DESCRIPTION,
			logo: { src: './src/assets/logo.svg', replacesTitle: false },
			favicon: '/favicon.svg',
			social: [{ icon: 'github', label: 'GitHub', href: REPO_URL }],
			lastUpdated: true,
			customCss: ['./src/styles/custom.css'],
			head: [
				{ tag: 'meta', attrs: { property: 'og:image', content: OG_IMAGE } },
				{ tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
				{ tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
				{ tag: 'meta', attrs: { property: 'og:image:alt', content: `${TITLE}: a free frontend architecture reference` } },
				{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
				{ tag: 'meta', attrs: { name: 'twitter:image', content: OG_IMAGE } },
				{
					tag: 'script',
					attrs: { type: 'application/ld+json' },
					content: JSON.stringify({
						'@context': 'https://schema.org',
						'@graph': [
							{
								'@type': 'WebSite',
								name: TITLE,
								url: `${SITE}${BASE}/`,
								description: DESCRIPTION,
								inLanguage: 'en',
							},
							{
								'@type': 'Book',
								name: TITLE,
								url: `${SITE}${BASE}/`,
								description: DESCRIPTION,
								author: { '@type': 'Person', name: 'blip-cmd', url: 'https://github.com/blip-cmd' },
								bookFormat: 'https://schema.org/EBook',
								isAccessibleForFree: true,
								license: 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
								inLanguage: 'en',
							},
						],
					}),
				},
			],
			sidebar: [
				{ label: 'Start Here', items: [{ label: 'Architecture Calculator', link: '/calculator/' }] },
				{ label: 'Chapters', items: [{ autogenerate: { directory: 'chapters' } }] },
				{ label: 'Decision Playbooks', items: [{ autogenerate: { directory: 'playbooks' } }] },
				{ label: 'Appendices', items: [{ autogenerate: { directory: 'appendices' } }] },
				{ label: 'Essays', collapsed: true, items: [{ autogenerate: { directory: 'essays' } }] },
				{
					label: 'Project',
					items: [
						{ label: 'Further Reading', slug: 'further-reading' },
						{ label: 'How to Contribute', slug: 'contribute' },
						{ label: 'Roadmap', link: `${REPO_URL}/blob/main/ROADMAP.md`, attrs: { target: '_blank' } },
					],
				},
			],
		}),
	],
});
