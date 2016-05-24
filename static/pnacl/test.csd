<CsoundSynthesizer>
<CsOptions>
-odac -W -d -b1024 -B2048
</CsOptions>
<CsInstruments>
sr     = 44100
ksmps  = 100
nchnls = 2
0dbfs = 1

; Sound generating instruments
instr 1

	; File management
	Sfile = "./local/soundfile"
	iNumChannels filenchnls Sfile
	iAmplitudeScaling = 1.0

	prints "NUMBER OF CHANNELS: "
	print iNumChannels

	; Get potmeter value(s)
	kAmp chnget "targetAmplitude"

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
	aDryL *= iAmplitudeScaling
	aDryR *= iAmplitudeScaling

	chnset aDryL, "target_effect_left"
	chnset aDryR, "target_effect_right"

endin

instr 2

	; File management
	Sfile = "./local/soundfile"
	iNumChannels filenchnls Sfile
	iAmplitudeScaling = 1.0

	prints "NUMBER OF CHANNELS: "
	print iNumChannels
	
	; Get potmeter value(s)
	kParam1 chnget "param1" 
	kParam2 chnget "param2"
	kAmp chnget "userAmplitude"

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
	aDryL *= iAmplitudeScaling
	aDryR *= iAmplitudeScaling	

	chnset aDryL, "reverbL"
	chnset aDryR, "reverbR"

endin

; Target effects
instr  10 

	a1 chnget "target_effect_left"
	a2 chnget "target_effect_right"

;**************** effect: reverbsc ********************************
	kfblvl     	= 0.772482674384
	kfco     	= 4905.79466643
	kmix     	= 0.807089803209
; FDN reverb
	ar1,ar2 reverbsc a1, a2, kfblvl, kfco

	a1	= (ar1*kmix) + (a1*(1-kmix))
	a2	= (ar2*kmix) + (a2*(1-kmix))

	chnmix a1, "masterL"
	chnmix a2, "masterR"
	chnclear "target_effect_left"
	chnclear "target_effect_right"

endin 

; User effects
instr 90

	aDryL chnget "reverbL"
	aDryR chnget "reverbR"
	kParam1 chnget "param1"
	kParam2 chnget "param2"
	kParam3 chnget "param3"
	kParam4 chnget "param4" ; Mix

	; Predelay
	kParam3 *= 0.001

	aDummyL delayr 2
	aDelayedL deltapi kParam3
	delayw aDryL

	aDummyR delayr 2
	aDelayedR deltapi kParam3
	delayw aDryR

	aWetL, aWetR reverbsc aDelayedL, aDelayedR, kParam1, kParam2

	chnmix aDryL * sqrt(1 - kParam4), "masterL"
	chnmix aDryR * sqrt(1 - kParam4), "masterR"
	chnmix aWetL * sqrt(kParam4), "masterL"
	chnmix aWetR * sqrt(kParam4), "masterR"
	chnclear "reverbL"
	chnclear "reverbR"

endin

; Master channel
instr 99

    aL chnget "masterL"
    aR chnget "masterR"
    outs aL, aR
    chnclear "masterL"
    chnclear "masterR"
    
endin

</CsInstruments>
<CsScore>
i10 0 	9999999
i90 0 	9999999
i99 0 	9999999
</CsScore>
</CsoundSynthesizer>
