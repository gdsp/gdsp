/* input parameters for this effect
	"kRevTime" range (0.6, 8.0) map (expon float) label "Time"
	"kHFDamp" range (0, 1) map (lin float) label "High frequency damp"
	"kmix" range (0.1, 1.0) map (lin float) label "Mix"
	input:stereo output:stereo
	tags:reverb, delay, allpass, comb, filter
*/

; freeverb room size converter
	giRevbSize	ftgen	0, 0, 8192, 27, \
						0, 	0,	\
						600,	0.0,	\
						700, 	0.1,	\
						800,	0.3,	\
						1000,	0.5,	\
						1200,	0.6,	\
						1500,	0.7,	\
						1800,	0.75,	\
						2000,	0.8,	\
						2300,	0.825,	\
						2400,	0.85,	\
						2900,	0.875,	\
						3600,	0.9,	\
						3800,	0.925,	\
						4600,	0.95,	\
						6000,	0.975,	\
						7000,	0.99,	\
						8000,	0.999,	\
						8192,	0.999

; freeverb
	kRevTime	limit kRevTime, 0.6, 8.0
	kRoomSize	table kRevTime*1000, giRevbSize
	inLevel	= 2					; empirically adjusted for natural balance between dry and reverb levels
	koutLevel	= ampdbfs(-kRevTime*0.6)	; slightly lower output for longer reverb (as the reverb algorithm will naturally be louder with more feedback)

	aoutL, aoutR freeverb a1*inLevel, a2*inLevel, kRoomSize, kHFDamp	
	aoutL	dcblock aoutL*koutLevel
	aoutR	dcblock aoutR*koutLevel
	a1	= (aoutL*kmix) + (a1*(1-kmix))
	a2	= (aoutR*kmix) + (a2*(1-kmix))

