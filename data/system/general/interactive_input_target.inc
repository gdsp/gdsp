
; Sound generating instruments
instr 1

	; File management
	Sfile = "./local/soundfile"
	iNumChannels filenchnls Sfile

	; Get audio level
	kAmp chnget "target_amplitude"
	kInputLevel chnget "input_level"

	if iNumChannels == 1 then
		aDryL diskin2 Sfile, 1, 0, 1
		aDryR = aDryL
	elseif iNumChannels == 2 then
		aDryL, aDryR diskin2 Sfile, 1, 0, 1
	endif

	aDeclickEnv madsr 0.001, 0, 1, 0.005

	aDryL *= aDeclickEnv
	aDryR *= aDeclickEnv
	aDryL *= kAmp
	aDryR *= kAmp
	aDryL *= kInputLevel
	aDryR *= kInputLevel

	chnset aDryL, "target_audio_left"
	chnset aDryR, "target_audio_right"

endin
