document.addEventListener('DOMContentLoaded', () => {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'indicatorName') {
            console.log("received indicatorName:", message.value);
            setIndicatorName(message.value);
        }
    });

    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        if (tabs[0].id) {
            chrome.scripting.executeScript({
                target: {tabId: tabs[0].id},
                func: fetchIndicatorName
            });
        }
    });
});





function fetchIndicatorName() {
    const indicatorNameElement = document.querySelector('.tv-chart-view__title-name.js-chart-view__name') as HTMLSpanElement | null;
    if (indicatorNameElement) {
        const indicatorName = indicatorNameElement.textContent || '';
        try {
            chrome.runtime.sendMessage({ type: 'indicatorName', value: indicatorName });
            console.log("sent indicatorName:", indicatorName);
        } catch {
            console.log("error caught sending message");
        }
    } else {
        console.error("indicatorName Element Not Found!");
    }
}


function setIndicatorName(newName: string): void {
    const indicatorNameElement = document.getElementById('indicatorName');

    if (indicatorNameElement) {
        indicatorNameElement.textContent = newName;
    } else {
        console.error('Indicator name element not found');
    }
}
