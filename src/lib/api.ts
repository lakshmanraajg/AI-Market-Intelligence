export type Freshness = 'LIVE' | 'DELAYED' | 'STALE' | 'UNAVAILABLE';

export interface MarketSnapshot {
  symbol: string;
  freshness: Freshness;
  as_of: string | null;
  provider: string | null;
  message: string;
}

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '');

export async function getMarketSnapshot(symbol: string, signal?: AbortSignal): Promise<MarketSnapshot> {
  const response = await fetch(
    `${apiBaseUrl}/api/v1/markets/snapshots/${encodeURIComponent(symbol)}`,
    { headers: { Accept: 'application/json' }, signal },
  );

  if (!response.ok) {
    throw new Error(`Market snapshot request failed with ${response.status}`);
  }

  return response.json() as Promise<MarketSnapshot>;
}
