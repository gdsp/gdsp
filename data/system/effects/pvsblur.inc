/* input parameters for this effect
	"kblurTime" range (0.2, 2) map (expon float)
	input:mono output:mono
	tags:spectral, fft, blur
*/
; pvs blur
	ifftsize 	= 1024
	ioverlap	= ifftsize/4
	iwinsize	= ifftsize
	iwintype 	= 0
	fsig1 		pvsanal a1, ifftsize, ioverlap, iwinsize, iwintype 
	iMax		= 4.1
	fblur		pvsblur fsig1, kblurTime, iMax
	a1	  	pvsynth   fblur
	a1		= a1 * (1+(kblurTime*0.1))	; amp compensate
