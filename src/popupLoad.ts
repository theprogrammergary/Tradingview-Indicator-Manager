// In your popup script (popup.ts)
const fetchDataButton = document.getElementById("fetchDataButton") as HTMLButtonElement | null;

if (fetchDataButton) {
    fetchDataButton.addEventListener("click", () => {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            if (tabs.length > 0 && tabs[0].id !== undefined) {
                const activeTabId = tabs[0].id as number;
                setTimeout( () => {
                    chrome.tabs.sendMessage(activeTabId, { text: "you got the goods?" });
                    console.log(`Sent request to Tab ID: ${activeTabId}, URL: ${tabs[0].url}`);
                }, 2000);
            } else {
                console.log("No active tab found or tab ID is undefined.");
            }
        });
    });
}

