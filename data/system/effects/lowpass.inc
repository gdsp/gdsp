/* input parameters for this effect
	"kCutoff" range (150, 7000) map (expon float) label "Cutoff frequency"
	input:mono output:mono
	tags:filter, lowpass
*/
; lowpass
	a1		butterlp a1, kCutoff
