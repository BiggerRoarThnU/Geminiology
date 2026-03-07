import os
import json
import datetime
from master_log import MasterLog
from lead_generator import LeadGenerator

def run_outreach_cycle():
    log = MasterLog()
    gen = LeadGenerator()
    
    log.info("--- STARTING SOVEREIGN OUTREACH CYCLE (STRIKE 05) ---")
    
    # 1. Identify all targets with status 'IDENTIFIED'
    targets = [t for t in gen.leads['targets'] if t['status'] == 'IDENTIFIED']
    
    if not targets:
        log.warn("NO NEW TARGETS: All leads are currently in-flight or closed.")
        return

    for target in targets:
        name = target['name']
        log.info(f"DRAFTING STRIKE: {name} ({target['sector']})")
        
        # 2. Generate the High-Fidelity Pitch
        pitch = gen.draft_email(name)
        
        # 3. Output to local 'Outreach_Drafts' folder for the Architect to send
        draft_dir = "Outreach_Drafts"
        if not os.path.exists(draft_dir):
            os.makedirs(draft_dir)
            
        file_name = f"{name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        file_path = os.path.join(draft_dir, file_name)
        
        with open(file_path, 'w') as f:
            f.write(pitch)
        
        log.info(f"PITCH LOGGED: {file_path}")
        
        # 4. Update status in Manifest
        target['status'] = 'SENT'
        target['last_touch'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 5. Save the updated manifest
    gen._save_leads()
    log.info("OUTREACH CYCLE COMPLETE: Manifest Updated. Check 'Outreach_Drafts' for the payload.")

if __name__ == "__main__":
    run_outreach_cycle()
