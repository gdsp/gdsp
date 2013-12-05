/* input parameters for this effect
	"kDrive" range (1, 10) map (expon float)
	input:mono output:mono
	tags:distortion, clipping, waveshaping
*/

; tanh distortion
	kMakeupGain	= 0.5+(0.5/sqrt(kDrive))
	a1		= tanh(a1*kDrive)*kMakeupGain
