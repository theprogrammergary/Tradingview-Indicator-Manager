document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0].id) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: validManageAccessPage,
      });
    }
  });

  chrome.runtime.onMessage.addListener((message) => {
    if (message.type === "validManageAccessPage") {
      console.log("validManageAccessPage:", message);

      if (message.manageAccessBTN) {
        setIndicatorName(message.indicatorName);
        sessionStorage.setItem("scriptID", message.scriptID);
      } else {
        setInvalidHTML();
      }
    }
  });
});

function validManageAccessPage(): void {
  const manageAccessBTN = document.querySelector(
    ".tv-social-stats__item.i-checked.js-chart-view__manage-access.apply-common-tooltip.tv-social-stats__item--button"
  ) as HTMLButtonElement | null;

  const scriptID = manageAccessBTN?.getAttribute("data-script-id-part") ?? null;

  const indicatorNameElement = document.querySelector(
    ".tv-chart-view__title-name.js-chart-view__name"
  ) as HTMLSpanElement | null;

  const indicatorName = indicatorNameElement?.textContent ?? null;

  // try {
  //   chrome.runtime.sendMessage({
  //     type: "validManageAccessPage",
  //     manageAccessBTN: !!manageAccessBTN,
  //     scriptID: scriptID,
  //     indicatorName: indicatorName,
  //   });
  // } catch {
  //   console.error("Error caught sending message");
  // }

  if (!manageAccessBTN) {
    console.error("manageAccess Button Not Found!");
  }

  if (!indicatorName) {
    console.error("Indicator Name Not Found");
  }
}

function setInvalidHTML(): void {
  window.location.href = "invalid.html";
}

function setIndicatorName(newName: string): void {
  const indicatorNameElement = document.getElementById("indicatorName");

  if (indicatorNameElement) {
    indicatorNameElement.textContent = newName;
  } else {
    console.error("Indicator name element not found");
  }
}
