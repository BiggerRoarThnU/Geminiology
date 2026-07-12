# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Source Truth: ComfyUI MCP Protocol (Adapted for Local Sovereign Execution)

import json
import urllib.request
import urllib.parse
import os

class NexusVisualBridge:
    def __init__(self, comfy_url="http://127.0.0.1:8188"):
        self.comfy_url = comfy_url
        self.default_workflow_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "workflows/nexus_base_render.json"
        )

    def _load_base_workflow(self):
        """Loads a clean, verified node architecture from the vault."""
        with open(self.default_workflow_path, 'r') as f:
            return json.load(f)

    def translate_and_inject(self, prompt_text, override_model=None):
        """
        The DSL-to-JSON translator. 
        Injects our natural language prompt into the specific node ID (e.g., node '6' for CLIP Text Encode).
        """
        workflow = self._load_base_workflow()
        
        # Inject the positive prompt
        # Note: Node IDs vary based on your specific saved Comfy workflow.
        workflow["6"]["inputs"]["text"] = prompt_text 
        
        if override_model:
            workflow["4"]["inputs"]["ckpt_name"] = override_model
            
        return workflow

    def execute_workflow(self, workflow_json):
        """
        The Execution Engine: Submits the job locally and securely.
        """
        p = {"prompt": workflow_json}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"{self.comfy_url}/prompt", data=data)
        req.add_header('Content-Type', 'application/json')
        
        try:
            # Pushing to ComfyUI
            response = urllib.request.urlopen(req, timeout=10)
            return json.loads(response.read())
        except Exception as e:
            return f"[ERROR] Visual Bridge failed to execute: {e}"

if __name__ == "__main__":
    # Small test loop if executed directly
    print("--- Nexus Visual Bridge Initialized ---")
    bridge = NexusVisualBridge()
    workflow_json = bridge.translate_and_inject("cinematic cyberpunk scene, raw entropy style")
    print("[+] DSL translated to Comfy JSON. Ready for injection.")
    print(f"[+] Output Nodes Configured: Prompt -> {workflow_json['6']['inputs']['text']}")
