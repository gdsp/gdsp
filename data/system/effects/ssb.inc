/* input parameters for this effect
	"kmodFreq" range (50, 5000) map (log float)
	"kSide" range (-1, 1) map (lin float)
	input:mono output:mono
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
	kUp		= (kSide > 0 ? 1 : 0)
	kDown		= (kUp == 0 ? 1 : 0)
	a1		= ((aDiff*kUp) + (aSum*kDown)) * 0.5
