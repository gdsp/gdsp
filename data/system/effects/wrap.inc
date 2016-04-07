/* input parameters for this effect
	"kWrap" range (0.1, 0.9) map (expon float) label "Wrap"
	input:mono output:mono
	tags:distortion, clipping
*/
; wrap
	kMakeupGain	= 1/sqrt(kWrap)			; Make up for gain loss in clipping stage
	a1		wrap	a1, -kWrap, kWrap	; wrap signal at threshold
	a1		= a1*kMakeupGain
