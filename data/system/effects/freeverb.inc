/* input parameters for this effect
	"kRoomSize" range (0.3, 1) map (expon float) label "Room size"
	"kHFDamp" range (0, 1) map (lin float) label "High frequency damp"
	"kmix" range (0.3, 1.0) map (lin float) label "Mix"
	input:stereo output:stereo
	tags:reverb, delay, allpass, comb, filter
*/
; freeverb
	ar1,ar2	freeverb a1, a2, kRoomSize, kHFDamp
	ar1	dcblock2 ar1
	ar2	dcblock2 ar2
	a1	= (ar1*kmix) + (a1*(1-kmix))
	a2	= (ar2*kmix) + (a2*(1-kmix))



