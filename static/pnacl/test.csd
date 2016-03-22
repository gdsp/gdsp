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

aOut 	oscili 0.2, 220

outs aOut, aOut

endin

</CsInstruments>
<CsScore>
;i1 0 	10
</CsScore>
</CsoundSynthesizer>
