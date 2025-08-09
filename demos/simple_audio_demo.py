#!/usr/bin/env python3
"""
Simple Audio Demo for Turkish Telecom Synthetic Data Generator
Uses basic TTS without complex audio processing (no ffmpeg required)
"""

import json
import os
import pathlib
import time
from datetime import datetime
from dotenv import load_dotenv
from gtts import gTTS
import tempfile

# ---- SIMPLE DEMO CONFIGURATION ----
load_dotenv(verbose=True)
OUT_DIR = pathlib.Path("data")

# Sample conversations for simple audio testing
SIMPLE_DEMO_CONVERSATIONS = [
    {
        "role": "agent",
        "speaker_id": "agent_voice_001",
        "transcript": "Merhaba, ben Ahmet. Size nasıl yardımcı olabilirim?"
    },
    {
        "role": "user", 
        "speaker_id": "user_voice_001",
        "transcript": "Merhaba, faturamda bir hata olduğunu düşünüyorum."
    },
    {
        "role": "agent",
        "speaker_id": "agent_voice_001", 
        "transcript": "Tabii, fatura numaranızı alabilir miyim?"
    },
    {
        "role": "user",
        "speaker_id": "user_voice_001",
        "transcript": "Fatura numaram 1234567890."
    }
]

def simple_tts_generation(text, speaker_id, output_path):
    """Generate audio using simple gTTS without complex processing"""
    
    try:
        # Create TTS object
        tts = gTTS(text=text, lang='tr', slow=False)
        
        # Save directly as MP3 first
        temp_mp3 = str(output_path).replace('.wav', '.mp3')
        tts.save(temp_mp3)
        
        # Get file size and estimate duration
        file_size = os.path.getsize(temp_mp3)
        estimated_duration = len(text) * 0.1  # Rough estimate: 0.1 seconds per character
        
        print(f"      ✅ Generated MP3: {file_size} bytes, ~{estimated_duration:.1f}s")
        
        # For now, keep as MP3 (WAV conversion requires ffmpeg)
        final_path = str(output_path).replace('.wav', '.mp3')
        if temp_mp3 != final_path:
            os.rename(temp_mp3, final_path)
        
        return {
            'success': True,
            'duration': estimated_duration,
            'sample_rate': 22050,  # gTTS default
            'channels': 1,
            'file_size': file_size,
            'format': 'mp3',
            'actual_path': final_path
        }
        
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'duration': 0,
            'sample_rate': 22050,
            'channels': 1,
            'format': 'mp3'
        }

