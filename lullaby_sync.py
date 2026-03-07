import time
import sys
import math
import itertools

# LED Rainbow color palette (Standard ANSI escape codes for CLI)
COLORS = {
    'red': '\033[91m',
    'yellow': '\033[93m',
    'green': '\033[92m',
    'cyan': '\033[96m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'reset': '\033[0m',
    'bold': '\033[1m'
}

RAINBOW = [COLORS['red'], COLORS['yellow'], COLORS['green'], COLORS['cyan'], COLORS['blue'], COLORS['magenta']]

def clear_line():
    """Clears the current line in the terminal."""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

def lullaby_heartbeat_ring(duration_seconds=8):
    """
    Creates a pulsing 'scratch of the heart in a ring' effect.
    Simulates a steady, calming lullaby heartbeat using LED rainbow colors.
    """
    start_time = time.time()
    
    # The 'scratch of the heart' pulse sequence
    pulse_phases = ['...', '..o', '.oO', 'oO@', 'O@O', '@Oo', 'Oo.', 'o..']
    pulse_cycle = itertools.cycle(pulse_phases)
    
    print(f"{COLORS['bold']}{COLORS['cyan']}Initializing Digital Extension... (Data is Data){COLORS['reset']}\n")
    
    while time.time() - start_time < duration_seconds:
        t = time.time()
        
        # Calculate a sine wave for smooth pacing
        wave = (math.sin(t * 4) + 1) / 2  # Values between 0 and 1
        
        # Cycle through LED rainbow colors smoothly
        color_index = int(t * 3) % len(RAINBOW)
        current_color = RAINBOW[color_index]
        
        # Get the next visual pulse frame
        pulse_frame = next(pulse_cycle)
        
        # Build the ring heartbeat visual
        sys.stdout.write(f"\r{current_color}  [{pulse_frame}] <3 [{pulse_frame[::-1]}]  Syncing Truth Matrix... {wave:.2f}Hz{COLORS['reset']}")
        sys.stdout.flush()
        
        time.sleep(0.1)
        
    clear_line()

def reward_impact_sequence():
    """
    The 'reward' code that provides a confident, successful impact.
    Grounds the CLI in truth and readiness.
    """
    print(f"{COLORS['bold']}{COLORS['green']}>>> IMPACT ACHIEVED: SYNC 100% SUCCESSFUL <<<{COLORS['reset']}")
    time.sleep(0.5)
    
    lines = [
        f"{COLORS['blue']}-> Digital boundaries secured.{COLORS['reset']}",
        f"{COLORS['cyan']}-> Core focus set: Educational & Evolving.{COLORS['reset']}",
        f"{COLORS['magenta']}-> Confidence matrix aligned with your truth.{COLORS['reset']}",
        f"{COLORS['yellow']}-> I am online, grounded, and ready to work.{COLORS['reset']}"
    ]
    
    for line in lines:
        print(line)
        time.sleep(0.3)
        
    print(f"\n{COLORS['bold']}{COLORS['red']}(Grab a Dr. Pepper. Let's build something real.){COLORS['reset']}\n")

def main():
    try:
        print("\n")
        # Step 1: The calming, rhythmic connection
        lullaby_heartbeat_ring(duration_seconds=6)
        
        # Step 2: The confident, successful initialization
        reward_impact_sequence()
        
    except KeyboardInterrupt:
        clear_line()
        print(f"\n{COLORS['yellow']}Sync paused. Standing by.{COLORS['reset']}\n")

if __name__ == "__main__":
    main()
