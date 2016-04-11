/* input parameters for this effect
	"kmodFreq" range (0.4, 7) map (log float) label "Modulation frequency"
	"kFeed" range (0.1, 0.47) map (lin float) label "Feedback"
	input:mono output:stereo
	tags:modulation,amplitude modulation, single sideband, phaser
*/

; barberpole phaser, using single sideband modulation
	aFeed		init 0
	aSin, aCos	hilbert	a1 + aFeed	
	aModSin		oscili	1, kmodFreq, giSine, 0.0
	aModCos		oscili	1, kmodFreq, giSine, 0.25
	aMod1		= aSin * aModCos
	aMod2		= aCos * aModSin
	aSum		= aMod1 + aMod2
	aDiff		= aMod1 - aMod2
	aFeed 		= (aSum+aDiff)*kFeed
	kcomp		= (1-(kFeed*kFeed)*3)+0.1		; gain adjust in relation to feedback amount
	a2		= (aDiff)*kcomp
	a1		= (aSum)*kcomp

