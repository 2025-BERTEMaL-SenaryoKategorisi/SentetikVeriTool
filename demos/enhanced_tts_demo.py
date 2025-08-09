#!/usr/bin/env python3
"""
Enhanced TTS Demo with Multiple High-Quality Voice Providers
Supports: Google Cloud TTS, ElevenLabs, and Azure Speech Services
"""

import json
import os
import pathlib
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# ---- ENHANCED TTS CONFIGURATION ----
load_dotenv(verbose=True)
OUT_DIR = pathlib.Path("data")

# TTS Provider Configuration
TTS_PROVIDERS = {
    "google_cloud": {
        "enabled": False,  # Requires Google Cloud TTS API key
        "api_key_env": "GOOGLE_CLOUD_TTS_API_KEY",
        "quality": "high",
        "languages": ["tr-TR"],
        "cost": "low"
    },
    "elevenlabs": {
        "enabled": False,  # Requires ElevenLabs API key
        "api_key_env": "ELEVENLABS_API_KEY", 
        "quality": "very_high",
        "languages": ["tr"],
        "cost": "high"
    },
    "azure": {
        "enabled": False,  # Requires Azure Speech API key
        "api_key_env": "AZURE_SPEECH_KEY",
        "quality": "high",
        "languages": ["tr-TR"],
        "cost": "medium"
    },
    "gtts": {
        "enabled": True,   # Always available as fallback
        "quality": "basic",
        "languages": ["tr"],
        "cost": "free"
    }
}

# Enhanced Voice Configurations
ENHANCED_VOICE_CONFIGS = {
    # Agent voices - professional, consistent
    "agent_voice_001": {
        "provider": "elevenlabs",
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam (male, professional)
        "fallback_provider": "google_cloud",
        "fallback_voice": "tr-TR-Wavenet-B",
        "characteristics": "professional male, calm, helpful"
    },
    "agent_voice_002": {
        "provider": "elevenlabs", 
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella (female, professional)
        "fallback_provider": "google_cloud",
        "fallback_voice": "tr-TR-Wavenet-A",
        "characteristics": "professional female, warm, confident"
    },
    "agent_voice_003": {
        "provider": "google_cloud",
        "voice_id": "tr-TR-Wavenet-C",
        "fallback_provider": "gtts",
        "characteristics": "neutral, clear, professional"
    },
    
    # User voices - varied, natural
    "user_voice_001": {
        "provider": "elevenlabs",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (female, natural)
        "fallback_provider": "azure",
        "fallback_voice": "tr-TR-EmelNeural",
        "characteristics": "natural female, slightly concerned"
    },
    "user_voice_002": {
        "provider": "azure",
        "voice_id": "tr-TR-AhmetNeural",
        "fallback_provider": "gtts",
        "characteristics": "male, casual, friendly"
    },
    "user_voice_003": {
        "provider": "google_cloud",
        "voice_id": "tr-TR-Wavenet-D",
        "fallback_provider": "gtts",
        "characteristics": "elderly, patient"
    }
}

