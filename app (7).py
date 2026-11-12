"""다음에 거기 가면 — Streamlit 위치 기반 준비물 알림.
배포: 이 파일과 requirements.txt를 GitHub 저장소 루트에 올린 뒤
Streamlit Community Cloud에서 app.py를 선택합니다. HTTPS에서 접속하세요.
GPS와 데이터는 브라우저 안에서 처리합니다. 외부 지도 타일/CDN 요청은 발생합니다.
브라우저 탭을 켜고 화면을 유지해야 합니다. 백그라운드 알림 앱이 아닙니다.
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="다음에 거기 가면", page_icon='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA3MiA3MiI+PHJlY3Qgd2lkdGg9IjcyIiBoZWlnaHQ9IjcyIiByeD0iMTkiIGZpbGw9IiMzZTYwZWUiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxOCAxOCkiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMi41Ij48cGF0aCBkPSJNMjkgMTVjMCA4LTExIDE2LTExIDE2UzcgMjMgNyAxNWExMSAxMSAwIDEgMSAyMiAwWiIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPjxjaXJjbGUgY3g9IjE4IiBjeT0iMTUiIHI9IjMuOCIvPjwvZz48L3N2Zz4=', layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
.block-container{padding:0.5rem 0.4rem 1rem;max-width:1050px}
header[data-testid="stHeader"]{display:none}
</style>""", unsafe_allow_html=True)

