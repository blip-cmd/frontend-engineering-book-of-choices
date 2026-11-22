#!/usr/bin/env node
// SPDX-License-Identifier: AGPL-3.0-only
// Copyright (C) 2026 blip-cmd and contributors

/**
 * Frontend Engineering as a Book of Choices - CLI Decision Engine
 * Maps project constraints directly to proven architectural patterns,
 * scaffolding recipes, and standardized Architectural Decision Records (ADRs).
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const PKG_VERSION = '1.0.0';
const REPO_ROOT = path.resolve(__dirname, '..');
const RECIPES_DIR = path.join(REPO_ROOT, 'recipes');

const ARCHETYPE_RECIPES = {
  content_first_astro: {
    title: 'Content Publishing and Documentation',
    stack: 'Astro 7 + Preact 11 islands + Tailwind 4',
    recipeDir: 'content_first_astro',
    playbook: 'book/09_decision_playbooks/content_first_publishing.md'
  },
  enterprise_b2b_saas: {
    title: 'B2B SaaS, Admin Portals, Data Grids',
    stack: 'Vite 8 + React 19 + TanStack Query 5 / Table 9 + Zod 4 + Tailwind 4',
    recipeDir: 'enterprise_b2b_saas',
    playbook: 'book/09_decision_playbooks/enterprise_b2b_saas.md'
  },
  realtime_dashboard: {
    title: 'Real-Time Telemetry and Financial Consoles',
    stack: 'Vite 8 + Solid 2 signals + uPlot + Web Worker',
    recipeDir: 'realtime_dashboard',
    playbook: 'book/09_decision_playbooks/high_frequency_realtime_dashboard.md'
  },
  collaborative_canvas: {
    title: 'Collaborative Canvas and Document Workspaces',
    stack: 'Vite 8 + React 19 + Yjs 13 (CRDT) + IndexedDB, optional y-websocket sync',
    recipeDir: 'collaborative_canvas',
    playbook: 'book/09_decision_playbooks/collaborative_canvas_workspace.md'
  },
  low_latency_ecommerce: {
    title: 'Low-Latency Global E-Commerce Storefronts',
    stack: 'Next.js 16 on Node.js + ISR revalidation + useOptimistic cart + Tailwind 4',
    recipeDir: 'low_latency_ecommerce',
    playbook: 'book/09_decision_playbooks/low_latency_ecommerce.md'
  },
  shared_configs: {
    title: 'Base Monorepo Configurations',
    stack: 'Shared tsconfig.base.json and Tailwind 4 design tokens (tokens.css)',
    recipeDir: 'shared_configs',
    playbook: 'book/05_design_engineering_and_ui.md'
  }
};

function evaluateArchitecture(profile) {
  const rec = {};

  // Execution Boundary
  if (profile.seo === 'critical') {
    if (profile.traffic === 'mostly_static') {
      rec.execution = 'Islands Architecture (Astro) or SSG';
      rec.executionChapter = 'book/01_where_code_runs.md';
      rec.suggestedRecipe = 'content_first_astro';
    } else {
      rec.execution = 'Streaming SSR / React Server Components (Next.js or Remix)';
      rec.executionChapter = 'book/01_where_code_runs.md';
      rec.suggestedRecipe = 'low_latency_ecommerce';
    }
  } else {
    if (profile.complexity === 'local_first' || profile.stateOrigin === 'local_first') {
      rec.execution = 'Local-First Desktop PWA (Vite + Wasm / OPFS)';
      rec.executionChapter = 'book/08_local_first_and_offline_resilience.md';
      rec.suggestedRecipe = 'collaborative_canvas';
    } else {
      rec.execution = 'Client-Side SPA (Vite + React / Solid)';
      rec.executionChapter = 'book/01_where_code_runs.md';
      if (profile.updateFrequency === 'high_telemetry') {
        rec.suggestedRecipe = 'realtime_dashboard';
      } else {
        rec.suggestedRecipe = 'enterprise_b2b_saas';
      }
    }
  }

  // Reactivity Engine
  if (profile.updateFrequency === 'high_telemetry') {
    rec.reactivity = 'Fine-Grained Signals (Solid 2, Svelte 5 runes, or Preact with signals in JSX)';
    rec.reactivityChapter = 'book/02_the_reactivity_dilemma.md';
  } else if (profile.teamSize === 'solo_founder') {
    rec.reactivity = 'Compile-Time AST (Svelte 5 Runes) or React';
    rec.reactivityChapter = 'book/02_the_reactivity_dilemma.md';
  } else {
    rec.reactivity = 'Virtual DOM (React 19) or Signals (Angular/Vue 3)';
    rec.reactivityChapter = 'book/02_the_reactivity_dilemma.md';
  }

  // State and Cache Topology
  if (profile.complexity === 'local_first' || profile.stateOrigin === 'local_first') {
    rec.state = 'Local Embedded DB (PGlite / SQLite Wasm over OPFS) + CRDTs (Yjs)';
    rec.stateChapter = 'book/08_local_first_and_offline_resilience.md';
  } else if (profile.stateOrigin === 'remote_api') {
    rec.state = 'Server Cache (TanStack Query) + URL State (nuqs)';
    rec.stateChapter = 'book/03_state_and_cache_topologies.md';
  } else {
    rec.state = 'Lightweight Client Store (Zustand) + Local Component State';
    rec.stateChapter = 'book/03_state_and_cache_topologies.md';
  }

  // API Contract
  if (profile.monorepoTs) {
    rec.api = 'tRPC (Zero code-gen, instant TypeScript inference)';
    rec.apiChapter = 'book/04_the_networking_contract.md';
  } else {
    rec.api = 'REST with OpenAPI code generation (Orval) or GraphQL';
    rec.apiChapter = 'book/04_the_networking_contract.md';
  }

  // UI Component and Styling Strategy
  if (profile.brandUniqueness === 'custom_brand') {
    rec.ui = 'Headless Primitives (shadcn/ui on Base UI or Radix) + Tailwind 4';
    rec.uiChapter = 'book/05_design_engineering_and_ui.md';
  } else {
    rec.ui = 'Complete UI Component Suite (MUI, Ant Design, Mantine)';
    rec.uiChapter = 'book/05_design_engineering_and_ui.md';
  }

  return rec;
}

function generateAdr(profile, rec, projectName = 'Web Application') {
  const today = new Date().toISOString().split('T')[0];
  const lines = [
    `# ADR-0001: Frontend Architecture Selection for ${projectName}`,
    '',
    '## Status',
    'Accepted',
    '',
    '## Date',
    today,
    '',
    '## Context and Problem Statement',
    'Selecting the core frontend architecture requires balancing discoverability, latency budgets, update frequencies, team skillset, and brand requirements. The project constraint profile was evaluated against the decision matrices in Frontend Engineering as a Book of Choices.',
    '',
    '### Project Constraint Profile',
    `* SEO Requirement: ${profile.seo || 'standard'}`,
    `* Traffic and Content Nature: ${profile.traffic || 'standard'}`,
    `* UI Update Frequency: ${profile.updateFrequency || 'standard'}`,
    `* Data Ownership Model: ${profile.stateOrigin || 'remote_api'}`,
    `* Monorepo Full-Stack TypeScript: ${profile.monorepoTs ? 'Yes' : 'No'}`,
    `* Brand Differentiation: ${profile.brandUniqueness || 'custom_brand'}`,
    '',
    '## Decision',
    'The following architectural foundation was determined based on evaluated constraints:',
    '',
    `1. **Execution Boundary**: ${rec.execution}`,
    `   * Reference: \`${rec.executionChapter}\``,
    `2. **Reactivity Engine**: ${rec.reactivity}`,
    `   * Reference: \`${rec.reactivityChapter}\``,
    `3. **State and Cache Topology**: ${rec.state}`,
    `   * Reference: \`${rec.stateChapter}\``,
    `4. **API Contract Layer**: ${rec.api}`,
    `   * Reference: \`${rec.apiChapter}\``,
    `5. **UI Component and Styling Strategy**: ${rec.ui}`,
    `   * Reference: \`${rec.uiChapter}\``,
    '',
    '## Consequences',
    '### Positive',
    '* Architecture directly aligns with the primary latency and discoverability requirements.',
    '* Minimizes unnecessary runtime abstraction layers and prevents architectural drift.',
    '* References concrete implementation playbooks and hardening checklists.',
    '',
    '### Negative and Trade-offs',
    '* Requires team adherence to the chosen execution boundaries and state ownership contracts.',
    '* Cross-boundary data passing must adhere strictly to the defined contract validation.',
    '',
    '## References',
    '* Book of Choices Catalog: `library/INDEX.md`',
    `* Suggested Starter Recipe: \`recipes/${rec.suggestedRecipe}/\``,
    '* Playbooks and Hardening Guides: `book/09_decision_playbooks/` and `book/10_appendices/`'
  ];
  return lines.join('\n');
}

function scaffoldRecipe(archetypeKey, targetDir) {
  if (!ARCHETYPE_RECIPES[archetypeKey]) {
    throw new Error(`Unknown archetype '${archetypeKey}'. Available: ${Object.keys(ARCHETYPE_RECIPES).join(', ')}`);
  }

  const recipeDirName = ARCHETYPE_RECIPES[archetypeKey].recipeDir;
  const src = path.join(RECIPES_DIR, recipeDirName);

  if (!fs.existsSync(src)) {
    throw new Error(`Recipe directory does not exist: ${src}`);
  }

  const dest = path.resolve(targetDir);
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const copiedFiles = [];
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      fs.cpSync(srcPath, destPath, { recursive: true });
      copiedFiles.push(`${entry.name}/`);
    } else {
      fs.copyFileSync(srcPath, destPath);
      copiedFiles.push(entry.name);
    }
  }

  return copiedFiles;
}

function askQuestion(rl, query, options) {
  return new Promise((resolve) => {
    console.log(`\n${query}`);
    options.forEach((opt, idx) => {
      console.log(`  [${idx + 1}] ${opt[0]} : ${opt[1]}`);
    });
    const prompt = () => {
      rl.question('\nSelect an option (number): ', (answer) => {
        const val = parseInt(answer.trim(), 10);
        if (!isNaN(val) && val >= 1 && val <= options.length) {
          resolve(val);
        } else {
          console.log('Invalid selection. Please enter a valid number.');
          prompt();
        }
      });
    };
    prompt();
  });
}

async function runInteractive(options) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  try {
    console.log('='.repeat(70));
    console.log(' FRONTEND ENGINEERING AS A BOOK OF CHOICES : DECISION ENGINE');
    console.log(' Answer the following 6 questions to generate your optimal architecture.');
    console.log('='.repeat(70));

    const seoChoice = await askQuestion(rl, '1. What is your SEO and Public Discoverability requirement?', [
      ['Critical', 'Every page must be indexed by search engines with high Core Web Vitals'],
      ['Moderate', 'Some marketing pages matter, but authenticated user dashboard dominates'],
      ['Irrelevant', 'Internal enterprise software, authenticated B2B portal, or desktop utility']
    ]);
    const seoMap = { 1: 'critical', 2: 'moderate', 3: 'irrelevant' };

    const trafficChoice = await askQuestion(rl, '2. What is the nature of your content and traffic?', [
      ['Mostly Static Content', 'Articles, documentation, marketing copy, product descriptions'],
      ['Highly Dynamic Personalized', 'Personalized social feeds, order status, real-time banking']
    ]);
    const trafficMap = { 1: 'mostly_static', 2: 'dynamic' };

    const freqChoice = await askQuestion(rl, '3. What is the update frequency of your user interface?', [
      ['Standard User Interaction', 'Form inputs, button clicks, page transitions, modal dialogs'],
      ['High-Frequency Streaming', '50-200 updates/second: financial tickers, telemetry, canvas']
    ]);
    const freqMap = { 1: 'standard', 2: 'high_telemetry' };

    const dataChoice = await askQuestion(rl, '4. What is the primary data ownership model?', [
      ['Remote Database / API', 'Data lives in cloud databases; browser fetches snapshots via HTTP'],
      ['Local-First & Offline', 'Data lives locally on user disk with background peer/cloud sync']
    ]);
    const dataMap = { 1: 'remote_api', 2: 'local_first' };

    const monoChoice = await askQuestion(rl, '5. Is your entire stack TypeScript in a single monorepo?', [
      ['Yes', 'Full-stack TypeScript in pnpm or Turborepo monorepo'],
      ['No', 'Polyglot backend (Go, Python, Java) or separate frontend repo']
    ]);
    const monoMap = { 1: true, 2: false };

    const brandChoice = await askQuestion(rl, '6. What is the requirement for visual brand differentiation?', [
      ['Custom Unique Brand', 'Distinctive design, custom tokens, bespoke micro-interactions'],
      ['Utility Over Brand', 'Standard internal admin tool where delivery speed is priority']
    ]);
    const brandMap = { 1: 'custom_brand', 2: 'standard_admin' };

    const profile = {
      seo: seoMap[seoChoice],
      traffic: trafficMap[trafficChoice],
      updateFrequency: freqMap[freqChoice],
      stateOrigin: dataMap[dataChoice],
      complexity: dataChoice === 2 ? 'local_first' : 'standard',
      teamSize: 'standard',
      monorepoTs: monoMap[monoChoice],
      brandUniqueness: brandMap[brandChoice]
    };

    const rec = evaluateArchitecture(profile);

    if (options.json) {
      console.log(JSON.stringify({ profile, recommendation: rec }, null, 2));
      return;
    }

    if (options.exportAdr) {
      const adr = generateAdr(profile, rec, options.projectName);
      if (options.output) {
        const outPath = path.resolve(options.output);
        fs.mkdirSync(path.dirname(outPath), { recursive: true });
        fs.writeFileSync(outPath, adr, 'utf8');
        console.log(`\n[SUCCESS] Architectural Decision Record written to: ${outPath}\n`);
      } else {
        console.log(`\n${adr}\n`);
      }
      return;
    }

    console.log('\n' + '='.repeat(70));
    console.log(' RECOMMENDED ARCHITECTURAL MATRIX PROFILE');
    console.log('='.repeat(70));
    console.log(`* Execution Boundary  : ${rec.execution}`);
    console.log(`  Reference Chapter   : ${rec.executionChapter}`);
    console.log(`* Reactivity Engine   : ${rec.reactivity}`);
    console.log(`  Reference Chapter   : ${rec.reactivityChapter}`);
    console.log(`* State and Cache     : ${rec.state}`);
    console.log(`  Reference Chapter   : ${rec.stateChapter}`);
    console.log(`* API Contract Layer  : ${rec.api}`);
    console.log(`  Reference Chapter   : ${rec.apiChapter}`);
    console.log(`* UI and Design Tokens: ${rec.ui}`);
    console.log(`  Reference Chapter   : ${rec.uiChapter}`);
    if (rec.suggestedRecipe) {
      console.log(`* Suggested Recipe    : recipes/${rec.suggestedRecipe}/`);
      console.log(`  Scaffold with       : npx @blip-cmd/choices init ${rec.suggestedRecipe} --target <dir>`);
    }
    console.log('='.repeat(70));
    console.log('Run complete. Consult the referenced chapters in the book/ directory.\n');
  } finally {
    rl.close();
  }
}

function parseCliArgs() {
  const args = process.argv.slice(2);
  const opts = {
    command: null,
    target: '.',
    output: null,
    projectName: 'Web Application',
    exportAdr: false,
    json: false,
    seo: null,
    traffic: null,
    updateFrequency: null,
    data: null,
    monorepoTs: false,
    brand: null
  };

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--help' || a === '-h' || a === 'help') {
      opts.command = 'help';
    } else if (a === '--version' || a === '-v') {
      opts.command = 'version';
    } else if (a === 'list' || a === '--list') {
      opts.command = 'list';
    } else if (a === 'init') {
      opts.command = 'init';
      if (args[i + 1] && !args[i + 1].startsWith('-')) {
        opts.archetype = args[++i];
      }
    } else if (a === 'export' || a === '--export-adr') {
      opts.exportAdr = true;
    } else if (a === '--target') {
      opts.target = args[++i];
    } else if (a === '--output') {
      opts.output = args[++i];
    } else if (a === '--project-name') {
      opts.projectName = args[++i];
    } else if (a === '--json') {
      opts.json = true;
    } else if (a === '--seo') {
      opts.seo = args[++i];
    } else if (a === '--traffic') {
      opts.traffic = args[++i];
    } else if (a === '--update-frequency') {
      opts.updateFrequency = args[++i];
    } else if (a === '--data') {
      opts.data = args[++i];
    } else if (a === '--monorepo-ts') {
      opts.monorepoTs = true;
    } else if (a === '--brand') {
      opts.brand = args[++i];
    }
  }

  return opts;
}

async function main() {
  const opts = parseCliArgs();

  if (opts.command === 'version') {
    console.log(`@blip-cmd/choices v${PKG_VERSION}`);
    return;
  }

  if (opts.command === 'help') {
    console.log(`
@blip-cmd/choices v${PKG_VERSION}
Frontend Engineering as a Book of Choices: Decision Engine and Scaffolding CLI
License: AGPL-3.0-only (starter recipes: MIT). No warranty.
Source:  https://github.com/blip-cmd/frontend-engineering-book-of-choices

USAGE:
  npx @blip-cmd/choices [command] [options]

COMMANDS:
  (no command)             Run the interactive architectural questionnaire
  list                     List all available starter recipes and playbooks
  init <archetype>         Scaffold an architecture recipe into a target folder
  export                   Generate an Architectural Decision Record (ADR)

OPTIONS:
  --target <dir>           Directory to scaffold files into (default: current directory)
  --output <file>          File path to save the generated ADR markdown
  --project-name <name>    Project name for the ADR title (default: "Web Application")
  --json                   Output recommendations in JSON format
  --seo <value>            critical | moderate | irrelevant
  --traffic <value>        mostly_static | dynamic
  --update-frequency <v>   standard | high_telemetry
  --data <value>           remote_api | local_first
  --monorepo-ts            Specify full-stack TypeScript in monorepo
  --brand <value>          custom_brand | standard_admin
  -h, --help               Show this help message
  -v, --version            Display package version
`);
    return;
  }

  if (opts.command === 'list') {
    console.log('\nAvailable Starter Architecture Recipes:');
    console.log('='.repeat(70));
    for (const [key, meta] of Object.entries(ARCHETYPE_RECIPES)) {
      console.log(`* ${key.padEnd(23)} : ${meta.title}`);
      console.log(`  Stack                   : ${meta.stack}`);
      console.log(`  Playbook Reference      : ${meta.playbook}`);
    }
    console.log('='.repeat(70));
    return;
  }

  if (opts.command === 'init') {
    if (!opts.archetype) {
      console.error('[ERROR] Please specify an archetype to initialize. Run `choices list` to see options.');
      process.exit(1);
    }
    try {
      const files = scaffoldRecipe(opts.archetype, opts.target);
      console.log(`\n[SUCCESS] Scaffolding recipe '${opts.archetype}' into: ${path.resolve(opts.target)}`);
      for (const f of files) {
        console.log(`  + ${f}`);
      }
      console.log('\nInitialization complete. Install dependencies and start development.\n');
    } catch (err) {
      console.error(`[ERROR] Scaffolding failed: ${err.message}`);
      process.exit(1);
    }
    return;
  }

  const hasFlags = opts.seo || opts.traffic || opts.updateFrequency || opts.data || opts.brand;

  if (hasFlags || opts.exportAdr && !process.stdin.isTTY) {
    const profile = {
      seo: opts.seo || 'moderate',
      traffic: opts.traffic || 'dynamic',
      updateFrequency: opts.updateFrequency || 'standard',
      stateOrigin: opts.data || 'remote_api',
      complexity: opts.data === 'local_first' ? 'local_first' : 'standard',
      teamSize: 'standard',
      monorepoTs: Boolean(opts.monorepoTs),
      brandUniqueness: opts.brand || 'custom_brand'
    };

    const rec = evaluateArchitecture(profile);

    if (opts.json) {
      console.log(JSON.stringify({ profile, recommendation: rec }, null, 2));
      return;
    }

    if (opts.exportAdr) {
      const adr = generateAdr(profile, rec, opts.projectName);
      if (opts.output) {
        const outPath = path.resolve(opts.output);
        fs.mkdirSync(path.dirname(outPath), { recursive: true });
        fs.writeFileSync(outPath, adr, 'utf8');
        console.log(`[SUCCESS] Architectural Decision Record written to: ${outPath}`);
      } else {
        console.log('\n' + adr + '\n');
      }
      return;
    }

    console.log('\n' + '='.repeat(70));
    console.log(' RECOMMENDED ARCHITECTURAL MATRIX PROFILE');
    console.log('='.repeat(70));
    console.log(`* Execution Boundary  : ${rec.execution}`);
    console.log(`  Reference Chapter   : ${rec.executionChapter}`);
    console.log(`* Reactivity Engine   : ${rec.reactivity}`);
    console.log(`  Reference Chapter   : ${rec.reactivityChapter}`);
    console.log(`* State and Cache     : ${rec.state}`);
    console.log(`  Reference Chapter   : ${rec.stateChapter}`);
    console.log(`* API Contract Layer  : ${rec.api}`);
    console.log(`  Reference Chapter   : ${rec.apiChapter}`);
    console.log(`* UI and Design Tokens: ${rec.ui}`);
    console.log(`  Reference Chapter   : ${rec.uiChapter}`);
    if (rec.suggestedRecipe) {
      console.log(`* Suggested Recipe    : recipes/${rec.suggestedRecipe}/`);
      console.log(`  Scaffold with       : npx @blip-cmd/choices init ${rec.suggestedRecipe} --target <dir>`);
    }
    console.log('='.repeat(70) + '\n');
    return;
  }

  await runInteractive(opts);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(`[FATAL] ${err.message}`);
    process.exit(1);
  });
}

module.exports = {
  ARCHETYPE_RECIPES,
  evaluateArchitecture,
  generateAdr,
  scaffoldRecipe
};
