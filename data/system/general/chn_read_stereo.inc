; read efx chn
	a1		chnget "efx_sendL"
	a2		chnget "efx_sendR"
	a0		= 0
			chnset a0, "efx_sendL"
			chnset a0, "efx_sendR"