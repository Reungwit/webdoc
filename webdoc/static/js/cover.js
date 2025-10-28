let authorCount = 1;
const maxAuthors = 3;
const container = document.getElementById('author-container');

let authors_th = [];
let authors_en = [];

try {
  authors_th = JSON.parse(container.dataset.authorsTh || '[]') || [];
  authors_en = JSON.parse(container.dataset.authorsEn || '[]') || [];
} catch (e) {
  authors_th = [];
  authors_en = [];
}




function createAuthorInput(index, name_th = '', name_en = '') {
  // label + input ภาษาไทย
  const labelTh = document.createElement('label');
  labelTh.setAttribute('for', `name_author_th_${index}`);
  labelTh.textContent = `ชื่อผู้จัดทำคนที่ ${index} (ภาษาไทย):`;

  const inputTh = document.createElement('input');
  inputTh.type = 'text';
  inputTh.id = `name_author_th_${index}`;
  inputTh.name = `name_author_th_${index}`;
  inputTh.size = 50;
  inputTh.value = name_th;

  // label + input ภาษาอังกฤษ
  const labelEn = document.createElement('label');
  labelEn.setAttribute('for', `name_author_en_${index}`);
  labelEn.textContent = `ชื่อผู้จัดทำคนที่ ${index} (ภาษาอังกฤษ):`;

  const inputEn = document.createElement('input');
  inputEn.type = 'text';
  inputEn.id = `name_author_en_${index}`;
  inputEn.name = `name_author_en_${index}`;
  inputEn.size = 50;
  inputEn.value = name_en;

  container.appendChild(labelTh);
  container.appendChild(document.createElement('br'));
  container.appendChild(inputTh);
  container.appendChild(document.createElement('br'));
  container.appendChild(document.createElement('br'));

  container.appendChild(labelEn);
  container.appendChild(document.createElement('br'));
  container.appendChild(inputEn);
  container.appendChild(document.createElement('br'));
  container.appendChild(document.createElement('br'));
}

function renderAuthorsFromData() {
  container.innerHTML = '';
  const count = Math.max(authors_th.length, authors_en.length);

  if (count === 0) {
    createAuthorInput(1);
    authorCount = 1;
  } else {
    for (let i = 0; i < count; i++) {
      createAuthorInput(i + 1, authors_th[i] || '', authors_en[i] || '');
    }
    authorCount = count;
  }

  document.getElementById('add-button').disabled = authorCount >= maxAuthors;
}


function addAuthor() {
  if (authorCount >= maxAuthors) return;
  authorCount++;
  createAuthorInput(authorCount);
  if (authorCount == maxAuthors) {
    document.getElementById('add-button').disabled = true;
  }
}

function removeAuthor() {
  if (authorCount > 1) {
    // ลบ 8 nodes ต่อคน (label, br, input, br, br, label, br, input, br, br)
    for (let i = 0; i < 10; i++) {
      container.removeChild(container.lastElementChild);
    }
    authorCount--;
    document.getElementById('add-button').disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", renderAuthorsFromData);
console.log("Loaded authors_th:", authors_th);