// ========================= CSRF Helper =========================
function getCookie(name){const v=`; ${document.cookie}`;const p=v.split(`; ${name}=`);if(p.length===2)return p.pop().split(";").shift();return""}
function getCsrfToken(){return getCookie("csrftoken")}

// ========================= Alert / Toast =========================
const alertBox=(()=>{const el=()=>document.getElementById("alert-box");
  function show(msg,type="info",t=3000){const b=el();if(!b)return;b.textContent=msg;b.className="alert-box "+type;
    if(t)setTimeout(()=>{if(b.textContent===msg){b.textContent="";b.className="alert-box"}},t)}
  function error(e){console.error(e);show(String(e&&e.message?e.message:e),"error",6000)}
  return{show,error}
})();

// ========================= Data Structures =========================
function emptyNode(){return {text:"", paragraphs:[], children:[], pictures:[]}}
function emptySection(title_no,title){return {title_no, title, body_paragraphs:[], items:[emptyNode()]}}

// global state (จะถูกแทนเมื่อ get_data)
let sectionsState=null;

// ========================= Utils / AJAX =========================
function ensureDefaultState(){
  if(!Array.isArray(sectionsState) || sectionsState.length!==2){
    sectionsState=[ emptySection("2.1","แนวคิดและทฤษฎีที่เกี่ยวข้อง"),
                    emptySection("2.2","งานวิจัยที่เกี่ยวข้อง") ];
  }
}
function syncHiddenField(){
  try{
    const h=document.getElementById("sections_json");
    if(h) h.value=JSON.stringify(sectionsState||[]);
  }catch(e){alertBox.error(e)}
}
async function postAction(action,extra={},file=null){
  const fd=new FormData();fd.append("action",action);
  Object.entries(extra).forEach(([k,v])=>fd.append(k,v));
  if(file)fd.append("pic_file",file);
  const res=await fetch(window.location.href,{method:"POST",headers:{"X-CSRFToken":getCsrfToken()},body:fd});
  const ct=res.headers.get("Content-Type")||"";
  if(!res.ok) throw new Error(await res.text());
  return ct.includes("application/json")?res.json():res.text();
}

// ========================= Paragraph Renders =========================
function renderParagraphs(arr,onChange){
  const wrap=document.createElement("div");
  (arr||[]).forEach((txt,idx)=>{
    const row=document.createElement("div");row.className="para-row";
    const ta=document.createElement("textarea");ta.value=txt||"";ta.placeholder="ย่อหน้า...";
    ta.addEventListener("input",(e)=>{arr[idx]=e.target.value;onChange&&onChange()});
    const del=document.createElement("button");del.type="button";del.className="btn-mini";del.textContent="ลบย่อหน้า";
    del.addEventListener("click",()=>{arr.splice(idx,1);onChange&&onChange(true)});
    row.appendChild(ta);row.appendChild(del);wrap.appendChild(row);
  });
  const add=document.createElement("button");add.type="button";add.className="btn-mini";add.textContent="➕ เพิ่มย่อหน้า";
  add.addEventListener("click",()=>{arr.push("");onChange&&onChange(true)});wrap.appendChild(add);
  return wrap;
}

