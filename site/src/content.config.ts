// SPDX-License-Identifier: AGPL-3.0-only
// Copyright (C) 2026 blip-cmd and contributors
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			// Review status copied from the book's front matter by scripts/sync-content.mjs.
			extend: z.object({
				reviewStatus: z.enum(['draft', 'reviewed', 'gold']).optional(),
				lastVerified: z.string().regex(/^\d{4}-\d{2}$/).optional(),
			}),
		}),
	}),
};
