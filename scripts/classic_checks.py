# Independent factual and encoding checks for the original eight fixed examples.
import hashlib
import importlib.util
import json
import math
import re
import sys
import uuid
from contextlib import contextmanager
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True

def require(v, message):
    if not v:
        raise AssertionError(message)

def close(a, b, tol=0.08):
    require(abs(float(a) - float(b)) <= tol, f'{a} != {b}')

def data(name):
    return json.loads((ROOT / 'evals/fixtures' / f'{name}.json').read_text(encoding='utf-8'))

def elements(svg, tag):
    return list(svg.iter('{http://www.w3.org/2000/svg}' + tag))

def marks(svg, name):
    return [e for e in svg.iter() if e.get('data-mark') == name]

def tick(svg, label, anchor=None):
    ts = [e for e in elements(svg, 'text') if e.text == label and (anchor is None or e.get('text-anchor') == anchor)]
    require(bool(ts), f'tick not found: {label}')
    return ts[0]

def pos(e, attr):
    return float(e.get(attr))

@contextmanager
def fixture_directory():
    p = ROOT / 'verification' / ('.audit-fixture-' + uuid.uuid4().hex)
    p.mkdir()
    try:
        yield p
    finally:
        (p / 'test.csv').unlink(missing_ok=True)
        p.rmdir()

def numerical():
    d = data('revenue')
    require(d['opening'] + sum((r['value'] for r in d['contributions'])) == d['closing'] == 1500, 'bridge reconciliation')
    d = data('latency')
    require(sorted(d['before'])[9] == 200 and sorted(d['after'])[9] == 150, 'nearest-rank p50')
    require(sorted(d['before'])[18] == 480 and sorted(d['after'])[18] == 900, 'nearest-rank p95')
    require(sum((x > 500 for x in d['before'])) == 1 and sum((x > 500 for x in d['after'])) == 4, 'strict threshold')
    p = data('paired')['participants']
    diff = sorted((r['after'] - r['before'] for r in p))
    require(len(p) == 12 and sum((x < 0 for x in diff)) == 11 and ((diff[5] + diff[6]) / 2 == -6), 'paired change')
    require([r['id'] for r in p if r['after'] > r['before']] == ['P07'], 'slow participant')
    rows = data('conversion')['rows']
    for version, k in [('Old', 100), ('New', 69)]:
        require(sum((r['success'] for r in rows if r['version'] == version)) == k, 'pooled successes')
        require(sum((r['n'] for r in rows if r['version'] == version)) == 200, 'pooled n')
    for seg in ['Organic', 'Paid']:
        a, b = [next((r for r in rows if r['segment'] == seg and r['version'] == v)) for v in ['Old', 'New']]
        require(b['success'] / b['n'] > a['success'] / a['n'], 'stratified direction')
    rows = data('sensor')['readings']
    require(sum((r['value'] is None for r in rows)) == 2, 'missing')
    require(sum((r['value'] is not None for r in rows)) == 13, 'observed')
    require(sum((r['value'] is not None and r['value'] > 70 for r in rows)) == 2, 'exceedance')
    g = data('geography')['rows']
    require(max(g, key=lambda r: r['requests'])['region'] == 'North', 'total rank')
    require(max(g, key=lambda r: r['requests'] / r['population'])['region'] == 'South', 'normalized rank')
    u = data('uncertainty')['rows']
    require(u[0]['low'] > 0 and u[1]['low'] < 0 < u[1]['high'] and (u[2]['low'] < 0 < u[2]['high']), 'intervals')
    require(max(u, key=lambda r: r['high'] - r['low'])['variant'] == 'B', 'widest interval')
    require(sum((r['amount_cents'] for r in data('ledger')['rows'])) == 421575, 'net cents')
    require(sum((r['count'] for r in data('channels')['rows'])) == 190, 'multi-select total')
    require(data('stages')['same_cohort'] is False and 'transition records' in data('stages')['missing'], 'missing transitions')
    c = data('causality')['rows']
    require(sum((r['revenue'] for r in c if not r['redesign'])) / 2 == 230, 'pre mean')
    require(sum((r['revenue'] for r in c if r['redesign'])) / 2 == 267.5, 'post mean')
    return '12 case datasets checked independently of rendering code; no causal estimator or reader study.'

