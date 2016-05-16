
var isPlaying = false;
var userInstanceIsPlaying = false;
var audioBuffer = 0;
var audioContext;
var wavesurfer = Object.create(WaveSurfer);

$(document).ready(function() {
    $('#body').show();
    try {
        // the AudioContext is the primary container for all audio objects
        audioContext = new AudioContext();
    } catch(e) {
        alert('Web Audio API is not supported in this browser');
    }
});

$(window).load(function(){
    console.log("window loaded!!!");
});

$(document).load(function(){
    console.log("document loaded!!!");
});

function attachListeners() {
    document.getElementById("playPauseButton").addEventListener("click", play);
    document.getElementById("switchInstanceButton").addEventListener("click", mute);

    // Trick waveform to return to beginning when reaching the end
    wavesurfer.on('finish', function() {
        wavesurfer.play();
    });
}

function handleMessage(message) {
    var mess = message.data;
    
    if(mess == "finished render") {
        ReadFile();
        return;
    } else if(mess == "Complete") {
        return;
    }
    var messField = document.getElementById("csound_message")
    if(messField) {
        messField.innerText += mess;
    }
}

function play() {
    if (isPlaying) {
        csound.Event("i-1 0 -1");
        csound.Event("i-2 0 -1");
        wavesurfer.stop();
        document.getElementById("playPauseButton").src = "/static/images/play_colored.png";
    } else {
        csound.Event("i1 0 -1");
        csound.Event("i2 0 -1");
        wavesurfer.play();
        document.getElementById("playPauseButton").src = "/static/images/pause_colored.png";
    }
    isPlaying = !isPlaying
}

function stop() {
    csound.Event("i-1 0 -1");
    csound.Event("i-2 0 -1");
    wavesurfer.stop();
}

function loadAudio(url) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    
    // When loaded, decode the data and store the audio buffer in memory
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

/*
* Use different scaling functions for the HTML input slider.
*/
function getValueFromCurve(inputValue, minValue, maxValue, curveType) {
    var minValueLog = Math.log(minValue);
    var maxValueLog = Math.log(maxValue);

    // Calculate adjustment factor
    var scale = (maxValueLog - minValueLog)/(maxValue - minValue);

    if (curveType === "lin") {
        return inputValue;
    } else if (curveType === "expon") {
        return Math.exp(minValueLog + scale*(inputValue - minValue));
    } else if (curveType === "log") {
        return (Math.log(inputValue) - minValueLog)/scale + minValue;
    } else if (curveType === "log_1p5") {
        // Not currently in use
    }

    return inputValue;
}

function getValueFromCurveInverse(inputValue, minValue, maxValue, curveType) {
    var minValueLog = Math.log(minValue);
    var maxValueLog = Math.log(maxValue);

    // Calculate adjustment factor
    var scale = (maxValueLog - minValueLog)/(maxValue - minValue);

    if (curveType === "lin") {
        return inputValue;
    } else if (curveType === "expon") {
        return (Math.log(inputValue) - minValueLog)/scale + minValue;
    } else if (curveType === "log") {
        return Math.exp(minValueLog + scale*(inputValue - minValue));
    } else if (curveType === "log_1p5") {
        // Not currently in use
    }

    return inputValue;
}

function getLabelValue(inputValue) {
    labelValue = parseFloat(inputValue.toString()).toFixed(2);

    if (labelValue.toString().length >= 8) {
        labelValue = parseFloat(labelValue.toString()).toFixed(0);
    } else if (labelValue.toString().length == 7) {
        labelValue = parseFloat(labelValue.toString()).toFixed(1);
    }

    return labelValue;
}

function blendColors(a, b, alpha) {
    var aa = [
        parseInt('0x' + a.substring(1, 3)), 
        parseInt('0x' + a.substring(3, 5)), 
        parseInt('0x' + a.substring(5, 7))
        ];

    var bb = [
        parseInt('0x' + b.substring(1, 3)), 
        parseInt('0x' + b.substring(3, 5)), 
        parseInt('0x' + b.substring(5, 7))
        ];

    r = '0' + Math.round(aa[0] + (bb[0] - aa[0])*alpha).toString(16);
    g = '0' + Math.round(aa[1] + (bb[1] - aa[1])*alpha).toString(16);
    b = '0' + Math.round(aa[2] + (bb[2] - aa[2])*alpha).toString(16);

    return '#'
          + r.substring(r.length - 2)
          + g.substring(g.length - 2)
          + b.substring(b.length - 2);
}

function fadeBetweenColors(colorFrom, colorTo, element) {
    var t = [];
    var steps = 100;
    var delay = 3000;
    for (var i = 0; i < steps; i++) {
        (function(j) {
            t[j] = setTimeout(function() {
            var alpha  = j / steps;
            var color = blendColors(colorFrom, colorTo, alpha);
            element.style.color = color;
        }, j * delay / steps);
        })(i);
    }
    return t;
}

function stopColorFade(t) {
     for (i in t) {
        clearTimeout(t[i]);
     }
}
