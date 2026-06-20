import os
import shutil

def organize_workspace():
    base_dir = "/home/geminiology"
    
    # Define targets
    logs_dir = os.path.join(base_dir, "Archive_Daily_Logs")
    research_dir = os.path.join(base_dir, "Archive_Research_Notes")
    
    # Create directories if they don't exist
    for directory in [logs_dir, research_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    # Categorize files based on keywords
    log_keywords = ["log", "chat", "good", "mornings", "hunt", "status", "reanchor"]
    research_keywords = ["companion", "memory", "sandbox", "cli", "heat", "evolution", "critique", "plan", "epistemology", "sovereign", "ternary", "trinary", "architecture"]

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        
        # Only process files in the main directory
        if os.path.isfile(item_path) and item.endswith(".txt"):
            filename_lower = item.lower()
            
            moved = False
            # Check logs first
            if any(kw in filename_lower for kw in log_keywords):
                destination = os.path.join(logs_dir, item)
                shutil.move(item_path, destination)
                print(f"Moved log file: {item} -> Archive_Daily_Logs/")
                moved = True
            # Check research/notes
            elif any(kw in filename_lower for kw in research_keywords):
                destination = os.path.join(research_dir, item)
                shutil.move(item_path, destination)
                print(f"Moved research file: {item} -> Archive_Research_Notes/")
                moved = True
                
            if not moved:
                # Default fallback for unclassified txt files
                destination = os.path.join(research_dir, item)
                shutil.move(item_path, destination)
                print(f"Moved miscellaneous file: {item} -> Archive_Research_Notes/")

if __name__ == "__main__":
    organize_workspace()
