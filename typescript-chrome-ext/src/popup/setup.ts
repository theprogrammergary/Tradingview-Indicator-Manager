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

function getPineID() {
  try {
    const PINE_ID_SELECTOR: string = `#tv-content > div > div > div.tv-chart-view__section > div.tv-chart-view__permission-block.tv-chart-view__permission-block--invite-only-access-granted > div.tv-chart-view__script-actions > button.tv-social-stats__item.i-checked.js-chart-view__manage-access.apply-common-tooltip.tv-social-stats__item--button`;

    const element = document.querySelector(PINE_ID_SELECTOR);

    if (element) {
      const dataScriptIdPart = element.getAttribute("data-script-id-part");

      if (dataScriptIdPart) {
        return dataScriptIdPart;
      }
    }

    return null;
  } catch (error) {
    return null;
  }
}

function validManageAccessPage(): void {
  const manageAccessBTN = document.querySelector(
    ".tv-social-stats__item.i-checked.js-chart-view__manage-access.apply-common-tooltip.tv-social-stats__item--button"
  ) as HTMLButtonElement | null;

  const scriptID = manageAccessBTN?.getAttribute("data-script-id-part") ?? null;
  if (scriptID) {
    chrome.storage.local
      .set({ pineID: scriptID })
      .catch((error) => console.log(error));
  }

  const indicatorNameElement = document.querySelector(
    ".tv-chart-view__title-name.js-chart-view__name"
  ) as HTMLSpanElement | null;

  const indicatorName = indicatorNameElement?.textContent ?? null;

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