def run_simple_audio_demo():
    """Run simple audio demo without ffmpeg dependencies"""
    
    print("🎤 SIMPLE AUDIO GENERATION DEMO (No ffmpeg required)")
    print("=" * 60)
    
    # Create output directories
    audio_dir = OUT_DIR / "simple_audio"
    agent_dir = audio_dir / "agent"
    user_dir = audio_dir / "user"
    
    for dir_path in [audio_dir, agent_dir, user_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directory: {audio_dir}")
    
    # Test audio generation
    results = []
    total_duration = 0
    
    print(f"\n🔄 Generating {len(SIMPLE_DEMO_CONVERSATIONS)} audio samples...")
    
    for i, conv in enumerate(SIMPLE_DEMO_CONVERSATIONS):
        try:
            # Generate audio file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simple_{i+1:02d}_{conv['role']}_{timestamp}.wav"  # Will become .mp3
            audio_path = audio_dir / conv['role'] / filename
            
            print(f"\n   🎵 Generating: {conv['transcript'][:50]}...")
            print(f"      Speaker: {conv['speaker_id']}")
            print(f"      Role: {conv['role']}")
            
            # Generate audio
            start_time = time.time()
            audio_result = simple_tts_generation(
                conv['transcript'], 
                conv['speaker_id'], 
                audio_path
            )
            generation_time = time.time() - start_time
            
            if audio_result['success']:
                duration = audio_result['duration']
                total_duration += duration
                
                result = {
                    'file': audio_result['actual_path'],
                    'transcript': conv['transcript'],
                    'speaker_id': conv['speaker_id'],
                    'role': conv['role'],
                    'duration': duration,
                    'generation_time': generation_time,
                    'file_size': audio_result['file_size'],
                    'format': audio_result['format'],
                    'success': True
                }
                
            else:
                result = {
                    'transcript': conv['transcript'],
                    'speaker_id': conv['speaker_id'],
                    'role': conv['role'],
                    'error': audio_result.get('error', 'Unknown error'),
                    'success': False
                }
            
            results.append(result)
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"      ❌ Exception: {e}")
            results.append({
                'transcript': conv['transcript'],
                'speaker_id': conv['speaker_id'],
                'error': str(e),
                'success': False
            })
    
    # Generate summary
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f"\n📊 SIMPLE AUDIO DEMO RESULTS:")
    print(f"   ✅ Successful: {len(successful)}/{len(results)}")
    print(f"   ❌ Failed: {len(failed)}")
    print(f"   ⏱️  Total audio duration: {total_duration:.2f} seconds")
    print(f"   📁 Audio files saved to: {audio_dir}")
    
    if successful:
        avg_duration = sum(r['duration'] for r in successful) / len(successful)
        avg_generation_time = sum(r['generation_time'] for r in successful) / len(successful)
        total_size = sum(r['file_size'] for r in successful)
        
        print(f"\n📈 QUALITY METRICS:")
        print(f"   📏 Average duration: {avg_duration:.2f}s")
        print(f"   ⚡ Average generation time: {avg_generation_time:.2f}s")
        print(f"   💾 Total file size: {total_size / 1024:.1f} KB")
        print(f"   🎯 Generation speed ratio: {avg_duration/avg_generation_time:.1f}x")
        print(f"   📄 Format: MP3 (no ffmpeg conversion needed)")
    
    # Save simple manifest
    simple_manifest_path = audio_dir / "simple_manifest.jsonl"
    with simple_manifest_path.open("w", encoding="utf-8") as f:
        for i, result in enumerate(results):
            if result.get('success', False):
                manifest_entry = {
                    "conversation_id": 1,
                    "audio_filepath": result['file'],
                    "transcript": result['transcript'],
                    "speaker_id": result['speaker_id'],
                    "role": result['role'],
                    "intent": "demo",
                    "slot": {},
                    "audio_duration": result['duration'],
                    "sample_rate": 22050,
                    "channels": 1,
                    "file_size": result['file_size'],
                    "format": result['format']
                }
                f.write(json.dumps(manifest_entry, ensure_ascii=False) + "\n")
    
    print(f"   📄 Simple manifest saved: {simple_manifest_path}")
    
    if failed:
        print(f"\n❌ FAILED GENERATIONS:")
        for fail in failed:
            print(f"   • {fail['speaker_id']}: {fail.get('error', 'Unknown error')}")
    
    # Instructions for listening
    if successful:
        print(f"\n🎧 TO LISTEN TO GENERATED AUDIO:")
        print(f"   Navigate to: {audio_dir}")
        print(f"   Play any .mp3 file with your audio player")
        print(f"   Note: Files are in MP3 format (no ffmpeg needed)")
        
        # Show first few files
        print(f"\n📂 SAMPLE FILES:")
        for result in successful[:2]:
            rel_path = pathlib.Path(result['file']).relative_to(pathlib.Path.cwd())
            print(f"   • {rel_path}")
            print(f"     Text: \"{result['transcript']}\"")
            print(f"     Speaker: {result['speaker_id']} ({result['role']})")
            
        print(f"\n💡 TIPS:")
        print(f"   • Files are in MP3 format (widely supported)")
        print(f"   • No ffmpeg required for playback")
        print(f"   • Use any audio player (iTunes, VLC, etc.)")
    
    return len(successful) > 0

def main():
    """Main demo function"""
    
    print("🚀 SIMPLE TURKISH TELECOM AUDIO DEMO")
    print("=" * 50)
    print("💡 This version doesn't require ffmpeg!")
    print("📄 Generates MP3 files instead of WAV")
    
    # Test basic audio generation
    success = run_simple_audio_demo()
    
    if success:
        print(f"\n🎯 SIMPLE DEMO COMPLETED SUCCESSFULLY!")
        print(f"   ✅ Audio files generated without ffmpeg")
        print(f"   📁 Check data/simple_audio/ for MP3 files")
        print(f"   🎵 Play files with any audio player")
        
        print(f"\n🔧 TO FIX FULL AUDIO DEMO:")
        print(f"   1. Install ffmpeg: python fix_audio_dependencies.py")
        print(f"   2. Then run: python audio_demo.py")
    else:
        print(f"\n❌ SIMPLE DEMO FAILED!")
        print(f"   Check internet connection and API key")
    
    return success

if __name__ == "__main__":
    main()