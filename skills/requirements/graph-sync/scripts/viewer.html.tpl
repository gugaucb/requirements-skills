<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Requirements graph</title>
<style>
:root{--bg:#fff;--fg:#1f2937;--mut:#6b7280;--panel:#f8fafc;--line:#e2e8f0;--acc:#2563eb}
@media (prefers-color-scheme:dark){:root{--bg:#0f172a;--fg:#e5e7eb;--mut:#94a3b8;--panel:#111c33;--line:#26324d;--acc:#60a5fa}}
*{box-sizing:border-box}html,body{height:100%;margin:0}
body{font:14px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
#app{display:grid;grid-template-columns:1fr 340px;height:100%}
#stage{position:relative;overflow:hidden;min-height:0;min-width:0}
#svg{width:100%;height:100%;display:block;touch-action:none;cursor:grab}
#svg.drag{cursor:grabbing}
#tools{position:absolute;left:10px;top:10px;display:flex;gap:6px}
button{font:inherit;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer}
button:hover{border-color:var(--acc)}
aside{background:var(--panel);border-left:1px solid var(--line);overflow:auto;padding:12px 14px;min-height:0}
h1{font-size:16px;margin:0 0 2px}h2{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:16px 0 6px}
#meta{color:var(--mut);font-size:12px}#warn{color:#dc2626;font-size:12px;margin-top:4px}
#search{width:100%;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);margin-top:10px;font:inherit}
.item{display:flex;gap:6px;align-items:center;padding:3px 4px;border-radius:4px;cursor:pointer}
.item:hover{background:var(--line)}
.sw{width:10px;height:10px;border-radius:2px;flex:none}
.tag{font-size:11px;border:1px solid var(--line);border-radius:10px;padding:0 6px;color:var(--mut);margin-left:auto;white-space:nowrap}
.lab{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
label.chk{display:flex;gap:6px;align-items:center;padding:2px 0}
#info .empty{color:var(--mut)}#info .id{font-weight:700;font-size:15px}
.badge{display:inline-block;font-size:11px;padding:0 7px;border-radius:10px;color:#fff;margin-left:6px}
.src{color:var(--mut);font-size:12px;word-break:break-all}
@media (max-width:720px){#app{grid-template-columns:1fr;grid-template-rows:55% 45%}aside{border-left:0;border-top:1px solid var(--line)}}
</style>
</head>
<body>
<div id="app">
<div id="stage"><svg id="svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Requirements graph"></svg>
<div id="tools"><button id="fit" title="Fit to screen">Fit</button><button id="clear" title="Clear selection">Clear</button><button id="save" title="Download as SVG">Save SVG</button></div></div>
<aside>
<h1 id="title">Requirements graph</h1><div id="meta"></div><div id="warn"></div>
<input id="search" type="search" placeholder="Search ID or text" autocomplete="off">
<div id="results"></div>
<h2>Selected</h2><div id="info"><span class="empty">Click a node. Orange = impacted if it changes, blue = what it depends on. Arrows point at the dependency.</span></div>
<h2>Needs attention</h2><div id="attention"></div>
<h2>Node types</h2><div id="types"></div>
<h2>Relations</h2><div id="rels"></div>
<h2>Status (border)</h2><div id="statuses"></div>
</aside>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
"use strict";
var D=JSON.parse(document.getElementById('data').textContent);
var NS="http://www.w3.org/2000/svg";
var TYPE_COLOR={GOAL:"#8b5cf6",CAP:"#6366f1",SPEC:"#14b8a6",EPIC:"#2dd4bf",US:"#3b82f6",FR:"#22c55e",NFR:"#84cc16",AC:"#eab308",DG:"#94a3b8",TC:"#f97316",FLD:"#0ea5e9",SCR:"#d946ef",DEC:"#ec4899",CHG:"#64748b"};
var TYPE_NAME={GOAL:"Goal",CAP:"Capability",SPEC:"Spec",EPIC:"Epic",US:"User story",FR:"Functional req.",NFR:"Non-functional req.",AC:"Acceptance criterion",DG:"Diagram",TC:"Test case",FLD:"Field",SCR:"Screen",DEC:"Decision",CHG:"Change"};
var COL={GOAL:0,CAP:1,US:2,FLD:3,SCR:3,FR:3,NFR:3,AC:4,DG:4,TC:5};
var BAND={SPEC:0,EPIC:0,DEC:1,CHG:2};
var IMPACT_RELS={serves:1,part_of:1,decided_by:1,blocked_by:1,verifies:1,proves:1,uses:1};
var RECORD_RELS={changes:1,impacts:1,needs_decision:1,changed_by:1,superseded_by:1};
var REL_LABEL={uses:"uses",serves:"serves",part_of:"part of",verifies:"verifies",proves:"proves",blocked_by:"blocked by",decided_by:"decided by",references:"references (weak)",records:"change records",redundant:"redundant skip-level links"};
var REL_DEFAULT={uses:true,serves:true,part_of:true,verifies:true,proves:true,blocked_by:true,decided_by:false,references:false,records:false,redundant:false};
var STATUS_COLOR={"Stale":"#ef4444","Blocked":"#f59e0b","Needs changes":"#f59e0b","Pending":"#f59e0b","Draft":"#94a3b8","Proposed":"#60a5fa","Ready for human review":"#3b82f6","Ready (team agreement)":"#16a34a","Confirmed":"#16a34a","Retired":"#6b7280","Superseded":"#6b7280"};
var NODE_W=170,NODE_H=40,COLW=240,ROWH=52,PAD=40;

var byId={},out={},inc={};
D.nodes.forEach(function(n){byId[n.id]=n;out[n.id]=[];inc[n.id]=[];});
var edges=D.edges.filter(function(e){return byId[e.s]&&byId[e.t];});
edges.forEach(function(e){out[e.s].push(e);inc[e.t].push(e);});

var redundant={};
["serves","blocked_by"].forEach(function(rel){
  var adj={};edges.forEach(function(e){if(e.r===rel){(adj[e.s]=adj[e.s]||[]).push(e.t);}});
  function path(a,b,skip){var seen={},q=[a];seen[a]=1;while(q.length){var c=q.shift();if(c===b)return true;(adj[c]||[]).forEach(function(n){if(!seen[n]&&!(c===a&&n===skip)){seen[n]=1;q.push(n);}});}return false;}
  edges.forEach(function(e){if(e.r===rel&&path(e.s,e.t,e.t))redundant[e.s+"|"+e.r+"|"+e.t]=true;});
});
var state={sel:null,types:{},rels:JSON.parse(JSON.stringify(REL_DEFAULT)),view:null,q:""};
D.nodes.forEach(function(n){state.types[n.type]=true;});

/* ---------- layout: layered columns + bottom bands, barycenter ordering ---------- */
var pos={};
function layout(){
  var cols={},bands={0:[],1:[],2:[]};
  D.nodes.forEach(function(n){
    if(n.type in COL){(cols[COL[n.type]]=cols[COL[n.type]]||[]).push(n.id);}
    else{bands[BAND[n.type]||0].push(n.id);}
  });
  var order=Object.keys(cols).map(Number).sort(function(a,b){return a-b;});
  order.forEach(function(c){cols[c].sort();});
  function bary(id,fromCols){
    var s=0,k=0;
    out[id].concat(inc[id]).forEach(function(e){
      var o=e.s===id?e.t:e.s,on=byId[o];
      if(on&&on.type in COL&&fromCols.indexOf(COL[on.type])>=0&&idx[o]!==undefined){s+=idx[o];k++;}
    });
    return k?s/k:null;
  }
  var idx={};
  function reindex(){order.forEach(function(c){cols[c].forEach(function(id,i){idx[id]=i;});});}
  reindex();
  for(var pass=0;pass<4;pass++){
    var seq=pass%2===0?order:order.slice().reverse();
    seq.forEach(function(c){
      var prev=order.filter(function(x){return pass%2===0?x<c:x>c;});
      var keyed=cols[c].map(function(id){var b=bary(id,prev);return {id:id,b:b===null?idx[id]:b};});
      keyed.sort(function(a,b){return a.b-b.b||(a.id<b.id?-1:1);});
      cols[c]=keyed.map(function(k){return k.id;});
      cols[c].forEach(function(id,i){idx[id]=i;});
    });
  }
  var maxRows=0;
  order.forEach(function(c){
    maxRows=Math.max(maxRows,cols[c].length);
    cols[c].forEach(function(id,i){pos[id]={x:PAD+c*COLW,y:PAD+i*ROWH};});
  });
  var y=PAD+maxRows*ROWH+60;
  [0,1,2].forEach(function(b){
    var ids=bands[b].sort();if(!ids.length)return;
    var cap=Math.max(4,order.length+1);
    ids.forEach(function(id,i){pos[id]={x:PAD+(i%cap)*(COLW*0.78),y:y+Math.floor(i/cap)*ROWH};});
    y+=Math.ceil(ids.length/cap)*ROWH+40;
  });
  var minX=1e9,minY=1e9,maxX=-1e9,maxY=-1e9;
  Object.keys(pos).forEach(function(id){var p=pos[id];minX=Math.min(minX,p.x);minY=Math.min(minY,p.y);maxX=Math.max(maxX,p.x+NODE_W);maxY=Math.max(maxY,p.y+NODE_H);});
  if(minX===1e9){minX=0;minY=0;maxX=400;maxY=300;}
  return {x:minX-PAD,y:minY-PAD,w:maxX-minX+2*PAD,h:maxY-minY+2*PAD};
}
var bounds=layout();
state.view={x:bounds.x,y:bounds.y,w:bounds.w,h:bounds.h};

/* ---------- impact sets (same rule as req-graph.py affected) ---------- */
function reach(start,dirDown){
  var seen={},q=[start],res={};
  seen[start]=1;
  while(q.length){
    var cur=q.shift();
    var list=dirDown?inc[cur]:out[cur];
    list.forEach(function(e){
      var weak=e.r==="references";
      if(!(IMPACT_RELS[e.r]||(weak&&state.rels.references)))return;
      var nxt=dirDown?e.s:e.t;
      if(seen[nxt])return;seen[nxt]=1;res[nxt]=(e);q.push(nxt);
    });
  }
  return res;
}

/* ---------- theme ---------- */
function pal(){
  var dark=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches;
  return dark?{bg:"#0f172a",fg:"#e5e7eb",mut:"#94a3b8",edge:"#475569",down:"#fb923c",up:"#60a5fa",card:"#16213a",sel:"#f8fafc"}
             :{bg:"#ffffff",fg:"#1f2937",mut:"#6b7280",edge:"#94a3b8",down:"#ea580c",up:"#2563eb",card:"#ffffff",sel:"#111827"};
}
function el(name,attrs,parent){
  var e=document.createElementNS(NS,name);
  for(var k in attrs){e.setAttribute(k,attrs[k]);}
  if(parent)parent.appendChild(e);return e;
}
function trunc(s,n){s=String(s||"");return s.length>n?s.slice(0,n-1)+"\u2026":s;}
var SHORT={"Ready for human review":"Review","Ready (team agreement)":"Ready","Needs changes":"Changes","Superseded":"Superseded"};
function shortStatus(s){return SHORT[s]||s;}
function statusColor(s){return STATUS_COLOR[s]||"#94a3b8";}

/* ---------- render ---------- */
var svg=document.getElementById("svg");
function relGroup(r){return RECORD_RELS[r]?"records":r;}
function render(){
  var P=pal(),sel=state.sel;
  var down=sel?reach(sel,true):{},up=sel?reach(sel,false):{};
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  svg.setAttribute("viewBox",[state.view.x,state.view.y,state.view.w,state.view.h].join(" "));
  var defs=el("defs",{},svg);
  [["n",P.edge],["d",P.down],["u",P.up]].forEach(function(m){
    var mk=el("marker",{id:"arr-"+m[0],viewBox:"0 0 10 10",refX:"9",refY:"5",markerWidth:"7",markerHeight:"7",orient:"auto"},defs);
    el("path",{d:"M0,0 L10,5 L0,10 z",fill:m[1]},mk);
  });
  el("rect",{x:state.view.x,y:state.view.y,width:state.view.w,height:state.view.h,fill:P.bg,id:"bgrect"},svg);
  var gE=el("g",{},svg),gN=el("g",{},svg);
  var inSet=function(id){return id===sel||down[id]||up[id];};
  edges.forEach(function(e){
    var a=byId[e.s],b=byId[e.t];
    if(!state.types[a.type]||!state.types[b.type])return;
    var kind=null;
    if(sel&&IMPACT_RELS[e.r]||sel&&e.r==="references"&&state.rels.references){
      if((e.t===sel||down[e.t])&&down[e.s])kind="d";
      else if((e.s===sel||up[e.s])&&up[e.t])kind="u";
    }
    if(redundant[e.s+"|"+e.r+"|"+e.t]&&!state.rels.redundant)return;
    var shown=state.rels[relGroup(e.r)];
    var incident=sel&&(e.s===sel||e.t===sel);
    if(!(shown||kind||incident))return;
    var pa=pos[e.s],pb=pos[e.t];if(!pa||!pb)return;
    var color=kind==="d"?P.down:kind==="u"?P.up:P.edge;
    var dim=sel&&!kind&&!incident;
    var x1,y1,x2,y2,d;
    var below=function(n){return n.type in BAND;};
    if(below(a)&&below(b)){
      var ca=pa.x+NODE_W/2,cb=pb.x+NODE_W/2;
      if(Math.abs(pa.y-pb.y)<1){x1=ca;y1=pa.y;x2=cb;y2=pb.y;d="M"+x1+","+y1+" C"+x1+","+(y1-45)+" "+x2+","+(y2-45)+" "+x2+","+y2;}
      else if(pb.y<pa.y){x1=ca;y1=pa.y;x2=cb;y2=pb.y+NODE_H;var m3=(y1+y2)/2;d="M"+x1+","+y1+" C"+x1+","+m3+" "+x2+","+m3+" "+x2+","+y2;}
      else{x1=ca;y1=pa.y+NODE_H;x2=cb;y2=pb.y;var m4=(y1+y2)/2;d="M"+x1+","+y1+" C"+x1+","+m4+" "+x2+","+m4+" "+x2+","+y2;}
    }
    else if(below(b)&&!below(a)){x1=pa.x+NODE_W/2;y1=pa.y+NODE_H;x2=pb.x+NODE_W/2;y2=pb.y;var m=(y1+y2)/2;d="M"+x1+","+y1+" C"+x1+","+m+" "+x2+","+m+" "+x2+","+y2;}
    else if(below(a)&&!below(b)){x1=pa.x+NODE_W/2;y1=pa.y;x2=pb.x+NODE_W/2;y2=pb.y+NODE_H;var m2=(y1+y2)/2;d="M"+x1+","+y1+" C"+x1+","+m2+" "+x2+","+m2+" "+x2+","+y2;}
    else if(Math.abs(pa.x-pb.x)<1){x1=pa.x+NODE_W;y1=pa.y+NODE_H/2;x2=pb.x+NODE_W;y2=pb.y+NODE_H/2;d="M"+x1+","+y1+" C"+(x1+50)+","+y1+" "+(x2+50)+","+y2+" "+x2+","+y2;}
    else if(pb.x<pa.x){x1=pa.x;y1=pa.y+NODE_H/2;x2=pb.x+NODE_W;y2=pb.y+NODE_H/2;var h=(x1+x2)/2;d="M"+x1+","+y1+" C"+h+","+y1+" "+h+","+y2+" "+x2+","+y2;}
    else{x1=pa.x+NODE_W;y1=pa.y+NODE_H/2;x2=pb.x;y2=pb.y+NODE_H/2;var h2=(x1+x2)/2;d="M"+x1+","+y1+" C"+h2+","+y1+" "+h2+","+y2+" "+x2+","+y2;}
    var p=el("path",{d:d,fill:"none",stroke:color,"stroke-width":kind?"2.2":"1.2","stroke-opacity":dim?"0.12":(kind?"1":"0.7"),"marker-end":"url(#arr-"+(kind||"n")+")","data-rel":e.r,"data-from":e.s,"data-to":e.t},gE);
    if(RECORD_RELS[e.r])p.setAttribute("stroke-dasharray","4 3");
    var t=el("title",{},p);t.textContent=e.s+" "+(REL_LABEL[e.r]||e.r.replace("_"," "))+" "+e.t+(e.impact?" ("+e.impact+")":"");
  });
  var q=state.q.trim().toLowerCase();
  D.nodes.forEach(function(n){
    if(!state.types[n.type])return;var p=pos[n.id];if(!p)return;
    var role=n.id===sel?"sel":down[n.id]?"down":up[n.id]?"up":"";
    var match=q&&(n.id.toLowerCase().indexOf(q)>=0||String(n.label).toLowerCase().indexOf(q)>=0);
    var dim=sel?!role:!!(q&&!match);
    var g=el("g",{transform:"translate("+p.x+","+p.y+")","data-id":n.id,"data-role":role,style:"cursor:pointer",opacity:dim?"0.22":"1"},gN);
    var tc=TYPE_COLOR[n.type]||"#94a3b8",sc=n.status?statusColor(n.status):P.edge;
    var fill=role==="down"?P.down:role==="up"?P.up:tc;
    el("rect",{width:NODE_W,height:NODE_H,rx:"6",fill:P.card,stroke:role==="sel"?P.sel:sc,"stroke-width":role==="sel"?"3":(n.status==="Stale"?"3":"1.6"),"stroke-dasharray":n.status==="Retired"?"4 3":"none"},g);
    el("rect",{width:NODE_W,height:NODE_H,rx:"6",fill:fill,"fill-opacity":role?"0.30":"0.14",stroke:"none"},g);
    el("rect",{width:"5",height:NODE_H,rx:"2",fill:fill},g);
    var t1=el("text",{x:"12",y:"16","font-size":"12","font-weight":"700",fill:P.fg,"font-family":"sans-serif"},g);t1.textContent=n.id;
    if(n.status){var ts=el("text",{x:String(NODE_W-7),y:"15","font-size":"9.5","font-weight":"700",fill:n.status==="Stale"?"#ef4444":P.mut,"text-anchor":"end","font-family":"sans-serif"},g);ts.textContent=shortStatus(n.status).toUpperCase();}
    var t2=el("text",{x:"12",y:"31","font-size":"10.5",fill:P.mut,"font-family":"sans-serif"},g);t2.textContent=trunc(n.label,28);
    var tt=el("title",{},g);tt.textContent=n.id+": "+n.label+(n.status?"\n"+n.status:"")+"\n"+n.file+":"+n.loc;
  });
  renderInfo(down,up);
}

/* ---------- side panel ---------- */
function add(parent,tag,cls,text){var e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;parent.appendChild(e);return e;}
function itemRow(parent,id,tagText){
  var n=byId[id];var r=add(parent,"div","item");
  var sw=add(r,"span","sw");sw.style.background=TYPE_COLOR[n.type]||"#94a3b8";
  add(r,"span","lab",id+"  "+n.label);
  if(tagText)add(r,"span","tag",tagText);
  r.addEventListener("click",function(){select(id,true);});
  r.title=n.label;return r;
}
function renderInfo(down,up){
  var box=document.getElementById("info");box.textContent="";
  var id=state.sel;
  if(!id){add(box,"span","empty","Click a node. Orange = impacted if it changes, blue = what it depends on. Arrows point at the dependency.");return;}
  var n=byId[id];
  var h=add(box,"div","id",id);
  if(n.status){var b=add(h,"span","badge",n.status);b.style.background=statusColor(n.status);}
  add(box,"div","",n.label);
  add(box,"div","src",(TYPE_NAME[n.type]||n.type)+"  \u00b7  "+n.file+":"+n.loc);
  var dk=Object.keys(down).sort(),uk=Object.keys(up).sort();
  var impactOf={};
  if(n.type==="CHG"){out[id].forEach(function(e){if(e.r==="impacts")impactOf[e.t]=e.impact||"";});}
  add(box,"h2","","Impacted if this changes ("+dk.length+")");
  var l1=add(box,"div","");dk.forEach(function(k){itemRow(l1,k,byId[k].status||"");});
  if(!dk.length)add(l1,"span","empty","Nothing depends on it.");
  add(box,"h2","","Depends on ("+uk.length+")");
  var l2=add(box,"div","");uk.forEach(function(k){itemRow(l2,k,byId[k].status||"");});
  if(!uk.length)add(l2,"span","empty","No upstream links.");
  if(n.type==="CHG"){
    var ik=Object.keys(impactOf).sort();
    add(box,"h2","","Change impact report ("+ik.length+")");
    var l3=add(box,"div","");ik.forEach(function(k){itemRow(l3,k,impactOf[k]);});
  }
}
function buildPanels(){
  var counts={};D.nodes.forEach(function(n){counts[n.type]=(counts[n.type]||0)+1;});
  var types=document.getElementById("types");
  Object.keys(TYPE_COLOR).filter(function(t){return counts[t];}).forEach(function(t){
    var l=add(types,"label","chk");var c=document.createElement("input");c.type="checkbox";c.checked=true;l.appendChild(c);
    var sw=add(l,"span","sw");sw.style.background=TYPE_COLOR[t];add(l,"span","",(TYPE_NAME[t]||t)+" ("+counts[t]+")");
    c.addEventListener("change",function(){state.types[t]=c.checked;render();});
  });
  var rels=document.getElementById("rels");
  Object.keys(REL_DEFAULT).forEach(function(r){
    var l=add(rels,"label","chk");var c=document.createElement("input");c.type="checkbox";c.checked=state.rels[r];l.appendChild(c);
    add(l,"span","",REL_LABEL[r]);
    c.addEventListener("change",function(){state.rels[r]=c.checked;render();});
  });
  var st=document.getElementById("statuses");
  Object.keys(STATUS_COLOR).forEach(function(s){var r=add(st,"div","item");var sw=add(r,"span","sw");sw.style.background=STATUS_COLOR[s];add(r,"span","",s);});
  var att=document.getElementById("attention");
  var stale=D.nodes.filter(function(n){return n.status==="Stale";});
  var pend=D.nodes.filter(function(n){return n.type==="DEC"&&n.status==="Pending";});
  var blocked=D.nodes.filter(function(n){return n.status==="Blocked"||n.status==="Needs changes";});
  [["Stale",stale],["Pending decisions",pend],["Blocked or needs changes",blocked]].forEach(function(g){
    if(!g[1].length)return;add(att,"div","src",g[0]+" ("+g[1].length+")");
    g[1].forEach(function(n){itemRow(att,n.id,n.status||"");});
  });
  if(!att.firstChild)add(att,"span","src","Nothing flagged.");
  document.getElementById("title").textContent=D.title||"Requirements graph";
  document.getElementById("meta").textContent=D.nodes.length+" nodes, "+edges.length+" links"+(D.digest?"  \u00b7  "+D.digest.slice(0,8):"");
  if(D.unresolved&&D.unresolved.length)document.getElementById("warn").textContent="Referenced but never defined: "+D.unresolved.join(", ");
}

/* ---------- interaction ---------- */
function select(id,center){
  state.sel=id;
  if(center&&pos[id]){var v=state.view;state.view.x=pos[id].x+NODE_W/2-v.w/2;state.view.y=pos[id].y+NODE_H/2-v.h/2;}
  render();
}
function fit(){state.view={x:bounds.x,y:bounds.y,w:bounds.w,h:bounds.h};fixAspect();render();}
function fixAspect(){
  var r=svg.getBoundingClientRect();if(!r.width||!r.height)return;
  var ar=r.width/r.height,v=state.view;
  if(v.w/v.h<ar){var nw=v.h*ar;v.x-=(nw-v.w)/2;v.w=nw;}else{var nh=v.w/ar;v.y-=(nh-v.h)/2;v.h=nh;}
}
svg.addEventListener("click",function(ev){
  if(moved)return;
  var g=ev.target.closest?ev.target.closest("g[data-id]"):null;
  if(g)select(g.getAttribute("data-id"),false);else if(ev.target.id==="bgrect"){state.sel=null;render();}
});
var dragging=false,moved=false,sx=0,sy=0,ox=0,oy=0;
svg.addEventListener("pointerdown",function(ev){dragging=true;moved=false;sx=ev.clientX;sy=ev.clientY;ox=state.view.x;oy=state.view.y;});
window.addEventListener("pointermove",function(ev){
  if(!dragging)return;var r=svg.getBoundingClientRect();if(!r.width)return;
  var dx=ev.clientX-sx,dy=ev.clientY-sy;if(Math.abs(dx)+Math.abs(dy)>4){moved=true;svg.classList.add("drag");}
  if(moved){state.view.x=ox-dx*state.view.w/r.width;state.view.y=oy-dy*state.view.h/r.height;svg.setAttribute("viewBox",[state.view.x,state.view.y,state.view.w,state.view.h].join(" "));}
});
window.addEventListener("pointerup",function(){dragging=false;svg.classList.remove("drag");if(moved)setTimeout(function(){moved=false;},0);});
svg.addEventListener("wheel",function(ev){
  ev.preventDefault();var r=svg.getBoundingClientRect();if(!r.width)return;
  var f=ev.deltaY<0?0.88:1.14,v=state.view;
  var mx=v.x+(ev.clientX-r.left)/r.width*v.w,my=v.y+(ev.clientY-r.top)/r.height*v.h;
  v.x=mx-(mx-v.x)*f;v.y=my-(my-v.y)*f;v.w*=f;v.h*=f;
  svg.setAttribute("viewBox",[v.x,v.y,v.w,v.h].join(" "));
},{passive:false});
document.getElementById("fit").addEventListener("click",fit);
document.getElementById("clear").addEventListener("click",function(){state.sel=null;state.q="";document.getElementById("search").value="";document.getElementById("results").textContent="";render();});
document.getElementById("save").addEventListener("click",function(){
  var s=new XMLSerializer().serializeToString(svg);
  var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([s],{type:"image/svg+xml"}));a.download="requirements-graph.svg";a.click();
});
var search=document.getElementById("search");
search.addEventListener("input",function(){
  state.q=search.value;var res=document.getElementById("results");res.textContent="";
  var q=state.q.trim().toLowerCase();
  if(q){D.nodes.filter(function(n){return n.id.toLowerCase().indexOf(q)>=0||String(n.label).toLowerCase().indexOf(q)>=0;}).slice(0,12).forEach(function(n){itemRow(res,n.id,n.status||"");});}
  render();
});
if(window.matchMedia){var mq=window.matchMedia("(prefers-color-scheme: dark)");if(mq.addEventListener)mq.addEventListener("change",render);}
window.addEventListener("resize",function(){fixAspect();render();});
buildPanels();fixAspect();render();
window.__reqGraph={select:select,state:state,reach:reach,fit:fit};
})();
</script>
</body>
</html>
