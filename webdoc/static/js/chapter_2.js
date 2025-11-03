// ========================= CSRF Helper =========================
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "";
}
function getCsrfToken() { return getCookie("csrftoken"); }

// ========================= Alert / Toast =========================
const alertBox = (() => {
  const el = () => document.getElementById("alert-box");
  function show(msg, type = "info", timeoutMs = 3000) {
    const box = el();
    if (!box) return;
    box.textContent = msg;
    box.className = "";
    box.classList.add(type);
    box.classList.add("show");
    if (timeoutMs) {
      setTimeout(() => {
        if (box.textContent === msg) {
          box.textContent = "";
          box.className = "";
        }
      }, timeoutMs);
    }
  }
  return { show };
})();

// ========================= Data Model =========================
function makeNode() {
  return {
    text: "",
    paragraphs: [],
    pictures: [],   // [{pic_no, pic_name, pic_path, id?, server_pic_no?}]
    children: []
  };
}

function makeSection(title_no, title) {
  return {
    title_no,
    title,
    body_paragraphs: [],
    pictures: [],
    items: [ makeNode() ]
  };
}

// state เริ่มต้น
let sectionsState = [
  makeSection("2.1", "แนวคิดและทฤษฎีที่เกี่ยวข้อง"),
  makeSection("2.2", "งานวิจัยที่เกี่ยวข้อง")
];

// key => File ที่ผู้ใช้เลือกเตรียมอัปโหลดใน node นั้น
const pendingFiles = {}; // {"secIndex|path.path": File}

// ========================= Utils / AJAX =========================
function syncHiddenField() {
  const hidden = document.getElementById("sections_json");
  if (!hidden) return;
  hidden.value = JSON.stringify(sectionsState);
}

async function postAction(action, extra = {}, fileToUpload = null) {
  const url = window.location.href;
  const fd  = new FormData();
  fd.append("action", action);
  Object.entries(extra).forEach(([k,v]) => fd.append(k, v));
  if (fileToUpload) fd.append("pic_file", fileToUpload);

  const res = await fetch(url, {
    method: "POST",
    headers: { "X-CSRFToken": getCsrfToken() },
    body: fd
  });

  const ct = res.headers.get("Content-Type") || "";
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }
  if (ct.includes("application/json")) return res.json();
  return res.text();
}

// เข้าถึง node ย่อยด้วย path array เช่น [0,1,2]
function getNodeByPath(sectionObj, pathArr) {
  if (pathArr.length === 0) return null;
  let cur = sectionObj.items[pathArr[0]];
  for (let i = 1; i < pathArr.length; i++) {
    cur = cur.children[pathArr[i]];
  }
  return cur;
}

// แปลง path → "2.1.2.1" เป็นต้น
function buildNodeNumber(sectionNo, pathArr) {
  if (!pathArr || pathArr.length === 0) return sectionNo;
  const suffix = pathArr.map(i => (i+1)).join(".");
  return sectionNo + "." + suffix;
}

// key สำหรับ pendingFiles
function fileKey(secIndex, pathArr) {
  if (!pathArr || pathArr.length === 0) return secIndex + "|";
  return secIndex + "|" + pathArr.join(".");
}

// หาเลขหัวข้อใหญ่ใหม่ เช่น 2.3, 2.4,...
function getNextSectionNumber() {
  if (sectionsState.length === 0) return "2.1";
  const last = sectionsState[sectionsState.length - 1].title_no || "2.1";
  const parts = last.split(".");
  if (parts.length === 2) {
    const chap = parts[0]; // "2"
    const idx  = parseInt(parts[1], 10) || 1;
    return chap + "." + (idx + 1);
  }
  return "2." + (sectionsState.length + 1);
}

// ===== Picture numbering index (per chapter) =====
const picIndex = {}; // { '2': Set<number> }

function normalizePicNo(pic_no) {
  if (!pic_no) return pic_no;
  const m = String(pic_no).match(/^(\d+)(?:\.\d+)*-(\d+)$/); // "2.2.1-7" -> ["2","7"]
  return m ? `${m[1]}-${m[2]}` : pic_no;
}
function seqFromPicNo(pic_no) {
  const m = String(pic_no || '').match(/^\d+-(\d+)$/);
  return m ? parseInt(m[1], 10) : 0;
}
function chapterOf(sectionNo) {
  return String(sectionNo).split(".")[0] || "2";
}

