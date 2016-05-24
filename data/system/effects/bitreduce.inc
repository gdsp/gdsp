/* input parameters for this effect
	"kBits" range (1, 12) map (expon int) label "Bits"
	input:mono output:mono
	tags:distortion, decimation, bit reduction
*/
; bitreduction
	kQuantize	= (powoftwo(kBits)/2)+1			; find number of discrete steps for this bit depth
	a1		= round(a1 * kQuantize)/kQuantize	; quantize audio signal (bit reduce)