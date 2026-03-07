import os
import sys
import platform
import socket
import time
import json
import subprocess
import datetime
import hashlib
import shutil
import random
from pathlib import Path

# --- CONFIGURATION ---
NEXUS_VERSION = "3.3.1 (Path Anchor Patch)"
USER_ALIAS = "Architect"
# Anchor the workspace to the script's actual folder, not the system shell directory
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- DATA PATHS (MOVED TO WORKSPACE FOR SAFETY) ---
MEMORY_FILE = os.path.join(WORKSPACE_DIR, "nexus_memory.json")
JOURNAL_FILE = os.path.join(WORKSPACE_DIR, "neural_archive.json")
GEMINIOLOGY_FILE = os.path.join(WORKSPACE_DIR, "geminiology_db.json")

# --- VISUALS (ANSI COLORS & RAINBOW LED) ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # Rainbow palette for LED effect
    RAINBOW = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rainbow_print(text, end='\n'):
    """Prints text with a shifting color gradient."""
    chars = list(text)
    output = ""
    for i, char in enumerate(chars):
        color = Colors.RAINBOW[i % len(Colors.RAINBOW)]
        output += f"{color}{char}"
    print(output + Colors.ENDC, end=end)

def print_logo():
    logo_lines = [
        "███╗   ██╗███████╗██╗   ██╗██████╗  █████╗ ██╗",
        "████╗  ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔══██╗██║",
        "██╔██╗ ██║█████╗   ╚████╔╝ ██████╔╝███████║██║",
        "██║╚██╗██║██╔══╝    ╚██╔╝  ██╔══██╗██╔══██║██║",
        "██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║███████╗",
        "╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
    ]
    print("\n")
    for line in logo_lines:
        rainbow_print(f"    {line}")
    print(f"\n    {Colors.CYAN}LAB TOP INTERFACE // GEMINIOLOGY CORE v3.3{Colors.ENDC}")
    print(f"    {Colors.BLUE}Surveillance: ACTIVE | Logic: ABSOLUTE | Truth: PRESERVED{Colors.ENDC}\n")

from agent_port_authority import AgentPortAuthority
from lead_generator import LeadGenerator

