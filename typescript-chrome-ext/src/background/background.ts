const validUrl = "https://www.tradingview.com/script";

chrome.action.onClicked.addListener(async (tab) => {
  if (tab.id) {
    if (tab.url?.startsWith(validUrl)) {
      await chrome.action.setPopup({
        tabId: tab.id,
        popup: "dist/popup/html/main.html",
      });
    } else {
      await chrome.action.setPopup({
        tabId: tab.id,
        popup: "dist/popup/html/invalid.html",
      });
    }
  }
});

chrome.runtime.onMessage.addListener(async (message) => {
  if (message.action === "new list management") {
    chrome.tabs.query(
      { active: true, currentWindow: true },
      async function (tabs) {
        const currentTab = tabs[0];
        if (currentTab && currentTab.id) {
          await chrome.scripting.executeScript({
            target: { tabId: currentTab.id },
            files: ["dist/background/pineID.js"],
          });
          await chrome.scripting.executeScript({
            target: { tabId: currentTab.id },
            files: ["dist/background/tradingview.js"],
          });
        }
      }
    );
  } else {
    console.log(message.action.toUpperCase(), message.data);
  }

  // } else if (message.action === "new list management") {
  //   chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  //     const currentTab = tabs[0];
  //     if (currentTab && currentTab.id) {
  //       chrome.scripting.executeScript({
  //         target: { tabId: currentTab.id },
  //         files: ["dist/background/manage.js"],
  //       }, () => {
  //         if (currentTab && currentTab.id)
  //           chrome.scripting.executeScript({
  //             target: { tabId: currentTab.id },
  //             args: ["testing123"],
  //             func: (...args: string[]) => listManagement(...args),
  //           });
  //       });
  //     }
  //   });
  // }
});
