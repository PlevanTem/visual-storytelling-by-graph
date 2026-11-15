"""Chromium QA for the static gallery. Existing Playwright/Chromium required."""
import argparse,hashlib,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'verification/screenshots'
def require(v,m):
    if not v:raise AssertionError(m)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8037/');parser.add_argument('--initial',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);works=json.loads((ROOT/'docs/collection.json').read_text(encoding='utf-8'))
    report={'status':'running','url':args.url,'checks':[],'limits':'Chromium emulation and author inspection, not physical-device, screen-reader, human-comprehension or aesthetic study.'}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True);report['browser']=browser.version
            context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,accept_downloads=True)
            page=context.new_page();errors=[];bad=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append({'url':r.url,'status':r.status}) if r.status>=400 and not 'github.com' in r.url else None)
            response=page.goto(args.url);require(response.status==200,'homepage HTTP status')
            page.locator('.work-art img').evaluate_all("es=>es.forEach(e=>e.loading='eager')");page.wait_for_function('[...document.querySelectorAll(".work-art img")].every(i=>i.complete&&i.naturalWidth>0)')
            require(page.locator('.work').count()==20,'20 works');require(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'desktop overflow')
            page.screenshot(path=str(OUT/'landing-desktop.png'))
            for section in ['use-cases','collection','skill','method']:
                page.locator('#'+section).scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'{section}-desktop.png'))
            for task in ['change','compare','distribution','structure']:
                page.locator(f'[data-filter="{task}"]').click();expected=[w['id'] for w in works if task in w['tasks']]
                require(page.locator('.work:visible').evaluate_all('(es)=>es.map(e=>e.dataset.id)')==expected,'task routing '+task)
                require(page.locator('#work-count').inner_text()==f'{len(expected)} / 20','filter count '+task)
            page.locator('[data-filter="all"]').click()
            for cid in ['C01','C02','C07','C18']:
                opener=page.locator(f'.scenario-row[data-open="{cid}"]');opener.click();require(page.locator('#exhibit').get_attribute('data-case')==cid,'scenario opens '+cid);page.keyboard.press('Escape');require(opener.evaluate('(e)=>e===document.activeElement'),'scenario focus return')
            page.goto(args.url+'#work-C02');page.wait_for_function('document.getElementById("exhibit").open');require(page.locator('#exhibit').get_attribute('data-case')=='C02','direct case URL');page.keyboard.press('Escape')
            request=page.locator('#request-template').inner_text();require(len(request.splitlines())>=7 and '$visual-storytelling-by-graph' in request,'usable request template')
            page.locator('#copy-request').click();page.wait_for_function('document.getElementById("request-status").textContent.trim().length>0')
            report['checks'].append({'check':'user_journey_task_filters_scenarios_permalink_request','status':'pass','tasks':4,'scenario_links':4})
            states=[]
            for w in works:
                opener=page.locator(f'.work[data-id="{w["id"]}"] .work-open');opener.click();require(page.locator('#exhibit').is_visible(),'dialog open')
                require(page.locator('#exhibit').get_attribute('data-case')==w['id'],'case identity')
                for j,state in enumerate(w['states']):
                    if len(w['states'])>1:page.locator(f'#state-controls button[data-index="{j}"]').click()
                    page.locator('#exhibit-image').evaluate('(i)=>i.decode()');require(page.locator('#exhibit').get_attribute('data-state')==state['key'],'state identity')
                    require(page.locator('#state-summary').inner_text()==state['summary']['en'],'summary state')
                    require(page.locator('#download-svg').get_attribute('aria-disabled')==str(not state['available']).lower(),'download availability')
                    states.append({'case':w['id'],'state':state['key'],'status':'pass'})
                if len(w['states'])>1:page.locator(f'#state-controls button[data-index="{w["defaultState"]}"]').click();page.locator('#exhibit-image').evaluate('(i)=>i.decode()')
                page.screenshot(path=str(OUT/f'{w["id"]}-desktop.png'))
                page.locator('#toggle-info').click();require(page.locator('#exhibit-info').is_visible(),'method panel');require(bool(page.locator('#work-question').inner_text()),'question content');page.locator('#toggle-info').click()
                page.locator('#close-exhibit').click();require(not page.locator('#exhibit').is_visible(),'close');require(opener.evaluate('(e)=>e===document.activeElement'),'focus return')
            report['checks'].append({'check':'desktop_gallery_and_all_states','status':'pass','viewport':[1440,1000],'states':states})
            page.locator('.work[data-id="C13"] .work-open').click();page.keyboard.press('ArrowRight');require(page.locator('#exhibit').get_attribute('data-case')=='C14','arrow next');page.keyboard.press('ArrowLeft');require(page.locator('#exhibit').get_attribute('data-case')=='C13','arrow previous');page.keyboard.press('Escape');require(not page.locator('#exhibit').is_visible(),'Escape close')
            page.locator('.work[data-id="C19"] .work-open').click();page.locator('#state-controls button[data-index="2"]').click()
            with page.expect_download() as download:page.locator('#download-svg').click()
            export=OUT/'export-recurrence-045.svg';download.value.save_as(str(export));require('epsilon 0.45' in export.read_text(encoding='utf-8'),'contextual SVG export');page.keyboard.press('Escape')
            page.locator('#language').click();require(page.locator('html').get_attribute('lang')=='zh-CN','Chinese');page.locator('.work[data-id="C17"] .work-open').click();require('我们的档案' in page.locator('#work-question').inner_text(),'Chinese question');page.keyboard.press('Escape');page.locator('#language').click()
            page.locator('#copy-install').click();page.wait_for_function('document.getElementById("copy-status").textContent.trim().length>0');require(bool(page.locator('#copy-status').inner_text()),'clipboard success or fallback feedback')
            if not args.initial:
                with page.expect_download() as package:page.locator('.install-actions a').click()
                target=OUT/'downloaded-skill.zip';package.value.save_as(str(target));require(target.stat().st_size>10000,'Skill download')
                import zipfile
                with zipfile.ZipFile(target) as z:require(z.testzip() is None,'download CRC');require(any(x.endswith('/SKILL.md') for x in z.namelist()),'package Skill')
                target.unlink()
            report['checks'].append({'check':'keyboard_language_copy_export_download','status':'pass','skill_download':'not_run' if args.initial else 'pass'})
            page.set_viewport_size({'width':390,'height':844});page.goto(args.url);page.screenshot(path=str(OUT/'landing-mobile.png'));require(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'mobile overflow')
            for w in works:
                page.locator(f'.work[data-id="{w["id"]}"] .work-open').click();page.locator('#exhibit-image').evaluate('(i)=>i.decode()');require('-mobile.svg' in page.locator('#exhibit-image').evaluate('(i)=>i.currentSrc'),'mobile asset selected');page.screenshot(path=str(OUT/f'{w["id"]}-mobile.png'));require(page.locator('#exhibit').evaluate('(e)=>e.scrollWidth<=innerWidth'),'mobile dialog width');page.keyboard.press('Escape')
            page.locator('#language').click();page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/'landing-mobile-zh.png'));require(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Chinese mobile width')
            for section in ['use-cases','skill','method']:
                page.locator('#'+section).scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'{section}-mobile-zh.png'))
            require('undefined' not in page.locator('body').inner_text(),'complete translation')
            report['checks'].append({'check':'mobile_all_works_bilingual','status':'pass','viewport':[390,844],'works':20})
            layouts=[]
            for file in sorted((ROOT/'docs/assets').glob('c*.svg')):
                if '-preview' in file.name:continue
                page.goto(args.url+'assets/'+file.name)
                result=page.evaluate('''() => {const v=document.documentElement.viewBox.baseVal,ts=[...document.querySelectorAll('text')].map(t=>{const b=t.getBBox();return{text:t.textContent,x:b.x,y:b.y,w:b.width,h:b.height}}),outside=ts.filter(b=>b.x<-.5||b.y<-.5||b.x+b.w>v.width+.5||b.y+b.h>v.height+.5),overlaps=[];for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){const a=ts[i],b=ts[j],x=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x),y=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);if(x>2&&y>2)overlaps.push([a.text,b.text,x,y])}return{outside,overlaps,text_count:ts.length}}''')
                layouts.append({'file':file.name,**result})
            report['checks'].append({'check':'full_svg_text_layout','status':'pass' if all(not r['outside'] and not r['overlaps'] for r in layouts) else 'fail','files':layouts})
            nojs=browser.new_context(java_script_enabled=False,viewport={'width':1280,'height':900});np=nojs.new_page();np.goto(args.url);require(np.locator('.work-open[href$=".svg"]').count()==20,'no JS static links');require(not np.locator('.filter-bar').is_visible(),'nonfunctional filters hidden');require(not np.locator('#copy-request').is_visible(),'nonfunctional copy hidden');nojs.close()
            require(not errors,'JavaScript errors: '+str(errors));require(not bad,'HTTP errors: '+str(bad))
            report['checks'].append({'check':'no_js_and_no_runtime_errors','status':'pass','page_errors':errors,'http_errors':bad})
            page.set_viewport_size({'width':1200,'height':630});page.goto(args.url);page.screenshot(path=str(ROOT/'docs/assets/social-preview.png'))
            context.close();browser.close()
        report['status']='pass' if all(x['status']=='pass' for x in report['checks']) else 'fail'
    except Exception as e:report['status']='fail';report['error']=f'{type(e).__name__}: {e}'
    report['hash_scheme']='SHA256 of UTF-8 text with CRLF normalized to LF; content is otherwise unchanged.'
    report['inputs_sha256']={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [ROOT/'docs/index.html',ROOT/'docs/style.css',ROOT/'docs/app.js',ROOT/'docs/collection.js',ROOT/'docs/assets/hero.svg',ROOT/'docs/assets/mark.svg',*sorted((ROOT/'docs/assets').glob('c*.svg'))]}
    (ROOT/'verification/gallery-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'checks':[(c['check'],c['status']) for c in report['checks']],'error':report.get('error')},indent=2));return int(report['status']!='pass')

if __name__=='__main__':sys.exit(main())
