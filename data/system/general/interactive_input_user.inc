
instr 2

; File management
Sfile = "./local/soundfile"
iNumChannels filenchnls Sfile

; Get audio level
kAmp chnget "user_amplitude"
kInputLevel chnget "input_level"

; Check if input file is mono or stereo
if iNumChannels == 1 then
	aDryL diskin2 Sfile, 1, 0, 1
	aDryR = aDryL
elseif iNumChannels == 2 then
	aDryL, aDryR diskin2 Sfile, 1, 0, 1
endif

; Add declick envelope when switching between A and B
aDeclickEnv madsr 0.01, 0, 1, 0.05

aDryL = aDryL * aDeclickEnv * kAmp * kInputLevel
aDryR = aDryR * aDeclickEnv * kAmp * kInputLevel

chnset aDryL, "user_audio_left"
chnset aDryR, "user_audio_right"

endin
