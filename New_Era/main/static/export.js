function exportSelected() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var values = Array.from(checkboxes, checkbox => checkbox.value);
    // Send AJAX request to Django views
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/export/');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        alert('Export successful!');
      } else {
        alert('Export failed!');
      }
    };
    xhr.send(JSON.stringify({ 'values': values }));
  }