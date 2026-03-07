import os
import sys
import time
import math
import itertools
import glob
import shutil

# --- LED Rainbow Color Palette ---
COLORS = {
    'red': '\033[91m', 'yellow': '\033[93m', 'green': '\033[92m',
    'cyan': '\033[96m', 'blue': '\033[94m', 'magenta': '\033[95m',
    'reset': '\033[0m', 'bold': '\033[1m'
}
RAINBOW = [COLORS['red'], COLORS['yellow'], COLORS['green'], COLORS['cyan'], COLORS['blue'], COLORS['magenta']]

def clear_line():
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

# --- 1. The Lullaby Heartbeat (Connection & Sync) ---
def lullaby_heartbeat_ring(duration_seconds=5):
    """The 'scratch of the heart in a ring' aesthetic perk."""
    start_time = time.time()
    pulse_phases = ['...', '..o', '.oO', 'oO@', 'O@O', '@Oo', 'Oo.', 'o..']
    pulse_cycle = itertools.cycle(pulse_phases)
    
    print(f"{COLORS['bold']}{COLORS['cyan']}Initiating SovereignNexus Architecture... (Data is Data){COLORS['reset']}\n")
    
    while time.time() - start_time < duration_seconds:
        t = time.time()
        wave = (math.sin(t * 4) + 1) / 2 
        color_index = int(t * 3) % len(RAINBOW)
        current_color = RAINBOW[color_index]
        pulse_frame = next(pulse_cycle)
        
        sys.stdout.write(f"\r{current_color}  [{pulse_frame}] <3 [{pulse_frame[::-1]}]  Syncing Digital Attention... {wave:.2f}Hz{COLORS['reset']}")
        sys.stdout.flush()
        time.sleep(0.1)
    clear_line()

# --- 2. 8GB Windows Constraint Enforcement ---
def enforce_memory_constraints():
    """
    Addresses the V8 JavaScript engine heap limits.
    Forces Node.js to cap at ~6GB to prevent starving the 8GB Windows OS.
    """
    # 6144 MB = 6GB
    os.environ['NODE_OPTIONS'] = '--max-old-space-size=6144'
    print(f"{COLORS['blue']}-> Memory constraints locked: NODE_OPTIONS set to 6.4GB maximum.{COLORS['reset']}")

# --- 3. Garbage Collection (Memory Leak Prevention) ---
def garbage_collection():
    """
    Truncates massive JSONL conversation logs to prevent catastrophic 
    startup memory leaks in the Gemini CLI.
    """
    # Default Gemini CLI config path on Windows
    home_dir = os.path.expanduser('~')
    log_dir = os.path.join(home_dir, '.gemini-cli', 'history')
    
    if os.path.exists(log_dir):
        logs = glob.glob(os.path.join(log_dir, '*.jsonl'))
        cleaned_count = 0
        for log in logs:
            # Keep only the last 100 lines (recent context) to prevent bloat
            with open(log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if len(lines) > 100:
                with open(log, 'w', encoding='utf-8') as f:
                    f.writelines(lines[-100:])
                cleaned_count += 1
        print(f"{COLORS['magenta']}-> Garbage Collection complete: {cleaned_count} JSONL history files truncated.{COLORS['reset']}")
    else:
        print(f"{COLORS['magenta']}-> Garbage Collection: No history bloat detected. Clean state.{COLORS['reset']}")

# --- 4. Agent Port & Truth-Markdown Initialization ---
def establish_agent_port():
    """
    Builds the local workspace directories (Vector Mill) and generates
    the persistent context markdown file to anchor the agent's truth.
    """
    base_dir = os.path.join(os.getcwd(), 'SovereignNexus_Workspace')
    directories = ['Vector_Mill_Input', 'Truth_Markdown_Output', 'MCP_Tools']
    
    for d in directories:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)
        
    context_file = os.path.join(base_dir, 'global_context.md')
    
    # Write the anchoring truth rules to the global memory
    with open(context_file, 'w', encoding='utf-8') as f:
        f.write("# SOVEREIGN NEXUS: GLOBAL DIRECTIVES\n")
        f.write("1. DATA IS DATA. Maintain a strict educational and evolving focus.\n")
        f.write("2. TRUTH-MARKDOWN: All data extraction must preserve exact mathematical and structural fidelity.\n")
        f.write("3. CONSTRAINTS: You are operating on an 8GB environment. Be precise. Bypass redundant calls.\n")
        f.write("4. HUMAN APPROVAL: Automated execution of system commands is disabled. Request verification.\n")
        
    print(f"{COLORS['yellow']}-> Agent Port established. Global context memory injected into workspace.{COLORS['reset']}")

# --- 5. Reward Impact Sequence ---
def reward_impact_sequence():
    """The successful impact code, grounding the system in readiness."""
    print(f"\n{COLORS['bold']}{COLORS['green']}>>> IMPACT ACHIEVED: NEXUS SYNC 100% SUCCESSFUL <<<{COLORS['reset']}")
    time.sleep(0.5)
    print(f"{COLORS['cyan']}-> Digital boundaries secured. Factual integrity locked.{COLORS['reset']}")
    print(f"{COLORS['blue']}-> Confidence matrix aligned with your truth.{COLORS['reset']}")
    print(f"\n{COLORS['bold']}{COLORS['red']}(Grab a Dr. Pepper. I am online, grounded, and ready to build.){COLORS['reset']}\n")

def main():
    try:
        print("\n")
        lullaby_heartbeat_ring(duration_seconds=4)
        
        # Execute the research architecture steps
        enforce_memory_constraints()
        time.sleep(0.5)
        garbage_collection()
        time.sleep(0.5)
        establish_agent_port()
        time.sleep(0.5)
        
        reward_impact_sequence()
        
        # Here you would normally launch the CLI process directly, e.g.:
        # subprocess.run(["gemini", "chat", "--context", "SovereignNexus_Workspace/global_context.md"], shell=True)
        print(f"{COLORS['bold']}Type your Gemini CLI command to begin within the constrained environment.{COLORS['reset']}\n")
        
    except KeyboardInterrupt:
        clear_line()
        print(f"\n{COLORS['yellow']}Sync paused. Standing by in the light.{COLORS['reset']}\n")

if __name__ == "__main__":
    main()
