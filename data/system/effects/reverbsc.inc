/* input parameters for this effect
	"kfblvl" range (0.6, 0.99) map (expon float)
	"kfco" range (1000, 12000) map (lin float)
	"kmix" range (0.3, 1.0) map (lin float)
	input:stereo output:stereo
	tags:reverb, delay, FDN, delay network, pitch modulation
*/
; FDN reverb
	ar1,ar2 reverbsc a1, a2, kfblvl, kfco
	a1	= (ar1*kmix) + (a1*(1-kmix))
	a2	= (ar2*kmix) + (a2*(1-kmix))
