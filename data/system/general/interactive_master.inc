; Master channel
instr 99

    aL chnget "masterL"
    aR chnget "masterR"
    outs aL, aR
    chnclear "masterL"
    chnclear "masterR"
    
endin
