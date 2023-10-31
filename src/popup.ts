// import { changeColorAndAlert } from './content';

// document.addEventListener("DOMContentLoaded", function () {
//   const button = document.getElementById("changeColorButton");

//   if (button) {
//     button.addEventListener("click", function () {
//       chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//         const tab = tabs[0];
//         if (tab && tab.id !== undefined) {
//           (chrome.scripting.executeScript as any)({
//             target: { tabId: tab.id },
//             function: changeColorAndAlert,
//           });
//         }
//       });
//     });
//   }


// });


