"""
RECOMMENDATION CHATBOT - STANDALONE RUNNER

Quick launcher for the emotion-based movie recommendation chatbot.
"""

import os
import sys

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(scripts_dir)
sys.path.insert(0, scripts_dir)

from chatbot import run_chatbot_interactive


def main():
    """Main entry point."""
    
    # Locate TTL file
    ttl_path = os.path.join(project_root, "movie-emotions.ttl")
    
    if not os.path.exists(ttl_path):
        print(f"❌ Error: Knowledge base not found at {ttl_path}")
        print("\nPlease ensure movie-emotions.ttl exists in the project root.")
        sys.exit(1)
    
    print(f"\n📂 Knowledge base loaded from: {ttl_path}\n")
    
    # Run interactive chatbot
    run_chatbot_interactive(ttl_path)


if __name__ == "__main__":
    main()