def encodings():
    count = 0
    for path in sorted((ROOT / 'examples/charts').glob('*.svg')):
        s = ET.parse(path).getroot()
        name = path.name
        if name.startswith('01'):
            y0 = pos(tick(s, '0', 'end'), 'y') - 6
            yt = pos(tick(s, '1800', 'end'), 'y') - 6
            scale = (y0 - yt) / 1800
            starts = [0, 1200, 1520, 1700, 1610, 0]
            ends = [1200, 1520, 1700, 1610, 1500, 1500]
            for e, a, b in zip(marks(s, 'bridge'), starts, ends):
                close(pos(e, 'y'), y0 - max(a, b) * scale)
                close(pos(e, 'height'), abs(b - a) * scale)
        elif name.startswith('02'):
            x0 = pos(tick(s, '0', 'middle'), 'x')
            xmax = pos(tick(s, '1500', 'middle'), 'x')
            y0 = pos(tick(s, '0%', 'end'), 'y') - 6
            y1 = pos(tick(s, '100%', 'end'), 'y') - 6
            for e in marks(s, 'ecdf'):
                values = data('latency')[e.get('data-series')]
                hs = [float(x) for x in re.findall('H ([\\d.]+)', e.get('d'))]
                vs = [float(y) for y in re.findall('V ([\\d.]+)', e.get('d'))]
                require(len(vs) == len(values), 'ECDF steps')
                for i, v in enumerate(sorted(values)):
                    close(hs[i], x0 + v / 1500 * (xmax - x0))
                    close(vs[i], y0 + (i + 1) / len(values) * (y1 - y0))
        elif name.startswith('03'):
            y40 = pos(tick(s, '40', 'end'), 'y') - 6
            y80 = pos(tick(s, '80', 'end'), 'y') - 6
            pairs = {r['id']: r for r in data('paired')['participants']}
            require(len(marks(s, 'pair')) == 12, 'pair lines')
            for e in marks(s, 'paired-point'):
                close(pos(e, 'cy'), y40 + (pairs[e.get('data-id')][e.get('data-period')] - 40) / 40 * (y80 - y40))
        elif name.startswith('04'):
            x0 = pos(tick(s, '0%', 'middle'), 'x')
            x1 = pos(tick(s, '100%', 'middle'), 'x')
            rows = data('conversion')['rows']
            for e in marks(s, 'rate'):
                rs = [r for r in rows if r['version'] == e.get('data-version') and (e.get('data-group') == 'All' or r['segment'] == e.get('data-group'))]
                r = sum((x['success'] for x in rs)) / sum((x['n'] for x in rs))
                close(pos(e, 'cx'), x0 + r * (x1 - x0))
                close(float(e.get('data-value')), r, 1e-09)
        elif name.startswith('05'):
            require(len(marks(s, 'observed-segment')) == 3, 'gap segments')
            require(len(marks(s, 'sensor')) == 13, 'observed marks')
            x0 = pos(tick(s, '08:00', 'middle'), 'x')
            x1 = pos(tick(s, '16:00', 'middle'), 'x')
            y50 = pos(tick(s, '50', 'end'), 'y') - 6
            y80 = pos(tick(s, '80', 'end'), 'y') - 6
            values = {r['time']: r['value'] for r in data('sensor')['readings']}
            start = datetime.fromisoformat(next(iter(values)))
            for e in marks(s, 'sensor'):
                t = e.get('data-time')
                v = values[t]
                close(pos(e, 'cx'), x0 + (datetime.fromisoformat(t) - start).total_seconds() / (8 * 3600) * (x1 - x0))
                close(pos(e, 'cy'), y50 + (v - 50) / 30 * (y80 - y50))
        elif name.startswith('06'):
            rows = {r['region']: r for r in data('geography')['rows']}
            for e in marks(s, 'geo'):
                metric = e.get('data-metric')
                maxlabel = '1000' if metric == 'requests' else '10'
                end = tick(s, maxlabel, 'middle')
                zeros = [t for t in elements(s, 'text') if t.text == '0' and abs(pos(t, 'y') - pos(end, 'y')) < 1]
                zero = max((z for z in zeros if pos(z, 'x') < pos(end, 'x')), key=lambda z: pos(z, 'x'))
                r = rows[e.get('data-region')]
                v = r['requests'] if metric == 'requests' else r['requests'] / r['population'] * 1000
                close(pos(e, 'cx'), pos(zero, 'x') + v / float(maxlabel) * (pos(end, 'x') - pos(zero, 'x')))
        elif name.startswith('07'):
            x0 = pos(tick(s, '-2', 'middle'), 'x')
            x1 = pos(tick(s, '4', 'middle'), 'x')
            rows = {r['variant']: r for r in data('uncertainty')['rows']}
            X = lambda v: x0 + (v + 2) / 6 * (x1 - x0)
            for e in marks(s, 'interval'):
                r = rows[e.get('data-variant')]
                close(pos(e, 'x1'), X(r['low']))
                close(pos(e, 'x2'), X(r['high']))
            for e in marks(s, 'estimate'):
                close(pos(e, 'cx'), X(rows[e.get('data-variant')]['estimate']))
        elif name.startswith('08'):
            require([int(e.get('data-cents')) for e in marks(s, 'amount')] == [128450, 75625, 230000, -12500], 'ledger amounts')
            require(marks(s, 'total')[0].text == '$4,215.75', 'ledger total label')
        count += 1
    return {'svg_files_with_encoding_checks': count, 'tolerance': '0.08 SVG units, 0.000000001 for stored rates'}

def csv_audit():
    spec = importlib.util.spec_from_file_location('bundle_audit', ROOT / 'scripts/audit_data.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with fixture_directory() as temp:
        p = Path(temp) / 'test.csv'
        p.write_text('code,amount,score\n001,10,NA\n002,Infinity,2\n001,10,NA\n003,3\n004,4,5,extra\n', encoding='utf-8')
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        r = mod.audit(p)
        require(r['rows'] == 5 and r['duplicate_rows'] == 1 and (r['ragged_row_lines'] == [5, 6]), 'CSV shape')
        require(r['columns']['score']['missing'] == 3, 'missing')
        require(r['columns']['amount']['non_finite_numeric'] == 1, 'nonfinite')
        require(r['columns']['code']['candidate_type'] == 'numeric_like', 'identifier candidate')
        require(hashlib.sha256(p.read_bytes()).hexdigest() == before, 'input changed')
        for content in ['', 'x,x\n1,2\n']:
            p.write_text(content, encoding='utf-8')
            try:
                mod.audit(p)
            except ValueError:
                pass
            else:
                raise AssertionError('ambiguous/empty CSV accepted')
    return 'Missing, duplicate, ragged, numeric-looking ID, non-finite, invalid headers, empty file, non-mutation.'