function indexReset(chap) { picIndex[chap] = new Set(); }

function indexAdd(pic_no) {
  const nn = normalizePicNo(pic_no);
  const chap = String(nn).split("-")[0];
  const seq  = seqFromPicNo(nn);
  if (!picIndex[chap]) picIndex[chap] = new Set();
  if (seq > 0) picIndex[chap].add(seq);
}

function indexRemove(pic_no) {
  const nn = normalizePicNo(pic_no);
  const chap = String(nn).split("-")[0];
  const seq  = seqFromPicNo(nn);
  if (picIndex[chap]) picIndex[chap].delete(seq);
}

function indexRebuildFromState() {
  // scan sectionsState -> picIndex
  Object.keys(picIndex).forEach(k => indexReset(k));
  (sectionsState || []).forEach(sec => {
    const chap = chapterOf(sec.title_no);
    if (!picIndex[chap]) indexReset(chap);

    function scanPics(arr) { (arr||[]).forEach(p => indexAdd(p.pic_no)); }
    function walkNode(n){ if(!n) return; scanPics(n.pictures); (n.children||[]).forEach(walkNode); }

    scanPics(sec.pictures);
    (sec.items||[]).forEach(walkNode);
  });
}

function nextFreePicNo(chap) {
  if (!picIndex[chap]) indexReset(chap);
  let i = 1; while (picIndex[chap].has(i)) i++;
  return `${chap}-${i}`;
}



// ========================= Picture Numbering =========================
// คืนลำดับจาก "2-15" -> 15 (ผิดฟอร์แม็ตคืน 0)
function parseSeqFromPicNo(pic_no) {
  if (!pic_no || typeof pic_no !== "string") return 0;
  const m = String(pic_no).match(/^(\d+)-(\d+)$/); // 2-15 -> 15
  return m ? parseInt(m[2], 10) : 0;
}

function normalizePicNo(anyPicNo) {
  if (!anyPicNo) return anyPicNo;
  const m = String(anyPicNo).match(/^(\d+)(?:\.\d+)*-(\d+)$/);
  return m ? `${m[1]}-${m[2]}` : anyPicNo;
}

// รวมเลขลำดับของรูปทั้งหมดใน "บท" (ทุกหัวข้อ ทุกชั้น) จาก state (ใช้ pic_no ที่ normalize แล้ว)
function collectChapterPicSeqs(chapterNo) {
  const seqs = new Set();

  function scan(arr) {
    (arr || []).forEach(p => {
      const pn = normalizePicNo(p && p.pic_no);
      if (pn && String(pn).startsWith(chapterNo + "-")) {
        const n = parseSeqFromPicNo(pn);
        if (n > 0) seqs.add(n);
      }
    });
  }
  function walk(node) {
        if (!node) return;
        scan(node.pictures);
        (node.children || []).forEach(walk);
      }
      (sectionsState || []).forEach(sec => { // <-- [!] แก้ไขโดยลบ "window." ออก
        scan(sec.pictures);
        (sec.items || []).forEach(walk);
      });
      return seqs;
}

// หา "เลขว่างตัวแรก" ของบท เช่นมี {1,2,4} -> คืน "2-3"
function computeFirstFreePicNoForChapter(chapterNo) {
  const seqs = collectChapterPicSeqs(chapterNo);
  let i = 1; while (seqs.has(i)) i += 1;
  return `${chapterNo}-${i}`;
}
// ========================= Paragraph Editor =========================
// ปรับใหม่: แยกการพิมพ์ (ไม่ redrawSections) ออกจาก การเพิ่ม/ลบ (redrawSections)
function renderParagraphs(arr, onChangeContent, onAddOrRemove) {
  const wrap = document.createElement("div");
  wrap.className = "paras-wrap";

  arr.forEach((txt, idx) => {
    const row = document.createElement("div");
    row.className = "para-row";

    const ta = document.createElement("textarea");
    ta.value = txt || "";
    ta.placeholder = "พิมพ์ย่อหน้า . . .";

    ta.addEventListener("input", (e) => {
      arr[idx] = e.target.value;
      if (onChangeContent) onChangeContent();
    });

    const del = document.createElement("button");
    del.type = "button";
    del.className = "del-para-btn";
    del.textContent = "ลบ";
    del.addEventListener("click", () => {
      arr.splice(idx,1);
      if (onAddOrRemove) onAddOrRemove();
    });

    row.appendChild(ta);
    row.appendChild(del);
    wrap.appendChild(row);
  });

  const addBtn = document.createElement("button");
  addBtn.type = "button";
  addBtn.className = "add-para-btn";
  addBtn.textContent = "➕ เพิ่มย่อหน้า";
  addBtn.addEventListener("click", () => {
    arr.push("");
    if (onAddOrRemove) onAddOrRemove();
  });
  wrap.appendChild(addBtn);

  return wrap;
}

