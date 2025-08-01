document.getElementById("myForm").addEventListener("submit", function (e) {
  // ✅ จัดการ textarea ทั้งหมดที่มี class="clean-textarea"
  const textareas = document.querySelectorAll(".clean-textarea");

  textareas.forEach(textarea => {
    const rawText = textarea.value;
    const cleanedText = rawText
      .replace(/\r?\n/g, "")      // ลบ \n และ \r
      .replace(/\s+/g, " ")       // ยุบช่องว่าง
      .trim();                    // ลบช่องว่างหัวท้าย
    textarea.value = cleanedText;
  });
});

let purposeCount = 1;
const maxPurpose = 3;
const container = document.getElementById('purpose_container');

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

  container.appendChild(label);
  container.appendChild(document.createElement('br'));
  container.appendChild(input);
  container.appendChild(document.createElement('br'));
  container.appendChild(document.createElement('br'));
}

function renderpurposeFromData() {
  container.innerHTML = '';
  if (!purpose || purpose.length === 0) {
    createpurposeInput(1);
    purposeCount = 1;
  } else {
    purpose.forEach((p, index) => {
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
      container.removeChild(container.lastElementChild);
    }
    purposeCount--;
    document.getElementById('add-button').disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", renderpurposeFromData);