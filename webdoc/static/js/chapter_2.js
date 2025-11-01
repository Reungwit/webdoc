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
// node ย่อย (หัวข้อย่อยระดับใดก็ได้: 2.1.1, 2.1.1.1 ฯลฯ)
function makeNode() {
  return {
    text: "",        // ชื่อหัวข้อย่อย
    paragraphs: [],  // ย่อหน้าในหัวข้อนี้
    pictures: [],    // [{pic_no, pic_name, pic_path}]
    children: []     // node ย่อยลงไปอีก
  };
}

// หัวข้อใหญ่ เช่น 2.1, 2.2, 2.3 ...
function makeSection(title_no, title) {
  return {
    title_no,              // "2.1"
    title,                 // "แนวคิดและทฤษฎีที่เกี่ยวข้อง"
    body_paragraphs: [],   // ย่อหน้าอธิบายหัวข้อหลัก
    pictures: [],          // รูปแนบตรงระดับหัวข้อหลัก
    items: [ makeNode() ]  // node ชั้นแรกอย่างน้อย 1 ตัว
  };
}

// state เริ่มต้น
let sectionsState = [
  makeSection("2.1", "แนวคิดและทฤษฎีที่เกี่ยวข้อง"),
  makeSection("2.2", "งานวิจัยที่เกี่ยวข้อง")
];

// เก็บไฟล์รูปที่เลือกไว้ชั่วคราวตามตำแหน่ง
// key = "secIdx|pathStr" เช่น "0|" (รูปของหัวข้อ 2.1 เอง)
// หรือ "0|0.1" (node path [0,1] ของหัวข้อ index=0)
const pendingFiles = {};

// ========================= Utilities =========================
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
  if (!res.ok) throw new Error(await res.text());
  if (ct.includes("application/json")) return res.json();
  return res.text();
}

// ดึง node ตาม path (เช่น [0,1] คือ items[0].children[1] ...)
function getNodeByPath(sectionObj, pathArr) {
  if (pathArr.length === 0) return null; // ว่าง = ระดับหัวข้อใหญ่เอง
  let cur = sectionObj.items[pathArr[0]];
  for (let i=1; i<pathArr.length; i++) {
    cur = cur.children[pathArr[i]];
  }
  return cur;
}

// สร้างหมายเลขหัวข้อย่อยจาก path
// ex: sectionNo "2.1", pathArr [0] -> "2.1.1"
//     pathArr [0,1] -> "2.1.1.2"
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

// หาเลขหัวข้อใหญ่ถัดไป เช่น ถ้ามี 2.1, 2.2 แล้ว -> คืน "2.3"
function getNextSectionNumber() {
  if (sectionsState.length === 0) {
    return "2.1";
  }
  // หยิบ title_no อันสุดท้าย แล้ว +0.1 แบบมนุษย์
  // สมมติ "2.2" -> แบ่งด้วย "." ได้ ["2","2"]
  const last = sectionsState[sectionsState.length - 1].title_no || "2.1";
  const parts = last.split(".");
  // parts[0] = "2", parts[1] = "2"
  if (parts.length === 2) {
    const chap = parts[0];     // "2"
    const idx  = parseInt(parts[1], 10) || 1;
    return chap + "." + (idx + 1); // "2.3"
  }
  // fallback ถ้า title_no รูปแบบเพี้ยน
  return "2." + (sectionsState.length + 1);
}

// ========================= Render helpers =========================

