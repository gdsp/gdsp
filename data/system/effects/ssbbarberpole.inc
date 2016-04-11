/* input parameters for this effect
	"kmodFreq" range (0.4, 7) map (log float) label "Modulation frequency"
	"kFeed" range (0.3, 0.7) map (lin float) label "Feedback"
	"kSide" range (-1, 1) map (lin float) label "Side"
	input:mono output:mono
*/

; barbarpole phaser, using single sideband modulation
	aFeed		init 0
	aSin, aCos	hilbert	a1	
	aModSin		oscili	1, kmodFreq, giSine, 0.0
	aModCos		oscili	1, kmodFreq, giSine, 0.25
	aMod1		= aSin * aModCos
	aMod2		= aCos * aModSin
	aSum		= aMod1 + aMod2
	aDiff		= aMod1 - aMod2
	kUp		= 1;(kSide > 0 ? 1 : 0)
	kDown		= 1;(kUp == 0 ? 1 : 0)
	aFeed		= ((aDiff*kUp) + (aSum*kDown))*kFeed
	kcomp		= (1-(kFeed*0.75))+0.25		; gain adjust in relation to feedback amount
	a1		= ((aDiff*kUp) + (aSum*kDown))*kcomp

