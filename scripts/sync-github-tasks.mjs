import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {readFileSync, writeFileSync, renameSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';

const root = fileURLToPath(new URL('../', import.meta.url));
const mode = process.argv[2];
if (!['--check', '--apply'].includes(mode) || process.argv.length !== 3) {
  console.error('Uso: node scripts/sync-github-tasks.mjs --check | --apply');
  process.exit(2);
}
const apply = mode === '--apply';
const repository = JSON.parse(readFileSync(resolve(root, 'docs/GITHUB_REPOSITORY.json'), 'utf8'));
const trackingPath = resolve(root, 'docs/GITHUB_TRACKING.json');
const tracking = JSON.parse(readFileSync(trackingPath, 'utf8'));
const todo = readFileSync(resolve(root, 'docs/TODO_T7.md'), 'utf8').replace(/\r\n/g, '\n');

if (repository.full_name !== 'BenjaAranda/DepartamentoT7' || repository.repository_id !== 1362108111 || tracking.repository !== repository.full_name) {
  throw new Error('El destino no coincide con el repositorio T7 autorizado.');
}

const stages = [];
let stage;
const allIds = new Set();
for (const line of todo.split(/\r?\n/)) {
  const heading = line.match(/^## (E\d{2})\. (.+)$/);
  if (heading) {
    stage = {id:heading[1], title:heading[2], lines:[], tasks:[]};
    stages.push(stage);
  } else if (line.startsWith('## ')) {
    stage = undefined;
  } else if (stage) {
    stage.lines.push(line);
    const task = line.match(/^- \[([ x])\] ((?:P|T)\d{2})\. /);
    if (task) {
      if (allIds.has(task[2])) throw new Error('ID de tarea duplicado: '+task[2]);
      allIds.add(task[2]);
      stage.tasks.push({id:task[2], done:task[1] === 'x'});
    }
  }
}
if (stages.length === 0 || stages.some(s => s.tasks.length === 0)) throw new Error('La lista de tareas no tiene la estructura esperada.');

let password;
try {
  const raw = execFileSync('git', ['-c','credential.interactive=false','credential','fill'], {
    input:'protocol=https\nhost=github.com\nusername=BenjaAranda\n\n',encoding:'utf8',
    stdio:['pipe','pipe','pipe'],env:{...process.env,GCM_INTERACTIVE:'never',GIT_TERMINAL_PROMPT:'0'}
  });
  password = raw.split(/\r?\n/).find(l => l.startsWith('password='))?.slice('password='.length);
} catch { throw new Error('No se pudo usar la sesión existente de GitHub.'); }
if (!password) throw new Error('No se recibió una credencial de GitHub.');

const headers = {Accept:'application/vnd.github+json',Authorization:'Bearer '+password,'X-GitHub-Api-Version':'2026-03-10','User-Agent':'T7-task-sync'};
let lastWrite = 0;
async function request(path, method='GET', body) {
  if (method !== 'GET') {
    if (!apply) throw new Error('El modo de comprobación no permite escrituras.');
    await delay(Math.max(0, 1500-(Date.now()-lastWrite)));
    lastWrite = Date.now();
  }
  const response = await fetch('https://api.github.com'+path, {
    method,headers:{...headers,...(body ? {'Content-Type':'application/json'} : {})},
    ...(body ? {body:JSON.stringify(body)} : {}),redirect:'error',signal:AbortSignal.timeout(30000)
  });
  const data = await response.json();
  if (!response.ok) throw new Error('GitHub devolvió HTTP '+response.status+' en '+method+' '+path+'. No se reintentó la escritura; comprobar el estado antes de reanudar.');
  return data;
}
const account = await request('/user');
if (account.login !== repository.owner) throw new Error('La cuenta autenticada no coincide con el propietario previsto.');
const remote = await request('/repos/'+repository.full_name);
if (remote.id !== repository.repository_id || remote.private !== true || remote.permissions?.push !== true) {
  throw new Error('No se confirmaron el destino privado y sus permisos de escritura.');
}

const endpoint = '/repos/'+repository.full_name+'/issues';
const issues = [];
for (let page=1; ; page++) {
  const batch = await request(endpoint+'?state=all&per_page=100&page='+page);
  if (!Array.isArray(batch)) throw new Error('La respuesta de tareas no es una lista.');
  issues.push(...batch.filter(item => !item.pull_request));
  if (batch.length < 100) break;
}

function saveMapping() {
  const temporary = trackingPath+'.tmp';
  writeFileSync(temporary, JSON.stringify(tracking,null,2)+'\n','utf8');
  renameSync(temporary,trackingPath);
}

const changes = [];
const results = [];
for (const stage of stages) {
  const start = '<!-- t7-stage:'+stage.id+':start -->';
  const end = '<!-- t7-stage:'+stage.id+':end -->';
  const managed = start+'\nFuente: [lista principal]('+repository.html_url+'/blob/main/docs/TODO_T7.md) · [plan y criterios]('+repository.html_url+'/blob/main/docs/PLAN_MAESTRO_T7.md).\n\n'+stage.lines.join('\n').trim()+'\n'+end;
  const state = stage.tasks.every(t => t.done) ? 'closed' : 'open';
  const candidates = issues.filter(issue => (issue.body ?? '').includes(start));
  if (candidates.length > 1) throw new Error('Hay tareas duplicadas para '+stage.id+'; revisar antes de sincronizar.');
  const savedNumber = tracking.stages?.[stage.id]?.issue_number;
  let issue = candidates[0];
  if (savedNumber && (!issue || issue.number !== savedNumber)) throw new Error('El registro persistente y la tarea remota no coinciden para '+stage.id+'.');
  const isNew = !issue;
  let body = managed;
  if (issue) {
    const existing = issue.body ?? '';
    const first = existing.indexOf(start);
    const last = existing.indexOf(end,first);
    if (last < first || existing.indexOf(start,first+start.length) !== -1 || existing.indexOf(end,last+end.length) !== -1) throw new Error('El bloque administrado está incompleto o duplicado en '+stage.id+'.');
    body = existing.slice(0,first)+managed+existing.slice(last+end.length);
  }
  const differs = isNew || issue.body !== body || issue.state !== state;
  if (differs) changes.push(stage.id);
  if (apply) {
    if (isNew) {
      issue = await request(endpoint,'POST',{title:'['+stage.id+'] '+stage.title,body});
      issues.push(issue);
      tracking.stages ??= {};
      tracking.stages[stage.id] = {issue_number:issue.number,issue_url:issue.html_url,task_ids:stage.tasks.map(t=>t.id)};
      saveMapping();
    }
    if (issue.body !== body || issue.state !== state) {
      const update = {body,state,...(state === 'closed' ? {state_reason:'completed'} : {})};
      issue = await request(endpoint+'/'+issue.number,'PATCH',update);
    }
    // A read after each mutation confirms the stored body and state.
    if (differs) issue = await request(endpoint+'/'+issue.number);
    if (issue.body !== body || issue.state !== state) throw new Error('No se confirmó la actualización de '+stage.id+'.');
    tracking.stages ??= {};
    tracking.stages[stage.id] = {issue_number:issue.number,issue_url:issue.html_url,task_ids:stage.tasks.map(t=>t.id)};
    saveMapping();
  }
  results.push({stage:stage.id,issue_number:issue?.number ?? null,state:issue?.state ?? null,task_count:stage.tasks.length,completed:stage.tasks.filter(t=>t.done).length,matches:apply || !differs});
  console.log(stage.id+': '+(apply ? (differs?'sincronizada':'sin cambios') : (differs?'requiere sincronización':'coincide')));
}
const summary = {checked_at:new Date().toISOString(),source_sha256:createHash('sha256').update(todo).digest('hex'),stage_count:stages.length,task_count:allIds.size,completed_tasks:stages.reduce((n,s)=>n+s.tasks.filter(t=>t.done).length,0),open_stages:results.filter(r=>r.state==='open').length,closed_stages:results.filter(r=>r.state==='closed').length,all_match:results.every(r=>r.matches),stages:results};
if (apply) {
  tracking.last_sync = summary;
  saveMapping();
}
console.log(JSON.stringify(summary,null,2));
if (!apply && changes.length) process.exitCode=1;
