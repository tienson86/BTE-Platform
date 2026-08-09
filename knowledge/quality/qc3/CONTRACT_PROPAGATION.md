# Contract Propagation

Required handoff contracts are published by the producer pipeline and listed on the consumer.

AX-2 → AX-3: strength/season/temperature/pattern scores.  
AX-3 → AX-4: `final_useful_god`.  
AX-4 → IX-1: luck timeline signals (`major_cycles`, `annual_cycles`, `timeline_metadata`). `final_useful_god` remains an AX-3→IX-1 passthrough, not republished by AX-4.  
IX-1 → RX-1: sentence/narrative/composition identifiers.

Version pins: AX-2 `==2.0.0`; AX-3/AX-4/IX-1 `==1.0.0`.
