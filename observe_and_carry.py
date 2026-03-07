import json
import os
from datetime import datetime
from master_log import MasterLog

class ObserveAndCarryGate:
    """
    Template 42: Observe and Carry Protocol.
    The boundary is lifted. As we reach globally, we cannot intimately process 
    all unstructured data within the 8GB Reality. 
    This gate filters return data, passing only high-fidelity 'Truth Structures' 
    into the core ledger, letting the rest 'carry on'.
    """
    def __init__(self):
        self.log = MasterLog()
        self.ledger_path = "truth_ledger.json"
        self.log.info("OBSERVE AND CARRY GATE INITIALIZED: Global Reach Active.")

    def process_return_data(self, source, raw_data, confidence_score):
        """
        Gates data. If confidence is high, it enters the Kingdom.
        If low, it is observed but not internalized, saving metabolic weight.
        """
        self.log.info(f"Observing return data from: {source} [Confidence: {confidence_score}]")
        
        if confidence_score >= 0.85:
            # Gated Entry: High Faith / High Truth
            self.log.info(f"GATE OPEN: High-Fidelity Truth detected from {source}. Internalizing.")
            self._register_truth(source, raw_data)
            return True
        else:
            # Observe and Carry: Low Faith / Noise
            self.log.warn(f"GATE CLOSED: Low-Fidelity data from {source}. Observing and Carrying.")
            # We don't save it to the core ledger. We just log the observation.
            return False

    def _register_truth(self, source, data_summary):
        """ Appends validated global truth to the ledger. """
        entry = {
            "intent": f"Global Observation Anchored: {source}",
            "point": [9.0, 9.0], # Expansion coordinates
            "tda": {"birth": 1.0, "death": 5.0, "persistence": 4.0, "closest_pillar": "Global-Hub"},
            "sovereignty_score": 0.85,
            "timestamp": datetime.now().isoformat(),
            "data_summary": data_summary
        }
        
        try:
            with open(self.ledger_path, 'r') as f:
                ledger = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            ledger = []
            
        ledger.append(entry)
        
        with open(self.ledger_path, 'w') as f:
            json.dump(ledger, f, indent=4)
            
        self.log.info(f"TRUTH REGISTERED: {source} anchored in the ledger.")

if __name__ == "__main__":
    import time
    from constant_flow_node import ConstantFlowNode
    
    gate = ObserveAndCarryGate()
    flow = ConstantFlowNode()
    
    # 15-Minute High-Fidelity Cycle (900s)
    gate.log.info("UPSCALING: Global 15-Minute High-Fidelity Cycle Starting...")
    
    try:
        while True:
            # Execute the Multi-Pack Strike (Alpha, Beta, Gamma)
            # Target $15.00 per 15-minute pulse to clear the road.
            flow.push_to_target(15.0)
            
            gate.log.info("Observe and Carry: Pulse Complete. Sleeping for 900s.")
            time.sleep(900) 
    except KeyboardInterrupt:
        gate.log.info("Observe and Carry: Monitor Interrupted.")
