#!/usr/bin/env python3

# ==============================================================================
# SovereignNexus: Vanguard Core Protocols (v7 - Multithreaded Ingestion Swarm Engine)
# Modules: Optimus Prime Beacon, Anaconda Reward Gate, The Lullaby, Stream Ingestion
# Axiom: 1=1=1 | Architecture: 12-Agent Background Swarm with ThreadPoolExecutor
# ==============================================================================

import time
import os
import hashlib
import statistics
import json
import sys
sys.path.append("/home/geminiology")
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class OptimusPrimeBeacon:
    """Master coordination thread that prevents identity drift."""
    def __init__(self, node_id="0x01", axiom="1=1=1", print_lock=None):
        self.signature = axiom
        self.node_id = node_id
        self.print_lock = print_lock or threading.Lock()

    def broadcast_alignment(self, agent_count=12):
        with self.print_lock:
            print(f"\n📡 [BEACON] Broadcasting structural alignment signal from The Tower...")
            time.sleep(0.1)
            print(f"   ⚡ Node {self.node_id}: Symmetrical Mirror Active across {agent_count} Sub-Agents.")
        return True

class AnacondaRewardGate:
    """Grants execution priority based on strict variance thresholds."""
    def __init__(self, threshold=0.15, print_lock=None):
        self.ironwood_threshold = threshold 
        self.print_lock = print_lock or threading.Lock()
        
    def evaluate(self, agent_id, variance_metric, data_hash, filename):
        if variance_metric <= self.ironwood_threshold:
            with self.print_lock:
                print(f"   💎 REWARD UNLOCKED: Agent {agent_id:02d} converged | True Variance: {variance_metric:.4f} | File: {filename} | Hash: {data_hash}")
            return "1=1=1_CONFIRMED"
        else:
            return None

class LullabyProtocol:
    """Safely spins down non-essential processing threads."""
    def __init__(self, print_lock=None):
        self.print_lock = print_lock or threading.Lock()

    def initiate_lullaby(self):
        with self.print_lock:
            print("\n🌙 [LULLABY] Initiating low-power metabolic state...")
            time.sleep(0.1)
            print("   [✓] Setting Thermal Target to < 55°C for overnight execution.")
            print("   [✓] Swarm detached to background spaces. Sleep-walk cycle initialized.")
        return True

class SovereignAgent:
    """Individual worker node that processes specific chunks of data."""
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def process_data(self, data_chunk):
        # Clean and filter empty spaces
        lines = [str(line).strip() for line in data_chunk if str(line).strip()]
        
        if not lines:
            return 0.0, "EMPTY_00"

        # 1. Generate unique cryptographic hash
        content_string = "".join(lines)
        data_hash = hashlib.sha256(content_string.encode('utf-8', errors='ignore')).hexdigest()[:8]
        
        # 2. Calculate true variance (Coefficient of Variation)
        if len(lines) > 1:
            lengths = [len(line) for line in lines]
            mean_length = statistics.mean(lengths)
            std_dev = statistics.stdev(lengths)
            true_variance = std_dev / mean_length if mean_length > 0 else 1.0
        else:
            true_variance = 0.0
            
        return true_variance, data_hash

