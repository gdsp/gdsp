<CsoundSynthesizer>
<CsOptions>
-odac -W -d
</CsOptions>
<CsInstruments>
sr     = 44100
ksmps  = 100
nchnls = 2
0dbfs = 1

instr 1

; File management
Sfile = "./local/soundfile"
iNumChannels filenchnls Sfile

prints "NUMBER OF CHANNELS: "
print iNumChannels

if iNumChannels == 1 then
	aDryL diskin2 Sfile, 1, 0, 1
	aDryR = aDryL
elseif iNumChannels == 2 then
	aDryL, aDryR diskin2 Sfile, 1, 0, 1
endif

outs aDryL, aDryR

endin

</CsInstruments>
<CsScore>
;i1 0 	10
</CsScore>
</CsoundSynthesizer>
