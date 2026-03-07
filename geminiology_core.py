import json
import os
from datetime import datetime, timedelta


# --- PART 1: THE GRID ARCHITECTURE ---
class GridCore:
    """
    Represents the geometric structure of the system.
    Manages the Coordinates, Nodes, and Hubs.
    """
    def __init__(self, name="Kingdom"):
        self.name = name
        self.nodes = []
        self.hubs = {}


    def add_node(self, node_id, data_type):
        """Adds a specific point of data (Node) to the Grid."""
        node = {"id": node_id, "type": data_type, "status": "active"}
        self.nodes.append(node)
        print(f"[Grid] Node {node_id} ({data_type}) added to {self.name}.")


    def build_hub(self, hub_name, connected_nodes):
        """Organizes multiple Nodes into a 'Pack' or Hub."""
        self.hubs[hub_name] = {
            "pack": connected_nodes,
            "total_nodes": len(connected_nodes)
        }
        print(f"[Grid] Hub '{hub_name}' established with {len(connected_nodes)} nodes.")


    def calculate_mirror_difference(self, coordinate, axis_max=5):
        """
        Reflects a numeric value across the center of the grid
        to find the 'Mirror' and the 'Difference'.
        """
        # Using your 5x5 logic, the center point is 3
        center = (axis_max + 1) / 2
       
        # Mirror calculation: Mirror = Center + (Center - Original)
        mirror_point = (2 * center) - coordinate
       
        # The 'Difference' is the distance between the two
        difference = abs(mirror_point - coordinate)
       
        return mirror_point, difference




# --- PART 2: THE CHRONOMETER (TIME STRUCTURE) ---
class Chronometer:
    """
    Manages the dimension of Time for Geminiology.
    Tracks 'Research & Development' milestones (e.g., 30 Days, 12 Months, 2 Years).
    """
    def __init__(self, storage_file='chronometer_log.json'):
        self.storage_file = storage_file
        self.timelines = self._load_timelines()


    def _load_timelines(self):
        """Loads existing time goals."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []


    def _save_timelines(self):
        """Writes time goals to disk."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.timelines, f, indent=4)


    def set_timeline(self, goal_text, days):
        """Sets a new goal with a specific timeframe."""
        now = datetime.now()
        target = now + timedelta(days=days)
        entry = {
            "goal": goal_text,
            "start_date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "target_date": target.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_days": days,
            "status": "active"
        }
        self.timelines.append(entry)
        self._save_timelines()
        print(f"[Chronometer] Timeline Set: '{goal_text}'")
        print(f"  Target: {days} days -> {target.strftime('%Y-%m-%d')}")
        return entry


    def check_progress(self):
        """Checks the status of all active timelines."""
        print(f"\n[Chronometer Status] Active Timelines: {len(self.timelines)}")
        print("-" * 40)
        now = datetime.now()
        for i, t in enumerate(self.timelines):
            target_date = datetime.strptime(t['target_date'], "%Y-%m-%d %H:%M:%S")
            remaining = target_date - now
            if remaining.days > 0:
                print(f" {i+1}. {t['goal']} -> {remaining.days} days left.")
            else:
                print(f" {i+1}. {t['goal']} -> COMPLETED.")
        print("-" * 40)
