/* input parameters for this effect
	"kDepth" range (5, 25) map (expon float) label "Depth"
	"kRate" range (0.1, 1)  map (lin float) label "Rate"
	"kOffset" range (10, 25)  map (expon float) label "Offset"
	input:mono output:stereo
	tags:time based, chorus, pitch modulation, modulation
*/

; chorus, dual voice
	kMix		= 0.5						; chorus wet/dry mix
	iChorWave	= giSine					; chorus waveform
	aDelayTime1	oscili	0.5, kRate, iChorWave, 0		; delay time oscillator (LFO)
	aDelayTime2	oscili	0.5, kRate, iChorWave, 0.25		; delay time oscillator (LFO)
	aDelayTime1	= ((aDelayTime1+0.5)*kDepth)+kOffset		; scale and offset LFO
	aDelayTime2	= ((aDelayTime2+0.5)*kDepth)+kOffset		; scale and offset LFO
	iMaxDelay	= 1
	iWindowSize	= 4
	aChorus1 	vdelayx a1, aDelayTime1*0.001, iMaxDelay, iWindowSize
	aChorus2 	vdelayx a1, aDelayTime2*0.001, iMaxDelay, iWindowSize
	a1		= ((a1*sqrt(1-kMix)) + (aChorus1*sqrt(kMix)))
	a2		= ((a1*sqrt(1-kMix)) + (aChorus2*sqrt(kMix)))
