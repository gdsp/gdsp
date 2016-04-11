/* input parameters for this effect
	"kDrive" range (0.01, 10) map (expon float) label "Drive"
	"kSlope" range (0, 0.1) map (lin float) label "Slope"
	"kDuty" range (0, 0.02) map (lin float) label "Duty"
	"kCutoff" range (1000, 9000) map (expon float) label "Cutoff frequency"
	input:mono output:mono
	tags:distortion, delay, slope
*/

; slope based delay distortion
	an1		delay1	a1		; delay audio by 1 sample
	aslope		= a1 - an1		; find difference between samples (= slope of the waveform)

	kDrive		= kDrive/100		; we want drive to have a range comparable to other distortion "drive" parameters
	kslope		= kSlope * kDrive
	kduty		= kDuty * kDrive

	atemp    	delayr  0.1                          
	aout   		deltapi 0.004 + ((2-a1)*kduty) + (aslope * kslope)	; Slope&Duty controlled delay time
			delayw  	a1

	a1		butterlp aout, kCutoff
