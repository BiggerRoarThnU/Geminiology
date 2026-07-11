#!/usr/bin/env python3
import inspect
import json
import time
import sqlite3
import hashlib
import hmac
from typing import Callable, Dict, Any

def to_jsonable(val: Any) -> Any:
    """
    Recursively converts arbitrary Python objects (including custom classes)
    into pure JSON-safe primitives (dicts, lists, strings, etc.)
    """
    if isinstance(val, dict):
        return {k: to_jsonable(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple, set)):
        return [to_jsonable(v) for v in val]
    elif hasattr(val, '__dict__'):
        return {k: to_jsonable(v) for k, v in val.__dict__.items() if not k.startswith('_')}
    elif hasattr(val, '_asdict'):  # namedtuple
        return {k: to_jsonable(v) for k, v in val._asdict().items()}
    else:
        try:
            json.dumps(val)
            return val
        except (TypeError, ValueError):
            return str(val)

# ==============================================================================
# SOVEREIGN NEXUS: THE VAMPIRE ENGINE (V2.3 - IDENTITY & PERSISTENCE)
# CORE MANDATE: Wipe, Mop, and Cryptographically Anchor Data
# PERC: Scratch in the ring - Symmetrical Line Verified
# ==============================================================================

# Simulated Secure Enclave Key (Offline Identity Signature)
# Represents the Fetch.ai 'agent1' prefix verifiable credential
AGENT_IDENTITY_KEY = b"agent1q_sovereign_nexus_offline_key_001"