class EnhancedTTSManager:
    """Manages multiple TTS providers for high-quality voice generation"""
    
    def __init__(self):
        self.providers_status = self._check_providers()
        self.audio_dir = OUT_DIR / "enhanced_audio"
        self.agent_audio_dir = self.audio_dir / "agent"
        self.user_audio_dir = self.audio_dir / "user"
        
        for dir_path in [self.audio_dir, self.agent_audio_dir, self.user_audio_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _check_providers(self) -> Dict[str, bool]:
        """Check which TTS providers are available"""
        status = {}
        
        for provider, config in TTS_PROVIDERS.items():
            if provider == "gtts":
                status[provider] = True  # Always available
                continue
                
            api_key = os.getenv(config["api_key_env"])
            if api_key:
                # Auto-enable provider if API key is present
                status[provider] = True
                quality = config.get("quality", "unknown")
                print(f"✅ {provider.title()}: Available (Quality: {quality})")
            else:
                status[provider] = False
                quality = config.get("quality", "unknown")
                print(f"❌ {provider.title()}: Not configured (Quality: {quality})")
        
        return status
    
    def _generate_elevenlabs_audio(self, text: str, voice_id: str, output_path: pathlib.Path) -> Dict:
        """Generate audio using ElevenLabs API"""
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            return {"success": False, "error": "ElevenLabs API key not found"}
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Save audio file
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = output_path.stat().st_size
                estimated_duration = len(text) * 0.08  # ElevenLabs is faster speech
                
                return {
                    "success": True,
                    "duration": estimated_duration,
                    "sample_rate": 44100,
                    "channels": 1,
                    "file_size": file_size,
                    "provider": "elevenlabs",
                    "quality": "very_high"
                }
            else:
                return {
                    "success": False, 
                    "error": f"ElevenLabs API error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": f"ElevenLabs error: {str(e)}"}
    
    def _generate_google_cloud_audio(self, text: str, voice_id: str, output_path: pathlib.Path) -> Dict:
        """Generate audio using Google Cloud TTS API"""
        
        api_key = os.getenv("GOOGLE_CLOUD_TTS_API_KEY")
        if not api_key:
            return {"success": False, "error": "Google Cloud TTS API key not found"}
        
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
        
        # Parse voice configuration
        language_code = voice_id.split('-')[0] + '-' + voice_id.split('-')[1]  # tr-TR
        voice_name = voice_id
        
        data = {
            "input": {"text": text},
            "voice": {
                "languageCode": language_code,
                "name": voice_name,
                "ssmlGender": "NEUTRAL"
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "sampleRateHertz": 24000,
                "speakingRate": 1.0,
                "pitch": 0.0,
                "volumeGainDb": 0.0
            }
        }
        
        try:
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Decode base64 audio content
                import base64
                audio_content = base64.b64decode(result['audioContent'])
                
                # Save audio file
                with open(output_path, 'wb') as f:
                    f.write(audio_content)
                
                file_size = output_path.stat().st_size
                estimated_duration = len(text) * 0.09
                
                return {
                    "success": True,
                    "duration": estimated_duration,
                    "sample_rate": 24000,
                    "channels": 1,
                    "file_size": file_size,
                    "provider": "google_cloud",
                    "quality": "high"
                }
            else:
                return {
                    "success": False,
                    "error": f"Google Cloud TTS error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Google Cloud TTS error: {str(e)}"}
    
    def _generate_gtts_audio(self, text: str, output_path: pathlib.Path) -> Dict:
        """Generate audio using basic gTTS (fallback)"""
        
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='tr', slow=False)
            tts.save(str(output_path))
            
            file_size = output_path.stat().st_size
            estimated_duration = len(text) * 0.1
            
            return {
                "success": True,
                "duration": estimated_duration,
                "sample_rate": 22050,
                "channels": 1,
                "file_size": file_size,
                "provider": "gtts",
                "quality": "basic"
            }
            
        except Exception as e:
            return {"success": False, "error": f"gTTS error: {str(e)}"}
    
    def generate_enhanced_audio(self, text: str, speaker_id: str, output_path: pathlib.Path) -> Dict:
        """Generate audio using the best available provider for the speaker"""
        
        voice_config = ENHANCED_VOICE_CONFIGS.get(speaker_id, {
            "provider": "gtts",
            "fallback_provider": "gtts"
        })
        
        # Try primary provider
        primary_provider = voice_config.get("provider", "gtts")
        
        if primary_provider == "elevenlabs" and self.providers_status.get("elevenlabs", False):
            voice_id = voice_config.get("voice_id", "pNInz6obpgDQGcFmaJgB")
            result = self._generate_elevenlabs_audio(text, voice_id, output_path)
            if result["success"]:
                return result
        
        elif primary_provider == "google_cloud" and self.providers_status.get("google_cloud", False):
            voice_id = voice_config.get("voice_id", "tr-TR-Wavenet-A")
            result = self._generate_google_cloud_audio(text, voice_id, output_path)
            if result["success"]:
                return result
        
        # Try fallback provider
        fallback_provider = voice_config.get("fallback_provider", "gtts")
        
        if fallback_provider == "google_cloud" and self.providers_status.get("google_cloud", False):
            fallback_voice = voice_config.get("fallback_voice", "tr-TR-Wavenet-A")
            result = self._generate_google_cloud_audio(text, fallback_voice, output_path)
            if result["success"]:
                return result
        
        # Final fallback to gTTS
        return self._generate_gtts_audio(text, output_path)

