import { afterEach, describe, expect, it, vi } from 'vitest';

import { getMarketSnapshot } from './api';

describe('market API client', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('encodes symbols and returns a source-safe snapshot response', async () => {
    const fetchStub = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          symbol: 'NSE:NIFTY50',
          freshness: 'UNAVAILABLE',
          as_of: null,
          provider: null,
          message: 'Data unavailable until an approved provider is configured.',
        }),
        { status: 200 },
      ),
    );
    vi.stubGlobal('fetch', fetchStub);

    await expect(getMarketSnapshot('NSE:NIFTY50')).resolves.toMatchObject({
      freshness: 'UNAVAILABLE',
      symbol: 'NSE:NIFTY50',
    });
    expect(fetchStub).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/markets/snapshots/NSE%3ANIFTY50',
      expect.objectContaining({ signal: undefined }),
    );
  });

  it('surfaces non-success API responses', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(null, { status: 503 })));

    await expect(getMarketSnapshot('NSE:NIFTY50')).rejects.toThrow(
      'Market snapshot request failed with 503',
    );
  });
});
