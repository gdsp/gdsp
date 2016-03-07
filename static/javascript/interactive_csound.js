
isPlaying = false;

$(document).ready(function() {
    $('#body').show();
});

function moduleDidLoad() {
    // Sound generation with Csound
    //csound.PlayCsd("http/effects.csd");
}

function attachListeners() {
    document.getElementById("playPauseButton").addEventListener("click", play);
}

// function handleMessage(message) {
//     var mess = message.data;
//     if(mess == "finished render"){
//         ReadFile();
//         return;
//     } else if(mess == "Complete"){
//     //saveFile();
//     //scrollTo(0, messField.scrollHeight);
//     return;
// }
//     var messField = document.getElementById("csound_message")
//     if(messField) {
//         messField.innerText += mess;
//         scrollTo(0, messField.scrollHeight);
//     }
// }

function play() {
    if (isPlaying) {
        csound.Event("i-1 0 -1");
        csound.Event("i-2 0 -1");
        document.getElementById("playPauseButton").src = "/static/images/play.png";
    } else {
        csound.Event("i1 0 -1");
        csound.Event("i2 0 -1");
        document.getElementById("playPauseButton").src = "/static/images/pause.png";
    }
    isPlaying = !isPlaying
}

function mute() {
}