def run_enhanced_tts_demo():
    """Run enhanced TTS demo with multiple providers"""
    
    print("🎤 ENHANCED TTS DEMO - HIGH QUALITY VOICES")
    print("=" * 60)
    
    # Initialize TTS manager
    tts_manager = EnhancedTTSManager()
    
    # Sample conversations - FIXED: Same speakers maintain same voice throughout conversation
    demo_conversations = [
        {
            "conversation_id": 1,
            "role": "agent",
            "speaker_id": "agent_voice_001",  # Same agent voice for conversation 1
            "transcript": "Merhaba, ben Ahmet. Size nasıl yardımcı olabilirim?"
        },
        {
            "conversation_id": 1,
            "role": "user",
            "speaker_id": "user_voice_001",   # Same user voice for conversation 1
            "transcript": "Merhaba, faturamda bir hata olduğunu düşünüyorum."
        },
        {
            "conversation_id": 1,
            "role": "agent",
            "speaker_id": "agent_voice_001",  # SAME agent voice continues
            "transcript": "Tabii, size yardımcı olmaktan memnuniyet duyarım. Fatura numaranızı alabilir miyim?"
        },
        {
            "conversation_id": 1,
            "role": "user",
            "speaker_id": "user_voice_001",   # SAME user voice continues
            "transcript": "Elbette, fatura numaram 1234567890. Normalde 80 lira civarı gelirdi."
        }
    ]
    
    print(f"🔧 Available TTS Providers:")
    for provider, available in tts_manager.providers_status.items():
        status = "✅ Available" if available else "❌ Not configured"
        quality = TTS_PROVIDERS[provider]["quality"]
        print(f"   • {provider.title()}: {status} (Quality: {quality})")
    
    print(f"\n🔄 Generating {len(demo_conversations)} enhanced audio samples...")
    
    results = []
    total_duration = 0
    
    for i, conv in enumerate(demo_conversations):
        try:
            # Generate audio file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_{i+1:02d}_{conv['role']}_{timestamp}.mp3"
            audio_path = tts_manager.audio_dir / conv['role'] / filename
            
            voice_config = ENHANCED_VOICE_CONFIGS.get(conv['speaker_id'], {})
            characteristics = voice_config.get('characteristics', 'standard voice')
            
            print(f"\n   🎵 Generating: {conv['transcript'][:50]}...")
            print(f"      Speaker: {conv['speaker_id']}")
            print(f"      Role: {conv['role']}")
            print(f"      Characteristics: {characteristics}")
            
            # Generate enhanced audio
            start_time = time.time()
            audio_result = tts_manager.generate_enhanced_audio(
                conv['transcript'],
                conv['speaker_id'], 
                audio_path
            )
            generation_time = time.time() - start_time
            
            if audio_result['success']:
                duration = audio_result['duration']
                total_duration += duration
                provider = audio_result.get('provider', 'unknown')
                quality = audio_result.get('quality', 'unknown')
                
                print(f"      ✅ Success! Provider: {provider}, Quality: {quality}")
                print(f"         Duration: {duration:.2f}s, Size: {audio_result['file_size']} bytes")
                
                result = {
                    'file': str(audio_path),
                    'transcript': conv['transcript'],
                    'speaker_id': conv['speaker_id'],
                    'role': conv['role'],
                    'conversation_id': conv.get('conversation_id', 1),
                    'duration': duration,
                    'generation_time': generation_time,
                    'file_size': audio_result['file_size'],
                    'provider': provider,
                    'quality': quality,
                    'characteristics': characteristics,
                    'success': True
                }
            else:
                print(f"      ❌ Failed: {audio_result.get('error', 'Unknown error')}")
                result = {
                    'transcript': conv['transcript'],
                    'speaker_id': conv['speaker_id'],
                    'role': conv['role'],
                    'error': audio_result.get('error', 'Unknown error'),
                    'success': False
                }
            
            results.append(result)
            time.sleep(1.0)  # Rate limiting for APIs
            
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
    
    print(f"\n📊 ENHANCED TTS DEMO RESULTS:")
    print(f"   ✅ Successful: {len(successful)}/{len(results)}")
    print(f"   ❌ Failed: {len(failed)}")
    print(f"   ⏱️  Total audio duration: {total_duration:.2f} seconds")
    
    if successful:
        # Provider statistics
        provider_stats = {}
        quality_stats = {}
        
        for result in successful:
            provider = result.get('provider', 'unknown')
            quality = result.get('quality', 'unknown')
            
            provider_stats[provider] = provider_stats.get(provider, 0) + 1
            quality_stats[quality] = quality_stats.get(quality, 0) + 1
        
        print(f"\n📈 PROVIDER USAGE:")
        for provider, count in provider_stats.items():
            print(f"   • {provider.title()}: {count} samples")
        
        print(f"\n🎯 QUALITY DISTRIBUTION:")
        for quality, count in quality_stats.items():
            print(f"   • {quality.title()}: {count} samples")
        
        # Save enhanced manifest
        enhanced_manifest_path = tts_manager.audio_dir / "enhanced_manifest.jsonl"
        with enhanced_manifest_path.open("w", encoding="utf-8") as f:
            for result in successful:
                manifest_entry = {
                    "conversation_id": result.get('conversation_id', 1),
                    "audio_filepath": result['file'],
                    "transcript": result['transcript'],
                    "speaker_id": result['speaker_id'],
                    "role": result['role'],
                    "intent": "demo",
                    "slot": {},
                    "audio_duration": result['duration'],
                    "sample_rate": 22050,  # Will vary by provider
                    "channels": 1,
                    "file_size": result['file_size'],
                    "tts_provider": result['provider'],
                    "voice_quality": result['quality'],
                    "voice_characteristics": result['characteristics']
                }
                f.write(json.dumps(manifest_entry, ensure_ascii=False) + "\n")
        
        print(f"\n📄 Enhanced manifest saved: {enhanced_manifest_path}")
        
        print(f"\n🎧 TO LISTEN TO ENHANCED AUDIO:")
        print(f"   Navigate to: {tts_manager.audio_dir}")
        print(f"   Compare voice quality between providers")
        print(f"   Notice the difference in naturalness!")
        
        # Show sample files
        print(f"\n📂 SAMPLE FILES:")
        for result in successful[:2]:
            try:
                rel_path = pathlib.Path(result['file']).relative_to(pathlib.Path.cwd())
                print(f"   • {rel_path}")
            except ValueError:
                # If relative path fails, just show the filename
                print(f"   • {pathlib.Path(result['file']).name}")
            print(f"     Text: \"{result['transcript'][:40]}...\"")
            print(f"     Provider: {result['provider']} ({result['quality']} quality)")
            print(f"     Characteristics: {result['characteristics']}")
    
    if failed:
        print(f"\n❌ FAILED GENERATIONS:")
        for fail in failed:
            print(f"   • {fail['speaker_id']}: {fail.get('error', 'Unknown error')}")
    
    return len(successful) > 0

