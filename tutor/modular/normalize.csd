<CsoundSynthesizer>
<CsOptions>
-n
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 10
nchnls = 2
0dbfs = 1

; **************************************************
; normalize soundfile and cut any silence at the end
; **************************************************

instr 1
	ipeak 		filepeak "test.wav"
	print ipeak
	a1,a2 		diskin "test.wav", 1, 0, 0 
	ilen 		filelen "test.wav" 
	if ipeak < 1 then
	inorm		= (((0.95/ipeak)-1)*0.5)+1 	; just boost a little bit (halfway to unity) if the input is less then maximal
	else
	inorm		= 0.95/ipeak 			; conventional normalize for overshoot
	endif
	krms		rms	a1+a2
			fout	"test_normalized.wav", 14, a1*inorm, a2*inorm
			outs a1*inorm, a2*inorm
	if krms < 0.0001 then
		timout 0, 1, end	; don't turn off if the sound comes on again within one second
	endif
	if krms < 0.0001 then
		turnoff2 p1, 0, 0.1
	endif
	end:
endin

</CsInstruments>
<CsScore>
f0 99
i 1 0 -1
e

</CsScore>
</CsoundSynthesizer>

