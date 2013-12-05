/* input parameters for this effect
	"kscale" range (0.25, 4) map (expon float)
	"ikeepform" range (0, 1) map (lin int)
	input:mono output:mono
	tags:spectral, fft, scale, pitch 
*/
; pvs scale (pitch shift)
	ifftsize 	= 1024
	ioverlap	= ifftsize/4
	iwinsize	= ifftsize
	iwintype 	= 0
	fsig1 		pvsanal a1, ifftsize, ioverlap, iwinsize, iwintype 
	fshift  	pvscale  fsig1,kscale, int(ikeepform), 1
	a1	  	pvsynth   fshift
