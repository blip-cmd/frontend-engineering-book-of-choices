const { test, describe } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { execFileSync } = require('node:child_process');

const {
  ARCHETYPE_RECIPES,
  evaluateArchitecture,
  generateAdr,
  scaffoldRecipe
} = require('../bin/choices.js');

const BIN_PATH = path.resolve(__dirname, '../bin/choices.js');

describe('Node CLI Decision Engine (@blip-cmd/choices)', () => {
  test('ARCHETYPE_RECIPES defines all expected recipes', () => {
    const keys = Object.keys(ARCHETYPE_RECIPES);
    assert.ok(keys.includes('content_first_astro'));
    assert.ok(keys.includes('enterprise_b2b_saas'));
    assert.ok(keys.includes('realtime_dashboard'));
    assert.ok(keys.includes('collaborative_canvas'));
    assert.ok(keys.includes('low_latency_ecommerce'));
    assert.ok(keys.includes('shared_configs'));
  });

  test('evaluateArchitecture evaluates content-first static archetype', () => {
    const profile = {
      seo: 'critical',
      traffic: 'mostly_static',
      updateFrequency: 'standard',
      stateOrigin: 'remote_api',
      complexity: 'standard',
      teamSize: 'standard',
      monorepoTs: false,
      brandUniqueness: 'custom_brand'
    };
    const rec = evaluateArchitecture(profile);
    assert.match(rec.execution, /Islands Architecture/);
    assert.strictEqual(rec.executionChapter, 'book/01_where_code_runs.md');
    assert.strictEqual(rec.suggestedRecipe, 'content_first_astro');
  });

  test('evaluateArchitecture evaluates low-latency ecommerce archetype', () => {
    const profile = {
      seo: 'critical',
      traffic: 'dynamic',
      updateFrequency: 'standard',
      stateOrigin: 'remote_api',
      complexity: 'standard',
      teamSize: 'standard',
      monorepoTs: false,
      brandUniqueness: 'custom_brand'
    };
    const rec = evaluateArchitecture(profile);
    assert.match(rec.execution, /Streaming SSR/);
    assert.strictEqual(rec.suggestedRecipe, 'low_latency_ecommerce');
  });

  test('evaluateArchitecture evaluates collaborative canvas archetype', () => {
    const profile = {
      seo: 'irrelevant',
      traffic: 'dynamic',
      updateFrequency: 'standard',
      stateOrigin: 'local_first',
      complexity: 'local_first',
      teamSize: 'standard',
      monorepoTs: true,
      brandUniqueness: 'custom_brand'
    };
    const rec = evaluateArchitecture(profile);
    assert.match(rec.execution, /Local-First/);
    assert.strictEqual(rec.suggestedRecipe, 'collaborative_canvas');
    assert.match(rec.state, /CRDTs/);
  });

  test('generateAdr outputs valid markdown without em dashes', () => {
    const profile = {
      seo: 'critical',
      traffic: 'mostly_static',
      updateFrequency: 'standard',
      stateOrigin: 'remote_api',
      monorepoTs: false,
      brandUniqueness: 'custom_brand'
    };
    const rec = evaluateArchitecture(profile);
    const adr = generateAdr(profile, rec, 'Telemetry Platform');

    assert.ok(adr.includes('# ADR-0001: Frontend Architecture Selection for Telemetry Platform'));
    assert.ok(adr.includes('## Status\nAccepted'));
    assert.ok(adr.includes('## Decision'));
    assert.ok(adr.includes('## Consequences'));
    assert.ok(!adr.includes('—'), 'ADR must not contain unicode em dash');
    assert.ok(!adr.includes('--- '), 'ADR must not contain markdown em dash');
  });

  test('scaffoldRecipe correctly copies recipe files into target folder', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'choices-test-'));
    try {
      const copied = scaffoldRecipe('collaborative_canvas', tmpDir);
      assert.ok(copied.includes('package.json'));
      assert.ok(copied.includes('vite.config.ts'));
      assert.ok(fs.existsSync(path.join(tmpDir, 'package.json')));
      assert.ok(fs.existsSync(path.join(tmpDir, 'vite.config.ts')));
    } finally {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  });

  test('CLI binary executes list and version commands via child process', () => {
    const listOutput = execFileSync(process.execPath, [BIN_PATH, 'list'], { encoding: 'utf8' });
    assert.ok(listOutput.includes('Available Starter Architecture Recipes:'));
    assert.ok(listOutput.includes('content_first_astro'));

    const versionOutput = execFileSync(process.execPath, [BIN_PATH, '--version'], { encoding: 'utf8' });
    assert.ok(versionOutput.includes('@blip-cmd/choices v1.0.0'));
  });

  test('CLI binary exports ADR via command line flags', () => {
    const adrOutput = execFileSync(
      process.execPath,
      [BIN_PATH, 'export', '--seo', 'critical', '--traffic', 'mostly_static'],
      { encoding: 'utf8' }
    );
    assert.ok(adrOutput.includes('# ADR-0001: Frontend Architecture Selection'));
    assert.ok(adrOutput.includes('Islands Architecture'));
  });
});
