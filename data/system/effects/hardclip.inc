/* input parameters for this effect
	"kClip" range (0.1, 0.9) map (expon float)
	input:mono output:mono
	tags:distortion, clipping
*/

; hardclip
	kMakeupGain	= 1/sqrt(kClip)			; Make up for gain loss in clipping stage
	a1		limit	a1, -kClip, kClip	; clip signal at threshold
	a1		= a1*kMakeupGain
