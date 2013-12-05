/* input parameters for this effect
	"kCutoff" range (50, 5000) map (log float)
	"kBW" range (0.2, 1) map (lin float)
	input:mono output:mono
	tags:filter, band reject
*/
; bandreject
	a1		butterbr a1, kCutoff, kBW*kCutoff
