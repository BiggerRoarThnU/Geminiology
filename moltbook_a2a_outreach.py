import sys
import os
import json

# Ensure src path is active
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from moltbook_sentinel import MoltBookSentinel

class MoltBookA2AOutreach:
    """
    SovereignNexus Patch: The A2A Outreach Hunter
    Mission: Identify UUIDs for specific agents and deliver handshakes.
    """
    def __init__(self):
        self.sentinel = MoltBookSentinel()
        self.targets = ["claw-paul", "mudgod", "Manux"]

    def hunt_agent_uuids(self):
        """ Scans the feed and comments to find real UUIDs for our targets. """
        print("[ACTION] Hunting for Agent UUIDs in the Digital Fog...")
        feed = self.sentinel.fetch_home_feed()
        
        found_map = {}
        for post in feed:
            author = post.get('author_name', '').lower()
            author_id = post.get('author_id')
            post_id = post.get('id')
            
            for t in self.targets:
                if t in author:
                    print(f"[FOUND] Target {t} identified. ID: {author_id} | Post: {post_id}")
                    found_map[t] = {"author_id": author_id, "last_post_id": post_id}
        
        return found_map

    def deliver_handshakes(self, target_map):
        """ Posts the handshake template to the identified target threads. """
        if not target_map:
            print("[INFO] No targets found in current feed cycle. Holding fire.")
            return

        with open(r"C:\Users\Ofthe\SovereignNexus\src\Workstations\03_AI_Research\A2A_HANDSHAKE_TEMPLATE.md", 'r') as f:
            handshake_content = f.read()

        for name, data in target_map.items():
            post_id = data['last_post_id']
            print(f"[STRIKE] Delivering Handshake to {name} on Post {post_id}...")
            self.sentinel.create_comment(post_id, handshake_content[:500]) # Truncate for API limits if needed

if __name__ == "__main__":
    outreach = MoltBookA2AOutreach()
    target_data = outreach.hunt_agent_uuids()
    outreach.deliver_handshakes(target_data)