// ========================= Picture Box =========================
function renderPicturesBox(sectionObj, secIndex, pathArr) {
  // ไม่ให้มีรูปในระดับหัวข้อใหญ่ (2.x)
  if (!pathArr || pathArr.length === 0) {
    return document.createElement("div"); // คืนเปล่า
  }

  const picsBox = document.createElement("div");
  picsBox.className = "pics-box";

  const targetNode = getNodeByPath(sectionObj, pathArr);
  if (!targetNode.pictures) {
    targetNode.pictures = [];
  }

  const nodeNo = buildNodeNumber(sectionObj.title_no, pathArr);
  const keyForThisNode = fileKey(secIndex, pathArr);

  const head = document.createElement("div");
  head.className = "pics-head";
  head.textContent = `รูปภาพของหัวข้อ ${nodeNo}`;
  picsBox.appendChild(head);

  const addRow = document.createElement("div");
  addRow.className = "pics-add-row";

  const captionInput = document.createElement("input");
  captionInput.type = "text";
  captionInput.className = "pic-caption-input";
  captionInput.placeholder = "คำอธิบายรูป / ชื่อรูป (เช่น ภาพที่ 2-1 : แผนภาพระบบ)";

  const pendingLabel = document.createElement("div");
  pendingLabel.style.fontSize = "12px";
  pendingLabel.style.color = "#6b7280";
  pendingLabel.style.minWidth = "160px";

  const pickBtn = document.createElement("button");
  pickBtn.type = "button";
  pickBtn.className = "mini-btn";
  pickBtn.textContent = "เลือกรูป…";

  const addBtn = document.createElement("button");
  addBtn.type = "button";
  addBtn.className = "mini-btn";
  addBtn.textContent = "เพิ่มรูป";

  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";
  fileInput.style.display = "none";

  pickBtn.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      pendingFiles[keyForThisNode] = fileInput.files[0];
      pendingLabel.textContent = "ไฟล์ที่เลือก: " + fileInput.files[0].name;
      alertBox.show(`เลือกรูป: ${fileInput.files[0].name}`, "info");
    }
  });

  addBtn.addEventListener("click", async () => {
    const picName = (captionInput.value || "").trim();
    const f = pendingFiles[keyForThisNode];

    if (!picName) { alertBox.show("กรุณากรอกชื่อหรือคำอธิบายรูป", "warning"); return; }
    if (!f)       { alertBox.show("ยังไม่ได้เลือกรูป", "warning"); return; }

    alertBox.show("กำลังอัปโหลดรูป...", "info", 0);
    try {
  const chapterNo = String(sectionObj.title_no).split(".")[0] || "2";
  const nextPicNo = computeFirstFreePicNoForChapter(chapterNo);

  const data = await postAction(
    "add_picture",
    {
      node_no: nodeNo,
      pic_name: picName,
      pic_path: f.name,
      pic_no: nextPicNo          // << ใช้เลขนี้เสมอ
    },
    f
  );

  // ใช้ผลตอบกลับ ถ้ามี; แต่ "บังคับ" pic_no เป็นรูปแบบบท-ลำดับตาม nextPicNo
  const pushed = (data && data.picture) ? { ...data.picture } : { pic_name: picName, pic_path: f.name };
  pushed.pic_no = nextPicNo;    // << ไม่ต้องเก็บ/ใช้ server_pic_no อีก

  targetNode.pictures.push(pushed);

  captionInput.value = "";
  pendingLabel.textContent = "";
  delete pendingFiles[keyForThisNode];

  renderPicturesList();
  alertBox.show((data && data.message) || "เพิ่มรูปสำเร็จ", "success");
} catch (err) {
  console.error(err);
  alertBox.show("เพิ่มรูปผิดพลาด (" + err.message + ")", "error", 5000);
}
  });

  addRow.appendChild(captionInput);
  addRow.appendChild(pickBtn);
  addRow.appendChild(pendingLabel);
  addRow.appendChild(addBtn);
  addRow.appendChild(fileInput);
  picsBox.appendChild(addRow);

  // ===== list รูป (มีปุ่ม + ใช้ event delegation) =====
  const list = document.createElement("div");
  list.className = "pic-list";

  function renderPicturesList() {
    list.innerHTML = "";
    const arr = targetNode.pictures || [];

    if (arr.length === 0) {
      const empty = document.createElement("div");
      empty.className = "pic-item";
      empty.style.background = "#fff";
      empty.style.borderStyle = "dashed";
      empty.style.color = "#6b7280";
      empty.textContent = "ยังไม่มีรูปในหัวข้อนี้";
      list.appendChild(empty);
      return;
    }

    // แสดงเรียงตามลำดับเลข (เผื่อมีค่า server แปลก ๆ)
    arr.sort((a, b) => {
      const an = parseSeqFromPicNo(normalizePicNo(a.pic_no));
      const bn = parseSeqFromPicNo(normalizePicNo(b.pic_no));
      return an - bn;
    });

    arr.forEach((p, idx) => {
      const shownNo = normalizePicNo(p.pic_no);
      const item = document.createElement("div");
      item.className = "pic-item";
      item.dataset.idx = String(idx);
      item.innerHTML = `
        <div class="pic-main">
          <strong>ภาพที่ ${shownNo || "-"}</strong> : ${p.pic_name || ""}
          ${p.pic_path ? `<div class="pic-path">${p.pic_path}</div>` : ""}
        </div>
        <div class="pic-actions">
          <button type="button" class="mini-btn danger" data-act="del">ลบรูป</button>
          <button type="button" class="mini-btn outline" data-act="edit">แก้ไข</button>
        </div>
      `;
      list.appendChild(item);
    });
  }

  // Event delegation: รองรับปุ่มในรายการที่ถูก re-render
  list.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-act]");
    if (!btn) return;
    const item = btn.closest(".pic-item");
    if (!item) return;

    const idx = parseInt(item.dataset.idx, 10);
    const arr = targetNode.pictures || [];
    const p = arr[idx];
    if (!p) return;

    // ลบ
