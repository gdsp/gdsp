/* input parameters for this effect
	"kSampleRate" range (1000, 15000) map(log int)
	input:mono output:mono
	tags:distortion, decimation, downsampling
*/

; downsampling
	aSampleClock	mpulse	1, 1/kSampleRate	; new sample clock 
	a1		samphold a1, aSampleClock	; sample and hold (downsample)

