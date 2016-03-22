
var isPlaying = false;
var userInstanceIsPlaying = false;
var audioBuffer = 0;
var audioContext;

$(document).ready(function() {
    $('#body').show();
    try {
        // the AudioContext is the primary container for all audio  objects
        audioContext = new AudioContext();
    }
    catch(e) {
        alert('Web Audio API is not supported in this browser');
    }
});

function moduleDidLoad() {
    localStorage.clear();

    // Load initial csd file
    var csd_url = "/static/pnacl/test.csd";
    var csd_name = "test.csd";
    csound.CopyUrlToLocal(csd_url, csd_name);

    // Load initial audio file
    loadAudio("/static/samples/keys.WAV");

    // Start csound
    csound.PlayCsd("local/test.csd");

    // Set levels to hear only the target sound
    csound.SetChannel("targetAmplitude", 1.0);
    csound.SetChannel("userAmplitude", 0.0);

    // Initialize parameters
    csound.SetChannel("param1", 0.5);
    csound.SetChannel("param2", 5000);
    csound.SetChannel("param3", 10);
    csound.SetChannel("param4", 0.5);
}

function attachListeners() {
    console.log("Attach listeners...");
    document.getElementById("playPauseButton").addEventListener("click", play);
    document.getElementById("switchInstanceButton").addEventListener("click", mute);
}

function handleMessage(message) {
    var mess = message.data;
    if(mess == "finished render"){
        ReadFile();
        return;
    } else if(mess == "Complete"){
    //saveFile();
    //scrollTo(0, messField.scrollHeight);
    return;
}
    var messField = document.getElementById("csound_message")
    if(messField) {
        messField.innerText += mess;
        scrollTo(0, messField.scrollHeight);
    }
}

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
    if(!userInstanceIsPlaying) {
        csound.SetChannel("targetAmplitude", 0.0);
        csound.SetChannel("userAmplitude", 1.0);
    } else {
        csound.SetChannel("targetAmplitude", 1.0);
        csound.SetChannel("userAmplitude", 0.0);
    }
    userInstanceIsPlaying = !userInstanceIsPlaying;
    console.log(userInstanceIsPlaying);
}

function loadAudio(url) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    // When loaded decode the data and store the audio buffer in memory
    request.onload = function() {
        audioContext.decodeAudioData(request.response, function(buffer) {
            audioBuffer = buffer;

            // Creating a blob to store binary audio data
            blob = new Blob([request.response], {type: "audio/wav"});
            var objectURL = window.URL.createObjectURL(blob);
            csound.CopyUrlToLocal(objectURL, "soundfile");
        }, onError);
    }
    request.send();
}

function onError(e) {
    console.log(e);
}
