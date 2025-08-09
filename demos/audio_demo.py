#!/usr/bin/env python3
"""
Audio Demo for Turkish Telecom Synthetic Data Generator
Tests TTS functionality with a small sample
"""

import json
import os
import random
import pathlib
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tqdm import tqdm

# Import the voice manager from the main audio script
import sys
sys.path.append('.')

try:
    from main3_with_audio import VoiceManager, SpeakerManager, clean_and_parse_json
    AUDIO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Audio dependencies not available: {e}")
    print("Please install: pip install gtts pydub librosa soundfile")
    AUDIO_AVAILABLE = False

# ---- DEMO CONFIGURATION ----
load_dotenv(verbose=True)
MODEL_NAME = "gemini-1.5-pro"
OUT_DIR = pathlib.Path("data")

# Sample conversations for audio testing
DEMO_CONVERSATIONS = [
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
    },
    {
        "role": "agent",
        "speaker_id": "agent_voice_002",
        "transcript": "Bir saniye lütfen, sistemi kontrol ediyorum."
    },
    {
        "role": "user",
        "speaker_id": "user_voice_002", 
        "transcript": "Tamamdır, bekliyorum."
    }
]

def test_audio_generation():
    """Test audio generation with sample conversations"""
    
    print("🎤 AUDIO GENERATION DEMO")
    print("=" * 50)
    
    if not AUDIO_AVAILABLE:
        print("❌ Audio generation not available. Please install dependencies.")
        return False
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  GOOGLE_API_KEY not found. Audio demo will use pre-defined text.")
    
    # Create output directories
    audio_dir = OUT_DIR / "demo_audio"
    agent_dir = audio_dir / "agent"
    user_dir = audio_dir / "user"
    
    for dir_path in [audio_dir, agent_dir, user_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize voice manager
    try:
        voice_manager = VoiceManager()
        print("✅ Voice manager initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize voice manager: {e}")
        return False
    
    # Test audio generation
    results = []
    total_duration = 0
    
    print(f"\n🔄 Generating {len(DEMO_CONVERSATIONS)} audio samples...")
    
    for i, conv in enumerate(DEMO_CONVERSATIONS):
        try:
            # Generate audio file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"demo_{i+1:02d}_{conv['role']}_{timestamp}.wav"
            audio_path = audio_dir / conv['role'] / filename
            
            print(f"\n   🎵 Generating: {conv['transcript'][:50]}...")
            print(f"      Speaker: {conv['speaker_id']}")
            print(f"      Role: {conv['role']}")
            
            # Generate audio
            start_time = time.time()
            audio_result = voice_manager.generate_audio(
                conv['transcript'], 
                conv['speaker_id'], 
                audio_path
            )
            generation_time = time.time() - start_time
            
            if audio_result['success']:
                duration = audio_result['duration']
                total_duration += duration
                
                result = {
                    'file': str(audio_path),
                    'transcript': conv['transcript'],
                    'speaker_id': conv['speaker_id'],
                    'role': conv['role'],
                    'duration': duration,
                    'generation_time': generation_time,
                    'file_size': audio_path.stat().st_size,
                    'success': True
                }
                
                print(f"      ✅ Success! Duration: {duration:.2f}s, Size: {result['file_size']} bytes")
                
            else:
                result = {
                    'transcript': conv['transcript'],
                    'speaker_id': conv['speaker_id'],
                    'role': conv['role'],
                    'error': audio_result.get('error', 'Unknown error'),
                    'success': False
                }
                print(f"      ❌ Failed: {result['error']}")
            
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
    
    print(f"\n📊 AUDIO DEMO RESULTS:")
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
    
    # Save demo manifest
    demo_manifest_path = audio_dir / "demo_manifest.jsonl"
    with demo_manifest_path.open("w", encoding="utf-8") as f:
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
                    "sample_rate": 16000,
                    "channels": 1,
                    "file_size": result['file_size']
                }
                f.write(json.dumps(manifest_entry, ensure_ascii=False) + "\n")
    
    print(f"   📄 Demo manifest saved: {demo_manifest_path}")
    
    # Test voice variations
    print(f"\n🎭 VOICE VARIATION TEST:")
    agent_voices = set(r['speaker_id'] for r in successful if r['role'] == 'agent')
    user_voices = set(r['speaker_id'] for r in successful if r['role'] == 'user')
    
    print(f"   🤖 Agent voices tested: {len(agent_voices)} ({', '.join(agent_voices)})")
    print(f"   👤 User voices tested: {len(user_voices)} ({', '.join(user_voices)})")
    
    if failed:
        print(f"\n❌ FAILED GENERATIONS:")
        for fail in failed:
            print(f"   • {fail['speaker_id']}: {fail.get('error', 'Unknown error')}")
    
    # Instructions for listening
    if successful:
        print(f"\n🎧 TO LISTEN TO GENERATED AUDIO:")
        print(f"   Navigate to: {audio_dir}")
        print(f"   Play any .wav file with your audio player")
        print(f"   Compare different speaker_id voices")
        
        # Show first few files
        print(f"\n📂 SAMPLE FILES:")
        for result in successful[:3]:
            rel_path = pathlib.Path(result['file']).relative_to(pathlib.Path.cwd())
            print(f"   • {rel_path}")
            print(f"     Text: \"{result['transcript']}\"")
            print(f"     Speaker: {result['speaker_id']} ({result['role']})")
    
    return len(successful) > 0

def test_voice_characteristics():
    """Test different voice characteristics"""
    
    if not AUDIO_AVAILABLE:
        return
    
    print(f"\n🎨 VOICE CHARACTERISTICS TEST:")
    
    test_text = "Merhaba, size nasıl yardımcı olabilirim?"
    voice_tests = [
        ("agent_voice_001", "Normal agent voice"),
        ("agent_voice_002", "Higher pitch agent"),
        ("agent_voice_003", "Slower agent voice"),
        ("user_voice_001", "Normal user voice"),
        ("user_voice_002", "Slower user voice"),
        ("user_voice_003", "Faster user voice")
    ]
    
    voice_manager = VoiceManager()
    audio_dir = OUT_DIR / "demo_audio" / "voice_test"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    for speaker_id, description in voice_tests:
        try:
            audio_path = audio_dir / f"{speaker_id}_test.wav"
            result = voice_manager.generate_audio(test_text, speaker_id, audio_path)
            
            if result['success']:
                print(f"   ✅ {speaker_id}: {description} ({result['duration']:.2f}s)")
            else:
                print(f"   ❌ {speaker_id}: Failed - {result.get('error', 'Unknown')}")
                
        except Exception as e:
            print(f"   ❌ {speaker_id}: Exception - {e}")

def main():
    """Main demo function"""
    
    print("🚀 TURKISH TELECOM AUDIO GENERATION DEMO")
    print("=" * 60)
    
    # Test basic audio generation
    success = test_audio_generation()
    
    if success:
        # Test voice characteristics
        test_voice_characteristics()
        
        print(f"\n🎯 DEMO COMPLETED SUCCESSFULLY!")
        print(f"   Check the generated audio files in data/demo_audio/")
        print(f"   Ready to run full audio generation with main3_with_audio.py")
    else:
        print(f"\n❌ DEMO FAILED!")
        print(f"   Please check dependencies and configuration")
    
    return success

if __name__ == "__main__":
    main()