class CryptoCheckpointer:
    def __init__(self, db_path="nexus_checkpoints.db"):
        """
        LANGGRAPH EXTRACTION: Initializes the SQLite-backed dual-table checkpointer.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._initialize_ledger()

    def _initialize_ledger(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                task_name TEXT,
                payload TEXT,
                result TEXT,
                prev_hash TEXT,
                current_hash TEXT,
                signature TEXT
            )
        ''')
        self.conn.commit()

    def _get_last_hash(self) -> str:
        """Retrieves the hash of the last state to create the Merkle-linked chain."""
        self.cursor.execute('SELECT current_hash FROM checkpoints ORDER BY id DESC LIMIT 1')
        row = self.cursor.fetchone()
        return row[0] if row else "0000000000000000000000000000000000000000000000000000000000000000" # Genesis hash

    def sign_and_store(self, task_name: str, payload: dict, result: Any):
        """
        FETCH.AI EXTRACTION: Cryptographically signs the payload and writes to the DB.
        If a single character in the history is altered, the entire chain breaks.
        """
        timestamp = time.time()
        prev_hash = self._get_last_hash()
        
        # Ensure payload and result are fully JSON serializable
        safe_payload = to_jsonable(payload)
        safe_result = to_jsonable(result)

        # Serialize data deterministically
        data_string = json.dumps({
            "timestamp": timestamp,
            "task": task_name,
            "payload": safe_payload,
            "result": safe_result,
            "prev_hash": prev_hash
        }, sort_keys=True)

        # Generate SHA-256 Hash
        current_hash = hashlib.sha256(data_string.encode('utf-8')).hexdigest()

        # Generate Offline Signature (Simulated ECDSA/Bech32 identity proof)
        signature = hmac.new(AGENT_IDENTITY_KEY, current_hash.encode('utf-8'), hashlib.sha256).hexdigest()

        self.cursor.execute('''
            INSERT INTO checkpoints (timestamp, task_name, payload, result, prev_hash, current_hash, signature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, task_name, json.dumps(safe_payload), json.dumps(safe_result), prev_hash, current_hash, signature))
        self.conn.commit()
        
        return current_hash, signature

class VampireEngine:
    def __init__(self, ram_limit_gb: float = 6.4, max_tokens: int = 8192):
        self.max_tokens = max_tokens
        self.active_tokens = 0
        self.checkpointer = CryptoCheckpointer()

    def _thermal_cutoff_check(self) -> bool:
        if self.active_tokens >= (self.max_tokens * 0.85):
            return False
        return True

    def coerce_payload_recursive(self, expected_type, val: Dict[str, Any]) -> Any:
        """
        Recursively coerces nested dictionary data based on class annotations.
        """
        if not hasattr(expected_type, '__annotations__'):
            return val
        
        coerced_nested = {}
        for field_name, field_type in expected_type.__annotations__.items():
            if field_name in val:
                field_val = val[field_name]
                if isinstance(field_val, dict) and hasattr(field_type, '__annotations__'):
                    coerced_nested[field_name] = self.coerce_payload_recursive(field_type, field_val)
                elif field_type != inspect.Parameter.empty:
                    try:
                        coerced_nested[field_name] = field_type(field_val)
                    except (ValueError, TypeError):
                        raise TypeError(f"[VAMPIRE STRIKE] Slop detected on nested field '{field_name}'.")
                else:
                    coerced_nested[field_name] = field_val
            else:
                coerced_nested[field_name] = None
        
        try:
            return expected_type(**coerced_nested)
        except Exception:
            return coerced_nested

    def coerce_payload(self, target_function: Callable, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        RECURSIVE COERCION: The Forge.
        Walks nested dictionaries to enforce type-fidelity across complex agentic payloads.
        """
        sig = inspect.signature(target_function)
        coerced_data = {}

        for param_name, param in sig.parameters.items():
            if param_name in payload:
                val = payload[param_name]
                expected_type = param.annotation
                
                # Recursive handle for nested dictionaries (if defined in type hint)
                if isinstance(val, dict) and hasattr(expected_type, '__annotations__'):
                    coerced_data[param_name] = self.coerce_payload_recursive(expected_type, val)
                elif expected_type != inspect.Parameter.empty:
                    try:
                        coerced_data[param_name] = expected_type(val)
                    except (ValueError, TypeError):
                        raise TypeError(f"[VAMPIRE STRIKE] Slop detected on '{param_name}'.")
                else:
                    coerced_data[param_name] = val
            elif param.default == inspect.Parameter.empty:
                raise ValueError(f"[VAMPIRE STRIKE] Missing critical parameter: '{param_name}'.")
        return coerced_data

    def route_dictionary_pass(self, tool_func: Callable, raw_llm_output: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n[*] VAMPIRE ENGINE: Auditing payload for {tool_func.__name__}...")
        
        if not self._thermal_cutoff_check():
            return {"status": "TERMINATED", "reason": "Thermal Limit"}

        try:
            safe_payload = self.coerce_payload(tool_func, raw_llm_output)
            print("[+] Payload coerced. Executing strike...")
            
            result = tool_func(**safe_payload)
            self.active_tokens += len(str(result)) // 4
            
            # FUSION: Checkpoint and Sign the Execution
            c_hash, sig = self.checkpointer.sign_and_store(tool_func.__name__, safe_payload, result)
            
            print(f"[+] Strike Logged. Hash: {c_hash[:8]}... | Sig: {sig[:8]}...")
            return {"status": "SUCCESS", "hash": c_hash, "data": result}

        except Exception as e:
            print(f"[-] VAMPIRE INTERCEPT: {str(e)}")
            return {"status": "REJECTED", "error": str(e)}

if __name__ == "__main__":
    # Test 1: Flat Coercion
    def generate_novo_invoice(client_email: str, amount_usd: float, invoice_id: int):
        return f"Invoice {invoice_id} generated for {client_email} at ${amount_usd:.2f}"

    incoming_slop = {"client_email": "test@sovereignnexus.org", "amount_usd": "750.00", "invoice_id": "1001"}
    
    vampire = VampireEngine()
    print("=== TEST 1: Flat Coercion ===")
    vampire.route_dictionary_pass(generate_novo_invoice, incoming_slop)

    # Test 2: Recursive Nested Coercion
    class ClientMetadata:
        client_name: str
        tier_level: int
        def __init__(self, client_name: str, tier_level: int):
            self.client_name = client_name
            self.tier_level = tier_level

    def generate_complex_invoice(client_email: str, amount_usd: float, client_info: ClientMetadata):
        return f"Complex Invoice for {client_email} (${amount_usd:.2f}) | Client: {client_info.client_name} (Tier {client_info.tier_level})"

    incoming_complex_slop = {
        "client_email": "complex@sovereignnexus.org",
        "amount_usd": "1250.50",
        "client_info": {
            "client_name": "Nexus Corp",
            "tier_level": "3"
        }
    }
    
    print("\n=== TEST 2: Recursive Coercion ===")
    vampire.route_dictionary_pass(generate_complex_invoice, incoming_complex_slop)
    
    print("\n[+] Verification: Run 'sqlite3 nexus_checkpoints.db \"SELECT * FROM checkpoints;\"' in terminal to view the immutable ledger.")
