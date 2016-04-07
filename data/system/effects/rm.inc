/* input parameters for this effect
	"kmodFreq" range (50, 5000) map (log float) label "Modulation freq"
	input:mono output:mono
	tags:modulation,amplitude modulation
*/

; ring modulation
	aMod		oscili	1, kmodFreq, giSine
	a1		= a1 * aMod


