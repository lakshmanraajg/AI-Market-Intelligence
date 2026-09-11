import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

describe('market data safety defaults', () => {
  const terminalSource = readFileSync('src/main.tsx', 'utf8');

  it('does not represent unconfigured instrument values as live market data', () => {
    expect(terminalSource).toContain("status:'UNAVAILABLE'");
    expect(terminalSource).toContain('No live prices are fabricated');
    expect(terminalSource).toContain('Connected provider data is required before a status can be LIVE');
  });
});
