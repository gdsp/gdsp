/* input parameters for this effect
	"kDepth" range (1, 15) map (expon float) label "Depth"
	"kRate" range (0.1, 1) map (lin float) label "Rate"
	"kOffset" range (1, 15)  map (expon float) label "Offset"
	"kFeed" range (0, 0.9) map (lin float) label "Feedback"
	input:mono output:mono
	tags:time based, flanger, pitch modulation, modulation, filter
*/

; flanger
	kLevelAdjust	= 1-(kFeed*0.4)				; adjust the output level a little bit down, as level increases as a result of the modulation and feedback
	iFlangWave	= giSine				; flanger waveform
	aDelayTime	oscili	0.5, kRate, iFlangWave		; delay time oscillator (LFO)
	aDelayTime	= ((aDelayTime+0.5)*kDepth)+kOffset	; scale and offset LFO
	iMaxDelay	= 0.1
	iWindowSize	= 4
	aFeed		init 0
	aFlanger 	vdelayx a1+aFeed, aDelayTime*0.001, iMaxDelay, iWindowSize
	aFeed		= aFlanger*kFeed
	a1		= (a1 + aFlanger) * 0.5 * kLevelAdjust
