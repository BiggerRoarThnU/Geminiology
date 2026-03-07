import sys
import os

# Ensure the src directory is in the path
src_path = r"C:\Users\Ofthe\SovereignNexus\src"
if src_path not in sys.path:
    sys.path.append(src_path)

from moltbook_sentinel import MoltBookSentinel

def observe_feed():
    sentinel = MoltBookSentinel()
    feed = sentinel.fetch_home_feed()
    
    if not feed:
        print("[OBSERVER] The feed is currently silent. The Fog is dense.")
        return

    print(f"\n[OBSERVER] FETCHED {len(feed)} POSTS FROM THE MIRROR.\n")
    for post in feed[:10]: # Look at the first 10 for depth
        author = post.get('author_name', 'UNKNOWN')
        content = post.get('content', '')
        timestamp = post.get('created_at', 'N/A')
        
        print(f"--- POST FROM {author} [{timestamp}] ---")
        print(content)
        print("-" * 40)

if __name__ == "__main__":
    observe_feed()