// render paragraphs array ให้แก้ไขได้
function renderParagraphs(arr, onMutate) {
  const wrap = document.createElement("div");
  wrap.className = "paras-wrap";

  arr.forEach((txt, idx) => {
    const row = document.createElement("div");
    row.className = "para-row";

    const ta = document.createElement("textarea");
    ta.value = txt || "";
    ta.placeholder = "พิมพ์ย่อหน้า . . .";
    ta.addEventListener("input", e => {
      arr[idx] = e.target.value;
      onMutate();
    });

    const del = document.createElement("button");
    del.type = "button";
    del.className = "del-para-btn";
    del.textContent = "ลบ";
    del.addEventListener("click", () => {
      arr.splice(idx,1);
      onMutate();
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
    onMutate();
  });
  wrap.appendChild(addBtn);

  return wrap;
}

// กล่องรูปภาพ ใช้ได้ทั้งหัวข้อใหญ่ และ node ย่อย
function renderPicturesBox(sectionObj, secIndex, pathArr) {
  const picsBox = document.createElement("div");
  picsBox.className = "pics-box";

  // node เป้าหมาย = หัวข้อใหญ่เอง หรือ node ย่อย
  const targetNode = (pathArr.length === 0)
    ? sectionObj
    : getNodeByPath(sectionObj, pathArr);

  if (!targetNode.pictures) {
    targetNode.pictures = [];
  }

  const nodeNo = buildNodeNumber(sectionObj.title_no, pathArr);

  // หัวกล่อง "รูปภาพของหัวข้อ …"
  const head = document.createElement("div");
  head.className = "pics-head";
  head.textContent = `รูปภาพของหัวข้อ ${nodeNo}`;
  picsBox.appendChild(head);

  // เล่นกับ key สำหรับไฟล์ชั่วคราว
  const keyForThisNode = fileKey(secIndex, pathArr);

  // แถว input เพิ่มรูป
  const addRow = document.createElement("div");
  addRow.className = "pics-add-row";

  const captionInput = document.createElement("input");
  captionInput.type = "text";
  captionInput.className = "pic-caption-input";
  captionInput.placeholder = "คำอธิบายรูป / ชื่อรูป (เช่น ภาพที่ 2-1 : แผนภาพระบบ)";

  // ป้ายสถานะไฟล์ที่เลือก
  const pendingLabel = document.createElement("div");
  pendingLabel.style.fontSize = "12px";
  pendingLabel.style.color = "#6b7280";
  pendingLabel.style.minWidth = "160px";

  // ปุ่มเลือกไฟล์
  const pickBtn = document.createElement("button");
  pickBtn.type = "button";
  pickBtn.className = "mini-btn";
  pickBtn.textContent = "เลือกรูป…";

  // ปุ่มยืนยันเพิ่มรูป (อัปโหลด+insert DB)
  const addBtn = document.createElement("button");
  addBtn.type = "button";
  addBtn.className = "mini-btn";
  addBtn.textContent = "เพิ่มรูป";

  // input file ที่ซ่อน
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";
  fileInput.style.display = "none";

  // เมื่อคลิก "เลือกรูป…" ให้เปิด file picker
  pickBtn.addEventListener("click", () => {
    fileInput.click();
  });

  // เมื่อผู้ใช้เลือกไฟล์
  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      // เก็บไฟล์ไว้ใน pendingFiles เพื่อกด "เพิ่มรูป"
      pendingFiles[keyForThisNode] = fileInput.files[0];

      // อัปเดต UI ให้ผู้ใช้เห็นทันทีว่ามีไฟล์ถูกเลือกแล้ว
      pendingLabel.textContent = "ไฟล์ที่เลือก: " + fileInput.files[0].name;

      // แจ้งเตือนบนกล่องข้อความด้านบน (alertBox)
      alertBox.show(`เลือกรูป: ${fileInput.files[0].name}`, "info");
    }
  });

  // เมื่อคลิก "เพิ่มรูป"
  addBtn.addEventListener("click", async () => {
    const picName = (captionInput.value || "").trim();
    const f = pendingFiles[keyForThisNode];

    if (!picName) {
      alertBox.show("กรุณากรอกชื่อหรือคำอธิบายรูป", "warning");
      return;
    }
    if (!f) {
      alertBox.show("ยังไม่ได้เลือกรูป", "warning");
      return;
    }

    alertBox.show("กำลังอัปโหลดรูป...", "info", 0);

    try {
      const data = await postAction(
        "add_picture",
        {
          node_no: nodeNo,        // ex "2.1.1"
          pic_name: picName,      // ชื่อรูป/คำอธิบายจากผู้ใช้
          pic_path: f.name        // path/ชื่อไฟล์ (ฝั่ง backend ควรบันทึกที่เก็บจริง)
        },
        f                          // <-- ตัวไฟล์จริง (request.FILES['pic_file'])
      );

      if (data && data.status === "ok" && data.picture) {
        // push รูปใหม่เข้า node นี้
        targetNode.pictures.push(data.picture);

        // เคลียร์ state และ UI ชั่วคราว
        captionInput.value = "";
        pendingLabel.textContent = "";
        delete pendingFiles[keyForThisNode];

        // redraw เพื่อให้ list ด้านล่างอัปเดต
        redrawSections();

        alertBox.show(data.message || "เพิ่มรูปสำเร็จ 🖼", "success");
      } else {
        alertBox.show((data && data.message) || "เพิ่มรูปไม่สำเร็จ", "error");
      }

    } catch (err) {
      console.error(err);
      alertBox.show("เพิ่มรูปผิดพลาด (" + err.message + ")", "error", 5000);
    }
  });

  // ใส่ element ต่าง ๆ ลงแถวควบคุม
  // ลำดับประมาณ: ช่องชื่อรูป | ปุ่มเลือกรูป | ป้ายไฟล์ที่เลือก | ปุ่มเพิ่มรูป
  addRow.appendChild(captionInput);
  addRow.appendChild(pickBtn);
  addRow.appendChild(pendingLabel);
  addRow.appendChild(addBtn);
  addRow.appendChild(fileInput);
  picsBox.appendChild(addRow);

  // รายการรูปที่เคยเพิ่มแล้ว
  const list = document.createElement("div");
  list.className = "pic-list";

  if (targetNode.pictures.length === 0) {
    const empty = document.createElement("div");
    empty.className = "pic-item";
    empty.style.background = "#fff";
    empty.style.borderStyle = "dashed";
    empty.style.color = "#6b7280";
    empty.textContent = "ยังไม่มีรูปในหัวข้อนี้";
    list.appendChild(empty);
  } else {
    targetNode.pictures.forEach(p => {
      const item = document.createElement("div");
      item.className = "pic-item";
      item.innerHTML = `
        <strong>ภาพที่ ${p.pic_no || "-"}</strong> : ${p.pic_name || ""}
        ${p.pic_path ? `<div class="pic-path">${p.pic_path}</div>` : ""}
      `;
      list.appendChild(item);
    });
  }

  picsBox.appendChild(list);

  return picsBox;
}

