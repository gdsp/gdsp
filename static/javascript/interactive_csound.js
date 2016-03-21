
isPlaying = false;
userInstanceIsPlaying = false;
console.log("interactive_csound");

$(document).ready(function() {
    $('#body').show();
});

function moduleDidLoad() {
    console.log("Inside module did load");

    // Sound generation with Csound
    //csound.PlayCsd("http/effects.csd");
}

function attachListeners() {
    console.log("Attach listeners...");
    document.getElementById("playPauseButton").addEventListener("click", play);
    document.getElementById("switchInstanceButton").addEventListener("click", mute);
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
    if(userInstanceIsPlaying) {
        csound.SetChannel("targetAmplitude", 0.0);
        csound.SetChannel("userAmplitude", 1.0);
    } else {
        csound.SetChannel("targetAmplitude", 1.0);
        csound.SetChannel("userAmplitude", 0.0);
    }
    userInstanceIsPlaying = !userInstanceIsPlaying;
    console.log(userInstanceIsPlaying);
}
