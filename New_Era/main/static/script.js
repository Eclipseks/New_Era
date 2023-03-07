let shiftPressed = false;
document.addEventListener('keydown', function(event) {
  if (event.shiftKey) {
    shiftPressed = true;
  }
});

document.addEventListener('keyup', function(event) {
  if (!event.shiftKey) {
    shiftPressed = false;
  }
});

let checkboxes = document.querySelectorAll('.checkbox.shift-select');
checkboxes.forEach(function(checkbox) {  checkbox.addEventListener('change', function(event) {
    if (shiftPressed) {
      let currentCheckboxIndex = Array.from(checkboxes).indexOf(this);
      let lastIndex = currentCheckboxIndex;
      let startIndex = currentCheckboxIndex;

      // Находим начальный и конечный индексы выделенных checkbox'ов
      for (let i = currentCheckboxIndex - 1; i >= 0; i--) {
        if (checkboxes[i].checked) {
          startIndex = i;
        } else {
          break;
        }
      }
      for (let i = currentCheckboxIndex + 1; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
          lastIndex = i;
        } else {
          break;
        }
      }

      // Выделяем checkbox'ы от начального до конечного индекса
      for (let i = startIndex; i <= lastIndex; i++) {
        checkboxes[i].checked = true;
      }
    }
  });
});

let selectAllCheckbox = document.getElementById('select-all');
selectAllCheckbox.addEventListener('change', function(event) {
  let checkboxes = document.querySelectorAll('.checkbox.shift-select');
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = event.target.checked;
  });
});

