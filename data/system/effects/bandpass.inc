/* input parameters for this effect
	"kCutoff" range (50, 5000) map (log float)
	"kBW" range (0.01, 1) map (lin float)
	input:mono output:mono
	tags:filter, bandpass
*/
; bandpass
	a1		butterbp a1, kCutoff, kBW*kCutoff
