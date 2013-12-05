/* input parameters for this effect
	"kMirror" range (0.1, 0.9) map (expon float)
	input:mono output:mono
	tags:distortion, clipping, mirror
*/
; mirror
	kMakeupGain	= 1/sqrt(kMirror)			; Make up for gain loss in clipping stage
	a1		mirror	a1, -kMirror, kMirror	; mirror signal at threshold
	a1		= a1*kMakeupGain
