// получаем ссылку на "главный" чекбокс и все остальные чекбоксы на странице
var mainCheckbox = document.getElementById('select-all');
var checkboxes = document.querySelectorAll('.checkbox');

// добавляем обработчик события для "главного" чекбокса
mainCheckbox.addEventListener('change', function() {
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = mainCheckbox.checked;
  });
});

// добавляем обработчик события для всех остальных чекбоксов
checkboxes.forEach(function(checkbox) {
  checkbox.addEventListener('change', function() {
    // если какой-то из остальных чекбоксов не выбран, то "главный" чекбокс не должен быть выбран
    if (!this.checked) {
      mainCheckbox.checked = false;
    }
  });
});
