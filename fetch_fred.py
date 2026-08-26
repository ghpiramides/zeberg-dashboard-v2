import json, os, time, urllib.request
from datetime import datetime, timezone

FRED_API_KEY = os.environ['FRED_API_KEY']
BASE = 'https://api.stlouisfed.org/fred/series/observations'

SERIES = {
    'CFNAI': 48, 'INDPRO': 48, 'PAYEMS': 36, 'RSAFS': 36,
    'UNRATE': 60, 'ICSA': 104, 'IC4WSA': 104, 'SAHMREALTIME': 48,
    'WALCL': 156, 'M2SL': 48, 'FEDFUNDS': 60,
    'T10Y2Y': 500, 'T10Y3M': 500, 'BAMLH0A0HYM2': 500, 'STLFSI4': 156,
    'VIXCLS': 500, 'UMCSENT': 120, 'RECPROUSM156N': 60,
}

out = {'fetched': datetime.now(timezone.utc).isoformat(), 'series': {}}

for sid, limit in SERIES.items():
    url = f'{BASE}?series_id={sid}&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit={limit}'
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            d = json.loads(resp.read())
        obs = [
            {'date': o['date'], 'raw': float(o['value'])}
            for o in reversed(d.get('observations', []))
            if o.get('value') not in ('.', '', None)
        ]
        out['series'][sid] = obs
        print(f'✓ {sid}: {len(obs)} data points')
    except Exception as e:
        print(f'✗ {sid}: {e}')
        out['series'][sid] = []
    time.sleep(0.2)

with open('data.json', 'w') as f:
    json.dump(out, f, separators=(',', ':'))

ok = sum(1 for v in out['series'].values() if v)
print(f'\ndata.json saved — {ok}/{len(SERIES)} series')
