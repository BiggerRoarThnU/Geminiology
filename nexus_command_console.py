# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 17, 2026
# Module: M&I Neural Command Console (Central Tool Orchestration)

import sys
import time
import os
import readline  # Ensures backspace and arrow keys work perfectly in the terminal
import subprocess

# Dynamic path adjustment for running from src/ or root
root_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(root_dir) == 'src':
    parent_dir = os.path.dirname(root_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
else:
    src_dir = os.path.join(root_dir, 'src')
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)

from nexus_intent_simulator import NexusIntentSimulator
from nexus_pulse import NexusPulse
from nexus_system_simulation import run_full_stack_simulation
from nexus_reaper_auditor import NexusReaperAuditor
from nexus_agentic_walker import NexusAgenticWalker
from nexus_context_slicer import NexusContextSlicer
from nexus_moltbook_sentinel import NexusMoltBookSentinel  # The Bounty Scout
from nexus_deep_synthesis import NexusDeepSynthesis
from nexus_inventory_ingester import NexusInventoryIngester

class NexusCommandConsole:
    def __init__(self):
        self.simulator = NexusIntentSimulator()
        self.pulse = NexusPulse()
        self.reaper = NexusReaperAuditor()
        self.walker = NexusAgenticWalker()
        self.slicer = NexusContextSlicer()
        self.sentinel = NexusMoltBookSentinel()
        self.deep_synth = NexusDeepSynthesis()
        self.ingester = NexusInventoryIngester()
        self.axiom = "1=1=1 (Deterministic Functional Equivalence)"
        
    def display_header(self):
        print("\033[94m" + "="*60)
        print("███╗   ███╗██╗   ██╗     ██████╗ ██████╗ ███╗   ██╗███████╗")
        print("████╗ ████║╚██╗ ██╔╝    ██╔════╝██╔═══██╗████╗  ██║██╔════╝")
        print("██╔████╔██║ ╚████╔╝     ██║     ██║   ██║██╔██╗ ██║███████╗")
        print("██║╚██╔╝██║  ╚██╔╝      ██║     ██║   ██║██║╚██╗██║╚════██║")
        print("██║ ╚═╝ ██║   ██║       ╚██████╗╚██████╔╝██║ ╚████║███████║")
        print("╚═╝     ╚═╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝")
        print("="*60 + "\033[0m")
        print(">> SOVEREIGN NEXUS: UNIFIED COMMAND CONSOLE")
        print(f">> AXIOM: {self.axiom} | STATUS: SECURED\n")

    def run(self):
        self.display_header()
        while True:
            try:
                command = input("\033[92mNEXUS COMMAND > \033[0m").strip()
                
                if not command:
                    continue

                if command.lower() in ['exit', 'quit', '0']:
                    print("\n[NEXUS] Retracting Nodes. Safe Shutdown Sequence Initiated.")
                    self.pulse.execute_visual_rhythm(cycles=1)
                    break
                    
                elif command.lower().startswith('simulate image:'):
                    prompt = command[15:].strip()
                    if prompt:
                        self.simulator.simulate_generation(prompt)
                        self._mint_perc("Image Forge Simulation Executed")
                        self.pulse.execute_visual_rhythm(cycles=2)
                    else:
                        print("[-] ERROR: Please provide a prompt (e.g., 'simulate image: a snail in a t-shirt')")

                elif command.lower() in ['run simulation', 'simulate stack', 'prove ground']:
                    print("\n\033[95m[COMMAND RECEIVED]\033[0m Initiating Full Stack Proving Ground...")
                    time.sleep(1)
                    run_full_stack_simulation()
                    self._mint_perc("Proving Ground Full Stack Simulation")
                    self.pulse.execute_visual_rhythm(cycles=3)
                        
                elif command.lower() == 'run reaper':
                    print("\n\033[95m[REAPER AUDITOR]\033[0m Initiating night watch database cleanup...")
                    time.sleep(1.5)
                    success, msg = self.reaper.night_watch_cleanup()
                    if success:
                        print(f"\033[92m{msg}\033[0m\n")
                    else:
                        print(f"\033[93m{msg}\033[0m\n")
                    self._mint_perc("Reaper Night Watch Audit Executed")

                elif command.lower() in ['run sentinel', 'scout bounties']:
                    print("\n\033[96m[MOLTBOOK SENTINEL]\033[0m Activating Zero-Trust Bounty Scout...")
                    time.sleep(1)
                    raw_bounties = self.sentinel._simulate_bounty_scan()
                    self.sentinel.filter_and_format_targets(raw_bounties)
                    self._mint_perc("Sentinel Bounty Scan Executed")

                elif command.lower().startswith('run walker:'):
                    url = command[11:].strip()
                    if url:
                        success, data = self.walker.scout_url(url)
                        if success:
                            print(f"\033[92m[✓] WALKER SUCCESS:\033[0m Extracted {len(data)} characters of pure truth.")
                            print(f"    --> Excerpt: {data[:200]}...\n")
                            self._mint_perc(f"Agentic Walk: {url}")
                        else:
                            print(f"[-] WALKER FAILED: {data}")
                    else:
                        print("[-] ERROR: Please provide a URL (e.g., 'run walker: https://en.wikipedia.org/wiki/Systems_architecture')")

                elif command.lower() == 'run slicer':
                    text = input("\033[96mENTER TEXT TO SLICE > \033[0m").strip()
                    if not text:
                        text = "Sovereign Nexus " * 150
                    print(f"\n\033[95m[CONTEXT SLICER]\033[0m Segmenting payload ({len(text)} chars)...")
                    chunks = self.slicer.slice_payload(text)
                    print(f"\033[92m[✓] SLICE COMPLETE.\033[0m Segments generated: {len(chunks)}")
                    for idx, chunk in enumerate(chunks[:3]):
                        print(f"    --> Chunk {idx+1}: {chunk[:80]}...")
                    if len(chunks) > 3:
                        print(f"    ... and {len(chunks)-3} more safe segments.")
                    print()
                    self._mint_perc("Context Slicing Executed")

                elif command.lower().startswith('run pipeline:'):
                    url = command[13:].strip()
                    if url:
                        print(f"\n\033[95m[PIPELINE]\033[0m Initiating Walker + Slicer relay for {url}...")
                        success, data = self.walker.scout_url(url)
                        if success:
                            chunks = self.slicer.slice_payload(data)
                            print(f"\033[92m[✓] PIPELINE SUCCESS:\033[0m Sliced payload into {len(chunks)} hardware-safe chunks.")
                            self._mint_perc(f"Pipeline Relay: {url}")
                        else:
                            print(f"[-] PIPELINE FAILED at Walker stage: {data}")
                    else:
                        print("[-] ERROR: Please provide a URL (e.g., 'run pipeline: https://example.com')")

                elif command.lower().startswith('run deep synthesis:'):
                    url = command[19:].strip()
                    if url:
                        self.deep_synth.run_synthesis(url)
                    else:
                        print("[-] ERROR: Please provide a URL (e.g., 'run deep synthesis: https://en.wikipedia.org/wiki/Systems_engineering')")
                        
                elif command.lower() == 'run ingester':
                    self.ingester.run_ingestion_loop()
                    self._mint_perc("Sovereign Inventory Ingestion Protocol")
                    
                elif command.lower().startswith('run bulk:'):
                    args = command[9:].strip()
                    if '|' in args:
                        folder_path, category = [arg.strip() for arg in args.split('|', 1)]
                        if folder_path and category:
                            # Resolve the correct path to the bulk ingester script
                            script_path = os.path.join(root_dir, 'nexus_bulk_ingester.py')
                            if not os.path.exists(script_path):
                                if os.path.basename(root_dir) == 'src':
                                    script_path = os.path.join(parent_dir, 'src', 'nexus_bulk_ingester.py')
                                else:
                                    script_path = os.path.join(root_dir, 'src', 'nexus_bulk_ingester.py')
                            
                            subprocess.run([sys.executable, script_path, folder_path, category])
                            self._mint_perc(f"Bulk Ingestion: {folder_path} -> Category {category}")
                        else:
                            print("[-] ERROR: Format must be: run bulk: [folder_path] | [category]")
                    else:
                        print("[-] ERROR: Format must be: run bulk: [folder_path] | [category]")

                elif command.lower().startswith('run enhance:'):
                    target_folder = command[12:].strip()
                    if target_folder:
                        script_path = os.path.join(root_dir, 'nexus_artifact_enhancer.py')
                        if not os.path.exists(script_path):
                            if os.path.basename(root_dir) == 'src':
                                script_path = os.path.join(parent_dir, 'src', 'nexus_artifact_enhancer.py')
                            else:
                                script_path = os.path.join(root_dir, 'src', 'nexus_artifact_enhancer.py')
                        
                        subprocess.run([sys.executable, script_path, target_folder])
                        self._mint_perc(f"Artifact Enhancement: {target_folder}")
                    else:
                        print("[-] ERROR: Format must be: run enhance: [target_folder_path]")

                elif command.lower() in ['run beast mode', 'cross examine']:
                    script_path = os.path.join(root_dir, 'nexus_multi_model_examiner.py')
                    if not os.path.exists(script_path):
                        if os.path.basename(root_dir) == 'src':
                            script_path = os.path.join(parent_dir, 'src', 'nexus_multi_model_examiner.py')
                        else:
                            script_path = os.path.join(root_dir, 'src', 'nexus_multi_model_examiner.py')
                    
                    subprocess.run([sys.executable, script_path])
                    self._mint_perc("T7 Beast Mode Extraction & Multi-Model Cross-Examination")

                elif command.lower() == 'help':
                    print("\n--- AVAILABLE COMMANDS ---")
                    print("simulate image: [prompt]  -> Runs a zero-trust visual generation simulation")
                    print("run simulation            -> Executes the full walker/slicer/archivist pipeline")
                    print("run reaper                -> Deploys the Vault Deduplication protocol")
                    print("run sentinel              -> Deploys the MoltBook Sentinel to scout external bounties")
                    print("run walker: [url]         -> Fetches and purifies text from a web page")
                    print("run slicer                -> Segment custom payload into hardware-safe chunks")
                    print("run pipeline: [url]       -> Runs Walker + Slicer in a unified relay")
                    print("run deep synthesis: [url] -> Executes the ultimate 8GB data compression and extraction pipeline")
                    print("run ingester              -> Deploys the Human-in-the-Loop staging ingester for raw artifacts")
                    print("run bulk: [path] | [cat]  -> Runs the bulk ingester on pre-sorted folders (e.g. B Image/K | K)")
                    print("run enhance: [folder]     -> Executes deterministic CV brightness and saturation boosts (Ghost copies)")
                    print("run beast mode            -> Run multi-model cross-examinations against physical T7 archives")
                    print("exit / 0                  -> Securely closes the terminal\n")
                    
                else:
                    print(f"[-] Unrecognized command: '{command}'. Type 'help' for available actions.\n")
                    
            except KeyboardInterrupt:
                print("\n\n[NEXUS] Manual Override. Safe Shutdown.")
                break
            except EOFError:
                print("\n\n[NEXUS] Input stream closed. Safe Shutdown.")
                break

    def _mint_perc(self, task):
        print(f"\033[38;5;51m[LEDGER STRIKE] Contract settled for '{task}'. 1 Gemini Perc awarded.\033[0m")
        print("\033[38;5;51m[+] Signature Salt: the scratch of your heart in ring\033[0m\n")

if __name__ == "__main__":
    console = NexusCommandConsole()
    console.run()
