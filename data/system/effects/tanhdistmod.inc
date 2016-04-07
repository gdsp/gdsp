/* input parameters for this effect
	"kDrive" range (1, 10) map (expon float) label "Drive"
	"kShape1" range (0, 1) map (lin float) label "Shape 1"
	"kShape2" range (0, 1) map (lin float) label "Shape 2"
	input:mono output:mono
	tags:distortion, clipping, waveshaping, tube amp
*/

; modified tanh distortion
	acomp	= a1
	kpostG	= (0.2+(0.8/sqrt(kDrive)))*(1-(sqrt(kShape1))*0.3)
	a1 	= (exp(a1 * (kShape1 + kDrive)) - exp(a1 * (kShape2 - kDrive))) / (exp(a1 * kDrive) + exp(-a1 * kDrive))
	a1	= a1 * kpostG
