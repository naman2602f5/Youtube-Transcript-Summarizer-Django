const summarize_button = document.getElementById("summarize");
const percent_dropdown = document.getElementById('percent-dropdown');
const choice_dropdown = document.getElementById('summary-dropdown');
const contents = document.getElementById('contents');
const load_icon = document.getElementById('load-icon');

summarize_button.disabled = true;

percent_dropdown.addEventListener("change", buttonUpdate);
choice_dropdown.addEventListener("change", buttonUpdate);

function buttonUpdate() {
    summarize_button.disabled = (percent_dropdown.selectedIndex <= 0 || choice_dropdown.selectedIndex <= 0);
}

function parse_choice(choice_index) {
    switch (choice_index) {
        case 1:
            return "freq-based";
        case 2:
            return "luhn-algo";
        case 3:
            return "abstractive";
        default:
            return "";
    }
}

document.getElementById('summarize').onclick = function () {
    console.log("Summarize button clicked");

    contents.innerHTML = "";
    contents.style.visibility = "hidden";

    load_icon.style.visibility = "visible";

    let percent_value = percent_dropdown.options[percent_dropdown.selectedIndex].text;
    let choice_index = choice_dropdown.selectedIndex;

    const percent = percent_value.split("%")[0];
    const choice = parse_choice(choice_index);

    console.log("Percent:", percent, "Choice:", choice);

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tab_id = tabs[0].id;
        const tab_url = tabs[0].url;

        console.log("Sending message to content script with URL:", tab_url);

        chrome.tabs.sendMessage(tab_id, { todo: "Summarize", url: tab_url, percent: percent, type: choice }, function (response) {

            load_icon.style.visibility = "hidden";

            if (response && response.summary) {
                contents.innerHTML = "<b>Summarized Text: </b><br>" + response.summary;
            } else {
                contents.innerHTML = "<b>Error:</b> Error" + response.error;
            }

            contents.style.visibility = "visible";;
        });
    });
}
