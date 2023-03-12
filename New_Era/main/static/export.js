const exportButton = document.getElementById('export-button');

exportButton.addEventListener('click', () => {
  const checkboxes = document.getElementsByName('checkboxes');
  const selectedCheckboxes = [];

  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      selectedCheckboxes.push(checkbox.value);
    }
  });

  const url = `/export/?checkboxes=${selectedCheckboxes.join(',')}`;
  window.location.href = url;
});
