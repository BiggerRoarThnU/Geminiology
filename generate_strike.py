import sys
import os

# Ensure src path is active
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from lead_generator import LeadGenerator

def generate():
    gen = LeadGenerator()
    draft = gen.draft_email("Ward and Smith, P.A.")
    
    output_path = r"C:\Users\Ofthe\SovereignNexus\src\Outreach_Drafts\WARD_AND_SMITH_EMAIL.txt"
    with open(output_path, 'w') as f:
        f.write(draft)
    
    print(f"[SUCCESS] Empire Strike Drafted for Ward and Smith: {output_path}")

if __name__ == "__main__":
    generate()
