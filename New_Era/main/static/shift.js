// var lastChecked = null;

// function onCheckboxClick(checkbox, event) {
//   if (event.shiftKey && lastChecked != null) {
//     var checkboxes = document.getElementsByClassName("checkbox");
//     var start = Array.prototype.indexOf.call(checkboxes, lastChecked);
//     var end = Array.prototype.indexOf.call(checkboxes, checkbox);
//     if (start > end) {
//       var temp = start;
//       start = end;
//       end = temp;
//     }
//     for (var i = start; i <= end; i++) {
//       checkboxes[i].checked = checkbox.checked;
//     }
//   }
//   lastChecked = checkbox;
// }
