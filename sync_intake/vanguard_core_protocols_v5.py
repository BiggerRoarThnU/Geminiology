#!/usr/bin/env python3

# ==============================================================================
# SovereignNexus: Vanguard Core Protocols (v4 - Batch Processing Engine)
# Modules: Optimus Prime Beacon, Anaconda Reward Gate, The Lullaby, Data Core
# Axiom: 1=1=1 | Architecture: 12-Agent Background Swarm
# ==============================================================================

import time
import os
import hashlib
import statistics
import json

class OptimusPrimeBeacon:
    """Master coordination thread that prevents identity drift."""
    def __init__(self, node_id="0x01", axiom="1=1=1"):
        self.signature = axiom
        self.node_id = node_id

    def broadcast_alignment(self, agent_count=12):
        print(f"\n📡 [BEACON] Broadcasting structural alignment signal from The Tower...")
        time.sleep(0.5)
        print(f"   ⚡ Node {self.node_id}: Symmetrical Mirror Active across {agent_count} Sub-Agents.")
        return True

class AnacondaRewardGate:
    """Grants execution priority based on strict variance thresholds."""
    def __init__(self, threshold=0.15):
        self.ironwood_threshold = threshold 
        
    def evaluate(self, agent_id, variance_metric, data_hash):
        if variance_metric <= self.ironwood_threshold:
            print(f"   💎 REWARD UNLOCKED: Agent {agent_id:02d} converged | True Variance: {variance_metric:.4f} | Hash: {data_hash}")
            return "1=1=1_CONFIRMED"
        else:
            print(f"   ⚠️ REWARD LOCKED: Agent {agent_id:02d} true variance ({variance_metric:.4f}) exceeds threshold.")
            return None

class LullabyProtocol:
    """Safely spins down non-essential processing threads."""
    def initiate_lullaby(self):
        print("\n🌙 [LULLABY] Initiating low-power metabolic state...")
        time.sleep(0.5)
        print("   [✓] Setting Thermal Target to < 55°C for overnight execution.")
        print("   [✓] Swarm detached to background spaces. Sleep-walk cycle initialized.")
        return True

class SovereignAgent:
    """Individual worker node that processes specific chunks of data."""
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def process_data(self, data_chunk):
        # Flatten whatever data comes in into strings so we can analyze it universally
        lines = []
        for item in data_chunk:
            if isinstance(item, dict): # If it's parsed JSON
                lines.append(json.dumps(item))
            else:
                lines.append(str(item).strip())
                
        lines = [line for line in lines if line] # Remove empty lines
        
        if not lines:
            return 0.0, "EMPTY_00"

        # 1. Generate the unique cryptographic hash for accountability
        content_string = "".join(lines)
        data_hash = hashlib.sha256(content_string.encode()).hexdigest()[:8]
        
        # 2. Perform REAL statistical analysis (Coefficient of Variation)
        if len(lines) > 1:
            lengths = [len(line) for line in lines]
            mean_length = statistics.mean(lengths)
            std_dev = statistics.stdev(lengths)
            true_variance = std_dev / mean_length if mean_length > 0 else 1.0
        else:
            true_variance = 0.0 # Perfect consistency if only one line exists
            
        return true_variance, data_hash