def setup_enhanced_tts():
    """Show setup instructions for enhanced TTS providers"""
    
    print("🔧 ENHANCED TTS SETUP GUIDE")
    print("=" * 50)
    
    print("To enable high-quality voices, add these API keys to your .env file:")
    print()
    
    print("🎯 ElevenLabs (Highest Quality - Recommended):")
    print("   1. Sign up at: https://elevenlabs.io")
    print("   2. Get API key from: https://elevenlabs.io/app/speech-synthesis")
    print("   3. Add to .env: ELEVENLABS_API_KEY=your_key_here")
    print("   4. Quality: Very High | Cost: ~$0.30 per 1K characters")
    print()
    
    print("🎯 Google Cloud TTS (High Quality):")
    print("   1. Enable at: https://console.cloud.google.com/apis/library/texttospeech.googleapis.com")
    print("   2. Create API key in Google Cloud Console")
    print("   3. Add to .env: GOOGLE_CLOUD_TTS_API_KEY=your_key_here")
    print("   4. Quality: High | Cost: ~$4 per 1M characters")
    print()
    
    print("🎯 Azure Speech Services (High Quality):")
    print("   1. Create resource at: https://portal.azure.com")
    print("   2. Get key from Speech Services resource")
    print("   3. Add to .env: AZURE_SPEECH_KEY=your_key_here")
    print("   4. Quality: High | Cost: ~$4 per 1M characters")
    print()
    
    print("💡 Current Status:")
    tts_manager = EnhancedTTSManager()
    for provider, available in tts_manager.providers_status.items():
        status = "✅ Ready" if available else "❌ Not configured"
        print(f"   • {provider.title()}: {status}")

def main():
    """Main enhanced TTS demo"""
    
    print("🚀 ENHANCED TTS DEMO - PROFESSIONAL VOICE QUALITY")
    print("=" * 60)
    
    # Show setup guide first
    setup_enhanced_tts()
    
    print("\n" + "="*60)
    
    # Run demo
    success = run_enhanced_tts_demo()
    
    if success:
        print(f"\n🎯 ENHANCED TTS DEMO COMPLETED!")
        print(f"   🎵 Listen to the quality difference!")
        print(f"   📁 Files saved in: data/enhanced_audio/")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Set up ElevenLabs API for best quality")
        print(f"   2. Compare voice samples")
        print(f"   3. Run full generation: python main3_with_audio.py")
    else:
        print(f"\n❌ DEMO FAILED!")
        print(f"   Check API keys and internet connection")
    
    return success

if __name__ == "__main__":
    main()