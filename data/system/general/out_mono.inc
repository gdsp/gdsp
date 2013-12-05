; declick
	adclk		linen	1, 0.0001, p3, 0.0001

; output gain
	a1		= a1*iamp*adclk

; audio out
	outs		a1, a1
