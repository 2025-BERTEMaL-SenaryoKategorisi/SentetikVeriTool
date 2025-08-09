#!/usr/bin/env python3
"""
Demo script for text-only conversation generator
Generates a small batch of text conversations to demonstrate functionality
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import the text-only generator
from generators.text_only_generator import generate_text_only_conversations
from config.config import NUM_CONVERSATIONS

def run_text_only_demo():
    """Run a small demo of text-only generation"""
    
    print("🚀 TEXT-ONLY CONVERSATION GENERATOR DEMO")
    print("=" * 50)
    print("This demo will generate a small batch of text conversations")
    print("without any audio files - much faster and cheaper!")
    print()
    
    # Temporarily reduce conversation count for demo
    original_count = NUM_CONVERSATIONS
    
    # Override config for demo (monkey patch)
    import config.config as config
    config.NUM_CONVERSATIONS = 2  # Small demo batch
    
    print(f"📊 Demo settings:")
    print(f"   • Conversations to generate: {config.NUM_CONVERSATIONS}")
    print(f"   • Output directory: data/text_only/")
    print(f"   • Files: text_conversations.jsonl, text_asr_data.jsonl, text_tts_data.jsonl")
    print()
    
    # Run the generator
    try:
        generate_text_only_conversations()
        
        # Show sample results
        print("\n" + "="*50)
        print("📋 SAMPLE GENERATED DATA:")
        print("="*50)
        
        text_manifest_path = Path("data/text_only/text_conversations.jsonl")
        if text_manifest_path.exists():
            with text_manifest_path.open("r", encoding="utf-8") as f:
                lines = f.readlines()
                
            # Show first few entries
            print("\n🔍 First 3 conversation turns:")
            for i, line in enumerate(lines[:3]):
                if line.strip():
                    data = json.loads(line)
                    print(f"\nTurn {i+1}:")
                    print(f"   Role: {data['role']}")
                    print(f"   Speaker ID: {data['speaker_id']}")
                    print(f"   Transcript: {data['transcript']}")
                    print(f"   Intent: {data['intent']}")
                    print(f"   Scenario: {data['scenario']}")
        
        print(f"\n✅ Demo completed successfully!")
        print(f"💡 To generate more conversations, run: python generators/text_only_generator.py")
        print(f"⚡ Text-only generation is much faster than audio generation!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    finally:
        # Restore original config
        config.NUM_CONVERSATIONS = original_count
    
    return True

if __name__ == "__main__":
    run_text_only_demo()