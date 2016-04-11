/* input parameters for this effect
	"kshift" range (-1000, 1000) map (lin float) label "Shift"
	"klowest" range (1, 1000) map (expon float) label "Lowest"
	"ikeepform" range (0, 1) map (lin int) label "Keep formants"
	input:mono output:mono
	tags:spectral, fft, shift
*/
; pvs shift (frequency shift)
	ifftsize 	= 1024
	ioverlap	= ifftsize/4
	iwinsize	= ifftsize
	iwintype 	= 0
	fsig1 		pvsanal a1, ifftsize, ioverlap, iwinsize, iwintype 
	fshift  	pvshift  fsig1,kshift, klowest, int(ikeepform), 1
	a1	  	pvsynth   fshift