// ========================= Picture Box =========================
const selectedPicFileByNode={};
function renderPicturesBoxForNode(nodeObj, sectionNo, numberStr){
  const box=document.createElement("div");box.className="picture-box";
  const title=document.createElement("h4");title.textContent=`รูปภาพประกอบหัวข้อ ${numberStr}`;box.appendChild(title);

  const file=document.createElement("input");file.type="file";file.accept="image/*";file.style.display="none";
  file.addEventListener("change",()=>{if(file.files&&file.files.length>0){selectedPicFileByNode[numberStr]=file.files[0];alertBox.show(`เลือกไฟล์ (${numberStr}) : ${file.files[0].name}`,"info")}else{delete selectedPicFileByNode[numberStr]}})
  box.appendChild(file);

  const nameInput=document.createElement("input");nameInput.type="text";nameInput.placeholder="ชื่อรูปภาพ / คำอธิบาย";

  const controls=document.createElement("div");controls.className="controls";
  const btnPick=document.createElement("button");btnPick.type="button";btnPick.className="btn-mini";btnPick.textContent="เลือกไฟล์…";btnPick.addEventListener("click",()=>file.click());
  const btnAdd=document.createElement("button");btnAdd.type="button";btnAdd.className="btn-mini";btnAdd.textContent="เพิ่มรูป";
  btnAdd.addEventListener("click",async()=>{
    try{
      const picName=(nameInput.value||"").trim(); if(!picName){alertBox.show("กรุณากรอกชื่อรูปภาพ","warning");return}
      const f=selectedPicFileByNode[numberStr]; if(!f){alertBox.show("ยังไม่ได้เลือกไฟล์","warning");return}
      alertBox.show("กำลังเพิ่มรูป...","info",0);
      // ส่ง sectionNo (เช่น "2.1" หรือ "2.2") ที่ถูกต้องไปยัง postAction
      const data=await postAction("add_picture_node",{section_no:sectionNo,node_no:numberStr,pic_name:picName,pic_path:f.name},f);
      if(data&&data.status==="ok"&&data.picture){
        nodeObj.pictures=nodeObj.pictures||[]; nodeObj.pictures.push(data.picture);
        nameInput.value=""; delete selectedPicFileByNode[numberStr];
        redrawSections(); alertBox.show(data.message||"เพิ่มรูปเรียบร้อย 🖼","success");
      }else{alertBox.show((data&&data.message)||"เพิ่มรูปไม่สำเร็จ","error")}
    }catch(e){alertBox.error(e)}
  });

  controls.appendChild(nameInput);controls.appendChild(btnPick);controls.appendChild(btnAdd);box.appendChild(controls);

  const list=document.createElement("div");list.className="pic-list";
  if(!nodeObj.pictures||nodeObj.pictures.length===0){const empty=document.createElement("div");empty.textContent="ยังไม่มีรูปในหัวข้อนี้";list.appendChild(empty)}
  else{
    nodeObj.pictures.forEach(p=>{const item=document.createElement("div");item.className="pic-item";
      item.innerHTML=`<strong>ภาพที่ ${p.pic_no||"-"}</strong> : ${p.pic_name||""}${p.pic_path?`<div class="pic-path">${p.pic_path}</div>`:""}`;
      list.appendChild(item);
    });
  }
  box.appendChild(list);
  return box;
}

