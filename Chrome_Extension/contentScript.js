let resultText;
let tab_id;
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if(request.todo == "Summarize") {
        var oReq = new XMLHttpRequest();
        console.log(request);
        console.log(sender);

        oReq.open("GET", "http://127.0.0.1:8000/api/summarize?youtube_url=" + request.url + "&choice=" + request.type + "&percent=" + request.percent, true);

        oReq.onreadystatechange = function() {
            if (oReq.readyState == 4) {
                console.log("Request completed with status:", oReq.status);
                if (oReq.status == 200) {
                    try {
                        resultText = JSON.parse(oReq.responseText);
                        console.log("Parsed response:", resultText);
                        sendResponse({summary: resultText.summary});
                    } catch (error) {
                        console.error('Error parsing JSON:', error);
                        sendResponse({error: 'Failed to parse response'});
                    }
                } else {
                    console.error('Error fetching summary:', oReq.statusText);
                    sendResponse({error: 'Failed to fetch summary: ' + oReq.statusText});
                }
            }
        };
        oReq.send();
        return true;
    }
});
