const validUrl = "https://www.tradingview.com/script";

chrome.action.onClicked.addListener(async (tab) => {
    if (tab.id) {
        if (tab.url?.startsWith(validUrl)) {
            await chrome.action.setPopup({ tabId: tab.id, popup: 'dist/popup_valid.html' });
            console.log("Extension enabled for the tab");
        } else {
            await chrome.action.setPopup({ tabId: tab.id, popup: 'dist/popup_invalid.html' });
            console.log("Extension disabled for the tab");
        }
    }
});
