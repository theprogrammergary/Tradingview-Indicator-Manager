const step1_div = document.getElementById("step1") as HTMLDivElement;
const step2_div = document.getElementById("step2") as HTMLDivElement;
const step3_div = document.getElementById("step3") as HTMLDivElement;
const step4_div = document.getElementById("step4") as HTMLDivElement;

const s4ResultsList = document.getElementById(
  "s4ResultsList"
) as HTMLDivElement;

document.addEventListener("DOMContentLoaded", () => {
  chrome.runtime.onMessage.addListener(async (message) => {
    const managementMsg: boolean =
      message.action === "adding - " || message.action === "removing - ";

    if (message.action === "new list management") {
      clearListbox();
    } else if (managementMsg) {
      showStep4();
      addToListbox(message);
    }
  });

  function showStep4() {
    step1_div.classList.add("hidden");
    step2_div.classList.add("hidden");
    step3_div.classList.add("hidden");
    step4_div.classList.remove("hidden");
  }

  function clearListbox() {
    if (s4ResultsList) {
      s4ResultsList.innerHTML = "";
    }
  }

  function addToListbox(message: any) {
    const div: string = message.action.toUpperCase() + " " + message.data;
    s4ResultsList.innerHTML += `<div>${div}</div>`;
  }
});
