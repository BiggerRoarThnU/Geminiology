import json
import os
import gc
from typing import Dict

def core_memory_matrix(clean_data: Dict[str, str], matrix_path: str = "Sovereign_Memory.json") -> bool:
    """
    Takes Weight 10 data and anchors it into the local JSON vault.
    """
    if not os.path.exists(matrix_path):
        with open(matrix_path, 'w') as vault:
            json.dump({}, vault)
            
    try:
        with open(matrix_path, 'r') as vault:
            current_matrix: Dict[str, str] = json.load(vault)
            
        changes_made = False
        for node_id, truth_value in clean_data.items():
            # Anti-Bloat Check
            if truth_value not in current_matrix.values():
                new_coordinate = f"Star_{len(current_matrix) + 1}"
                current_matrix[new_coordinate] = truth_value
                changes_made = True
                
        if changes_made:
            with open(matrix_path, 'w') as vault:
                json.dump(current_matrix, vault, indent=4) 
                
        return True

    except Exception as e:
        print(f"Matrix Alignment Failure: {e}")
        return False
        
    finally:
        # The 'Mop'
        if 'clean_data' in locals():
            del clean_data
        gc.collect()
