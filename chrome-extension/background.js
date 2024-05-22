chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: takeScreenshot
    });
});

function takeScreenshot() {
    chrome.tabs.captureVisibleTab(null, { format: 'png' }, (dataUrl) => {
    });
}
