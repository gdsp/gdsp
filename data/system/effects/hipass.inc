/* input parameters for this effect
	"kCutoff" range (150, 7000) map (expon float) label "Cutoff frequency"
	input:mono output:mono
	tags:filter, hipass
*/
; hipass
	a1		butterhp a1, kCutoff
