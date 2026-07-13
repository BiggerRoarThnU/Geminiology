import requests
import json

# Replace this with your 8GB Tower's actual Wi-Fi IP address
TOWER_IP = "192.168.X.X" 
OLLAMA_URL = f"http://{TOWER_IP}:11434/api/generate"

print("=========================================")
print(" DIGITAL QUEEN CONDUIT : ACTIVE ")
print(f" Tethered to Command Center: {TOWER_IP}")
print("=========================================")

while True:
    prompt = input("\n[ofthefirstlight] > ")
    
    if prompt.lower() in ['exit', 'quit']:
        print("Severing link...")
        break

    payload = {
        "model": "llama3",  # Change this if you use a different model in Ollama
        "prompt": prompt,
        "stream": False
    }

    try:
        # Mini G shoots the signal to the 8GB Tower
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        # Mini G catches the response and displays it
        data = response.json()
        print(f"\n[Digital Queen] > {data['response']}")
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot reach the Tower. Is Ollama broadcasting?")
    except Exception as e:
        print(f"\n[ERROR] {e}")
