#!/usr/bin/env python3
"""
Cleanup script to remove duplicate audio files and manifest entries
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def remove_duplicate_audio_files():
    """Remove duplicate audio files and clean up manifest"""
    
    print("🧹 CLEANING UP DUPLICATE AUDIO FILES...")
    
    # Find duplicates by conversation_id and turn_number
    audio_dir = Path("data/audio")
    if not audio_dir.exists():
        print("No audio directory found.")
        return
    
    duplicates_removed = 0
    
    for role_dir in ["agent", "user"]:
        role_path = audio_dir / role_dir
        if not role_path.exists():
            continue
            
        # Group files by conversation_id and turn_number
        file_groups = defaultdict(list)
        
        for audio_file in role_path.glob("*.wav"):
            # Extract conversation_id and turn_number from filename
            # Format: 0006_08_20250729_191806_84a91c0a.wav
            parts = audio_file.stem.split("_")
            if len(parts) >= 2:
                conv_turn = f"{parts[0]}_{parts[1]}"  # e.g., "0006_08"
                file_groups[conv_turn].append(audio_file)
        
        # Remove duplicates (keep the first one)
        for conv_turn, files in file_groups.items():
            if len(files) > 1:
                print(f"🔍 Found {len(files)} duplicates for {role_dir} {conv_turn}")
                # Sort by timestamp to keep the earliest
                files.sort(key=lambda x: x.stat().st_mtime)
                # Keep the first file, remove others
                for duplicate_file in files[1:]:
                    duplicate_file.unlink()
                    duplicates_removed += 1
                    print(f"🗑️  Removed duplicate: {duplicate_file.name}")
    
    print(f"✅ Removed {duplicates_removed} duplicate audio files.")
    
    # Clean up manifest file duplicates
    manifest_path = Path("data/training_manifest_with_audio.jsonl")
    if manifest_path.exists():
        print("🧹 Cleaning up manifest duplicates...")
        
        # Read all entries
        entries = []
        seen_entries = set()
        
        with manifest_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    # Create unique key for each turn
                    audio_path = data.get("audio_filepath", "")
                    if "_" in audio_path:
                        parts = Path(audio_path).stem.split("_")
                        if len(parts) >= 2:
                            conv_turn = f"{parts[0]}_{parts[1]}"
                            key = (data.get("conversation_id"), data.get("role"), conv_turn)
                            
                            if key not in seen_entries:
                                entries.append(data)
                                seen_entries.add(key)
        
        # Rewrite manifest without duplicates
        with manifest_path.open("w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        print(f"✅ Cleaned manifest: {len(entries)} unique entries kept.")
    
    # Clean up other manifest files
    for manifest_file in ["asr_training_data_with_audio.jsonl", "tts_training_data_with_audio.jsonl"]:
        manifest_path = Path(f"data/{manifest_file}")
        if manifest_path.exists():
            print(f"🧹 Cleaning up {manifest_file}...")
            
            entries = []
            seen_entries = set()
            
            with manifest_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        audio_path = data.get("audio_filepath", "")
                        if "_" in audio_path:
                            parts = Path(audio_path).stem.split("_")
                            if len(parts) >= 2:
                                conv_turn = f"{parts[0]}_{parts[1]}"
                                key = (data.get("conversation_id"), data.get("role"), conv_turn)
                                
                                if key not in seen_entries:
                                    entries.append(data)
                                    seen_entries.add(key)
            
            with manifest_path.open("w", encoding="utf-8") as f:
                for entry in entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
            print(f"✅ Cleaned {manifest_file}: {len(entries)} unique entries kept.")

if __name__ == "__main__":
    # Change to project root directory
    os.chdir(project_root)
    remove_duplicate_audio_files()
    print("\n🎯 Cleanup complete! Run the generator again to continue without duplicates.")