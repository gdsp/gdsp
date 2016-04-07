/* input parameters for this effect
	"kmodFreq" range (50, 5000) map (log float) label "Modulation freq"
	input:mono output:stereo
	tags:modulation,amplitude modulation, single sideband
*/

; single sideband modulation
	aSin, aCos	hilbert	a1	
	aModSin		oscili	1, kmodFreq, giSine, 0.0
	aModCos		oscili	1, kmodFreq, giSine, 0.25
	aMod1		= aSin * aModCos
	aMod2		= aCos * aModSin
	aSum		= aMod1 + aMod2
	aDiff		= aMod1 - aMod2
	a1		= aDiff
	a2		= aSum
