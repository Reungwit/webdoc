// === CLEAN TEXTAREA ก่อน submit ===
document.getElementById("myForm").addEventListener("submit", function (e) {
  const textareas = document.querySelectorAll(".clean-textarea");
  textareas.forEach(textarea => {
    const rawText = textarea.value;
    const cleanedText = rawText
      .replace(/\r?\n/g, "")
      .replace(/\s+/g, " ")
      .trim();
    textarea.value = cleanedText;
  });
});

// === PURPOSE ===
let purposeCount = 1;
const maxPurpose = 3;
const purposeContainer = document.getElementById('purpose_container');

function createpurposeInput(index, purpose = '') {
  const label = document.createElement('label');
  label.setAttribute('for', `purpose_${index}`);
  label.textContent = `วัตถุประสงค์ ข้อที่ ${index}`;

  const input = document.createElement('input');
  input.type = 'text';
  input.id = `purpose_${index}`;
  input.name = `purpose_${index}`;
  input.size = 60;
  input.value = purpose;

  purposeContainer.appendChild(label);
  purposeContainer.appendChild(document.createElement('br'));
  purposeContainer.appendChild(input);
  purposeContainer.appendChild(document.createElement('br'));
  purposeContainer.appendChild(document.createElement('br'));
}

function renderpurposeFromData() {
  purposeContainer.innerHTML = '';
  let data = window.purpose || [];
  if (!data.length) {
    createpurposeInput(1);
    purposeCount = 1;
  } else {
    purposeCount = 0;
    data.forEach((p, index) => {
      createpurposeInput(index + 1, p);
      purposeCount++;
    });
  }
  document.getElementById('add-button').disabled = purposeCount >= maxPurpose;
}


function addPurpose() {
  if (purposeCount >= maxPurpose) return;
  purposeCount++;
  createpurposeInput(purposeCount);
  document.getElementById('add-button').disabled = purposeCount >= maxPurpose;
}

function removePurpose() {
  if (purposeCount > 1) {
    for (let i = 0; i < 5; i++) {
      purposeContainer.removeChild(purposeContainer.lastElementChild);
    }
    purposeCount--;
    document.getElementById('add-button').disabled = false;
  }
}

// === SCOPE ===
let scopeCount = 1;
let subCounts = {1: 1}; // {หัวข้อใหญ่: จำนวนย่อย}
let scopeValues = {};   // เก็บค่า input เดิม

function initScopeFromData() {
  const data = window.scopeInitial || [];
  scopeCount = data.length || 1;
  subCounts = {};
  scopeValues = {};

  for (let i = 0; i < scopeCount; i++) {
    let idx = i + 1;
    let item = data[i];
    scopeValues[`scope_b_${idx}`] = item.main || "";
    subCounts[idx] = item.subs?.length || 1;

    for (let j = 0; j < subCounts[idx]; j++) {
      scopeValues[`scope_s_${idx}_${j + 1}`] = item.subs[j] || "";
    }
  }
}





function saveScopeValues() {
  scopeValues = {};
  for (let i = 1; i <= scopeCount; i++) {
    // ขอบเขตหัวข้อใหญ่
    let mainVal = document.getElementById(`scope_b_${i}`)?.value || "";
    scopeValues[`scope_b_${i}`] = mainVal;
    let subCount = subCounts[i] || 1;
    for (let j = 1; j <= subCount; j++) {
      let subVal = document.getElementById(`scope_s_${i}_${j}`)?.value || "";
      scopeValues[`scope_s_${i}_${j}`] = subVal;
    }
  }
}

function renderScopeInputs() {
  document.addEventListener("DOMContentLoaded", function () {
  renderpurposeFromData();
  initScopeFromData();      // <<<< 🆕
  renderScopeInputs();      // <<<< 🆕 ตอนนี้จะใช้ค่าจาก scopeInitial
});

  
  const container = document.getElementById('scope_container');
  container.innerHTML = '';
  for (let i = 1; i <= scopeCount; i++) {
    let mainVal = scopeValues[`scope_b_${i}`] || "";
    container.innerHTML += `
      <label>2.3.${i} ขอบเขตหัวข้อใหญ่ ข้อที่ ${i}</label><br>
      <input type="text" id="scope_b_${i}" name="scope_b_${i}" size="80" value="${mainVal}"><br>
      <button type="button" onclick="addScopeS(${i})">เพิ่ม ขอบเขตหัวข้อย่อย</button>
      <button type="button" onclick="removeScopeS(${i})">ลบ ขอบเขตหัวข้อย่อย</button><br>
      <input type="hidden" name="scope_subcount_${i}" id="scope_subcount_${i}" value="${subCounts[i] || 1}">
    `;
    let subCount = subCounts[i] || 1;
    for (let j = 1; j <= subCount; j++) {
      let subVal = scopeValues[`scope_s_${i}_${j}`] || "";
      container.innerHTML += `
        <label>2.3.${i}.${j} ขอบเขตหัวข้อย่อย ข้อที่ ${j}</label><br>
        <input type="text" id="scope_s_${i}_${j}" name="scope_s_${i}_${j}" size="80" value="${subVal}"><br>
      `;
    }
  }
  saveScopeValues();
  document.getElementById('scope_count').value = scopeCount;
}


function addScopeB() {
  renderScopeInputs(); // save ก่อน
  scopeCount++;
  subCounts[scopeCount] = 1;
  renderScopeInputs();
}
function removeScopeB() {
  renderScopeInputs();
  if (scopeCount > 1) {
    delete subCounts[scopeCount];
    scopeCount--;
    renderScopeInputs();
  }
}
function addScopeS(bi) {
  renderScopeInputs();
  subCounts[bi] = (subCounts[bi] || 1) + 1;
  renderScopeInputs();
}
function removeScopeS(bi) {
  renderScopeInputs();
  if ((subCounts[bi] || 1) > 1) {
    subCounts[bi]--;
    renderScopeInputs();
  }
}
renderScopeInputs();


// === RUN PURPOSE เมื่อโหลด ===
document.addEventListener("DOMContentLoaded", renderpurposeFromData);