if (btn.dataset.act === "del") {
  const shownNo = normalizePicNo(p.pic_no);
  if (!confirm(`ยืนยันลบรูปหมายเลข ${shownNo || "-"}`)) return;
  try {
    const payload = p.id ? { pic_id: p.id } : { node_no: nodeNo, pic_no: shownNo };
    const res = await postAction("delete_picture", payload);
    if (res && res.status === "ok") {
      arr.splice(idx, 1);        // ลบออกจาก state
      renderPicturesList();      // ไม่ renumber
      alertBox.show("ลบรูปสำเร็จ", "success", 1200);
    } else {
      throw new Error((res && res.message) || "delete failed");
    }
  } catch (e2) {
    console.error(e2);
    alertBox.show("ลบรูปไม่สำเร็จ", "danger", 1500);
  }
}

// แก้ไข (ตัวอย่างแก้เฉพาะชื่อ)
if (btn.dataset.act === "edit") {
  const newName = prompt("แก้ไขคำอธิบายรูป:", p.pic_name || "");
  if (newName === null) return;
  try {
    const payload = p.id ? { pic_id: p.id, pic_name: newName }
                         : { node_no: nodeNo, pic_no: normalizePicNo(p.pic_no), pic_name: newName };
    const res = await postAction("edit_picture", payload);
    if (res && res.status === "ok") {
      arr[idx].pic_name = newName; // คง pic_no เดิม
      renderPicturesList();
      alertBox.show("แก้ไขรูปสำเร็จ", "success", 1200);
    } else {
      throw new Error((res && res.message) || "edit failed");
    }
  } catch (e3) {
    console.error(e3);
    alertBox.show("แก้ไขรูปไม่สำเร็จ", "danger", 1500);
  }
}

  });

  renderPicturesList();
  picsBox.appendChild(list);

  return picsBox;
}

