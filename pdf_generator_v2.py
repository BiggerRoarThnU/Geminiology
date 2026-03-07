import os
from PIL import Image, ImageDraw, ImageFont

def text_to_pdf_via_image(input_path, output_path):
    # Set up the high-fidelity "Nexus" look
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    width, height = 1275, 1650 # Standard 150 DPI Letter size
    
    # Try to find a monospace font, fallback to default
    try:
        font = ImageFont.truetype("cour.ttf", 24)
    except:
        font = ImageFont.load_default()

    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Create the image surface
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Draw the text with professional margins
    margin = 80
    y_position = margin
    
    for line in text.split('\n'):
        draw.text((margin, y_position), line, font=font, fill=text_color)
        y_position += 35
        if y_position > height - margin:
            break # Simple one-page anchor for Guru
            
    # Save as PDF
    image.save(output_path, "PDF", resolution=150.0)

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
    output_name = os.path.splitext(file_name)[0] + ".pdf"
    output_file = os.path.join(upload_dir, output_name)
    
    if os.path.exists(input_file):
        print(f"ANCHORING PDF: {output_name}...")
        text_to_pdf_via_image(input_file, output_file)
        print(f"RESULT: {output_name} SECURED.")
