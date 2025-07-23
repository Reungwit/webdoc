
  let authorCount = 1;
  const maxAuthors = 3;
  const container = document.getElementById('author-container');

  const authors = {{ initial.authors|default:"[]"|safe }};

  function createAuthorInput(index, name = '') {
    const label = document.createElement('label');
    label.setAttribute('for', `name_author_th_${index}`);
    label.textContent = `ชื่อนักศึกษาผู้จัดทำโครงการ คนที่ ${index}`;

    const input = document.createElement('input');
    input.type = 'text';
    input.id = `name_author_th_${index}`;
    input.name = `name_author_th_${index}`;
    input.size = 50;
    input.value = name;

    container.appendChild(label);
    container.appendChild(document.createElement('br'));
    container.appendChild(input);
    container.appendChild(document.createElement('br'));
    container.appendChild(document.createElement('br'));
  }

  function renderAuthorsFromData() {
    // ล้างทั้งหมดก่อน
    container.innerHTML = '';
    if (authors.length === 0) {
      createAuthorInput(1);
      authorCount = 1;
    } else {
      authors.forEach((name, index) => {
        createAuthorInput(index + 1, name);
      });
      authorCount = authors.length;
    }

    document.getElementById('add-button').disabled = authorCount >= maxAuthors;
  }

  function addAuthor() {
    if (authorCount >= maxAuthors) return;
    authorCount++;
    createAuthorInput(authorCount);
    if (authorCount === maxAuthors) {
      document.getElementById('add-button').disabled = true;
    }
  }

  function removeAuthor() {
    if (authorCount > 1) {
      for (let i = 0; i < 4; i++) {
        container.removeChild(container.lastElementChild);
      }
      authorCount--;
      document.getElementById('add-button').disabled = false;
    }
  }

  // เมื่อหน้าโหลดเสร็จ
  document.addEventListener("DOMContentLoaded", renderAuthorsFromData);