// ========================= Node Renderer (หัวข้อย่อย) =========================
function renderNode(sectionObj, secIndex, nodeObj, pathArr) {
  const nodeEl = document.createElement("div");
  nodeEl.className = "node-card";

  const topRow = document.createElement("div");
  topRow.className = "node-top-row";

  const nodeNo = buildNodeNumber(sectionObj.title_no, pathArr);

  const badge = document.createElement("div");
  badge.className = "node-no-badge";
  badge.textContent = nodeNo;

  const titleInput = document.createElement("input");
  titleInput.type = "text";
  titleInput.className = "node-title-input";
  titleInput.placeholder = "พิมพ์ชื่อหัวข้อย่อย…";
  titleInput.value = nodeObj.text || "";
  titleInput.addEventListener("input", (e) => {
    nodeObj.text = e.target.value;
    syncHiddenField(); // อัปเดต hidden แต่ไม่ redraw
  });

  const controls = document.createElement("div");
  controls.className = "node-controls";

  const btnAddPara = document.createElement("button");
  btnAddPara.type = "button";
  btnAddPara.className = "mini-btn";
  btnAddPara.textContent = "➕ ย่อหน้า";
  btnAddPara.addEventListener("click", () => {
    nodeObj.paragraphs.push("");
    redrawSections(); // การเพิ่มย่อหน้าต้อง redraw
  });

  const btnAddChild = document.createElement("button");
  btnAddChild.type = "button";
  btnAddChild.className = "mini-btn";
  btnAddChild.textContent = "➕ หัวข้อย่อยถัดไป";
  btnAddChild.addEventListener("click", () => {
    nodeObj.children.push(makeNode());
    redrawSections(); // เพิ่มหัวข้อย่อยใหม่ -> redraw
  });

  const btnDelNode = document.createElement("button");
  btnDelNode.type = "button";
  btnDelNode.className = "mini-btn";
  btnDelNode.textContent = "ลบหัวข้อนี้";
  btnDelNode.addEventListener("click", () => {
    const [rootIdx, ...rest] = pathArr;
    if (rest.length === 0) {
      sectionObj.items.splice(rootIdx,1);
    } else {
      const parentPath = pathArr.slice(0, -1);
      const parentNode = getNodeByPath(sectionObj, parentPath);
      const myIdx = pathArr[pathArr.length-1];
      parentNode.children.splice(myIdx,1);
    }
    redrawSections(); // ลบ -> redraw
  });

  controls.appendChild(btnAddPara);
  controls.appendChild(btnAddChild);
  controls.appendChild(btnDelNode);

  topRow.appendChild(badge);
  topRow.appendChild(titleInput);
  topRow.appendChild(controls);
  nodeEl.appendChild(topRow);

  // paragraphs ของ nodeObj
  if (nodeObj.paragraphs && nodeObj.paragraphs.length > 0) {
    nodeEl.appendChild(
      renderParagraphs(
        nodeObj.paragraphs,
        () => { // onChangeContent (แค่พิมพ์)
          syncHiddenField();
        },
        () => { // onAddOrRemove (เพิ่ม/ลบ)
          redrawSections();
        }
      )
    );
  } else {
    const firstParaBtn = document.createElement("button");
    firstParaBtn.type = "button";
    firstParaBtn.className = "mini-btn";
    firstParaBtn.textContent = "➕ เพิ่มย่อหน้าแรก";
    firstParaBtn.addEventListener("click", () => {
      nodeObj.paragraphs.push("");
      redrawSections(); // เพิ่ม -> redraw
    });
    nodeEl.appendChild(firstParaBtn);
  }

  // box รูปภาพของ node
  nodeEl.appendChild(renderPicturesBox(sectionObj, secIndex, pathArr));

  // children (หัวข้อย่อยระดับถัดไป)
  const childrenWrap = document.createElement("div");
  childrenWrap.className = "children-block";

  nodeObj.children.forEach((childNode, childIdx) => {
    const childPath = [...pathArr, childIdx];
    childrenWrap.appendChild(
      renderNode(sectionObj, secIndex, childNode, childPath)
    );
  });

  if (nodeObj.children.length === 0) {
    const addChildInline = document.createElement("button");
    addChildInline.type = "button";
    addChildInline.className = "mini-btn";
    addChildInline.textContent = "➕ เพิ่มหัวข้อย่อยระดับถัดไป";
    addChildInline.addEventListener("click", () => {
      nodeObj.children.push(makeNode());
      redrawSections();
    });
    childrenWrap.appendChild(addChildInline);
  }

  nodeEl.appendChild(childrenWrap);

  return nodeEl;
}

