/* input parameters for this effect
	"kPan" range (0.0, 1.0) map (lin float)
	input:mono output:stereo
	tags:pan
*/

; (square root) equal power panning
	a2		= a1 * sqrt(kPan)
	a1		= a1 * sqrt(1-kPan)