// ========================= Tree Renderer =========================
function renderNode(node, path, onMutate, numberStr, sectionNo){
  const wrap=document.createElement("div");wrap.className="tree-node";
  const row=document.createElement("div");row.className="row";

  const noBadge=document.createElement("div");noBadge.className="node-no-badge";noBadge.textContent=numberStr||"";
  const input=document.createElement("input");input.type="text";input.placeholder="พิมพ์ชื่อหัวข้อย่อย…";input.value=node.text||"";
  input.addEventListener("input",(e)=>{node.text=e.target.value;onMutate&&onMutate()});

  const controls=document.createElement("div");controls.className="controls";
  const btnAddPara=document.createElement("button");btnAddPara.type="button";btnAddPara.className="btn-mini";btnAddPara.textContent="➕ ย่อหน้า";
  btnAddPara.addEventListener("click",()=>{node.paragraphs.push("");onMutate(true)});
  const btnAddChild=document.createElement("button");btnAddChild.type="button";btnAddChild.className="btn-mini";btnAddChild.textContent="➕ หัวข้อย่อยระดับถัดไป";
  btnAddChild.addEventListener("click",()=>{node.children.push(emptyNode());onMutate(true)});
  const btnAddSibling=document.createElement("button");btnAddSibling.type="button";btnAddSibling.className="btn-mini";btnAddSibling.textContent="➕ หัวข้อย่อยระดับเดียวกัน";
  btnAddSibling.addEventListener("click",()=>{const secIndex=path[0]; if(path.length===2){sectionsState[secIndex].items.splice(path[1]+1,0,emptyNode());onMutate(true)}});

  const btnDel=document.createElement("button");btnDel.type="button";btnDel.className="btn-mini";btnDel.textContent="ลบหัวข้อนี้";
  btnDel.addEventListener("click",()=>{
    const secIndex=path[0];
    function getParentAndIndex(items,p){
      if(p.length===2) return {parent:sectionsState[secIndex].items, idx:p[1]};
      let cur=sectionsState[secIndex].items[p[1]];
      for(let j=2;j<p.length-1;j++) cur=cur.children[p[j]];
      return {parent:cur.children, idx:p[p.length-1]};
    }
    const {parent,idx}=getParentAndIndex(sectionsState[secIndex].items,path);
    parent.splice(idx,1); onMutate(true);
  });

  controls.appendChild(btnAddPara);
  controls.appendChild(btnAddChild);
  if(path.length===2) controls.appendChild(btnAddSibling);
  controls.appendChild(btnDel);

  row.appendChild(noBadge); row.appendChild(input); row.appendChild(controls);
  wrap.appendChild(row);

  // paragraphs
  if(node.paragraphs && node.paragraphs.length>0){
    wrap.appendChild(renderParagraphs(node.paragraphs,()=>{syncHiddenField();redrawSections()}));
  }else{
    const addFirstPara=document.createElement("button");addFirstPara.type="button";addFirstPara.className="btn-mini";addFirstPara.textContent="➕ เพิ่มย่อหน้าแรก";
    addFirstPara.addEventListener("click",()=>{node.paragraphs.push("");redrawSections()}); wrap.appendChild(addFirstPara);
  }

  // children
  const childrenWrap=document.createElement("div");childrenWrap.className="children";
  node.children.forEach((child,i)=>{
    const childNumber=`${numberStr}.${i+1}`;
    childrenWrap.appendChild(renderNode(child, [...path,i], onMutate, childNumber, sectionNo));
  });
  wrap.appendChild(childrenWrap);

  return wrap;
}

function renderTree(sectionObj, secIndex){
  const treeWrap=document.createElement("div");treeWrap.className="tree";

  sectionObj.items.forEach((n,i)=>{
    const numberStr=`${sectionObj.title_no}.${i+1}`;
    // node ปกติ
    const nodeDom = renderNode(n, [secIndex,i], ()=>{syncHiddenField();redrawSections()}, numberStr, sectionObj.title_no);
    treeWrap.appendChild(nodeDom);
    
    // ==========================================================
    // === 🔴 จุดที่แก้ไข ===
    // กล่องรูป: ใส่ให้ทุก root ของ 2.1 (2.1.x) และ 2.2 (2.2.x)
    if(sectionObj.title_no==="2.1" || sectionObj.title_no==="2.2"){
      // ส่ง sectionObj.title_no (ซึ่งอาจจะเป็น "2.1" หรือ "2.2")
      // ไปยังฟังก์ชัน renderPicturesBoxForNode
      treeWrap.appendChild( renderPicturesBoxForNode(n, sectionObj.title_no, numberStr) );
    }
    // === สิ้นสุดจุดที่แก้ไข ===
    // ==========================================================
  });

  const addRoot=document.createElement("button");addRoot.type="button";addRoot.className="btn-mini";addRoot.textContent="➕ เพิ่มหัวข้อย่อยระดับแรก";
  addRoot.addEventListener("click",()=>{sectionObj.items.push(emptyNode());redrawSections()});
  treeWrap.appendChild(addRoot);

  return treeWrap;
}

