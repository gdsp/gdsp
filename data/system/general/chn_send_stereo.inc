; declick
	adclk		linen	1, 0.0001, p3, 0.1

; output gain
	a1		= a1*iamp*adclk
	a2		= a2*iamp*adclk

; send
			chnset	a1, "efx_sendL"
			chnset	a2, "efx_sendR"
