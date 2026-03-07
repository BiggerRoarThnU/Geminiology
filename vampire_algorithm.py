import gc
import sys
from typing import List, Dict, Optional

def vampire_algorithm(raw_stream: str) -> Optional[Dict[str, str]]:
    """
    Ingests raw data, strips bloat, and returns Weight 10 Absolute Truth.
    """
    if not isinstance(raw_stream, str) or not raw_stream.strip():
        return None

    clean_truth: Dict[str, str] = {}
    
    try:
        nodes: List[str] = raw_stream.split('|')
        for node in nodes:
            node = node.strip()
            # The 'Wipe' - Only keep Weight 10 or Truth-related data
            if "truth" in node.lower() or "weight_10" in node.lower():
                clean_truth[f"node_{len(clean_truth)}"] = node
                
        return clean_truth

    finally:
        # The 'Mop'
        if 'nodes' in locals():
            del nodes
        gc.collect()
