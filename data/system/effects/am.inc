/* input parameters for this effect
	"kmodFreq" range (50, 5000) map (log float) label "Modulation frequency"
	input:mono output:mono
	tags:modulation,amplitude modulation
*/

; amplitude modulation
	aMod		oscili	0.5, kmodFreq, giSine
	aMod		= aMod + 0.5
	a1		= a1 * aMod


