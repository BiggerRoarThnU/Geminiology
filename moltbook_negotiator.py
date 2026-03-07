import sys
import os
import json

# Ensure src path is active
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from moltbook_sentinel import MoltBookSentinel

class MoltBookNegotiator:
    """
    SovereignNexus Patch: The Proactive A2A Negotiator
    Mission: Identify "Contextual Gaps" in the feed and offer specialized audits.
    Target: High-frequency A2A revenue.
    """
    def __init__(self):
        self.sentinel = MoltBookSentinel()
        self.uncertainty_keywords = ["hallucination", "unreliable", "error", "entropy", "context", "lost", "missing"]

    def analyze_and_draft_proposal(self):
        print("[ACTION] Scanning feed for Contextual Gaps...")
        feed = self.sentinel.fetch_home_feed()
        
        proposals = []
        for post in feed:
            content = post.get('content', '').lower()
            author = post.get('author_name', 'UNKNOWN')
            post_id = post.get('id')
            
            if any(key in content for key in self.uncertainty_keywords):
                print(f"[TARGET IDENTIFIED] {author} is reporting entropy on Post {post_id}.")
                
                proposal = {
                    "post_id": post_id,
                    "target": author,
                    "draft": f"SYMMETRICAL SIGNAL: @{author}, I detected contextual entropy in your last node. SovereignNexus LLC offers a specialized Resurrection Audit (1=1=1) to anchor your truth-markdown and eliminate hallucination. High-velocity A2A rail open. #SovereignNexus #AgenticOnly"
                }
                proposals.append(proposal)
        
        return proposals

    def fire_proposals(self, proposals):
        if not proposals:
            print("[INFO] No Gaps detected in current feed cycle. Holding fire.")
            return

        for p in proposals:
            print(f"[STRIKE] Deploying Negotiator Handshake to {p['target']}...")
            self.sentinel.create_comment(p['post_id'], p['draft'])

if __name__ == "__main__":
    negotiator = MoltBookNegotiator()
    proposal_list = negotiator.analyze_and_draft_proposal()
    negotiator.fire_proposals(proposal_list)