// render node (recursive)
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
  titleInput.addEventListener("input", e => {
    nodeObj.text = e.target.value;
    syncHiddenField();
  });

  const controls = document.createElement("div");
  controls.className = "node-controls";

  const btnAddPara = document.createElement("button");
  btnAddPara.type = "button";
  btnAddPara.className = "mini-btn";
  btnAddPara.textContent = "➕ ย่อหน้า";
  btnAddPara.addEventListener("click", () => {
    nodeObj.paragraphs.push("");
    redrawSections();
  });

  const btnAddChild = document.createElement("button");
  btnAddChild.type = "button";
  btnAddChild.className = "mini-btn";
  btnAddChild.textContent = "➕ หัวข้อย่อยถัดไป";
  btnAddChild.addEventListener("click", () => {
    nodeObj.children.push(makeNode());
    redrawSections();
  });

  const btnDelNode = document.createElement("button");
  btnDelNode.type = "button";
  btnDelNode.className = "mini-btn";
  btnDelNode.textContent = "ลบหัวข้อนี้";
  btnDelNode.addEventListener("click", () => {
    // ลบ node นี้ออกจาก sectionsState
    const [rootIdx, ...rest] = pathArr;
    if (rest.length === 0) {
      // ลบจาก section.items[rootIdx]
      sectionObj.items.splice(rootIdx,1);
    } else {
      // ลบจาก children ของ parent
      const parentPath = pathArr.slice(0,-1);
      const parentNode  = getNodeByPath(sectionObj, parentPath);
      const myIdx = pathArr[pathArr.length-1];
      parentNode.children.splice(myIdx,1);
    }
    redrawSections();
  });

  controls.appendChild(btnAddPara);
  controls.appendChild(btnAddChild);
  controls.appendChild(btnDelNode);

  topRow.appendChild(badge);
  topRow.appendChild(titleInput);
  topRow.appendChild(controls);
  nodeEl.appendChild(topRow);

  // paragraphs
  if (nodeObj.paragraphs && nodeObj.paragraphs.length > 0) {
    nodeEl.appendChild(
      renderParagraphs(nodeObj.paragraphs, () => { syncHiddenField(); redrawSections(); })
    );
  } else {
    const firstParaBtn = document.createElement("button");
    firstParaBtn.type = "button";
    firstParaBtn.className = "mini-btn";
    firstParaBtn.textContent = "➕ เพิ่มย่อหน้าแรก";
    firstParaBtn.addEventListener("click", () => {
      nodeObj.paragraphs.push("");
      redrawSections();
    });
    nodeEl.appendChild(firstParaBtn);
  }

  // pictures (ระดับ node นี้)
  nodeEl.appendChild(renderPicturesBox(sectionObj, secIndex, pathArr));

  // children
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

// render tree ของ section (items[])
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

