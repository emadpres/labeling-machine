function InitProgressbar(progress_labeled, progress_total) {
    var progress_percentage = Math.ceil(progress_labeled * 100 / progress_total);
    document.getElementById("top-progress-bar-status").innerHTML = progress_percentage + '%';
    document.getElementById("top-progress-bar-status").style.width = progress_percentage + "%";
}

FlagBtnCallback = function (response, status) {
    console.log("<<fpBtnCallback>>: " + status + response.toString());
    var response_json = $.parseJSON(response.toString());
    if (response_json['error'] == "") {
        $("#fpBtn").text("Flag (" + response_json['nFP'] + ")");
        if (response_json['new_status']) {
            $("#fpBtn").removeClass("btn-outline-danger");
            $("#fpBtn").addClass("btn-danger");
        }
        else {
            $("#fpBtn").removeClass("btn-danger");
            $("#fpBtn").addClass("btn-outline-danger");
        }
    }
    else
        alert("Error Happened:\n---------\n" + status + "\n---------------------\n" + response);
};

function InitFlagBtn(artifact_id) {
    $.post("/flag_artifact", {
        artifact_id: artifact_id,
        action: 'status'
    }, FlagBtnCallback);
}

function ToggleFlagBtn(artifact_id) {
    $.post("/flag_artifact", {
        artifact_id: artifact_id,
        action: 'toggle'
    }, FlagBtnCallback);
}





InterestingBtnCallback = function (response, status) {
    console.log("<<interestingBtnCallback>>: " + status + response.toString());
    var response_json = $.parseJSON(response.toString());
    if (response_json['error'] == "") {
        $("#interestingBtn").text("Interesting (" + response_json['total'] + ")");
        if (response_json['Interesting_new_status']) {
            $("#interestingBtn").removeClass("btn-outline-info");
            $("#interestingBtn").addClass("btn-info");
        }
        else {
            $("#interestingBtn").removeClass("btn-info");
            $("#interestingBtn").addClass("btn-outline-info");
        }

    }
    else
        alert("Error Happened:\n---------\n" + status + "\n---------------------\n" + response);
};

function InitInterestingBtn(artifact_id) {
    $.post("/note", {
        artifact_id: artifact_id,
        note: 'Interesting',
        action: 'status'
    }, InterestingBtnCallback);
}

function ToggleInterestingBtn(artifact_id) {
    $.post("/note", {
        artifact_id: artifact_id,
        note: 'Interesting',
        action: 'toggle'
    }, InterestingBtnCallback);
}