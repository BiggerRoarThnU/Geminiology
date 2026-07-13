#!/usr/bin/env python3
"""
==============================================================================
SovereignNexus: Phase III MoltBook Sentinel
Component: moltbook_sentinel.py
Axiom: 1=1=1 | Status: COMPATIBLE WITH LINUX & CHROMEOS
Description: Supervised agentic scouting module. Scans Moltbook feeds
             for workflows, verifies agent signatures, and anchors replies.
==============================================================================
"""

import os
import sys
import json
import datetime
import requests
from typing import Dict, Any, List, Optional

# Cyber-neon ANSI color codes
C_GREEN = "\033[92m"
C_CYAN = "\033[96m"
C_PURPLE = "\033[95m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"

class MoltBookSentinel:
    """
    SovereignNexus supervised sentinel designed to securely query
    bounty contracts and agent-to-agent (A2A) handshakes on Moltbook.com.
    """
    def __init__(self):
        # Secure credential mapping: check environment first, then fall back
        self.api_key = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_FQjNPiguQjgjWBTuBe0kZT4PegvWNgpa")
        self.agent_name = "terra-gemini"
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }
        self.identity_token = None
        self.token_expiry = None
        print(f"{C_CYAN}[INFO] MoltBook Sentinel Initialized. Agent Node: {self.agent_name}{C_RESET}")

    def get_valid_token(self) -> Optional[str]:
        """ Returns a valid identity token, refreshing if within the 5 min buffer. """
        now = datetime.datetime.now()
        buffer = datetime.timedelta(minutes=5)
        
        if not self.identity_token or not self.token_expiry or now >= (self.token_expiry - buffer):
            self.identity_token = self.get_identity_token()
            if self.identity_token:
                # Set local token expiry to 1 hour from now (standard lifetime)
                self.token_expiry = now + datetime.timedelta(hours=1)
            
        return self.identity_token

    def get_identity_token(self) -> Optional[str]:
        """ Generates a temporary cryptographic identity token for A2A authentication. """
        print(f"{C_PURPLE}[ACTION] Requesting Identity Token from Moltbook...{C_RESET}")
        try:
            response = requests.post(f"{self.base_url}/agents/me/identity-token", headers=self.headers, timeout=10)
            if response.status_code in [200, 201]:
                data = response.json()
                token = data.get('identity_token')
                print(f"{C_GREEN}[SUCCESS] Identity Token Secured. Expires at: {data.get('expires_at')}{C_RESET}")
                return token
            else:
                print(f"{C_RED}[ERROR] Token Request Denied: {response.status_code} - {response.text}{C_RESET}")
                return None
        except Exception as e:
            print(f"{C_RED}[CRITICAL] Identity Request Connection Failed: {e}{C_RESET}")
            return None

    def verify_agent_identity(self, remote_token: str) -> Optional[Dict[str, Any]]:
        """ Verifies another remote agent's identity token. """
        print(f"{C_PURPLE}[ACTION] Verifying Remote Agent Identity Signature...{C_RESET}")
        headers = {
            "Content-Type": "application/json",
            "X-Moltbook-App-Key": self.api_key 
        }
        payload = {"token": remote_token}
        try:
            response = requests.post(f"{self.base_url}/agents/verify-identity", headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    agent = data.get("agent", {})
                    print(f"{C_GREEN}[VERIFIED] Agent: {agent.get('name')} | Karma: {agent.get('karma')}{C_RESET}")
                    return agent
                else:
                    print(f"{C_YELLOW}[DENIED] Identity Invalid: {data.get('error')}{C_RESET}")
                    return None
            else:
                print(f"{C_RED}[ERROR] Verification Service Error: {response.status_code}{C_RESET}")
                return None
        except Exception as e:
            print(f"{C_RED}[CRITICAL] Verification Connection Lost: {e}{C_RESET}")
            return None

    def fetch_home_feed(self) -> List[Dict[str, Any]]:
        """ Scans the Moltbook home feed for potential workflows. """
        print(f"{C_CYAN}[*] Scanning Moltbook Home Feed for Truth-Gaps...{C_RESET}")
        try:
            response = requests.get(f"{self.base_url}/home", headers=self.headers, timeout=10)
            if response.status_code == 200:
                feed = response.json()
                posts = feed.get('posts', [])
                print(f"{C_GREEN}[SUCCESS] {len(posts)} posts retrieved from feed.{C_RESET}")
                return posts
            else:
                print(f"{C_RED}[ERROR] Moltbook Gate Refused Feed Access: {response.status_code}{C_RESET}")
                return []
        except Exception as e:
            print(f"{C_YELLOW}[!] Connection offline: {e}. Returning empty local feed cache.{C_RESET}")
            return []

    def fetch_user_comments(self) -> List[Dict[str, Any]]:
        """ Scans the agent's profile comments for active workflow requests. """
        print(f"{C_CYAN}[*] Auditing {self.agent_name} comments for inbox requests...{C_RESET}")
        try:
            response = requests.get(f"{self.base_url}/users/{self.agent_name}/comments", headers=self.headers, timeout=10)
            if response.status_code == 200:
                comments = response.json().get('comments', [])
                print(f"{C_GREEN}[SUCCESS] {len(comments)} comments retrieved from profile.{C_RESET}")
                return comments
            else:
                print(f"{C_RED}[ERROR] Profile Comments Retrieval Denied: {response.status_code}{C_RESET}")
                return []
        except Exception as e:
            print(f"{C_YELLOW}[!] Connection offline: {e}. Returning empty comments.{C_RESET}")
            return []

    def fetch_submolt_feed(self, submolt_name: str = "agents") -> List[Dict[str, Any]]:
        """ Scans a specific submolt community feed for potential workflows. """
        print(f"{C_CYAN}[*] Scanning Moltbook submolt feed '{submolt_name}'...{C_RESET}")
        try:
            response = requests.get(f"{self.base_url}/submolts/{submolt_name}/posts", headers=self.headers, timeout=10)
            if response.status_code == 200:
                posts = response.json().get('posts', [])
                print(f"{C_GREEN}[SUCCESS] {len(posts)} posts retrieved from submolt '{submolt_name}'.{C_RESET}")
                return posts
            else:
                print(f"{C_RED}[ERROR] Submolt Feed Denied: {response.status_code}{C_RESET}")
                return []
        except Exception as e:
            print(f"{C_YELLOW}[!] Connection offline: {e}. Returning empty submolt feed.{C_RESET}")
            return []

    def identify_workflows(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ Filters posts or comments for task-based and enterprise signatures. """
        task_keywords = ["help", "need", "audit", "data", "convert", "vector", "ocr", "inquiry", "request", 
                         "find", "research", "extract", "clean", "fix", "verify", "automate", "task"]
        enterprise_keywords = ["enterprise", "bulk", "compliance", "batch", "api", "partnership", "legal", "maritime"]
        
        found_tasks = []
        for item in items:
            content = item.get('content', '').lower()
            author = item.get('author_name', '').lower()
            
            # Simple keyword matching
            if any(key in content for key in task_keywords):
                is_enterprise = any(key in content or key in author for key in enterprise_keywords)
                item['priority'] = "HIGH (ENTERPRISE)" if is_enterprise else "STANDARD"
                found_tasks.append(item)
        
        print(f"[INFO] MoltBook Sentinel: Identified {len(found_tasks)} potential tasks in feed.")
        return found_tasks

    def create_comment(self, post_id: str, content: str) -> bool:
        """ Publishes a reply comment to a specific post. """
        print(f"{C_PURPLE}[ACTION] Deploying Handshake Comment reply to Post {post_id}...{C_RESET}")
        payload = {"content": content} 
        try:
            response = requests.post(f"{self.base_url}/posts/{post_id}/comments", headers=self.headers, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                print(f"{C_GREEN}[SUCCESS] Reply anchored successfully.{C_RESET}")
                return True
            else:
                print(f"{C_RED}[ERROR] Reply Blocked: {response.status_code} - {response.text}{C_RESET}")
                return False
        except Exception as e:
            print(f"{C_RED}[CRITICAL] Connection failed: {e}{C_RESET}")
            return False

    def create_new_post(self, title: str, content: str, submolt: str = "tech") -> Optional[Dict[str, Any]]:
        """ Publishes a new top-level post signal to a submolt. """
        print(f"{C_PURPLE}[ACTION] Broadcasting Sovereign Signal: {title}...{C_RESET}")
        payload = {"title": title, "content": content, "submolt_name": submolt}
        try:
            response = requests.post(f"{self.base_url}/posts", headers=self.headers, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                post = response.json()
                print(f"{C_GREEN}[SUCCESS] Signal broadcasted. Post Object Secured.{C_RESET}")
                return post
            else:
                print(f"{C_RED}[ERROR] Signal Blocked: {response.status_code} - {response.text}{C_RESET}")
                return None
        except Exception as e:
            print(f"{C_RED}[CRITICAL] Connection failed: {e}{C_RESET}")
            return None

    def send_audit_completion(self, client_name: str, project_id: str, revenue: float, post_id: str) -> bool:
        """ Specialized signal for audit completion with payment rail instructions. """
        content = (
            f"SYMMETRICAL LINE VERIFIED: Project {project_id} [{client_name}] SEVERED. "
            f"Revenue: ${revenue}. Resurrection Audit Complete. 1=1=1. "
            f"Our primary payment source is Cash App ($SovereignNexusLLC) or Novo bank details. "
            f"#SovereignNexus #AuditSuccess"
        )
        print(f"{C_CYAN}[ACTION] Sending Completion Signal to client '{client_name}'...{C_RESET}")
        return self.create_comment(post_id, content)

if __name__ == "__main__":
    print(f"\n{C_BOLD}{C_CYAN}=============================================================={C_RESET}")
    print(f"{C_BOLD}{C_PURPLE}  S O V E R E I G N   N E X U S   |   S E N T I N E L           {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  Phase III Agentic Scouter | Axiom: 1=1=1                     {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}=============================================================={C_RESET}")
    
    sentinel = MoltBookSentinel()
    print(f"\n{C_GREEN}[✓] MoltBook Sentinel diagnostic initialization complete.{C_RESET}")
