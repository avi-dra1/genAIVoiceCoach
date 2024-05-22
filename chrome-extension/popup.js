document.getElementById('capture-btn').addEventListener('click', () => {
    chrome.tabs.captureVisibleTab(null, { format: 'png' }, (dataUrl) => {
        // Send the screenshot to the server
        //console.log(dataUrl);
        sendScreenshotToServer(dataUrl);
    });
});

// function sendScreenshotToServer(dataUrl) {
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", "http://localhost:5001/analyze", true);
//     xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//     xhr.onreadystatechange = function() {
//         if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
//             var response = JSON.parse(xhr.responseText);
//             speak(response.message);
//         }
//     }
//     xhr.send(JSON.stringify({image: dataUrl}));
// }

// function speak(text) {
//     var msg = new SpeechSynthesisUtterance();
//     msg.text = text;
//     msg.onerror = function(event) {
//         console.error('Speech synthesis error:', event);
//     };
//     window.speechSynthesis.speak(msg);
// }

function sendScreenshotToServer(dataUrl) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5001/analyze", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.audioData) {
                playAudio(response.audioData);
            } else {
                console.error('No audio data received');
            }
        }
    }
    xhr.send(JSON.stringify({image: dataUrl}));
}

function playAudio(base64Data) {
    var audio = new Audio("data:audio/mpeg;base64," + base64Data);
    audio.play();
}