HTML = r'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<style>
:root{--bg:#f5f7fc;--ink:#17243a;--muted:#65748c;--blue:#3e64ec;--line:#e0e6f0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,'Segoe UI',sans-serif}button,input,select,textarea{font:inherit}button{cursor:pointer;border:0;border-radius:12px;padding:11px 16px;background:#e9eefc;color:#2444a3;font-weight:650}button.primary{background:var(--blue);color:white}button.danger{background:#fff0ef;color:#b43e36}button:disabled{opacity:.45;cursor:not-allowed}button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #9db6ff;outline-offset:2px}input,select,textarea{width:100%;border:1px solid #cdd6e5;border-radius:10px;padding:10px;background:white;color:var(--ink)}label{display:block;font-size:13px;font-weight:650;margin:10px 0 5px}small,.muted{color:var(--muted)}h1,h2,h3,p{margin-top:0}h1{font-size:29px;letter-spacing:-1px}h2{font-size:20px}h3{font-size:16px}.wrap{max-width:980px;margin:auto;padding:22px}.card{background:white;border:1px solid var(--line);border-radius:21px;padding:22px;margin-bottom:16px}.hero{background:linear-gradient(125deg,#e9efff,#f0fbf7)}.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.row>*{min-width:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.badge{background:#edf2ff;color:#3454b3;border-radius:30px;padding:4px 12px;font-size:12px;display:inline-block;margin-bottom:12px}.bigicon{font-size:62px;background:white;border-radius:28px;display:inline-block;padding:12px 24px;margin:14px 0 22px}.hidden{display:none!important}.hint{font-size:13px;color:var(--muted)}#map{height:310px;border-radius:14px;margin-top:12px;z-index:0}.place,.item,.event{border-top:1px solid var(--line);padding:12px 0}.place:first-child,.item:first-child{border:0}.item{display:flex;align-items:center;gap:10px}.item input{width:20px;height:20px}.item span{flex:1}.done{text-decoration:line-through;color:#8b95a5}.toast{position:fixed;top:12px;left:50%;transform:translateX(-50%);width:min(92%,600px);background:#15243d;color:white;border-radius:17px;padding:18px;z-index:2000;box-shadow:0 12px 40px #14234840;max-height:70vh;overflow:auto}.toast button{margin-top:10px}.status{padding:12px;border-radius:12px;background:#f1f5ff;margin:12px 0;white-space:pre-line}.tab{background:transparent}.tab.active{background:#dfe8ff}.list-buttons button{padding:5px 10px;font-size:12px;margin:3px}.metric{font-size:27px;font-weight:750;color:#3458d4}#landing{text-align:center;padding:55px 22px}#landing p{max-width:470px;margin:0 auto 22px}details summary{cursor:pointer;font-weight:650}#qr img{margin:15px auto}a{color:#3655ba}.warn{color:#96510a} @media(max-width:680px){.grid{grid-template-columns:1fr}.wrap{padding:12px}.card{padding:17px}h1{font-size:25px}.row.mobile>*{width:100%}}

/* Minimal welcome screen; existing home panels and event handlers preserved. */
body:has(#home.hidden){background:#fff}
#landing{text-align:center;position:relative;min-height:740px;padding:0;background:#fff}
#landing .landing-content{padding:207px 20px 90px}
#landing .app-icon{width:72px;height:72px;margin:0 auto 28px}
#landing .app-icon svg{display:block;width:72px;height:72px}
#landing h1{font-size:32px;font-weight:700;line-height:1.4;letter-spacing:-1.2px;color:#182438;margin:0 0 15px}
#landing p{max-width:none;margin:0;color:#687487;font-size:18px;line-height:1.7}
#landing #enter{display:block;width:280px;max-width:100%;height:54px;margin:38px auto 0;padding:0 16px;border-radius:12px;background:#3e60ee;color:#fff;font-size:17px;font-weight:600}
#landing #enter:hover{background:#3454d8}
@media(max-width:680px){#landing{min-height:650px}#landing .landing-content{padding:150px 8px 80px}#landing h1{font-size:28px}#landing p{font-size:16px}}
</style></head><body>
<div class="wrap">
<section id="landing" aria-labelledby="landing-title"><div class="landing-content"><div class="app-icon" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"><rect width="72" height="72" rx="19" fill="#3e60ee"/><g transform="translate(18 18)" fill="none" stroke="white" stroke-width="2.5"><path d="M29 15c0 8-11 16-11 16S7 23 7 15a11 11 0 1 1 22 0Z" stroke-linejoin="round"/><circle cx="18" cy="15" r="3.8"/></g></svg></div><h1 id="landing-title">다음에 거기 가면</h1><p>그곳에 가면, 살 것과 챙길 것을 알려드려요.</p><button class="primary" id="enter" type="button">시작하기</button></div></section>
<main id="home" class="hidden">
<div class="row" style="justify-content:space-between;margin-bottom:16px"><div><span class="badge">작은 기억 도우미</span><h1 style="margin:0">📍 다음에 거기 가면</h1></div><button id="intro">소개 화면</button></div>
<div class="row" style="margin-bottom:15px"><button class="tab active" data-tab="travel">내 물건 알림</button><button class="tab" data-tab="places">장소 · 준비물</button><button class="tab" data-tab="settings">QR · 데이터</button></div>
<section id="travel" class="panel">
<div class="card hero"><h2>오늘도, 잊지 말고 챙겨요</h2><p class="hint">위치를 켜면 등록한 모든 장소의 100m 안에서 살 것과 챙길 것을 알려드려요. 휴대폰 잠금·탭 전환 시 GPS가 멈출 수 있습니다.</p><div class="row"><button class="primary" id="gpsOn">📡 내 위치 켜기</button><button id="gpsOff">위치 끄기</button><button id="sound">🔇 소리 꺼짐</button></div><div id="gpsStatus" class="status" role="status">위치가 꺼져 있습니다.</div><form id="destSearchForm" class="search-form"><label for="destSearchQuery">장소 이름 검색</label><div class="row"><input id="destSearchQuery" maxlength="100" placeholder="예: 이마트, 스타벅스, 서울시청" required style="flex:1;min-width:160px"><button class="primary" id="destSearchButton" type="submit">검색</button></div><label class="hint"><input id="destSearchNearby" type="checkbox" checked style="width:auto"> 주변 20km에서 찾기</label><p class="hint">현재 위치를 켜면 내 주변에서, 꺼져 있으면 지도 중심 주변에서 찾습니다.</p><div id="destSearchStatus" class="hint" role="status" aria-live="polite"></div><div id="destSearchResults"></div></form><div id="map"></div><p class="hint">장소 검색: <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">© OpenStreetMap contributors</a> · 공개 검색은 일부 건물이 누락될 수 있습니다.</p><p class="hint">검색 결과를 선택하거나 위성지도에서 원하는 건물을 누르세요. </p></div>
<div class="card"><h2>최근 도착 알림</h2><div id="history"></div><p class="hint">도착지 100m 안에서 약 4초간 위치를 확인한 뒤 알립니다. 위치 오차가 크면 알림을 보류합니다. 실제 위치와 반경 경계 부근에서는 GPS 오차로 오작동할 수 있습니다.</p></div>
</section>
<section id="places" class="panel hidden"><div class="grid"><div><div class="card"><h2 id="formTitle">자주 가는 장소 추가</h2><form id="placeSearchForm" class="search-form"><label for="placeSearchQuery">장소 이름 검색</label><div class="row"><input id="placeSearchQuery" maxlength="100" placeholder="예: 이마트, 스타벅스, 서울시청" required style="flex:1;min-width:160px"><button class="primary" id="placeSearchButton" type="submit">검색</button></div><label class="hint"><input id="placeSearchNearby" type="checkbox" checked style="width:auto"> 주변 20km에서 찾기</label><p class="hint">현재 위치를 켜면 내 주변에서, 꺼져 있으면 지도 중심 주변에서 찾습니다.</p><div id="placeSearchStatus" class="hint" role="status" aria-live="polite"></div><div id="placeSearchResults"></div></form><label for="placeName">장소 이름</label><input id="placeName" maxlength="50" placeholder="집, 마트, 회사…"><input id="lat" type="hidden"><input id="lng" type="hidden"><div id="selectedPlace" class="status" role="status">장소 이름을 검색한 뒤 결과를 선택하세요.</div><button id="useHere" style="margin-top:10px">현재 GPS 위치 사용</button><p class="hint">검색 결과를 선택하거나 위성지도에서 위치를 지정하세요. 장소 이름은 집·회사 등으로 바꿀 수 있습니다.</p><input id="radius" type="hidden" value="100"><p class="hint">도착지 반경 100m에 들어오면 자동으로 알려드려요.</p><div class="row" style="margin-top:15px"><button class="primary" id="savePlace">장소 저장</button><button id="cancelEdit">새로 입력</button></div></div><div class="card"><h2>준비물 · 살 물건 추가</h2><label for="destination">물건을 등록할 장소</label><select id="destination"></select><p id="itemTarget" class="status" role="status">먼저 도착지를 선택하세요.</p><label for="kind">알림 종류</label><select id="kind"><option value="pack">챙기기</option><option value="buy">구매하기</option></select><label for="itemText">물건 이름</label><input id="itemText" maxlength="100" placeholder="예: 우산, 건전지"><button id="addItem" class="primary" style="margin-top:12px">알림 목록에 추가</button><p class="hint">완료 체크한 물건은 알림에서 제외됩니다. 다시 필요하면 체크를 해제하세요.</p></div></div><div class="card"><h2>내 장소와 준비물</h2><div id="placeList"></div></div></div></section>
<section id="settings" class="panel hidden"><div class="card"><h2>QR로 접속하기</h2><p>배포된 앱의 <b>공유 주소</b>를 붙여넣고 QR을 만들어보세요.</p><label for="appUrl">Streamlit 앱 URL</label><input id="appUrl" type="url" placeholder="https://your-app.streamlit.app"><button id="makeQr" class="primary" style="margin-top:12px">QR 만들기</button><div id="qr"></div><p class="hint">QR은 앱을 여는 용도이며 자동으로 위치 권한을 허용하지 않습니다. 메신저 내장 브라우저보다 Safari·Chrome에서 여는 것을 권장합니다. 기기마다 장소를 따로 설정하거나 아래 백업 파일을 가져오세요.</p></div><div class="card"><h2>내 데이터</h2><p>장소·준비물는 <b>이 기기의 같은 브라우저</b>에 저장됩니다. 계정 동기화 기능은 없습니다. GPS 좌표는 Python 서버로 전달하지 않습니다. 장소 검색 시 검색어와 주변 검색 범위가 외부 검색 서비스로 전송됩니다. 위성지도 제공자는 요청한 지도 영역을 알 수 있습니다.</p><div id="storageStatus" class="hint"></div><div class="row"><button id="export">JSON 백업 내려받기</button><button id="importButton">JSON 백업 가져오기</button></div><input type="file" accept="application/json,.json" id="importFile" class="hidden"><p class="hint">백업에는 집 등 민감한 위치가 포함될 수 있습니다. 공개 GitHub에 올리지 마세요. 브라우저 기록 삭제·시크릿 모드·배포 주소 변경 시 저장 데이터가 사라질 수 있습니다.</p></div><div class="card"><h2>알림이 잘 오도록</h2><p>① HTTPS로 접속하고 위치 권한을 허용하세요.<br>② 장소와 물건을 등록한 뒤 ‘내 위치 켜기’를 누르세요.<br>③ 화면을 켜두고 이 앱을 전면에 유지하세요.<br>④ 알림은 앱 안 배너와 기록으로 표시됩니다. 소리는 직접 켠 경우에만 시도합니다.</p><p class="hint">OS 푸시·백그라운드 추적은 제공하지 않습니다. 브라우저 정책상 소리·진동·화면 유지가 제한될 수 있습니다. 지도/CDN 로딩에는 인터넷 연결이 필요합니다. </p></div></section>
</main></div><div id="toast" class="toast hidden" role="alert" aria-live="assertive"><div id="toastText"></div><button id="dismiss">확인</button></div>
<script>
'use strict';
const $=id=>document.getElementById(id), KEY='there-next-time-v1';
let data={version:1,places:[],routes:[],history:[]}, storageOK=true;
function validate(x){
 if(!x||x.version!==1||!Array.isArray(x.places)||!Array.isArray(x.routes)||!Array.isArray(x.history))throw Error('지원하지 않는 백업 형식입니다.');
 if(x.places.length>200||x.routes.length>200||x.history.length>100)throw Error('백업 크기가 너무 큽니다.');
 const ids=new Set();for(const p of x.places){if(!p||typeof p.id!=='string'||ids.has(p.id)||typeof p.name!=='string'||!p.name.trim()||p.name.length>50||!Number.isFinite(p.lat)||Math.abs(p.lat)>90||!Number.isFinite(p.lng)||Math.abs(p.lng)>180||![100,200,300,500].includes(p.radius)||!Array.isArray(p.items)||p.items.length>500)throw Error('장소 데이터가 올바르지 않습니다.');ids.add(p.id);const ii=new Set();for(const i of p.items){if(!i||typeof i.id!=='string'||ii.has(i.id)||typeof i.text!=='string'||!i.text.trim()||i.text.length>100||!['pack','buy'].includes(i.kind)||typeof i.done!=='boolean')throw Error('준비물 데이터가 올바르지 않습니다.');ii.add(i.id);}}
 for(const r of x.routes){if(!r||typeof r.id!=='string'||typeof r.name!=='string'||!Array.isArray(r.stops)||!r.stops.length||r.stops.length>100||r.stops.some(id=>!ids.has(id))||!(r.start===''||ids.has(r.start))||typeof r.repeat!=='boolean')throw Error('경로 데이터가 올바르지 않습니다.');}
 for(const h of x.history){if(!h||typeof h.time!=='string'||typeof h.place!=='string'||typeof h.text!=='string')throw Error('알림 기록 형식이 올바르지 않습니다.');}x.places.forEach(p=>p.radius=100);return x;
}
try{const raw=localStorage.getItem(KEY);if(raw)data=validate(JSON.parse(raw));}catch(e){storageOK=false;}
function save(){try{localStorage.setItem(KEY,JSON.stringify(data));storageOK=true;}catch(e){storageOK=false;}$('storageStatus').textContent=storageOK?'브라우저 저장 사용 중 · 백업을 정기적으로 권장합니다.':'저장 공간이 차단되었거나 기존 데이터를 읽지 못했습니다. 현재 변경은 유지되지 않을 수 있으니 백업하세요.';}
function id(){return Date.now().toString(36)+Math.random().toString(36).slice(2);}
function node(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
function button(text,fn,cls){const b=node('button',text,cls);b.onclick=fn;return b;}
let searchLayer=null,selectedMarker=null,searchBusy=false,lastSearchTime=0;
const SEARCH_ENDPOINT='https://nominatim.openstreetmap.org/search';
const searchCache=new Map();
let watch=null,pos=null,lastFix=0,editId=null,extra=[],active=null,map=null,userMarker=null,mapLayer=null,soundOn=false,audio=null,wake=null;
function message(text){$('toastText').textContent=text;$('toast').classList.remove('hidden');}
$('dismiss').onclick=()=>$('toast').classList.add('hidden');
function tab(name){document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('hidden',p.id!==name));document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('active',b.dataset.tab===name));if(name==='travel')setTimeout(()=>{initMap();if(map)map.invalidateSize();},100);}
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>tab(b.dataset.tab));
$('enter').onclick=()=>{$('landing').classList.add('hidden');$('home').classList.remove('hidden');tab('travel');};
$('intro').onclick=()=>{$('home').classList.add('hidden');$('landing').classList.remove('hidden');};

function selectLocation(lat,lng,name,label){
 let chosenName=name;
 if(!chosenName){chosenName=prompt('이 장소의 이름을 입력하세요.','');if(chosenName===null)return;chosenName=chosenName.trim();if(!chosenName)return message('장소 이름을 입력해주세요.');}
 chosenName=chosenName.trim().slice(0,50);
 const existing=data.places.find(p=>distance(p,{lat,lng})<10&&p.name===chosenName);
 if(existing){$('destination').value=existing.id;updateItemTarget();tab('places');message('이미 저장된 장소입니다. 살 것과 챙길 것을 추가해주세요.');$('itemText').focus();return;}
 if(data.places.length>=200)return message('장소는 최대 200개입니다.');
 if(!confirm('“'+chosenName+'”을(를) 저장할까요?\n'+label+'\n\n저장하면 이곳의 100m 안에서 살 것과 챙길 것을 알려드려요.'))return;
 resetForm();$('lat').value=lat;$('lng').value=lng;$('placeName').value=chosenName;
 $('savePlace').click();
 ['destSearch','placeSearch'].forEach(prefix=>{$(prefix+'Query').value='';$(prefix+'Results').replaceChildren();$(prefix+'Status').textContent='';});
 if(searchLayer)searchLayer.clearLayers();
 if(selectedMarker&&map){map.removeLayer(selectedMarker);selectedMarker=null;}
 tab('places');$('itemText').focus();
 message('“'+chosenName+'”을(를) 저장했습니다. 이곳에서 살 것 또는 챙길 것을 추가해주세요.');
}
async function searchPlaces(prefix){
 const q=$(prefix+'Query').value.trim(),status=$(prefix+'Status'),results=$(prefix+'Results');
 if(!q)return;
 
 if(searchBusy){status.textContent='다른 검색이 진행 중입니다. 잠시 기다려주세요.';return;}
 if(Date.now()-lastSearchTime<1200){status.textContent='잠시 후 다시 검색해주세요.';return;}
 initMap();const center=pos&&Date.now()-lastFix<60000?pos:(map?map.getCenter():null);
 const nearby=$(prefix+'Nearby').checked;
 if(nearby&&!center){status.textContent='내 위치를 켜거나 주변 찾기를 해제하고 지역명과 함께 검색하세요.';return;}
 const u=new URL(SEARCH_ENDPOINT);u.searchParams.set('q',q);u.searchParams.set('format','jsonv2');u.searchParams.set('limit','15');u.searchParams.set('addressdetails','1');u.searchParams.set('namedetails','1');u.searchParams.set('accept-language','ko');
 if(nearby){const dl=20/111,dx=20/(111*Math.max(.1,Math.cos(center.lat*Math.PI/180)));u.searchParams.set('viewbox',[Math.max(-180,center.lng-dx),Math.min(90,center.lat+dl),Math.min(180,center.lng+dx),Math.max(-90,center.lat-dl)].join(','));u.searchParams.set('bounded','1');}
 results.replaceChildren();status.textContent='장소를 찾고 있습니다…';searchBusy=true;
 ['destSearch','placeSearch'].forEach(p=>$(p+'Button').disabled=true);
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
 try{
  let rows=searchCache.get(u.href);
  if(!rows){lastSearchTime=Date.now();const response=await fetch(u.href,{signal:controller.signal,referrerPolicy:'strict-origin-when-cross-origin'});if(!response.ok)throw Error(response.status===429?'검색 요청이 많습니다. 잠시 후 다시 시도하세요.':'검색 서비스에 연결하지 못했습니다.');rows=await response.json();if(!Array.isArray(rows))throw Error('검색 응답을 읽지 못했습니다.');rows=rows.filter(r=>Number.isFinite(Number(r.lat))&&Number.isFinite(Number(r.lon)));searchCache.set(u.href,rows);}
  rows=[...rows];if(center)rows.sort((a,b)=>distance(center,{lat:Number(a.lat),lng:Number(a.lon)})-distance(center,{lat:Number(b.lat),lng:Number(b.lon)}));
  if(searchLayer)searchLayer.clearLayers();
  status.textContent=rows.length?rows.length+'곳을 찾았습니다. 원하는 장소를 선택하세요.':'찾은 장소가 없습니다. 주변 찾기를 해제하고 지역명·지점명을 함께 검색하거나 지도에서 선택하세요.';
  for(const r of rows){const lat=Number(r.lat),lng=Number(r.lon),name=r.namedetails?.['name:ko']||r.name||r.display_name.split(',')[0],label=r.display_name||name;
   const select=()=>selectLocation(lat,lng,name,label);const box=node('div',undefined,'place');box.append(node('b',name),node('div',label,'hint'));
   if(center){const d=distance(center,{lat,lng});box.append(node('small',(pos&&Date.now()-lastFix<60000?'내 위치':'지도 중심')+'에서 직선 '+(d>=1000?(d/1000).toFixed(1)+'km':Math.round(d)+'m')));}
   box.append(button('이 장소 저장',select));results.append(box);
   if(map&&searchLayer){const marker=L.circleMarker([lat,lng],{radius:8,color:'#fff',weight:2,fillColor:'#ff9e2c',fillOpacity:1}).addTo(searchLayer);const popup=node('div');popup.append(node('b',name),node('p',label),button('이 장소 저장',select));marker.bindPopup(popup);}
  }
  if(map&&rows.length){const bounds=L.latLngBounds(rows.map(r=>[Number(r.lat),Number(r.lon)]));map.fitBounds(bounds.pad(.2),{maxZoom:16});}
 }catch(e){status.textContent=e.name==='AbortError'?'검색 시간이 초과되었습니다. 다시 시도하거나 지도에서 선택하세요.':(e.message==='Failed to fetch'?'검색 서비스 연결이 차단되었거나 인터넷 연결이 불안정합니다. 다시 시도하거나 지도에서 선택하세요.':e.message);}
 finally{clearTimeout(timer);searchBusy=false;['destSearch','placeSearch'].forEach(p=>$(p+'Button').disabled=false);}
}
['destSearch','placeSearch'].forEach(prefix=>{$(prefix+'Form').addEventListener('submit',e=>{e.preventDefault();searchPlaces(prefix);});});

function distance(a,b){const rad=Math.PI/180,dlat=(b.lat-a.lat)*rad,dlng=(b.lng-a.lng)*rad;const v=Math.sin(dlat/2)**2+Math.cos(a.lat*rad)*Math.cos(b.lat*rad)*Math.sin(dlng/2)**2;return 6371000*2*Math.asin(Math.sqrt(Math.min(1,Math.max(0,v))));}
function place(pid){return data.places.find(p=>p.id===pid);}
function initMap(){if(map||!window.L)return;map=L.map('map').setView([37.5665,126.978],12);L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,maxNativeZoom:19,attribution:'Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community'}).addTo(map);searchLayer=L.layerGroup().addTo(map);L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Labels &copy; Esri'}).addTo(map);mapLayer=L.layerGroup().addTo(map);map.on('click',e=>{selectLocation(e.latlng.lat,e.latlng.lng,null,'지도에서 선택한 위치');});drawMap();}
function drawMap(){if(!map)return;mapLayer.clearLayers();for(const p of data.places){L.circle([p.lat,p.lng],{radius:100,color:'#4966df',weight:2,fillOpacity:.08}).addTo(mapLayer).bindTooltip(()=>node('span',p.name));}}
function fillSelect(el,first){const prev=el.value;el.replaceChildren();const o=node('option',first);o.value='';el.append(o);for(const p of data.places){const op=node('option',p.name);op.value=p.id;el.append(op);}if(place(prev))el.value=prev;}
function itemList(p,parent){if(!p.items.length)parent.append(node('p','아직 등록한 물건이 없습니다.','hint'));for(const i of p.items){const row=node('div',undefined,'item'),check=document.createElement('input');check.type='checkbox';check.checked=i.done;check.setAttribute('aria-label',i.text+' 완료');check.onchange=()=>{i.done=check.checked;save();render();};row.append(check,node('span',(i.kind==='buy'?'🛒 ':'🎒 ')+i.text,i.done?'done':''),button('삭제',()=>{p.items=p.items.filter(v=>v.id!==i.id);save();render();}));parent.append(row);}}
function render(){fillSelect($('destination'),'물건을 등록할 장소를 선택하세요');$('placeList').replaceChildren();if(!data.places.length)$('placeList').append(node('p','집이나 마트 등 첫 장소를 등록해보세요.','hint'));for(const p of data.places){const box=node('div',undefined,'place');box.append(node('h3',p.name),node('small',`도착 알림 반경 ${p.radius}m`));const row=node('div',undefined,'row list-buttons');row.append(button('수정',()=>edit(p)),button('물건 추가',()=>{tab('places');$('destination').value=p.id;updateItemTarget();$('itemText').focus();}),button('장소 삭제',()=>{if(!confirm(p.name+'와 연결된 준비물를 삭제할까요?'))return;data.places=data.places.filter(v=>v.id!==p.id);data.routes=data.routes.filter(r=>r.start!==p.id&&!r.stops.includes(p.id));extra=extra.filter(v=>v!==p.id);save();render();},'danger'));box.append(row);itemList(p,box);$('placeList').append(box);}
 $('history').replaceChildren();if(!data.history.length)$('history').append(node('p','도착하면 여기에 알림을 기록합니다.','hint'));for(const h of data.history.slice(0,15)){const el=node('div',undefined,'event');el.append(node('b',h.place),node('div',h.text),node('small',new Date(h.time).toLocaleString('ko-KR')));$('history').append(el);}drawMap();updateItemTarget();}