// ========================= Section & App =========================
function renderSection(sectionObj, secIndex){
  const card=document.createElement("div");card.className="section-card";
  const header=document.createElement("div");header.className="section-header-row";
  const no=document.createElement("div");no.className="section-title-no";no.textContent=sectionObj.title_no;
  const title=document.createElement("input");title.type="text";title.className="section-title-input";title.placeholder="ชื่อหัวข้อใหญ่";title.value=sectionObj.title||"";
  title.addEventListener("input",(e)=>{sectionObj.title=e.target.value;syncHiddenField()});
  header.appendChild(no); header.appendChild(title); card.appendChild(header);

  const bodyWrap=document.createElement("div");bodyWrap.className="section-body";
  bodyWrap.appendChild(renderParagraphs(sectionObj.body_paragraphs,()=>{syncHiddenField();redrawSections()}));
  card.appendChild(bodyWrap);

  card.appendChild(renderTree(sectionObj, secIndex));
  return card;
}

function redrawSections(){
  try{
    ensureDefaultState();
    const container=document.getElementById("sections-container");
    if(!container){throw new Error("ไม่พบ #sections-container ในหน้า")}
    container.innerHTML="";
    sectionsState.forEach((s,i)=>container.appendChild(renderSection(s,i)));
    syncHiddenField();
  }catch(e){alertBox.error(e)}
}

// ========================= Buttons =========================
function walkEnsurePictures(node){
  const n={text:node.text||"", paragraphs:Array.isArray(node.paragraphs)?node.paragraphs.slice():[], pictures:Array.isArray(node.pictures)?node.pictures:[], children:[]};
  if(Array.isArray(node.children)) n.children=node.children.map(walkEnsurePictures);
  else n.children=[];
  return n;
}

function wireButtons(){
  const btnGet=document.getElementById("btnGetData");
  const btnSave=document.getElementById("btnSave");
  const btnGen=document.getElementById("btnGenerate");
  const intro=document.getElementById("intro_body");
  const hidden=document.getElementById("sections_json");

  btnGet.addEventListener("click",async()=>{
    alertBox.show("กำลังดึงข้อมูล...","info",0);
    try{
      const data=await postAction("get_data");
      if(data&&data.initial){
        intro.value=data.initial.intro_body||"";
        const arr=data.initial.sections||[];
        sectionsState=arr.map(s=>({
          title_no:s.title_no||"",
          title:s.title||"",
          body_paragraphs:Array.isArray(s.body_paragraphs)?s.body_paragraphs.slice():[],
          items:Array.isArray(s.items)?s.items.map(walkEnsurePictures):[emptyNode()]
        }));
        redrawSections(); alertBox.show("ดึงข้อมูลสำเร็จ ✅","success");
      }else{alertBox.show("โครงสร้างข้อมูลไม่ถูกต้อง","error")}
    }catch(e){alertBox.error(e)}
  });

  btnSave.addEventListener("click",async()=>{
    alertBox.show("กำลังบันทึก...","info",0); syncHiddenField();
    try{
      const data=await postAction("save",{intro_body:intro.value,sections_json:hidden.value});
      if(data&&data.status==="ok"){alertBox.show("บันทึกเรียบร้อย 💾","success")} else {alertBox.show("บันทึกไม่สำเร็จ","error")}
    }catch(e){alertBox.error(e)}
  });

  btnGen.addEventListener("click",async()=>{
    alertBox.show("กำลังสร้างเอกสาร...","info",0); syncHiddenField();
    try{
      const data=await postAction("generate_doc",{intro_body:intro.value,sections_json:hidden.value});
      if(typeof data==="string"){alertBox.show(data,"success",5000)} else {alertBox.show("สร้างเอกสารเสร็จ (mock) 📄","success",5000)}
    }catch(e){alertBox.error(e)}
  });
}

// ========================= init =========================
document.addEventListener("DOMContentLoaded",()=>{
  try{
    sectionsState=[ emptySection("2.1","แนวคิดและทฤษฎีที่เกี่ยวข้อง"),
                    emptySection("2.2","งานวิจัยที่เกี่ยวข้อง") ];
    redrawSections();
    wireButtons();
    alertBox.show("พร้อมแก้ไขบทที่ 2 ✅ (รูปภาพอยู่ในทุกหัวข้อ 2.1.x และ 2.2.x)","success");
  }catch(e){alertBox.error(e)}
});