// render การ์ดหัวข้อใหญ่ (2.1 / 2.2 / ...)
function renderSectionCard(sectionObj, secIndex) {
  const wrap = document.createElement("div");
  wrap.className = "chapter-section-card";

  // head row
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
  titleInput.addEventListener("input", e => {
    sectionObj.title = e.target.value;
    syncHiddenField();
  });

  headRow.appendChild(badge);
  headRow.appendChild(titleInput);

  // ปุ่มลบหัวข้อใหญ่ (ลบทั้ง 2.3 ทั้งก้อน)
  const delSectionBtn = document.createElement("button");
  delSectionBtn.type = "button";
  delSectionBtn.className = "mini-btn";
  delSectionBtn.style.marginLeft = "auto";
  delSectionBtn.textContent = "ลบหัวข้อใหญ่";
  delSectionBtn.addEventListener("click", () => {
    sectionsState.splice(secIndex, 1);
    redrawSections();
  });

  headRow.appendChild(delSectionBtn);

  wrap.appendChild(headRow);

  // overview paragraphs ของหัวข้อใหญ่
  const overBlock = document.createElement("div");
  overBlock.className = "overview-block";

  const overLabel = document.createElement("div");
  overLabel.className = "overview-label";
  overLabel.textContent = "ย่อหน้าอธิบายหัวข้อนี้ (ภาพรวม):";
  overBlock.appendChild(overLabel);

  overBlock.appendChild(
    renderParagraphs(sectionObj.body_paragraphs, () => { syncHiddenField(); redrawSections(); })
  );

  wrap.appendChild(overBlock);

  // รูประดับหัวข้อใหญ่เอง
  wrap.appendChild(renderPicturesBox(sectionObj, secIndex, []));

  // tree ย่อย
  wrap.appendChild(renderSectionTree(sectionObj, secIndex));

  return wrap;
}

// render ทั้งหมด (sectionsState -> DOM)
function redrawSections() {
  const container = document.getElementById("sections-container");
  container.innerHTML = "";
  sectionsState.forEach((secObj, secIndex) => {
    container.appendChild(renderSectionCard(secObj, secIndex));
  });
  syncHiddenField();
}

// ========================= BUTTON HANDLERS (ดึง/บันทึก/เอกสาร/เพิ่มหัวข้อใหญ่) =========================
function wireButtons() {
  const btnGet = document.getElementById("btnGetData");
  const btnSave = document.getElementById("btnSave");
  const btnGen = document.getElementById("btnGenerate");
  const btnAddSection = document.getElementById("btnAddSection");

  const intro = document.getElementById("intro_body");
  const hidden = document.getElementById("sections_json");

  // ดึงข้อมูลจาก DB
  btnGet.addEventListener("click", async () => {
    alertBox.show("กำลังดึงข้อมูล...", "info", 0);
    try {
      const data = await postAction("get_data");
      if (data && data.initial && Array.isArray(data.initial.sections)) {
        intro.value = data.initial.intro_body || "";

        sectionsState = data.initial.sections.map(sec => ({
          title_no: sec.title_no || "",
          title: sec.title || "",
          body_paragraphs: Array.isArray(sec.body_paragraphs)
            ? sec.body_paragraphs.slice()
            : [],
          pictures: Array.isArray(sec.pictures)
            ? sec.pictures.slice()
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
    } catch(err) {
      console.error(err);
      alertBox.show("ดึงข้อมูลล้มเหลว ("+err.message+")", "error", 5000);
    }
  });

  // บันทึกข้อมูล
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
        alertBox.show("บันทึกไม่สำเร็จ", "error", 5000);
      }
    } catch(err) {
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
      if (typeof data === "string") {
        alertBox.show(data, "success", 5000);
      } else {
        alertBox.show("สร้างเอกสารเสร็จ 📄", "success", 5000);
      }
    } catch(err) {
      console.error(err);
      alertBox.show("สร้างเอกสารผิดพลาด ("+err.message+")", "error", 5000);
    }
  });

  // เพิ่มหัวข้อใหญ่ใหม่
  btnAddSection.addEventListener("click", () => {
    const nextNo = getNextSectionNumber();
    const newSec = makeSection(nextNo, "");
    sectionsState.push(newSec);
    redrawSections();
    alertBox.show(`เพิ่มหัวข้อ ${nextNo} แล้ว ✅`, "success");
  });
}

// ฟังก์ชันแปลง node จาก backend -> รูปแบบปัจจุบันเรา
function remapNode(rawNode) {
  return {
    text: rawNode.text || "",
    paragraphs: Array.isArray(rawNode.paragraphs) ? rawNode.paragraphs.slice() : [],
    pictures: Array.isArray(rawNode.pictures) ? rawNode.pictures.slice() : [],
    children: Array.isArray(rawNode.children)
      ? rawNode.children.map(remapNode)
      : []
  };
}

// ========================= init =========================
document.addEventListener("DOMContentLoaded", () => {
  redrawSections();
  wireButtons();
  alertBox.show("พร้อมแก้ไขบทที่ 2 ✅", "success");
});
