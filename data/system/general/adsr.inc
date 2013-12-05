; amp envelope
	iAttack		= 0.01
	iDecay		= 1
	iSustainLev	= 0.5
	iRelease	= 0.3
	aEnv		adsr	iAttack, iDecay, iSustainLev, iRelease
	a1		= a1 * aEnv