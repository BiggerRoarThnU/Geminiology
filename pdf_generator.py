import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def text_to_pdf(input_path, output_path):
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER
    
    # Set font to a clean, authoritative monospace for the "Nexus" look
    c.setFont("Courier-Bold", 14)
    y_position = height - 50
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if y_position < 50:
            c.showPage()
            c.setFont("Courier-Bold", 14)
            y_position = height - 50
            
        # Handle title/headers with bolding if starts with # or =
        if line.startswith("#") or line.startswith("="):
            c.setFont("Courier-Bold", 12)
        else:
            c.setFont("Courier", 10)
            
        wrapped_lines = simpleSplit(line.strip(), c._fontname, c._fontsize, width - 100)
        for w_line in wrapped_lines:
            c.drawString(50, y_position, w_line)
            y_position -= 15
            
    c.save()

# Directory Calibration
upload_dir = r"C:\Users\Ofthe\SovereignNexus\src\Guru_Uploads"
files_to_convert = [
    "Sovereign_Proof_Sample.txt",
    "Vector_Mill_Conversion_Sample.md",
    "SovereignNexus_Executive_Summary.txt",
    "Sovereign_Legal_Dashboard_Sample.txt",
    "Sentinel_Compliance_Audit_Sample.txt"
]

for file_name in files_to_convert:
    input_file = os.path.join(upload_dir, file_name)
    # Remove original extension and add .pdf
    output_name = os.path.splitext(file_name)[0] + ".pdf"
    output_file = os.path.join(upload_dir, output_name)
    
    if os.path.exists(input_file):
        print(f"ANCHORING: {output_name}...")
        text_to_pdf(input_file, output_file)
        print(f"RESULT: {output_name} SECURED.")