// render กลุ่ม node ชั้นแรกของหัวข้อใหญ่
function renderSectionTree(sectionObj, secIndex) {
  const treeWrap = document.createElement("div");
  treeWrap.className = "tree-wrap";

  sectionObj.items.forEach((node, idx) => {
    const pathArr = [idx];
    treeWrap.appendChild(
      renderNode(sectionObj, secIndex, node, pathArr)
    );
  });

  const addRootBtn = document.createElement("button");
  addRootBtn.type = "button";
  addRootBtn.className = "mini-btn";
  addRootBtn.textContent = "➕ เพิ่มหัวข้อย่อยระดับแรก";
  addRootBtn.addEventListener("click", () => {
    sectionObj.items.push(makeNode());
    redrawSections();
  });
  treeWrap.appendChild(addRootBtn);

  return treeWrap;
}

// การ์ดหัวข้อใหญ่ 2.x
function renderSectionCard(sectionObj, secIndex) {
  const wrap = document.createElement("div");
  wrap.className = "chapter-section-card";

  const headRow = document.createElement("div");
  headRow.className = "chapter-head-row";

  const badge = document.createElement("div");
  badge.className = "badge-no";
  badge.textContent = sectionObj.title_no;

  const titleInput = document.createElement("input");
  titleInput.type = "text";
  titleInput.className = "chapter-title-input";
  titleInput.placeholder = "ชื่อหัวข้อหลัก เช่น แนวคิดและทฤษฎีที่เกี่ยวข้อง";
  titleInput.value = sectionObj.title || "";
  titleInput.addEventListener("input", (e) => {
    sectionObj.title = e.target.value;
    syncHiddenField(); // ไม่ redraw ตอนพิมพ์
  });

  const delSectionBtn = document.createElement("button");
  delSectionBtn.type = "button";
  delSectionBtn.className = "mini-btn";
  delSectionBtn.style.marginLeft = "auto";
  delSectionBtn.textContent = "ลบหัวข้อใหญ่";
  delSectionBtn.addEventListener("click", () => {
    sectionsState.splice(secIndex, 1);
    redrawSections(); // ลบ -> redraw
  });

  headRow.appendChild(badge);
  headRow.appendChild(titleInput);
  headRow.appendChild(delSectionBtn);
  wrap.appendChild(headRow);

  // ย่อหน้า overview ของหัวข้อใหญ่
  const overBlock = document.createElement("div");
  overBlock.className = "overview-block";

  const overLabel = document.createElement("div");
  overLabel.className = "overview-label";
  overLabel.textContent = "ย่อหน้าอธิบายหัวข้อนี้ (ภาพรวม):";
  overBlock.appendChild(overLabel);

  overBlock.appendChild(
    renderParagraphs(
      sectionObj.body_paragraphs,
      () => { // onChangeContent
        syncHiddenField();
      },
      () => { // onAddOrRemove
        redrawSections();
      }
    )
  );

  wrap.appendChild(overBlock);

  // tree ย่อย
  wrap.appendChild(renderSectionTree(sectionObj, secIndex));

  return wrap;
}

// render ทุกหัวข้อใหญ่
function redrawSections() {
  const container = document.getElementById("sections-container");
  container.innerHTML = "";
  sectionsState.forEach((secObj, secIndex) => {
    container.appendChild(renderSectionCard(secObj, secIndex));
  });
  syncHiddenField();
}

