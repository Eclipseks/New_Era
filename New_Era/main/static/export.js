const exportButton = document.getElementById('export-button');

exportButton.addEventListener('click', (e) => {
  e.preventDefault(); // Prevent the default behavior of the button click
  const checkboxes = document.getElementsByName('checkboxes');
  const selectedCheckboxes = [];

  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      selectedCheckboxes.push(checkbox.value);
    }
  });

  let format;
  do {
    format = prompt("Enter the desired format (excel or csv):");
    if (format) {
      format = format.toLowerCase();
    }
  } while (format !== 'excel' && format !== 'csv');

  const url = `/export/?checkboxes=${selectedCheckboxes.join(',')}&format=${format}`;
  window.location.href = url;
});
