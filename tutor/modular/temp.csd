<CsoundSynthesizer>
<CsOptions>
-otest.wav -f
</CsOptions>
<CsInstruments>

	sr = 44100  
	ksmps = 1
	nchnls = 2
	0dbfs = 1

	giSine		ftgen	0, 0, 65536, 10, 1					; sine
	giTriangle	ftgen	0, 0, 65536, 7, 0, 16384, 1, 32768, -1, 16384, 0	; triangle wave
	giSquarePos	ftgen	0, 0, 1024, 7, 1, 512, 1, 0, 0, 512, 0			; square, positive only
	giSquarePosWide	ftgen	0, 0, 1024, 7, 1, 1000, 1, 0, 0, 24, 0			; square, positive only


;*****************************************************
instr	1 
;*****************************************************

	iamp 		= ampdbfs(-0) 


;****************sound generator***********************
	a1 		diskin "/home/tidemann/mysite/DSP/modular/samples/ce01_mono.wav", 1, 0, 1 
	ilen 		filelen "/home/tidemann/mysite/DSP/modular/samples/ce01_mono.wav" 
	p3 		= ilen 

;*** generate event for the effects processing instr ***
			event_i "i", 9, 0, p3+30

; declick
	adclk		linen	1, 0.0001, p3, 0.1

; output gain
	a1		= a1*iamp*adclk

; send
			chnset	a1, "efx_send"

endin

;*****************************************************
instr	9 
;*****************************************************

	iamp 		= 1 

; read efx chn
	a1		chnget "efx_send"
	a0		= 0
			chnset a0, "efx_send"

;****************effect********************************
	kSampleRate     	= 2034

; downsampling
	aSampleClock	mpulse	1, 1/kSampleRate	; new sample clock 
	a1		samphold a1, aSampleClock	; sample and hold (downsample)



;****************effect********************************
	kmodFreq     	= 484.586042429

;****************output********************************
; declick
	adclk		linen	1, 0.0001, p3, 0.0001

; output gain
	a1		= a1*iamp*adclk

; audio out
	outs		a1, a1

endin 

</CsInstruments>
<CsScore>
i 1 0 1
e
</CsScore>
</CsoundSynthesizer>