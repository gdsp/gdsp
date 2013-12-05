/* input parameters for this effect
	"kCutoff" range (150, 7000) map (log float)
	input:mono output:mono
	tags:filter, hipass
*/
; hipass
	a1		butterhp a1, kCutoff
