const validUrl = "https://www.tradingview.com/script";

chrome.action.onClicked.addListener(async (tab) => {
  if (tab.id) {
    if (tab.url?.startsWith(validUrl)) {
      await chrome.action.setPopup({
        tabId: tab.id,
        popup: "dist/popupValid.html",
      });
    } else {
      await chrome.action.setPopup({
        tabId: tab.id,
        popup: "dist/popupInvalid.html",
      });
    }
  }
});
