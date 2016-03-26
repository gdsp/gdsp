; Master channel
instr 999

    aTargetLeft chnget "target_audio_left"
    aTargetRight chnget "target_audio_right"    
    aUserLeft chnget "user_audio_left"
    aUserRight chnget "user_audio_right"

    outs aTargetLeft + aUserLeft, aTargetRight + aUserRight

    chnclear "target_audio_left"
    chnclear "target_audio_right"
    chnclear "user_audio_left"
    chnclear "user_audio_right"
    
endin

