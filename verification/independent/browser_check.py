from pathlib import Path
import json
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
report={'scope':'Chromium, local HTML; desktop 1200x900 and narrow 390x844; no human-reader study','checks':[]}
def record(label, condition):
    assert condition,label
    report['checks'].append({'name':label,'status':'pass'})
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1200,'height':900},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((HERE/'index.html').as_uri())
    record('Default C17 counts visible',page.locator('#C17-0').is_visible() and '64 objects | 15 exact patterns' in page.locator('#C17-0').inner_text())
    page.locator('[data-select="C17-1"]').click()
    record('C17 filtered counts and mode visible',page.locator('#C17-1').is_visible() and not page.locator('#C17-0').is_visible() and '42 objects | 11 exact patterns' in page.locator('#C17-1').inner_text())
    for idx,expected in enumerate(['422/4032 = 10.47%','986/4032 = 24.45%','1744/4032 = 43.25%']):
        page.locator(f'[data-select="C19-{idx}"]').click()
        record(f'C19 threshold {idx} data/summary visible',expected in page.locator(f'#C19-{idx}').inner_text() and page.locator(f'#C19-{idx}').is_visible())
    page.locator('[data-reset="C19-0"]').focus()
    page.keyboard.press('Enter')
    record('Keyboard reset returns C19 default',page.locator('#C19-0').is_visible() and page.locator('[data-select="C19-0"]').get_attribute('aria-pressed')=='true')
    page.locator('[data-reset="C17-0"]').click()
    record('C17 reset restores counts',page.locator('#C17-0').is_visible() and '64 objects' in page.locator('#C17-0').inner_text())
    # Actual SVG text bounds, in native viewBox coordinates, for every state, made visible in turn.
    outliers=[]
    for case,states in [('C15',1),('C17',2),('C19',3),('C23',1)]:
        for idx in range(states):
            page.locator(f'[data-select="{case}-{idx}"]').click()
            bad=page.locator(f'#{case}-{idx} svg').evaluate('''svg=>{const b=svg.viewBox.baseVal;return [...svg.querySelectorAll('text')].map(t=>({text:t.textContent,b:t.getBBox()})).filter(t=>t.b.x<0||t.b.y<0||t.b.x+t.b.width>b.width||t.b.y+t.b.height>b.height).map(t=>t.text)}''')
            outliers.extend({'state':f'{case}-{idx}','text':s} for s in bad)
    record('All state SVG text stays inside native viewBox',not outliers)
    page.locator('[data-select="C17-0"]').click();page.locator('[data-select="C19-0"]').click()
    page.screenshot(path=str(HERE/'desktop.png'),full_page=True)
    for case in ['C15','C17','C19','C23']:
        page.locator(f'section[data-case="{case}"]').screenshot(path=str(HERE/f'{case}-desktop.png'))
    page.set_viewport_size({'width':390,'height':844})
    record('390px layout has no document horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.locator('[data-select="C17-1"]').click()
    record('390px filter operates',page.locator('#C17-1').is_visible())
    page.screenshot(path=str(HERE/'narrow.png'),full_page=True)
    record('No browser JS errors',not errors)
    report['errors']=errors
    report['text_outliers']=outliers
    browser.close()
(HERE/'browser-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
results=json.loads((HERE/'results.json').read_text(encoding='utf-8'))
results['verification']['render']='pass: Chromium desktop 1200x900; narrow 390x844; native SVG text bounds for all seven states'
results['verification']['interaction']='pass: C17 filter/reset; C19 three thresholds; keyboard Enter reset; narrow C17 filter'
results['verification']['browser_evidence']='browser-results.json; desktop.png; narrow.png; C15/C17/C19/C23-desktop.png'
(HERE/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
