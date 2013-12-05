/* input parameters for this effect
	input:mono output:stereo
	"kmix" range (0.3, 1.0) map (lin float)
	tags:reverb, delay, allpass, comb, filter
*/

;----------------------------------------------------------------------------------
; Medium Room Reverb (copied from gardverb.orc)
;----------------------------------------------------------------------------------

adel71 init     0
adel11 init     0
adel12 init     0
adel13 init     0
adel31 init     0
adel61 init     0
adel62 init     0

; Initialize
aflt01 butterlp a1, 6000              	; Pre-Filter (audio input here)
aflt02 butterbp .4*adel71, 1000, 500     ; Feed-Back Filter
asum01  =       aflt01+.5*aflt02         ; Initial Mix

; Double Nested All-Pass
asum11  =       adel12-.35*adel11        ; First  Inner Feedforward
asum12  =       adel13-.45*asum11        ; Second Inner Feedforward
aout11  =       asum12-.25*asum01        ; Outer Feedforward
adel11  delay   asum01+.25*aout11, .0047 ; Outer Feedback
adel12  delay   adel11+.35*asum11, .0083 ; First  Inner Feedback
adel13  delay   asum11+.45*asum12, .022  ; Second Inner Feedback

adel21  delay   aout11, .005             ; Delay 1

; All-Pass 1
asub31  =       adel31-.45*adel21        ; Feedforward
adel31  delay   adel21+.45*asub31,.030   ; Feedback

adel41  delay   asub31, .067             ; Delay 2
adel51  delay   .4*adel41, .015          ; Delay 3
aout51  =       aflt01+adel41

; Single Nested All-Pass
asum61  =       adel62-.35*adel61        ; Inner Feedforward
aout61  =       asum61-.25*aout51        ; Outer Feedforward
adel61  delay   aout51+.25*aout61, .0292 ; Outer Feedback
adel62  delay   adel61+.35*asum61, .0098 ; Inner Feedback

aout    =       .5*aout11+.5*adel41+.5*aout61 ; Combine Outputs

adel71  delay   aout61, .108                  ; Delay 4

aout	dcblock2	aout


	a1	= (aout*kmix) + (a1*(1-kmix))
	a2	= (-aout*kmix) + (a1*(1-kmix))
