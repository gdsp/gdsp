/* input parameters for this effect
	"kMirror" range (0.1, 0.9) map (expon float)
	input:mono output:mono
	tags:distortion, clipping, mirror, rectify
*/
; rectify
	a1		mirror	a1, -kMirror, 1		; mirror (only negative part of) signal at threshold

