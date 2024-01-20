document.addEventListener("DOMContentLoaded", () => {
  chrome.runtime.onMessage.addListener((message) => {
    if (message.action === "valid manage access page") {
      if (message.data.valid) {
        setIndicatorName(message.data.indicatorName);
        sessionStorage.setItem("scriptID", message.scriptID);
      } else {
        setInvalidHTML();
      }
    }
  });

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0].id) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: validManageAccessPage,
      });
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

  if (!manageAccessBTN) {
    chrome.runtime.sendMessage({
      action: "valid manage access page",
      data: { pineID: "", indicatorName: "", valid: false },
    });
    return;
  }

  const indicatorNameElement = document.querySelector(
    ".tv-chart-view__title-name.js-chart-view__name"
  ) as HTMLSpanElement | null;
  if (!indicatorNameElement) {
    chrome.runtime.sendMessage({
      action: "valid manage access page",
      data: { pineID: "", indicatorName: "", valid: false },
    });
    return;
  }

  const indicatorName = indicatorNameElement?.textContent ?? null;
  const scriptID = manageAccessBTN?.getAttribute("data-script-id-part") ?? null;
  if (scriptID) {
    chrome.storage.local
      .set({ pineID: scriptID })
      .catch((error) => console.log(error));
  }

  chrome.runtime.sendMessage({
    action: "valid manage access page",
    data: { pineID: scriptID, indicatorName: indicatorName, valid: true },
  });
}

function setInvalidHTML(): void {
  window.location.href = "invalid.html";
}

function setIndicatorName(newName: string): void {
  const indicatorNameElement = document.getElementById("indicatorName");

  if (indicatorNameElement) {
    indicatorNameElement.textContent = newName;
  } else {
    chrome.runtime.sendMessage({
      action: "valid manage access page",
      data: { pineID: "", indicatorName: "", valid: false },
    });
  }
}