function updateItemTarget(){const p=place($('destination').value);$('itemTarget').textContent=p?'등록 장소: '+p.name+' · 반경 100m에서 자동 알림':'물건을 등록할 장소를 선택하세요.';}
$('destination').addEventListener('change',updateItemTarget);
function edit(p){editId=p.id;$('formTitle').textContent='장소 수정';$('placeName').value=p.name;$('lat').value=p.lat;$('lng').value=p.lng;$('radius').value=p.radius;$('selectedPlace').textContent=p.name+' · 저장된 위치';tab('places');}
function resetForm(){editId=null;$('formTitle').textContent='자주 가는 장소 추가';['placeName','lat','lng'].forEach(k=>$(k).value='');$('radius').value='100';$('selectedPlace').textContent='장소 이름을 검색한 뒤 결과를 선택하세요.';}
$('cancelEdit').onclick=resetForm;
$('savePlace').onclick=()=>{const name=$('placeName').value.trim(),lat=Number($('lat').value),lng=Number($('lng').value);if(!name||!$('lat').value.trim()||!$('lng').value.trim()||!Number.isFinite(lat)||!Number.isFinite(lng)||Math.abs(lat)>90||Math.abs(lng)>180)return message('장소 이름을 입력하고 검색 결과나 지도에서 위치를 선택하세요.');if(!editId&&data.places.length>=200)return message('장소는 최대 200개입니다.');const p=place(editId);if(p)Object.assign(p,{name,lat,lng,radius:100});else data.places.push({id:id(),name,lat,lng,radius:100,items:[]});const savedId=p?p.id:data.places[data.places.length-1].id;save();resetForm();render();$('destination').value=savedId;updateItemTarget();message('장소를 저장하고 도착지로 선택했습니다. 살 것 또는 챙길 것을 추가하세요. 위치가 켜져 있으면 자동으로 알려드립니다.');};
$('useHere').onclick=()=>{if(!pos||Date.now()-lastFix>30000)return message('먼저 내 위치를 켜서 최신 위치를 받아주세요.');selectLocation(pos.lat,pos.lng,null,'현재 위치');};
$('addItem').onclick=()=>{const p=place($('destination').value),text=$('itemText').value.trim();if(!p||!text)return message('물건을 등록할 장소와 물건 이름을 입력하세요.');if(p.items.length>=500)return message('장소당 물건은 최대 500개입니다.');p.items.push({id:id(),text,kind:$('kind').value,done:false});$('itemText').value='';save();render();};
function play(){if(!soundOn||!audio)return;try{audio.resume();const o=audio.createOscillator(),g=audio.createGain();o.connect(g);g.connect(audio.destination);o.frequency.value=830;g.gain.setValueAtTime(.12,audio.currentTime);g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+.6);o.start();o.stop(audio.currentTime+.6);}catch(e){}}
$('sound').onclick=()=>{soundOn=!soundOn;if(soundOn){try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();play();}catch(e){soundOn=false;message('이 브라우저에서는 알림 소리를 사용할 수 없습니다.');}}$('sound').textContent=soundOn?'🔊 소리 켜짐':'🔇 소리 꺼짐';};
const arrivalStates=new Map();
function evaluate(){
 if(!pos||watch===null)return;
 const now=Date.now(),fresh=now-lastFix<=30000&&document.visibilityState==='visible';
 for(const p of data.places){
  let state=arrivalStates.get(p.id);if(!state){state={since:0,notified:false};arrivalStates.set(p.id,state);}
  if(!fresh||pos.accuracy>50){state.since=0;continue;}
  const d=distance(pos,p);
  if(d>100+Math.max(30,pos.accuracy)){state.notified=false;state.since=0;}
  if(d>100){state.since=0;continue;}
  if(state.notified||!p.items.some(i=>!i.done))continue;
  if(!state.since)state.since=now;
  if(now-state.since>=4000){state.notified=true;arrive(p);}
 }
}
function arrive(p){const pending=p.items.filter(i=>!i.done);if(!pending.length)return;
 const text=pending.map(i=>(i.kind==='buy'?'살 것: ':'챙길 것: ')+i.text).join('\n');
 data.history.unshift({time:new Date().toISOString(),place:p.name,text});data.history=data.history.slice(0,100);save();
 // Keep simultaneous nearby-place reminders in the same banner.
 const previous=$('toast').classList.contains('hidden')?'':$('toastText').textContent+'\n\n';
 message(previous+p.name+'에서 잊지 마세요.\n'+text);play();try{if(navigator.vibrate)navigator.vibrate([150,70,150]);}catch(e){}render();
}
function resetArrivalTimers(){arrivalStates.forEach(state=>state.since=0);}
function gpsError(e){const texts={1:'위치 권한이 거부되었습니다. 브라우저 사이트 설정에서 위치를 허용하고 다시 켜세요.',2:'위치를 확인할 수 없습니다. 기기의 위치 기능과 인터넷 연결을 확인하세요.',3:'위치 응답이 지연됩니다. 탁 트인 곳에서 기다리거나 다시 켜세요.'};$('gpsStatus').textContent=texts[e.code]||'위치 확인 오류';resetArrivalTimers();if(e.code===1&&watch!==null){navigator.geolocation.clearWatch(watch);watch=null;pos=null;lastFix=0;releaseWake();resetArrivalTimers();}}
$('gpsOn').onclick=()=>{if(!navigator.geolocation)return message('이 브라우저는 GPS를 지원하지 않습니다.');if(watch!==null)return message('위치 확인이 이미 켜져 있습니다.');$('gpsStatus').textContent='위치 권한을 요청하고 GPS를 기다리고 있습니다…';try{watch=navigator.geolocation.watchPosition(p=>{pos={lat:p.coords.latitude,lng:p.coords.longitude,accuracy:p.coords.accuracy};lastFix=p.timestamp||Date.now();$('gpsStatus').textContent=`내 위치 확인 중\n정확도 약 ±${Math.round(pos.accuracy)}m · ${new Date(lastFix).toLocaleTimeString('ko-KR')}`;initMap();if(map){if(!userMarker){userMarker=L.circleMarker([pos.lat,pos.lng],{radius:8,color:'white',weight:3,fillColor:'#3e64ec',fillOpacity:1}).addTo(map);map.setView([pos.lat,pos.lng],15);}else userMarker.setLatLng([pos.lat,pos.lng]);}requestWake();evaluate();},gpsError,{enableHighAccuracy:true,maximumAge:0,timeout:20000});}catch(e){watch=null;message('위치 요청이 차단되었습니다. HTTPS 주소와 브라우저의 위치 권한을 확인하세요.');}};
$('gpsOff').onclick=()=>{if(watch!==null)navigator.geolocation.clearWatch(watch);watch=null;pos=null;lastFix=0;if(userMarker&&map){map.removeLayer(userMarker);userMarker=null;}$('gpsStatus').textContent='위치를 껐습니다.';releaseWake();resetArrivalTimers();};
async function requestWake(){try{if('wakeLock'in navigator&&document.visibilityState==='visible'&&!wake){wake=await navigator.wakeLock.request('screen');wake.addEventListener('release',()=>wake=null);}}catch(e){}}
function releaseWake(){if(wake){wake.release().catch(()=>{});wake=null;}}
document.addEventListener('visibilitychange',()=>{resetArrivalTimers();if(document.visibilityState==='visible'&&watch!==null){requestWake();evaluate();}});
setInterval(()=>{if(watch!==null){if(lastFix&&Date.now()-lastFix>30000){resetArrivalTimers();$('gpsStatus').textContent='최신 위치를 기다리고 있습니다. 화면과 위치 권한을 확인하세요.';}evaluate();}},1000);
$('makeQr').onclick=()=>{let u;try{u=new URL($('appUrl').value.trim());if(!['https:','http:'].includes(u.protocol)||u.username||u.password)throw Error();}catch(e){return message('올바른 앱의 HTTPS 주소를 입력하세요.');}if(u.protocol!=='https:')return message('GPS 사용을 위해 HTTPS 배포 주소를 사용하세요.');if(!window.QRCode)return message('QR 라이브러리를 불러오지 못했습니다. 연결을 확인하고 새로고침하세요.');$('qr').replaceChildren();try{new QRCode($('qr'),{text:u.href,width:220,height:220,correctLevel:QRCode.CorrectLevel.M});}catch(e){message('주소가 너무 깁니다. 앱의 기본 공유 주소를 사용하세요.');}};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='there-next-time-backup.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('importButton').onclick=()=>$('importFile').click();$('importFile').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>3*1024*1024)throw Error('3MB 이하의 백업 파일만 가능합니다.');const incoming=validate(JSON.parse(await f.text()));if(!confirm('현재 장소·준비물·기록을 백업 내용으로 교체할까요?'))return;data=incoming;extra=[];resetForm();save();render();message('백업을 가져왔습니다.');}catch(err){message('가져오기 실패: '+err.message);}finally{e.target.value='';}};
if(!window.L)$('map').textContent='지도를 불러오지 못했습니다. 장소 이름 검색과 GPS 알림은 사용할 수 있습니다.';
$('storageStatus').textContent=storageOK?'브라우저 저장 사용 중 · 백업을 정기적으로 권장합니다.':'저장된 데이터를 읽지 못했습니다. 백업을 가져오거나 브라우저 저장 권한을 확인하세요.';
render();
</script></body></html>'''

components.html(HTML, height=1550, scrolling=True)
