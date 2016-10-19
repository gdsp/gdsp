/* input parameters for this effect
	"kClip" range (0.1, 0.9) map (expon float) label "Clip"
	"kType" range (0, 2) map (lin int) label "Effect type"
	input:mono output:mono
	tags:distortion, clipping
*/

; softclip

	kType		= int(kType)			;  Saturation (soft clip) type: 0=Bram de Jong, 1=sine, 2=tanh
	ipi		= 3.14159265358979323846264338	; The pi constant

	aClip		limit	a1, -kClip, kClip	; hard clipping part
	aRest		= a1-aClip			; the rest (hard clipped part) of the signal, this is the signal we will soft clip

	aBramClip	= aRest/(1+(aRest/(1-kClip))^2)	; Bram de Jong soft clipping
	aSinClip	= sin(aRest*ipi*0.5)*kClip	; sin based soft clipping
	aTanhClip	= tanh(aRest/kClip)*kClip	; tanh based soft clipping

	kBram		= (kType == 0 ? 1 : 0)
	kSin		= (kType == 1 ? 1 : 0)
	kTan		= (kType == 2 ? 1 : 0)
	aSoft		= (aBramClip*kBram)+(aSinClip*kSin)+(aTanhClip*kTan)
	a1		= (aClip+aSoft)
