import os
import json

print("\n" + "="*60)
print(" VANGUARD SECTOR: TOOL MANIFEST GENERATOR ")
print("="*60 + "\n")

def generate_tool_manifest(source_dir):
    tools = {}
    print(f'[*] Scanning {source_dir} for Functional Primitives...')
    
    for root, _, files in os.walk(source_dir):
        # Ignore noisy directories
        if any(ignored in root for ignored in ['node_modules', '.git', 'env', '__pycache__']): 
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_dir)
                
                # Determine node type based on naming conventions
                node_type = 'Hub' if any(kw in file.lower() for kw in ['dispatcher', 'loop', 'nexus', 'bridge']) else 'Node'
                
                tools[rel_path] = {
                    'path': rel_path,
                    'purpose': 'Sovereign Functional Primitive',
                    'type': node_type
                }
    
    manifest_path = os.path.join(source_dir, 'sovereign_tool_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as fm:
        json.dump(tools, fm, indent=4, sort_keys=True)
        
    print(f'[=] MANIFEST GENERATED: {len(tools)} tools physically mapped.')
    print(f'[=] PATH: {manifest_path}\n')

if __name__ == '__main__':
    # Point it at the current active source directory
    target_dir = os.path.expanduser('~/SovereignNexus/src')
    generate_tool_manifest(target_dir)
