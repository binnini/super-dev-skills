// Pixel Ability-fx Forge를 화면 없이 돌려 시트(atlas)를 여러 장 내보낸다.
// <work_dir>에서(playwright를 설치한 폴더): node <skill_dir>/scripts/forge_gen.js <jobs.json> <out_dir> [forge_url]
//   jobs.json: [{ "name": "s215", "family": "aura", "power": "solar", "element": "holy",
//                 "canvas": 128, "frames": 24, "seed": 215 }, ...]
//   forge_url 기본값 http://localhost:8731/index.html (forge 폴더를 <python> -m http.server 8731 로 띄움)
// 모양(motif)은 시드가 정한다. motifSelect를 바꿔도 시드가 덮어쓰니 시드를 여러 개 돌려 고른다(10-24 확인).
// 이 파일은 플러그인 캐시에 있으므로 playwright는 이 파일 옆이 아니라 실행한 폴더(cwd)에서 찾는다
const { chromium } = require(require.resolve('playwright', { paths: [process.cwd(), __dirname] }));
const fs = require('fs');
const path = require('path');

const set = (p, id, v) => p.evaluate(([id, v]) => {
  const s = document.getElementById(id); s.value = String(v);
  s.dispatchEvent(new Event('change', { bubbles: true })); return s.value;
}, [id, v]);

(async () => {
  const [jobsFile, outDir, url = 'http://localhost:8731/index.html'] = process.argv.slice(2);
  if (!jobsFile || !outDir) { console.error('node <skill_dir>/scripts/forge_gen.js <jobs.json> <out_dir> [forge_url]'); process.exit(2); }
  const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ acceptDownloads: true })).newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url); await p.waitForTimeout(1200);
  const log = [];
  for (const j of jobs) {
    await set(p, 'familySelect', j.family || 'aura'); await p.waitForTimeout(150);
    await set(p, 'powerSelect', j.power || 'solar');
    await set(p, 'elementSelect', j.element || 'holy');
    await set(p, 'canvasSizeSelect', j.canvas || 128);
    await set(p, 'frameCountSelect', j.frames || 24);
    await p.fill('#seedInput', String(j.seed)); await p.dispatchEvent('#seedInput', 'change'); await p.waitForTimeout(300);
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 20000 }), p.click('#exportAtlasBtn')]);
    const out = path.join(outDir, `${j.name}_${dl.suggestedFilename()}`);
    await dl.saveAs(out);
    log.push({ ...j, file: path.basename(out) });
    console.log(out);
  }
  fs.writeFileSync(path.join(outDir, 'jobs_done.json'), JSON.stringify(log, null, 2));
  if (errs.length) console.error('page errors:', errs);
  await b.close();
})();
