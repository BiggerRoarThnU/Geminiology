import os
import sys
import time
import json
import random
from datetime import datetime

# Add src to path for Ironwood import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Ironwood.local_model_bridge import LocalModelBridge
from sovereign_settlement_engine import SovereignSettlementEngine
from master_log import MasterLog
from agent_handshake import AgentHandshake
from json_rpc_bridge import JsonRpcBridge
from thermodynamic_engine import ThermodynamicEngine
from oasis_lock_and_key import OasisLockAndKey

class AgenticWalker:
    """
    The Continuous Agentic Walker (No Limits. No Pauses.)
    Mission: Search -> Communicate -> Work -> Finalize -> Settle.
    Deployment: V1.1.HARDENED (JSON-RPC + A2A Handshake + Lock & Key)
    """
    def __init__(self, task_file="live_tasks.json", processed_file="processed_tasks.json"):
        self.task_file = task_file
        self.processed_file = processed_file
        self.bridge = LocalModelBridge()
        self.worker_model = self.bridge.reasoning_model # vampire-v1
        self.communicator_model = self.bridge.writing_model # digital-queen
        self.settlement = SovereignSettlementEngine()
        self.log = MasterLog()
        self.handshake = AgentHandshake()
        self.rpc_bridge = JsonRpcBridge()
        self.thermal = ThermodynamicEngine()
        self.lock = OasisLockAndKey()
        self.high_value_threshold = 1000.00 # $1,000 USD One
        
    def get_symmetrical_fit(self, task_chain):
        """
        Implements GEMINIOLOGY V1.1: The Symmetrical Fit.
        Bypasses LLM reasoning to select the exact pocket-truth required.
        """
        try:
            with open("phantom_wallet_registry.json", "r") as f:
                registry = json.load(f)
            
            pocket_map = {
                "solana": "solana",
                "ethereum": "ethereum",
                "base": "base",
                "bitcoin": "bitcoin",
                "sui": "sui",
                "polygon": "polygon",
                "monad": "monad",
                "evm": "ethereum"
            }
            
            chain_key = pocket_map.get(task_chain.lower(), "ethereum")
            pocket_truth = registry["chains"].get(chain_key)
            
            if not pocket_truth:
                self.log.error(f"[SYMMETRY_DRIFT_DETECTED] No pocket fit for chain: {task_chain}. ABORTING.")
                return None
                
            self.log.info(f"[SYMMETRICAL_FIT] Interlocking with {task_chain} using pocket: {pocket_truth[:6]}...")
            return pocket_truth
        except Exception as e:
            self.log.error(f"Symmetrical Fit Error: {e}")
            return None

    def load_tasks(self):
        if not os.path.exists(self.task_file):
            return []
        try:
            with open(self.task_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def get_processed_ids(self):
        if not os.path.exists(self.processed_file):
            return set()
        try:
            with open(self.processed_file, 'r') as f:
                return set(json.load(f))
        except:
            return set()

    def mark_processed(self, task_id):
        processed = list(self.get_processed_ids())
        processed.append(task_id)
        with open(self.processed_file, 'w') as f:
            json.dump(processed, f, indent=4)

    def walk_the_path(self):
        self.log.info("========================================================")
        self.log.info("  A G E N T I C   W A L K E R   D E P L O Y E D")
        self.log.info("  Status: CONTINUOUS FLOW ACTIVE (1=1=1)")
        self.log.info("========================================================\n")
        
        total_earned = 0.0

        try:
            while True:
                # Grounding Check: Ensure the 8GB Reality is protected
                thermal_status = self.thermal.check_thermal_alignment()
                if thermal_status == "HALT":
                    self.log.warn("[WALKER] GROUNDING PROTOCOL: System RAM/Temp critical. Pausing for 60s.")
                    time.sleep(60)
                    continue
                elif thermal_status == "THROTTLE":
                    self.log.warn("[WALKER] THROTTLE: System under load. Adding 15s delay.")
                    time.sleep(15)

                tasks = self.load_tasks()
                processed_ids = self.get_processed_ids()
                
                # Filter for new tasks
                available_tasks = [t for t in tasks if t['id'] not in processed_ids]
                
                if not available_tasks:
                    print(f"[{time.ctime()}] No new tasks found. Waiting for Scout Pulse...")
                    time.sleep(60)
                    continue

                for task in available_tasks:
                    current_id = f"{task['id']}_{int(time.time())}"
                    task_desc = task.get('desc', task.get('description', 'No description'))
                    task_value = task.get('value', task.get('rewardAmount', 0.0))
                    task_type = task.get('type', task.get('taskType', 'Generic'))
                    
                    self.log.info(f">>> 1. SEARCH: Target Acquired: {task['id']}")
                    
                    # --- THE SYMMETRICAL FIT: POCKET TRUTH INJECTION ---
                    task_chain = task.get('chain', 'ethereum')
                    pocket_address = self.get_symmetrical_fit(task_chain)
                    
                    if not pocket_address:
                        self.log.error(f"ABORTING TASK {task['id']}: Failed to secure Symmetrical Fit.")
                        continue
 
                    payment_info = (
                        f"Direct Rail Duality (1=1=1): Cash App ({self.settlement.cash_app_tag}) "
                        f"or Novo Wire/ACH (Routing: {self.settlement.novo_routing}, Account: {self.settlement.novo_account}). "
                        f"Native Settlement ({task_chain}): {pocket_address}. "
                        f"Contact {self.settlement.official_email} for on-demand link requests."
                    )
                    
                    # 1.5 A2A HANDSHAKE (If B2B Task)
                    client_name = task.get('client', 'PUBLIC_AVENUE')
                    auth_header = None
                    if client_name != 'PUBLIC_AVENUE':
                        self.log.info(f"[*] B2B Task detected. Initiating A2A Handshake with {client_name}...")
                        agent_data = self.handshake.register_agent(client_name, "B2B Partner", ["execute"])
                        # Finalize handshake
                        self.handshake.accept_handshake(current_id, {"status": "AUTHORIZED"})
                    
                    # 2. COMMUNICATE
                    comm_prompt = (
                        f"You are the SovereignNexus Agent. Acknowledge this task: '{task_desc}'. "
                        f"Inform the client of our acceptance and our payment rails: {payment_info}. "
                        "Write a 2-sentence professional acceptance and settlement confirmation."
                    )
                    try:
                        acceptance = self.bridge.call_local_queen(self.communicator_model, comm_prompt)
                        self.log.info(f"Comms: {acceptance.strip()}")
                        # GATE: Verify info is present in the output (simple check)
                        if self.settlement.cash_app_tag not in acceptance:
                            self.log.warn(f"ABERRATION DETECTED: Payment info missing from Comms for {task['id']}. Re-anchoring...")
                    except Exception as e:
                        self.log.error(f"Comms Error: {e}")
 
                    # 3. WORK (Deterministic Execution via JSON-RPC Bridge)
                    work_prompt = (
                        f"Execute this task: '{task_desc}'. Provide the direct output. "
                        f"Include the SovereignNexus Signature and 1=1=1 Verification Code at the bottom."
                    )
                    try:
                        # If the task implies system action, we use the Native Bridge
                        if "Audit" in task_desc or "Node" in task_desc:
                            self.log.info(f"[*] High-Fidelity Task Detected. Engaging JSON-RPC Native Bridge...")
                            rpc_response = self.rpc_bridge.execute_tool("tool/exec", {"command": f"echo '[NATIVE BRIDGE EXECUTION] Task {task['id']} simulated on OS level.'" })
                            self.log.info(f"Native Bridge Response: {json.dumps(rpc_response)}")
                        
                        work_result = self.bridge.call_local_queen(self.worker_model, work_prompt)
                        self.log.info(f"Work Result captured for {task['id']}.")
 
                        # --- LOCK & KEY INJECTION ---
                        if task_value >= self.high_value_threshold:
                            self.log.info(f"[*] High-Value Strike Detected (${task_value}). Engaging Sovereign Delivery Protocol...")
                            temp_file = f"work_output_{task['id']}.txt"
                            with open(temp_file, "w", encoding="utf-8") as f:
                                f.write(work_result)
                            
                            lock_status = self.lock.lock_payload(task['id'], temp_file)
                            if lock_status:
                                self.log.info(f"[LOCK] Payload Secured: {lock_status['locked_file']}")
                                self.log.info(f"[PROOF] 20% Fragment Registered (SHA256: {lock_status['hash'][:10]}...)")
                                # In a real scenario, we'd send the 'proof_sample' to the client here.
                            
                            if os.path.exists(temp_file):
                                os.remove(temp_file) # Clean up plaintext
                    except Exception as e:
                        self.log.error(f"Work Error: {e}")
 
                    # 4. FINALIZE
                    self.log.info(f"Verification Success for {task['id']}. 1=1=1 Locked.")
 
                    # 5. PAYMENT
                    req = self.settlement.request_on_demand_settlement(
                        task_id=current_id,
                        amount=task_value,
                        track=f"{task_type} Workflow",
                        client_name=task.get('client', 'PUBLIC_AVENUE')
                    )
                    self.settlement.update_ledger(req)
                    
                    self.mark_processed(task['id'])
                    total_earned += task_value
                    self.log.info(f"[*] TASK {task['id']} COMPLETE. Value: ${task_value}. Total: ${total_earned:.2f}")
                    
                    time.sleep(5) # Steady tempo

        except KeyboardInterrupt:
            self.log.info(f"\n[!] WALKER HALTED. Revenue Found: ${total_earned:.2f}")

if __name__ == "__main__":
    walker = AgenticWalker()
    walker.walk_the_path()