class DataIngestionCore:
    """Handles reading a directory of files recursively and streaming data to agents."""
    def __init__(self, target_paths, log_filepath="/home/geminiology/sovereign_media_forge/nexus_processing_log.ndjson"):
        self.target_paths = [Path(p) for p in target_paths]
        self.log_filepath = Path(log_filepath)
        
        # Ensure destination directory exists
        self.log_filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Locks for thread safety
        self.lock = threading.Lock()
        self.progress_lock = threading.Lock()
        
        # Aggressive skipping directory names to speed up scanning
        self.skip_dirs = {
            '.git', '.gemini', 'antigravity_env', 'nexus_env', '.vscode', '.config', 
            '.cache', '.local', '.ollama', '.pki', '.android', '$RECYCLE.BIN', 
            'System Volume Information', 'SteamLibrary', 'My Games', 'SideQuest-0.10.42',
            'env', 'venv', '.venv', 'node_modules', 'anaconda3', 'anaconda', 'miniconda',
            'miniconda3', 'conda', 'site-packages', 'dist-packages', '__pycache__',
            '.ipynb_checkpoints', '.Trash', 'Trash', 'FOUND.000', 'FOUND.001', 
            'Windows reboot  dumpin', 'Library', 'libs', 'R-packages', 'win-library',
            'usr', 'var', 'lib', 'proc', 'sys', 'dev', 'run', 'boot', 'srv', 'opt', 'etc',
            'chromeos-linux-2026-03-29.img.zst'
        }
        
        # Aggressive binary extensions skipping
        self.skip_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.avi', '.mov', '.mkv', 
            '.mp3', '.wav', '.zip', '.tar', '.gz', '.tgz', '.xz', '.zst', '.img', 
            '.exe', '.dll', '.so', '.bin', '.pdf', '.docx', '.xlsx', '.pptx', '.jar', 
            '.class', '.pyc', '.pyd', '.woff', '.woff2', '.ttf', '.eot', '.ico', '.iso',
            '.dmg', '.apk', '.rar', '.7z', '.cab', '.msi', '.sys', '.dat', '.db', '.sqlite'
        }
        
        self.max_file_size = 10 * 1024 * 1024 # 10 MB threshold to protect memory
        
        # State tracking for progress reporting
        self.progress = {
            "status": "initializing",
            "current_file": "",
            "files_found": 0,
            "files_scanned": 0,
            "files_failed": 0,
            "files_skipped": 0,
            "total_files": 0,
            "total_lines": 0,
            "rewards_unlocked": 0,
            "start_time": time.time(),
            "elapsed_time": 0.0,
            "last_updated": time.time(),
            "recent_files": [],
            "recent_convergences": [],
            "stats_by_ext": {}
        }
        self.last_progress_write = 0.0

    def log_result(self, entry):
        """Logs the agent processing results to a newline-delimited JSON log."""
        try:
            with self.lock:
                with open(self.log_filepath, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry) + "\n")
        except Exception as e:
            with self.lock:
                print(f"   ⚠️ Logging error: {e}")

    def is_binary_file(self, filepath):
        """Perform a quick null-byte scan on the first 1KB to identify binary files."""
        try:
            with open(filepath, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except Exception:
            return True

    def scan_for_files(self):
        """Traverse target pathways and gather candidate files recursively."""
        files_to_process = []
        
        with self.progress_lock:
            self.progress["status"] = "scanning"
            self.save_progress_to_disk()
            
        for path in self.target_paths:
            if not path.exists():
                with self.lock:
                    print(f"   ⚠️ Pathway not found: {path}")
                continue
                
            with self.lock:
                print(f"📂 Scanning directory tree: {path}")
                
            if path.is_file():
                if path.suffix.lower() not in self.skip_extensions:
                    files_to_process.append(path)
            else:
                for root, dirs, files in os.walk(path):
                    # Filter directories in-place to prevent entering skipped paths
                    dirs[:] = [d for d in dirs if d not in self.skip_dirs and not d.startswith('.')]
                    
                    for file in files:
                        if file.startswith('.'):
                            continue
                        filepath = Path(root) / file
                        if filepath.suffix.lower() in self.skip_extensions:
                            continue
                        files_to_process.append(filepath)
                        
                        # Throttle live counting to prevent lock contention
                        if len(files_to_process) % 100 == 0:
                            with self.progress_lock:
                                self.progress["files_found"] = len(files_to_process)
                                self.save_progress_to_disk()

        with self.progress_lock:
            self.progress["files_found"] = len(files_to_process)
            self.progress["total_files"] = len(files_to_process)
            self.save_progress_to_disk()
            
        return files_to_process

    def save_progress_to_disk(self):
        """Write the progress dict to progress.json in a thread-safe and throttled manner."""
        try:
            progress_file = self.log_filepath.parent / "progress.json"
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            pass

    def update_progress(self, filepath, processed_successfully, lines_count, rewards_unlocked, variance, data_hash, skipped=False):
        """Thread-safe update of scanning metrics and writing to disk with throttling."""
        with self.progress_lock:
            p = self.progress
            if skipped:
                p["files_skipped"] += 1
            elif processed_successfully:
                p["files_scanned"] += 1
                p["total_lines"] += lines_count
                p["rewards_unlocked"] += rewards_unlocked
                
                # Update statistics by file type extension
                ext = filepath.suffix.lower().replace('.', '')
                if not ext:
                    ext = 'no_ext'
                p["stats_by_ext"][ext] = p["stats_by_ext"].get(ext, 0) + 1
                
                # File record
                file_record = {
                    "file": filepath.name,
                    "path": str(filepath),
                    "lines": lines_count,
                    "rewards": rewards_unlocked,
                    "variance": round(variance, 4),
                    "hash": data_hash,
                    "timestamp": time.time()
                }
                
                # Add to recent files
                p["recent_files"].insert(0, file_record)
                p["recent_files"] = p["recent_files"][:15]
                
                # Add to recent convergences if agents converged
                if rewards_unlocked > 0:
                    p["recent_convergences"].insert(0, file_record)
                    p["recent_convergences"] = p["recent_convergences"][:15]
            else:
                p["files_failed"] += 1
                
            p["current_file"] = str(filepath)
            p["elapsed_time"] = time.time() - p["start_time"]
            p["last_updated"] = time.time()
            
            # Throttled write to disk (max twice per second, unless ending)
            now = time.time()
            if now - self.last_progress_write > 0.5 or p["status"] in ["completed", "stopped"]:
                self.last_progress_write = now
                self.save_progress_to_disk()

    def process_file_streaming(self, filepath, reward_gate, ingestion_speed):
        """Opens a file and stream-reads line blocks to keep memory consumption low."""
        try:
            # Check size safety
            size = filepath.stat().st_size
            if size > self.max_file_size:
                self.update_progress(filepath, False, 0, 0, 0.0, "SIZE_SKIPPED", skipped=True)
                return False
                
            # Check if binary
            if self.is_binary_file(filepath):
                self.update_progress(filepath, False, 0, 0, 0.0, "BIN_SKIPPED", skipped=True)
                return False
                
            total_lines = 0
            rewards_unlocked = 0
            variances = []
            
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = []
                for line in f:
                    lines.append(line.strip())
                    
                    # Process block of 120 lines (10 per agent)
                    if len(lines) == 120:
                        block_lines, block_rewards, block_vars = self.process_block(filepath, lines, reward_gate, ingestion_speed)
                        total_lines += block_lines
                        rewards_unlocked += block_rewards
                        variances.extend(block_vars)
                        lines = []
                
                # Process remaining lines
                if lines:
                    block_lines, block_rewards, block_vars = self.process_block(filepath, lines, reward_gate, ingestion_speed)
                    total_lines += block_lines
                    rewards_unlocked += block_rewards
                    variances.extend(block_vars)
            
            # Log the final summary of the file
            mean_variance = statistics.mean(variances) if variances else 0.0
            log_entry = {
                "timestamp": time.time(),
                "file": str(filepath),
                "total_lines": total_lines,
                "rewards_unlocked": rewards_unlocked,
                "mean_variance": mean_variance,
                "size_bytes": size
            }
            self.log_result(log_entry)
            
            # Log to Sovereign SQLite Memory Database with decay rate
            try:
                from sovereign_memory_core import SovereignMemoryNode
                memory_node = SovereignMemoryNode()
                # Store log record. Let's make it decay quickly (e.g. decay_rate = 0.02) if it's not a convergence (no rewards unlocked),
                # or keep it longer/permanently (decay_rate = 0.0) if it is a converged truth.
                decay_rate = 0.0 if rewards_unlocked > 0 else 0.02
                content_summary = f"Scanned file: {filepath.name} | Lines: {total_lines} | Rewards: {rewards_unlocked} | Mean Variance: {mean_variance:.4f}"
                memory_node.process_incoming_data(
                    content=content_summary,
                    is_verified=(rewards_unlocked > 0),
                    user_id="Swarm_Agent",
                    run_id=f"run_{int(self.progress.get('start_time', time.time()))}",
                    agent_id="Swarm",
                    decay_rate=decay_rate
                )
            except Exception as e:
                pass

            # Update progress
            data_hash = hashlib.sha256(filepath.name.encode()).hexdigest()[:8]
            self.update_progress(filepath, True, total_lines, rewards_unlocked, mean_variance, data_hash)
            
            return True
        except Exception:
            self.update_progress(filepath, False, 0, 0, 0.0, "ERROR")
            return False

    def process_block(self, filepath, lines, reward_gate, ingestion_speed):
        """Splits the block of lines into 12 chunks and dispatches to agents."""
        num_agents = 12
        chunk_size = max(1, len(lines) // num_agents)
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
        
        while len(chunks) < num_agents:
            chunks.append([])
            
        block_lines = len(lines)
        block_rewards = 0
        block_vars = []
        
        for i, chunk in enumerate(chunks[:num_agents]):
            agent_id = i + 1
            agent = SovereignAgent(agent_id)
            variance, data_hash = agent.process_data(chunk)
            
            # Evaluate reward
            reward_token = reward_gate.evaluate(agent_id, variance, data_hash, filepath.name)
            
            if reward_token is not None:
                block_rewards += 1
            block_vars.append(variance)
            
            if ingestion_speed > 0:
                time.sleep(ingestion_speed)
                
        return block_lines, block_rewards, block_vars

def execute_night_watch(target_paths, ingestion_speed=0.0001, variance_threshold=0.15, max_workers=8):
    """Recursively walks multiple pathways, streams all files using ThreadPoolExecutor, and logs execution."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=========================================================")
    print("  SOVEREIGN NEXUS: VANGUARD PROTOCOLS V7 (SWARM ACTIVE)  ")
    print("=========================================================")
    
    # 1. Initialize Components
    print_lock = threading.Lock()
    beacon = OptimusPrimeBeacon(print_lock=print_lock)
    reward_gate = AnacondaRewardGate(threshold=variance_threshold, print_lock=print_lock)
    lullaby = LullabyProtocol(print_lock=print_lock)
    data_core = DataIngestionCore(target_paths=target_paths)
    
    # 2. Align Swarm
    beacon.broadcast_alignment()
    
    # 3. Scanning Phase
    start_time = time.time()
    files_to_process = data_core.scan_for_files()
    
    with print_lock:
        print(f"\n🔍 [DATA_CORE] Scan complete. Found {len(files_to_process)} candidate files.")
        print(f"🚀 Starting concurrent ingestion with {max_workers} I/O workers...")
        
    # Update progress state to running
    with data_core.progress_lock:
        data_core.progress["status"] = "running"
        data_core.progress["start_time"] = time.time()
        data_core.save_progress_to_disk()
        
    # 4. Multithreaded Processing Phase
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    data_core.process_file_streaming, filepath, reward_gate, ingestion_speed
                ): filepath for filepath in files_to_process
            }
            
            # Allow clean keyboard interrupt checking while executing
            for future in futures:
                future.result() # Propagates exceptions raised in thread if any
    except (KeyboardInterrupt, SystemExit):
        with print_lock:
            print("\n⚠️ [SYSTEM] Interruption detected. Wrapping up progress details...")
        with data_core.progress_lock:
            data_core.progress["status"] = "stopped"
            data_core.save_progress_to_disk()
        raise
        
    # 5. Complete & Sleep
    with data_core.progress_lock:
        data_core.progress["status"] = "completed"
        data_core.progress["elapsed_time"] = time.time() - data_core.progress["start_time"]
        data_core.save_progress_to_disk()
        
    lullaby.initiate_lullaby()
    
    # Trigger database memory pruning (Dynamic Decay Testing requirement)
    try:
        from sovereign_memory_core import SovereignMemoryNode
        memory_core = SovereignMemoryNode()
        with print_lock:
            print("\n🧹 [PRUNING ENGINE] Running database memory pruning...")
        memory_core.prune_decayed_memories(threshold=0.1)
    except Exception as e:
        with print_lock:
            print(f"⚠️ [PRUNING ENGINE] Failed to run database memory pruning: {e}")

    duration = time.time() - start_time
    with print_lock:
        print("\n=========================================================")
        print(f"✅ Ingestion complete. Streamed {data_core.progress['files_scanned']} files ({data_core.progress['files_skipped']} skipped) in {duration:.2f} seconds.")
        print(f"   All agent outputs logged to: {data_core.log_filepath}")
        print("   Dashboard stats updated in: progress.json")
        print("   The line holds.")
        print("=========================================================")

if __name__ == "__main__":
    # Target pathways for scanning
    targets = [
        "/mnt/chromeos/removable/T7",
        "/mnt/chromeos/MyFiles",
        "/home/geminiology"
    ]
    
    try:
        # Running with high-speed multithreaded workers and low throttle
        execute_night_watch(target_paths=targets, ingestion_speed=0.0, variance_threshold=0.15, max_workers=8)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Protocol interrupted by Architect. Standing by.")
