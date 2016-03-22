<CsoundSynthesizer>
<CsOptions>
-odac -W -d
</CsOptions>
<CsInstruments>
sr     = 44100
ksmps  = 100
nchnls = 2
0dbfs = 1

; BUG: For some reason, there must be at least one blank line between each include statement

; Sound generating instruments
#include "target_instr.inc"			; instr 1

#include "user_instr.inc"			; instr 2

; Target effects
#include "target_effect.inc" 		; instr 10

; User effects
#include "user_effect.inc" 			; instr 90

; Master channel
#include "master_channel.inc"		; instr 99

</CsInstruments>
<CsScore>
i10 0 	9999999
i90 0 	9999999
i99 0 	9999999
</CsScore>
</CsoundSynthesizer>
