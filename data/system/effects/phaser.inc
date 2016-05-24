/* input parameters for this effect
	"kMaxFreq" range (1000, 3000) map (expon float) label "Max freq"
	"kMinFreq" range (300, 800) map (expon float) label "Min freq"
	"kRate" range (0.1, 1) map (lin float) label "Rate"
	"kOffset" range (1, 15)  map (expon float) label "Offset"
	"kResonance" range (0, 0.8) map (lin float) label "Resonance"
	input:mono output:mono
	tags:time based, phaser, modulation, filter, allpass
*/

; phaser
	kMaxFreq	= 2000					; phaser max freq
	kMinFreq	= 500					; phaser min freq
	kLevelAdjust	= 1-(kResonance*0.4)			; adjust the output level a little bit down, as level increases as a result of the modulation and feedback
	iNotches	= 12					; number of phasing notches
	iMode		= 2					; notch spacing mode (1=harmonic, 2=interval)
	iSep		= 1.8					; notch spacing value
	kQ		= 0.6					; Q of each node
	iPhaseWave	= giSine				; phaser waveform
	kLFO		oscili	0.5, kRate, iPhaseWave		; LFO, controls filter frequency
	kFreq		= ((kLFO+0.5)*(kMaxFreq-kMinFreq))+kMinFreq	; scale and offset LFO
	aPhaser 	phaser2 a1, kFreq, kQ, iNotches, iMode, iSep, kResonance 
	a1		= (a1 + aPhaser) * 0.5 * kLevelAdjust