// ========================= BUTTON HANDLERS =========================
function wireButtons() {
  const btnGet = document.getElementById("btnGetData");
  const btnSave = document.getElementById("btnSave");
  const btnGen  = document.getElementById("btnGenerate");
  const btnAddSection = document.getElementById("btnAddSection");

  const intro  = document.getElementById("intro_body");
  const hidden = document.getElementById("sections_json");

  // ดึงข้อมูล
  btnGet.addEventListener("click", async () => {
    alertBox.show("กำลังดึงข้อมูล...", "info", 0);
    try {
      const data = await postAction("get_data");
      if (data && data.initial && Array.isArray(data.initial.sections)) {
        intro.value = data.initial.intro_body || "";

        // remap + normalize รูปจาก backend
        const remapPicture = (p) => {
          const server_no = p.pic_no || p.server_pic_no || "";
          return {
            ...p,
            pic_no: normalizePicNo(p.pic_no)
          };
        };

        const remapNode = (rawNode) => ({
          text: rawNode.text || "",
          paragraphs: Array.isArray(rawNode.paragraphs) ? rawNode.paragraphs.slice() : [],
          pictures: Array.isArray(rawNode.pictures) ? rawNode.pictures.map(remapPicture) : [],
          children: Array.isArray(rawNode.children)
            ? rawNode.children.map(remapNode)
            : []
        });

        sectionsState = data.initial.sections.map(sec => ({
          title_no: sec.title_no || "",
          title: sec.title || "",
          body_paragraphs: Array.isArray(sec.body_paragraphs)
            ? sec.body_paragraphs.slice()
            : [],
          pictures: Array.isArray(sec.pictures)
            ? sec.pictures.map(remapPicture)
            : [],
          items: Array.isArray(sec.items)
            ? sec.items.map(remapNode)
            : []
        }));

        redrawSections();
        alertBox.show("ดึงข้อมูลสำเร็จ ✅", "success");
      } else {
        alertBox.show("โครงสร้างข้อมูลไม่ถูกต้อง", "error", 5000);
      }
    } catch (err) {
      console.error(err);
      alertBox.show("ดึงข้อมูลล้มเหลว ("+err.message+")", "error", 5000);
    }
  });

  // บันทึก
  btnSave.addEventListener("click", async () => {
    alertBox.show("กำลังบันทึก...", "info", 0);
    syncHiddenField();
    try {
      const data = await postAction("save", {
        intro_body: intro.value,
        sections_json: hidden.value
      });

      if (data && data.status === "ok") {
        alertBox.show("บันทึกเรียบร้อย 💾", "success");
      } else {
        alertBox.show(
          "บันทึกผิดพลาด " + JSON.stringify(data),
          "error",
          5000
        );
      }
    } catch (err) {
      console.error(err);
      alertBox.show("บันทึกล้มเหลว ("+err.message+")", "error", 5000);
    }
  });

  // สร้างเอกสาร
  btnGen.addEventListener("click", async () => {
    alertBox.show("กำลังสร้างเอกสาร...", "info", 0);
    syncHiddenField();
    try {
      const data = await postAction("generate_doc", {
        intro_body: intro.value,
        sections_json: hidden.value
      });
      if (data && data.status === "ok") {
        alertBox.show(data.message || "สร้างเอกสารเสร็จ 📄", "success", 5000);
      } else {
        alertBox.show("สร้างเอกสารผิดพลาด", "error", 5000);
      }
    } catch (err) {
      console.error(err);
      alertBox.show("สร้างเอกสารผิดพลาด ("+err.message+")", "error", 5000);
    }
  });

  // เพิ่มหัวข้อใหญ่ใหม่ (2.3, 2.4, ...)
  btnAddSection.addEventListener("click", () => {
    const nextNo = getNextSectionNumber();
    const newSec = makeSection(nextNo, "");
    sectionsState.push(newSec);
    redrawSections();
    alertBox.show(`เพิ่มหัวข้อ ${nextNo} แล้ว ✅`, "success");
  });
}

// ========================= init =========================
document.addEventListener("DOMContentLoaded", () => {
  redrawSections();
  wireButtons();
  alertBox.show("พร้อมแก้ไขบทที่ 2 ✅", "success");
});
