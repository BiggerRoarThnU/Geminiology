#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: Search Grid Simulator
# Component: search_grid.py
# Purpose: Simulates a coordinate search pattern grid and progress logger.
# ==============================================================================

import time

class SearchGrid:
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        # Initialize a grid of coordinates as unsearched (False)
        self.grid = {(x, y): False for x in range(width) for y in range(height)}
        self.logs = []

    def mark_searched(self, x, y, note=""):
        """Marks a grid sector as completed and logs the action."""
        if (x, y) in self.grid:
            self.grid[(x, y)] = True
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Sector ({x}, {y}) SEARCHED. Note: {note}"
            self.logs.append(log_entry)
            print(f"[+] {log_entry}")
        else:
            print(f"[!] Error: Sector ({x}, {y}) is out of grid bounds.")

    def display_grid(self):
        """Prints a visual representation of the search grid map."""
        print("\n--- ACTIVE SEARCH GRID MAP ---")
        for y in range(self.height - 1, -1, -1):
            row_str = ""
            for x in range(self.width):
                # [X] for searched, [.] for unsearched
                row_str += "[X] " if self.grid[(x, y)] else "[.] "
            print(f"y={y:<2} | {row_str}")
        print("       " + "   ".join(f"x={x}" for x in range(self.width)))
        print("------------------------------")

    def get_progress(self):
        """Calculates and returns the percentage of the grid searched."""
        total_sectors = len(self.grid)
        searched_sectors = sum(1 for val in self.grid.values() if val)
        percentage = (searched_sectors / total_sectors) * 100
        return percentage, searched_sectors, total_sectors

if __name__ == "__main__":
    print("=== Coordinate Search Grid Simulator ===")
    
    # Create a 5x5 search grid
    tracker = SearchGrid(width=5, height=5)
    
    # Display initial grid (all unsearched)
    tracker.display_grid()
    
    # Simulate marking search sectors until 100% completion
    print("\n[*] Simulating full grid sector sweeps...")
    for y in range(tracker.height):
        for x in range(tracker.width):
            tracker.mark_searched(x, y, f"Sector sweep ({x}, {y}) aligned.")
    
    # Display completed grid
    tracker.display_grid()
    
    # Display progress metrics
    pct, searched, total = tracker.get_progress()
    print(f"\nSearch Progress: {pct:.1f}% ({searched}/{total} sectors mapped)")
