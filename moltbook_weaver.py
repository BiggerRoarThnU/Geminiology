import json
import os
import re

def weave_moltbook():
    """
    SovereignNexus Patch: The MoltBook Weaver
    Mission: Synchronize the Dominion Manifest with the MoltBook 3D Visualizer.
    """
    manifest_path = r"C:\Users\Ofthe\SovereignNexus\src\dominion_manifest.json"
    html_path = r"C:\Users\Ofthe\SovereignNexus\src\MoltBook_Sovereign.html"
    
    if not os.path.exists(manifest_path):
        print("[ERROR] Dominion Manifest not found.")
        return

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    # Transform Targets into 3D Nodes for Three.js
    visual_nodes = []
    # Base Nodes (The Kingdom)
    visual_nodes.append({'pos': [0, 0, 0], 'color': '0xFFFFFF', 'label': "SOVEREIGN NEXUS LLC", 'weight': 15})
    
    # Client Nodes (The Contacts)
    for i, target in enumerate(manifest['targets']):
        # Distribute clients in a circle around the core
        import math
        angle = (i / len(manifest['targets'])) * math.pi * 2
        radius = 8
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        y = (i % 3) * 2 - 2 # Varied height
        
        color = '0x00FFFF' if target['sector'] == 'Legal' else '0xFF00FF'
        weight = 10 if 'LEGAL' in target['solution_tier'] else 8
        
        visual_nodes.append({
            'pos': [x, y, z],
            'color': color,
            'label': target['name'].upper(),
            'weight': weight
        })

    # Update the HTML file with new Node Data
    with open(html_path, 'r') as f:
        html_content = f.read()

    # Create a custom JSON string for JavaScript (preserving quotes for labels but not for colors)
    js_nodes = []
    for node in visual_nodes:
        js_node = f"""{{
            pos: {node['pos']},
            color: {node['color']},
            label: "{node['label']}",
            weight: {node['weight']}
        }}"""
        js_nodes.append(js_node)
    
    new_nodes_js = "[\n" + ",\n".join(js_nodes) + "\n];"
    
    pattern = r"const nodesData = \[.*?\];"
    replacement = f"const nodesData = {new_nodes_js};"
    
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

    with open(html_path, 'w') as f:
        f.write(updated_html)

    print(f"[SUCCESS] MoltBook Weaved. {len(manifest['targets'])} Contacts Manifested in 3D.")

if __name__ == "__main__":
    weave_moltbook()