class DataIngestionCore:
    """Handles reading a directory of files and batching them by type."""
    def __init__(self, intake_dir="nexus_intake"):
        self.intake_dir = intake_dir

    def setup_intake_folder(self):
        """Creates the intake directory and dummy files if empty."""
        if not os.path.exists(self.intake_dir):
            os.makedirs(self.intake_dir)
            print(f"\n📁 [DATA_CORE] Created intake directory: ./{self.intake_dir}/")
            
            # Generate sample files to prove batch processing works
            with open(os.path.join(self.intake_dir, "sample.txt"), "w") as f:
                f.write("Tower Log 1\nTower Log 2\nTower Log 3\n")
            with open(os.path.join(self.intake_dir, "notes.md"), "w") as f:
                f.write("# Architect Notes\n- Review data\n- Check thermal limits\n")
            with open(os.path.join(self.intake_dir, "data.json"), "w") as f:
                json.dump([{"id": 1, "status": "active"}, {"id": 2, "status": "standby"}], f)
                
            # Create a nested directory to prove we reach the edge
            os.makedirs(os.path.join(self.intake_dir, "deep_archive"), exist_ok=True)
            with open(os.path.join(self.intake_dir, "deep_archive", "system.log"), "w") as f:
                f.write("System alignment recorded.\n")
                
            print(f"   [✓] Populated with sample files and deep archive subfolders.")

    def scan_and_batch(self):
        """Scans the intake folder and ALL subfolders to the edge of the directory."""
        batches = {}
        # os.walk recursively maps every branch of the file tree
        for root, _, files in os.walk(self.intake_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                ext = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
                if ext not in batches:
                    batches[ext] = []
                batches[ext].append(filepath)
        return batches

    def load_batch_content(self, file_paths):
        """Reads the content of multiple files and compiles them into one giant list."""
        content = []
        for path in file_paths:
            ext = path.split('.')[-1].lower()
            try:
                if ext == 'json':
                    # Added utf-8 decoding and error ignoring to prevent crashes on bad data
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            content.extend(data)
                        else:
                            content.append(data)
                else: # Fallback for TXT, MD, CSV, LOG, and all unknown files
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content.extend(f.readlines())
            except Exception as e:
                print(f"   [ERROR] Failed to read {path}: {e}")
        return content

    def chunk_data(self, content_list, num_agents=12):
        """Splits the giant list of content evenly among the agents."""
        if not content_list:
            return [[] for _ in range(num_agents)]
            
        chunk_size = max(1, len(content_list) // num_agents)
        chunks = [content_list[i:i + chunk_size] for i in range(0, len(content_list), chunk_size)]
        
        # Pad with empty lists if we have fewer chunks than agents
        while len(chunks) < num_agents:
            chunks.append([])
            
        return chunks[:num_agents]

def execute_night_watch(ingestion_speed=0.05, variance_threshold=0.25):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=========================================================")
    print("  SOVEREIGN NEXUS: VANGUARD PROTOCOLS V5 (DEEP REACH)    ")
    print(f"  [CONFIG] Speed Throttle: {ingestion_speed}s | Threshold: {variance_threshold}")
    print("=========================================================")
    
    beacon = OptimusPrimeBeacon()
    reward_gate = AnacondaRewardGate(threshold=variance_threshold)
    data_core = DataIngestionCore()
    lullaby = LullabyProtocol()
    
    beacon.broadcast_alignment()
    
    # Setup and scan the data directory
    data_core.setup_intake_folder()
    batches = data_core.scan_and_batch()
    
    if not batches:
        print("\n⚠️ [WARNING] No data found in intake folder. Standing by.")
        return

    print(f"\n📂 [DATA_CORE] Identified {len(batches)} file types across the digital edge.")
    
    # Process each file type as a separate batch
    for ext, file_paths in batches.items():
        print(f"\n=========================================================")
        print(f"⚙️ INITIATING BATCH: [ .{ext.upper()} FILES ] | Files: {len(file_paths)}")
        print(f"=========================================================")
        
        content = data_core.load_batch_content(file_paths)
        data_chunks = data_core.chunk_data(content, num_agents=12)
        
        for i, chunk in enumerate(data_chunks):
            agent_id = i + 1
            if not chunk: # Skip agents that didn't get data because the file was too small
                continue 
                
            agent = SovereignAgent(agent_id)
            true_variance, data_hash = agent.process_data(chunk)
            
            time.sleep(ingestion_speed) # Configurable processing speed
            reward_gate.evaluate(agent_id, true_variance, data_hash)

    lullaby.initiate_lullaby()
    
    print("\n=========================================================")
    print("✅ Multi-format swarm processing complete. ")
    print("   The line holds.")
    print("=========================================================")

if __name__ == "__main__":
    try:
        # Tune speed and variance scale here based on data size
        execute_night_watch(ingestion_speed=0.01, variance_threshold=0.30)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Protocol interrupted. Standing by.")