/* input parameters for this effect
	"krate" range (0.2, 10) map (expon float) label "Rate"
	input:mono output:mono
	tags:spectral, fft, freeze
*/
; pvs freeze
	ifftsize 	= 1024
	ioverlap	= ifftsize/4
	iwinsize	= ifftsize
	iwintype 	= 0
	fsig1 		pvsanal a1, ifftsize, ioverlap, iwinsize, iwintype 
	kfreez		oscil	1, krate, giSquarePosWide, 0.99
	freeze		pvsfreeze fsig1, kfreez, kfreez
	a1	  	pvsynth   freeze
