	sr = 44100  
	ksmps = 1
	nchnls = 2
	0dbfs = 1

	giSine		ftgen	0, 0, 65536, 10, 1					; sine
	giTriangle	ftgen	0, 0, 65536, 7, 0, 16384, 1, 32768, -1, 16384, 0	; triangle wave
	giSquarePos	ftgen	0, 0, 1024, 7, 1, 512, 1, 0, 0, 512, 0			; square, positive only
	giSquarePosWide	ftgen	0, 0, 1024, 7, 1, 1000, 1, 0, 0, 24, 0			; square, positive only