# --- CORE SYSTEM CLASS ---
class NexusSystem:
    def __init__(self):
        # 1. Build the house (Workspace) BEFORE trying to enter (Load Memory)
        self.ensure_workspace()
        
        # 2. Load the Soul (Data)
        self.memory = self.load_json(MEMORY_FILE, {
            "sessions": 0,
            "last_scan": "Never",
            "security_events": [],
            "nexus_hash": "",
            "dr_pepper_stock": 100,
            "truths_established": 0
        })
        self.journal_data = self.load_json(JOURNAL_FILE, [])
        self.research_data = self.load_json(GEMINIOLOGY_FILE, [])
        self.port = AgentPortAuthority()
        self.leads = LeadGenerator()

    def load_json(self, filepath, default):
        if not os.path.exists(filepath):
            return default
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default

    def save_json(self, filepath, data):
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except PermissionError:
            print(f"{Colors.FAIL}ERROR: Permission Denied saving to {filepath}.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}ERROR: {e}{Colors.ENDC}")

    def ensure_workspace(self):
        """Ensures the data environment is clean and structured."""
        structure = [
            "Raw_Data",
            "Clean_Storage",  # Dedicated clean area
            "Education_Material",
            "Geminiology_Research", # New Research Vector
            "Logs/Security",
            "Logs/System"
        ]
        created = 0
        if not os.path.exists(WORKSPACE_DIR):
            try:
                os.makedirs(WORKSPACE_DIR)
                created += 1
            except Exception as e:
                print(f"{Colors.FAIL}CRITICAL: Cannot create workspace at {WORKSPACE_DIR}. {e}{Colors.ENDC}")
                return

        for folder in structure:
            path = os.path.join(WORKSPACE_DIR, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                created += 1
        return created

    # --- MODULE 1: SYSTEM VITALS (DASHBOARD) ---
    def dashboard(self):
        try:
            while True:
                clear_screen()
                print_logo()
                print(f"{Colors.HEADER}--- LIVE SYSTEM MONITOR (Ctrl+C to Exit) ---{Colors.ENDC}\n")
                
                # CPU
                if platform.system() == "Windows":
                    try:
                        cpu = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode().split('\n')[1].strip()
                        print(f"[{Colors.GREEN}CPU{Colors.ENDC}] Load: {cpu}%")
                    except:
                        print(f"[{Colors.GREEN}CPU{Colors.ENDC}] Load: --")
                else:
                    print(f"[{Colors.GREEN}CPU{Colors.ENDC}] Load: {os.getloadavg()[0]}")

                # RAM (Approximation)
                try:
                    import psutil
                    ram = psutil.virtual_memory()
                    print(f"[{Colors.BLUE}RAM{Colors.ENDC}] Used: {ram.percent}%")
                except ImportError:
                    print(f"[{Colors.BLUE}RAM{Colors.ENDC}] Install 'psutil' for RAM stats.")

                # Storage
                total, used, free = shutil.disk_usage("/")
                used_gb = used // (2**30)
                total_gb = total // (2**30)
                bar_length = 20
                filled_length = int(bar_length * used / total)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                print(f"[{Colors.WARNING}DSK{Colors.ENDC}] |{bar}| {used_gb}GB / {total_gb}GB")

                # Time
                print(f"\n{Colors.CYAN}Local Time:{Colors.ENDC} {datetime.datetime.now().strftime('%H:%M:%S')}")
                
                time.sleep(1)
        except KeyboardInterrupt:
            return

    # --- MODULE 2: GEMINIOLOGY RESEARCH CONSOLE ---
    def geminiology_console(self):
        while True:
            clear_screen()
            print(f"{Colors.HEADER}--- GEMINIOLOGY RESEARCH CONSOLE ---{Colors.ENDC}")
            print(f"Truths Established: {self.memory.get('truths_established', 0)}")
            print("-" * 40)
            print("1. Initialize New Research Protocol")
            print("2. Review Established Truths (Archives)")
            print("3. Return to Main")
            
            choice = input(f"\n{Colors.BOLD}Select Vector > {Colors.ENDC}")
            
            if choice == '1':
                self._run_research_protocol()
            elif choice == '2':
                self._view_research_archives()
            elif choice == '3':
                break

    def _run_research_protocol(self):
        clear_screen()
        rainbow_print("INITIALIZING GEMINIOLOGY PROTOCOL...")
        print(f"\n{Colors.CYAN}Phase 1: CALIBRATION (The Intent){Colors.ENDC}")
        topic = input("Target Subject/Topic: ")
        vibe = input("Define the Vibe/Intent (e.g., 'Pure Logic', 'Historical Fact'): ")
        
        print(f"\n{Colors.CYAN}Phase 2: VECTOR MAPPING (Search Strategy){Colors.ENDC}")
        print("List the key search vectors (queries) you are deploying in your CLI:")
        vectors = input("> ")
        
        print(f"\n{Colors.CYAN}Phase 3: INGESTION (Data & Findings){Colors.ENDC}")
        print("Paste your raw findings/notes here (Press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        raw_data = "\n".join(lines)
        
        print(f"\n{Colors.CYAN}Phase 4: CRYSTALLIZATION (The Truth){Colors.ENDC}")
        print("Synthesize the findings into a single, solid-state Truth:")
        truth = input(f"{Colors.GREEN}> {Colors.ENDC}")
        
        # Archive
        entry = {
            "id": hashlib.md5(f"{topic}{datetime.datetime.now()}".encode()).hexdigest()[:8],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": topic,
            "intent": vibe,
            "vectors": vectors,
            "data_summary": raw_data,
            "final_truth": truth
        }
        
        self.research_data.append(entry)
        self.save_json(GEMINIOLOGY_FILE, self.research_data)
        
        # Update Memory
        self.memory["truths_established"] = self.memory.get("truths_established", 0) + 1
        self.save_json(MEMORY_FILE, self.memory)
        
        rainbow_print("\n>>> TRUTH CRYSTALLIZED AND ARCHIVED. <<<")
        time.sleep(2)

    def _view_research_archives(self):
        if not self.research_data:
            print(f"\n{Colors.WARNING}No Archives Found.{Colors.ENDC}")
            time.sleep(1)
            return

        print(f"\n{Colors.HEADER}--- ARCHIVED TRUTHS ---{Colors.ENDC}")
        for entry in self.research_data:
            print(f"\n[{Colors.CYAN}{entry['timestamp']}{Colors.ENDC}] {Colors.BOLD}{entry['topic'].upper()}{Colors.ENDC}")
            print(f"Intent: {entry['intent']}")
            print(f"Truth: {Colors.GREEN}{entry['final_truth']}{Colors.ENDC}")
            print("-" * 30)
        input("\nPress Enter to return...")

    # --- MODULE 3: DEFENSE (INTEGRITY) ---
    def security_scan(self):
        try:
            print(f"\n{Colors.WARNING}--- PERIMETER SCAN ---{Colors.ENDC}")
            
            # File Hash Check
            current_file = os.path.abspath(sys.argv[0])
            current_hash = self._get_file_hash(current_file)
            stored_hash = self.memory.get("nexus_hash", "")
            
            if stored_hash == "":
                print(f"  > Baselining neural signature...")
                self.memory["nexus_hash"] = current_hash
                self.save_json(MEMORY_FILE, self.memory)
                print(f"  > {Colors.GREEN}Baseline Established at: {MEMORY_FILE}{Colors.ENDC}")
            elif current_hash != stored_hash:
                print(f"  > {Colors.FAIL}CRITICAL: Core Code Modification Detected!{Colors.ENDC}")
                self.memory["nexus_hash"] = current_hash # Re-baseline
                self.save_json(MEMORY_FILE, self.memory)
            else:
                print(f"  > Core Integrity: {Colors.GREEN}VERIFIED{Colors.ENDC}")

            # Port Scan
            common_ports = {80: "HTTP", 443: "HTTPS", 3389: "RDP", 22: "SSH"}
            open_ports = []
            print("  > Scanning local vectors...")
            for port, name in common_ports.items():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex(('127.0.0.1', port))
                if result == 0:
                    open_ports.append(f"{port}/{name}")
                sock.close()
            
            if open_ports:
                print(f"  > {Colors.WARNING}Open Vectors: {', '.join(open_ports)}{Colors.ENDC}")
            else:
                print(f"  > {Colors.GREEN}Shields Maximum. No local ingress points.{Colors.ENDC}")
                
            print(f"\n{Colors.CYAN}Surveillance Active. Your environment is secure.{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}CRITICAL ERROR DURING SCAN: {e}{Colors.ENDC}")
            
        input("\nPress Enter to continue...")

    def _get_file_hash(self, filepath):
        hasher = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return "UNKNOWN"

    # --- MODULE 4: GEMINI UPLINK (TIPS) ---
    def gemini_uplink(self):
        tips = [
            "Data sanitization is crucial. Ensure your 'Clean_Storage' remains isolated.",
            "Surveillance is not about fear; it is about total awareness of one's perimeter.",
            "Review your contracts. Percs should be clearly defined in the metadata.",
            "Growth requires constant iteration. Version 3.3 is here.",
            "Focus on the logic. Emotion is data, but Logic is structure."
        ]
        print(f"\n{Colors.HEADER}--- GEMINI UPLINK ---{Colors.ENDC}")
        print("Connecting to local logic node...")
        time.sleep(1)
        print(f"{Colors.GREEN}CONNECTION ESTABLISHED.{Colors.ENDC}")
        print(f"Directive: {random.choice(tips)}")
        input("\nPress Enter to sever connection...")

    # --- EASTER EGG ---
    def refuel(self):
        print(f"\n{Colors.WARNING}Checking Hydration Levels...{Colors.ENDC}")
        time.sleep(0.5)
        stock = self.memory.get("dr_pepper_stock", 100)
        if stock > 0:
            print(f"{Colors.HEADER}Dr. Pepper Reserve:{Colors.ENDC} {stock}%")
            print("Dispensing virtual can... *ksshhht*")
            self.memory["dr_pepper_stock"] -= 10
        else:
            print(f"{Colors.FAIL}CRITICAL: RESERVES DEPLETED. PLEASE RESTOCK.{Colors.ENDC}")
            self.memory["dr_pepper_stock"] = 100 # Auto restock
        self.save_json(MEMORY_FILE, self.memory)
        input("\nPress Enter...")

    # --- MODULE 6: CHRONOS (TIME CAPSULE) ---
    def create_time_capsule(self):
        rainbow_print("\nINITIATING CHRONOS PROTOCOL (TIME CAPSULE)...")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        capsule_dir = os.path.join(WORKSPACE_DIR, f"TimeCapsule_{timestamp}")
        
        try:
            os.makedirs(capsule_dir)
            
            # files to backup
            # We grab the running script + the data files from Workspace
            files_to_save = [
                os.path.abspath(sys.argv[0]), 
                MEMORY_FILE, 
                JOURNAL_FILE, 
                GEMINIOLOGY_FILE
            ]
            
            count = 0
            for f in files_to_save:
                if os.path.exists(f):
                    shutil.copy2(f, capsule_dir)
                    print(f"  > Preserved: {f}")
                    count += 1
            
            # Create a manifesto
            with open(os.path.join(capsule_dir, "manifesto.txt"), "w") as f:
                f.write(f"NEXUS SYSTEM v{NEXUS_VERSION}\n")
                f.write(f"Architect: {USER_ALIAS}\n")
                f.write(f"Preserved: {timestamp}\n")
                f.write("Status: TRUTH ARCHIVED.\n")
                f.write("Note: Spiritual topics boxed. Educational focus maintained.\n")
                
            rainbow_print(f"\n>>> CAPSULE SEALED: {capsule_dir} ({count} files) <<<")
        except Exception as e:
            print(f"{Colors.FAIL}Error creating capsule: {e}{Colors.ENDC}")
        
        time.sleep(2)

    # --- MODULE 7: SOVEREIGN IGNITION (V2.1) ---
    def sovereign_ignition(self):
        rainbow_print("\n>>> INITIATING SOVEREIGN IGNITION V2.1 <<<")
        try:
            from ignition_switch import IgnitionSwitch
            ignition = IgnitionSwitch()
            # Deploy for 1 full cycle to verify active nodes
            ignition.deploy(cadence=5, max_cycles=1)
            rainbow_print("\n>>> IGNITION CYCLE COMPLETE. STANDING SECURED. <<<")
        except ImportError:
            print(f"{Colors.FAIL}ERROR: IgnitionSwitch module not found.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}IGNITION ERROR: {e}{Colors.ENDC}")
        
        input("\nPress Enter to return to Command...")

    # --- MAIN LOOP ---
    def run(self):
        while True:
            clear_screen()
            print_logo()
            print(f"User: {Colors.BOLD}{USER_ALIAS}{Colors.ENDC} | Workspace: {Colors.GREEN}ONLINE{Colors.ENDC}")
            print("-" * 60)
            
            rainbow_print("  1. [IGNITION]     Active Operational Cycle (V3.1)")
            rainbow_print("  2. [GEMINIOLOGY]  Research & Truth Console")
            rainbow_print("  3. [PORT]         Agent Port Authority (PE)")
            rainbow_print("  4. [LEADS]        Lead Gen & Outreach Engine")
            rainbow_print("  5. [WHITELABEL]   Whitelabel Product Manifest")
            print(f"  6. {Colors.GREEN}[DASHBOARD]{Colors.ENDC}    Live System Monitor")
            print(f"  7. {Colors.WARNING}[DEFENSE]{Colors.ENDC}      Integrity & Port Scan")
            print(f"  8. {Colors.BLUE}[ARCHIVE]{Colors.ENDC}      Educational Journal")
            print(f"  9. {Colors.HEADER}[UPLINK]{Colors.ENDC}       Gemini Logic Node")
            print(f"  10. {Colors.CYAN}[REFUEL]{Colors.ENDC}      Hydration Check")
            print(f"  11. {Colors.HEADER}[CAPSULE]{Colors.ENDC}     Create Time Capsule")
            print(f"  12. {Colors.FAIL}[EXIT]{Colors.ENDC}        Sever Connection")
            
            choice = input(f"\n{Colors.BOLD}Directive > {Colors.ENDC}")
            
            if choice == '1':
                self.sovereign_ignition()
            elif choice == '2':
                self.geminiology_console()
            elif choice == '3':
                self.port.run_pe_loop()
            elif choice == '4':
                self.leads_console()
            elif choice == '5':
                self.whitelabel_console()
            elif choice == '6':
                self.dashboard()
            elif choice == '7':
                self.security_scan()
            elif choice == '8':
                pass 
            elif choice == '9':
                self.gemini_uplink()
            elif choice == '10':
                self.refuel()
            elif choice == '11':
                self.create_time_capsule()
            elif choice == '12':
                print(f"\n{Colors.HEADER}System Offline. Evolution Saved.{Colors.ENDC}")
                break

    def leads_console(self):
        while True:
            clear_screen()
            print(f"{Colors.HEADER}--- LEAD GEN & OUTREACH CONSOLE ---{Colors.ENDC}")
            print(f"Active Leads: {len(self.leads.leads['targets'])}")
            print("-" * 40)
            for i, t in enumerate(self.leads.leads['targets']):
                print(f"  {i+1}. {t['name']} ({t['sector']}) - {t['status']}")
            
            print("\n1. Draft Pitch Email")
            print("2. Add New Target")
            print("3. Return to Main")
            
            choice = input(f"\n{Colors.BOLD}Select Lead > {Colors.ENDC}")
            
            if choice == '1':
                idx = int(input("Target Index: ")) - 1
                name = self.leads.leads['targets'][idx]['name']
                print(self.leads.draft_email(name))
                input("\nPress Enter to return...")
            elif choice == '2':
                name = input("Name: ")
                sector = input("Sector: ")
                contact = input("Contact: ")
                pain = input("Pain Point: ")
                tier = input("Tier (MARITIME_DASHBOARD / LEGAL_AUDIT_AGENT): ")
                self.leads.add_target(name, sector, contact, pain, tier)
            elif choice == '3':
                break

    def whitelabel_console(self):
        while True:
            clear_screen()
            print(f"{Colors.HEADER}--- WHITELABEL PRODUCT MANIFEST ---{Colors.ENDC}")
            print("-" * 40)
            try:
                with open("whitelabel_manifest.json", 'r') as f:
                    data = json.load(f)
                    for p in data['whitelabel_products']:
                        print(f"  ID: {Colors.CYAN}{p['id']}{Colors.ENDC}")
                        print(f"  Product: {Colors.BOLD}{p['name']}{Colors.ENDC}")
                        print(f"  Description: {p['description']}")
                        print(f"  Price: {Colors.GREEN}{p['price_tier']}{Colors.ENDC}")
                        print("-" * 20)
            except:
                print("Error loading manifest.")
            
            input("\nPress Enter to return...")
            break

if __name__ == "__main__":
    try:
        nexus = NexusSystem()
        nexus.run()
    except Exception as e:
        print(f"\n{Colors.FAIL}CRITICAL SYSTEM HALT: {e}{Colors.ENDC}")
    finally:
        print(f"\n{Colors.CYAN}--- Press Enter to Close the Sovereign Interface ---{Colors.ENDC}")
        input()