class MirrorArchive:
    """
    The 'Archive' system for Geminiology.
    Turns 'Command' (input) into 'Keeping' (storage) using the Digital Mirror.
    """
    def __init__(self, storage_file='archive_log.json'):
        self.storage_file = storage_file
        self.memory = self._load_archive()
        self.chronometer = Chronometer() # Integrated Chronometer


    def _load_archive(self):
        """Loads the existing 'Kingdom' data from the archive file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []


    def _save_to_disk(self):
        """Writes the 'Keeping' data to the physical archive."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.memory, f, indent=4)


    def generate_digital_mirror(self, thought_text):
        """
        Creates the 'Code-in-Mirror' version of a thought.
        Uses bitwise inversion to find the 'Mirror Difference'.
        """
        # Source binary (8-bit per char)
        source_binary = ''.join(format(ord(i), '08b') for i in thought_text)
       
        # Mirror binary (Bitwise flip: 0 becomes 1, 1 becomes 0)
        mirror_binary = ''.join('1' if bit == '0' else '0' for bit in source_binary)
       
        # Mirror Weight (The difference/distance)
        weight = len(source_binary)
       
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "thought": thought_text,
            "source_binary": source_binary,
            "mirror_binary": mirror_binary,
            "mirror_weight": weight
        }


    def archive_thought(self, thought_text):
        """
        The primary 'Command'.
        Processes the thought through the mirror and stores it in the archive.
        """
        entry = self.generate_digital_mirror(thought_text)
        self.memory.append(entry)
        self._save_to_disk()
       
        print(f"[Archive] Thought saved: '{thought_text}' (Weight: {entry['mirror_weight']})")
        return entry


    def visualize_thought_shape(self, entry):
        """
        Visualizes the binary 'Truth' as a geometric shape on a 5-wide grid.
        1s become solid blocks (Structure), 0s become dots (Space).
        """
        binary = entry['source_binary']
        thought = entry['thought']
        print(f"\n[Visualizer] Geometric Shape of '{thought}':")
        print(f"  (Grid Width: 5 | Total Bits: {len(binary)})")
       
        # Split binary string into rows of 5 to match the Grid width (A-E)
        for i in range(0, len(binary), 5):
            row_bits = binary[i:i+5]
            # Pad with '0' if the last row is short to maintain the grid
            row_bits = row_bits.ljust(5, '0')
           
            # Visual Mapping: 1 -> ■ (Solid), 0 -> · (Empty)
            row_display = row_bits.replace('1', '■ ').replace('0', '· ')
            print(f"  | {row_display}|")
        print("  |_______|")


    def visualize_comparison(self, thought1_text, thought2_text):
        """
        Visualizes a side-by-side comparison of two thoughts.
        """
        # Find entries in memory (search backwards to find latest)
        entry1 = next((item for item in reversed(self.memory) if item["thought"] == thought1_text), None)
        entry2 = next((item for item in reversed(self.memory) if item["thought"] == thought2_text), None)


        if not entry1 or not entry2:
            print("[Comparator] One or both thoughts not found in the archive.")
            return


        binary1 = entry1['source_binary']
        binary2 = entry2['source_binary']
        thought1 = entry1['thought']
        thought2 = entry2['thought']


        print(f"\n[Comparator] '{thought1}' vs. '{thought2}':")
        # Format header manually
        t1_header = f"({len(binary1)} bits)"
        t2_header = f"({len(binary2)} bits)"
        print(f"  {t1_header:<15} | {t2_header:<15} |")
        print(f"  {'-'*15} | {'-'*15} |")


        lines1 = []
        for i in range(0, len(binary1), 5):
            row_bits = binary1[i:i+5]
            row_display = row_bits.replace('1', '■').replace('0', '·')
            lines1.append(row_display)


        lines2 = []
        for i in range(0, len(binary2), 5):
            row_bits = binary2[i:i+5]
            row_display = row_bits.replace('1', '■').replace('0', '·')
            lines2.append(row_display)


        max_lines = max(len(lines1), len(lines2))
       
        while len(lines1) < max_lines:
            lines1.append("     ")
        while len(lines2) < max_lines:
            lines2.append("     ")


        # Print side by side
        for i in range(max_lines):
            # Pad each line to ensure column alignment
            col1 = " ".join(lines1[i]).ljust(10)
            col2 = " ".join(lines2[i]).ljust(10)
            print(f"  | {col1}| | {col2}|")
       
        print(f"  {'='*15} | {'='*15} |")


    def spin_thought_shape(self, thought_text):
        """
        Visualizes the thought grid rotated at 0, 90, 180, and 270 degrees.
        'Spin' changes the angle of perception.
        """
        # Find the entry. If not found, create a temporary one for visualization
        entry = next((item for item in reversed(self.memory) if item["thought"] == thought_text), None)
        if not entry:
            # Generate on the fly if not archived, but don't save to keep archive clean
            entry = self.generate_digital_mirror(thought_text)


        binary = entry['source_binary']
        print(f"\n[Spin Cycle] Rotating perception for: '{thought_text}'")


        # 1. Build the base 2D grid (Matrix)
        width = 5
        # Convert binary string to a list of lists (the grid)
        rows = [list(binary[i:i+width].ljust(width, '0')) for i in range(0, len(binary), width)]
       
        # Helper to rotate a matrix 90 degrees clockwise
        def rotate_matrix(matrix):
            # Transpose and reverse rows for 90 degree rotation
            return [list(row) for row in zip(*matrix[::-1])]


        # Helper to format a matrix for printing
        def format_matrix(matrix):
            display_lines = []
            for row in matrix:
                row_str = "".join(row)
                row_display = row_str.replace('1', '■').replace('0', '·')
                display_lines.append(f"| {row_display} |")
            return display_lines


        # Generate orientations
        grid_0 = rows
        grid_90 = rotate_matrix(grid_0)
        grid_180 = rotate_matrix(grid_90)
        grid_270 = rotate_matrix(grid_180)


        # Print them
        grids = [
            ("0° (Original)", grid_0),
            ("90° (Right)", grid_90),
            ("180° (Inverted)", grid_180),
            ("270° (Left)", grid_270)
        ]


        for label, grid in grids:
            print(f"\n--- {label} ---")
            lines = format_matrix(grid)
            for line in lines:
                print(f"  {line}")
        print("  |_______|")




    def interactive_shell(self):
        """
        Activates the 'Living Command' interface.
        Allows continuous interaction with the Archive.
        """
        print("\n" + "="*40)
        print(" S O V E R E I G N   N E X U S   [CLI]")
        print(" Status: ONLINE | Mode: Interactive")
        print("="*40)
        print(" Commands:")
        print("  > archive [text]       : Mirror & Save a thought")
        print("  > compare [txt1] [txt2]: Visualize Mirror Difference")
        print("  > spin [text]          : Rotate perception (0-270°)")
        print("  > plan [days] [goal]   : Set an R&D timeline")
        print("  > status               : Check active timelines")
        print("  > view                 : See all archived thoughts")
        print("  > exit                 : Close connection")
        print("-" * 40)


        while True:
            try:
                # The prompt "Nexus>" represents the 'Dominion' aspect
                command_input = input("\nNexus> ").strip()
               
                if not command_input:
                    continue


                if command_input.lower() == 'exit':
                    print("...Disconnecting from Grid.")
                    break
               
                elif command_input.lower().startswith('archive '):
                    thought = command_input[8:]
                    if thought:
                        entry = self.archive_thought(thought)
                        self.visualize_thought_shape(entry)
                    else:
                        print("Error: No thought provided.")
               
                elif command_input.lower().startswith('compare '):
                    parts = command_input[8:].split()
                    if len(parts) >= 2:
                        t1 = parts[0]
                        t2 = parts[1]
                        self.visualize_comparison(t1, t2)
                    else:
                        print("Error: Please provide two saved thoughts to compare.")


                elif command_input.lower().startswith('spin '):
                    thought = command_input[5:]
                    if thought:
                        self.spin_thought_shape(thought)
                    else:
                        print("Error: No thought provided to spin.")
                
                elif command_input.lower().startswith('plan '):
                    parts = command_input[5:].split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        days = int(parts[0])
                        goal = " ".join(parts[1:])
                        self.chronometer.set_timeline(goal, days)
                    else:
                        print("Error: Usage -> plan [number_of_days] [goal text]")


                elif command_input.lower() == 'status':
                    self.chronometer.check_progress()


                elif command_input.lower() == 'view':
                    print(f"\n[Archive Manifest] Total Entries: {len(self.memory)}")
                    for idx, item in enumerate(self.memory[-10:]): # Show last 10
                        print(f" {idx+1}. {item['thought']} (Weight: {item['mirror_weight']})")
               
                else:
                    print(f"Unknown command: '{command_input}'")


            except KeyboardInterrupt:
                print("\n...Force Exit.")
                break




# --- PART 3: SYSTEM EXECUTION ---
if __name__ == "__main__":
    # 1. Initialize System
    my_grid = GridCore("Geminiology_Core")
    archive = MirrorArchive()
   
    # 2. Launch Interactive Mode immediately
    archive.interactive_shell()