#!/usr/bin/env python3
"""
Enhanced Turkish Telecom Synthetic Data Generator with TTS Audio Generation
Generates both text transcripts and actual audio files for ASR/TTS training
"""

import json
import os
import random
import re
import pathlib
import time
import uuid
import librosa
import soundfile as sf
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tqdm import tqdm
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
import base64

# ---- LOAD ENVIRONMENT FIRST ----
# Load .env from project root directory before importing config
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path, verbose=True)

# Import configuration after loading environment
sys.path.append(project_root)
from config.config import *

# ---- AUDIO CONFIGURATION ----
AUDIO_CONFIG = {
    'sample_rate': 16000,  # Standard for ASR
    'channels': 1,         # Mono
    'bit_depth': 16,       # 16-bit
    'format': 'wav',       # WAV format
    'normalize': True,     # Normalize audio levels
    'add_noise': True,     # Add slight background noise for realism
    'speed_variation': True, # Vary speech speed slightly
}

# ---- ENHANCED TTS VOICE MAPPING SYSTEM ----
# Turkish Name Gender Classification
TURKISH_MALE_NAMES = {
    "Ahmet", "Mehmet", "Ali", "Veli", "Burak", "Cem", "Furkan", "Hakan",
    "Kemal", "Murat", "Oğuz", "Rıza", "Tolga", "Ufuk", "Volkan", "Zeki",
    "Emre", "Serkan", "Özkan", "Taner", "Selim", "Berk", "Kaan", "Onur",
    "Barış", "Arda", "Eren", "Kağan", "Alper", "Sinan", "Gökhan", "Erhan"
}

TURKISH_FEMALE_NAMES = {
    "Ayşe", "Fatma", "Zeynep", "Elif", "Deniz", "Ece", "Gül", "İrem",
    "Leyla", "Nalan", "Pınar", "Seda", "Yasemin", "Aslı", "Ebru", "Gamze",
    "Hülya", "Işıl", "Jale", "Kübra", "Lale", "Melike", "Nazlı", "Özlem",
    "Pelin", "Reyhan", "Sibel", "Tülay", "Ülkü", "Vildan", "Yeliz", "Zuhal"
}

# Gender-Aware ElevenLabs Voice Configurations
ENHANCED_VOICE_CONFIGS = {
    # MALE AGENT VOICES - Professional, authoritative
    "agent_male_001": {
        "provider": "elevenlabs",
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam (male, professional)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "pNInz6obpgDQGcFmaJgB",
        "gender": "male",
        "characteristics": "professional male, calm, helpful"
    },
    "agent_male_002": {
        "provider": "elevenlabs",
        "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni (male, professional)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "ErXwobaYiN019PkySvjV",
        "gender": "male",
        "characteristics": "professional male, clear, authoritative"
    },
    "agent_male_003": {
        "provider": "elevenlabs",
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Arnold (male, authoritative)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "VR6AewLTigWG4xSOukaG",
        "gender": "male",
        "characteristics": "professional male, confident, mature"
    },
    
    # FEMALE AGENT VOICES - Professional, warm
    "agent_female_001": {
        "provider": "elevenlabs",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella (female, professional)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "EXAVITQu4vr4xnSDxMaL",
        "gender": "female",
        "characteristics": "professional female, warm, confident"
    },
    "agent_female_002": {
        "provider": "elevenlabs",
        "voice_id": "pMsXgVXv3BLzUgSXRplE",  # Domi (female, confident)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "pMsXgVXv3BLzUgSXRplE",
        "gender": "female",
        "characteristics": "professional female, authoritative, clear"
    },
    "agent_female_003": {
        "provider": "elevenlabs",
        "voice_id": "ThT5KcBeYPX3keUQqHPh",  # Dorothy (female, energetic)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "ThT5KcBeYPX3keUQqHPh",
        "gender": "female",
        "characteristics": "professional female, energetic, helpful"
    },
    
    # MALE USER VOICES - Natural, varied
    "user_male_001": {
        "provider": "elevenlabs",
        "voice_id": "flq6f7yk4E4fJM5XTYuZ",  # Michael (male, natural)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "flq6f7yk4E4fJM5XTYuZ",
        "gender": "male",
        "characteristics": "natural male, casual, friendly"
    },
    "user_male_002": {
        "provider": "elevenlabs",
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam (male, variant)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "pNInz6obpgDQGcFmaJgB",
        "gender": "male",
        "characteristics": "natural male, concerned, mature"
    },
    "user_male_003": {
        "provider": "elevenlabs",
        "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni (male, variant)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "ErXwobaYiN019PkySvjV",
        "gender": "male",
        "characteristics": "natural male, patient, elderly"
    },
    
    # FEMALE USER VOICES - Natural, varied
    "user_female_001": {
        "provider": "elevenlabs",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (female, natural)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "21m00Tcm4TlvDq8ikWAM",
        "gender": "female",
        "characteristics": "natural female, slightly concerned"
    },
    "user_female_002": {
        "provider": "elevenlabs",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella (female, variant)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "EXAVITQu4vr4xnSDxMaL",
        "gender": "female",
        "characteristics": "natural female, patient, mature"
    },
    "user_female_003": {
        "provider": "elevenlabs",
        "voice_id": "ThT5KcBeYPX3keUQqHPh",  # Dorothy (female, variant)
        "fallback_provider": "elevenlabs",
        "fallback_voice": "ThT5KcBeYPX3keUQqHPh",
        "gender": "female",
        "characteristics": "natural female, energetic, young"
    }
}

def get_gender_from_name(name: str) -> str:
    """Determine gender from Turkish name"""
    if name in TURKISH_MALE_NAMES:
        return "male"
    elif name in TURKISH_FEMALE_NAMES:
        return "female"
    else:
        # Default fallback based on common Turkish name patterns
        if name.endswith(('e', 'a', 'ş', 'ü', 'ö')):
            return "female"
        else:
            return "male"

def get_voice_for_agent(agent_name: str) -> str:
    """Get appropriate voice ID for agent based on gender"""
    gender = get_gender_from_name(agent_name)
    
    if gender == "male":
        male_voices = [k for k in ENHANCED_VOICE_CONFIGS.keys() if k.startswith("agent_male_")]
        return random.choice(male_voices)
    else:
        female_voices = [k for k in ENHANCED_VOICE_CONFIGS.keys() if k.startswith("agent_female_")]
        return random.choice(female_voices)

def get_voice_for_user(gender_preference: str = None) -> str:
    """Get appropriate voice ID for user based on gender preference"""
    if gender_preference is None:
        gender_preference = random.choice(["male", "female"])
    
    if gender_preference == "male":
        male_voices = [k for k in ENHANCED_VOICE_CONFIGS.keys() if k.startswith("user_male_")]
        return random.choice(male_voices)
    else:
        female_voices = [k for k in ENHANCED_VOICE_CONFIGS.keys() if k.startswith("user_female_")]
        return random.choice(female_voices)

# TTS Provider Configuration
TTS_PROVIDERS = {
    "google_cloud": {
        "enabled": False,
        "api_key_env": "GOOGLE_CLOUD_TTS_API_KEY",
        "quality": "high"
    },
    "elevenlabs": {
        "enabled": False,
        "api_key_env": "ELEVENLABS_API_KEY",
        "quality": "very_high"
    },
    "azure": {
        "enabled": False,
        "api_key_env": "AZURE_SPEECH_KEY",
        "quality": "high"
    },
    "gtts": {
        "enabled": True,
        "quality": "basic"
    }
}

class EnhancedVoiceManager:
    """Enhanced TTS voice generation with multiple high-quality providers"""
    
    def __init__(self):
        self.providers_status = self._check_providers()
        
        # Create audio output directories
        self.audio_dir = OUT_DIR / "audio"
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
                status[provider] = True
                print(f"✅ {provider.title()}: Available (Quality: {config['quality']})")
            else:
                status[provider] = False
                print(f"❌ {provider.title()}: Not configured (Quality: {config['quality']})")
        
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
                # Save audio file as MP3 first
                mp3_path = output_path.with_suffix('.mp3')
                with open(mp3_path, 'wb') as f:
                    f.write(response.content)
                
                # Convert to WAV
                audio = AudioSegment.from_mp3(str(mp3_path))
                audio = audio.set_frame_rate(AUDIO_CONFIG['sample_rate'])
                audio = audio.set_channels(AUDIO_CONFIG['channels'])
                audio.export(str(output_path), format="wav")
                
                # Clean up MP3
                os.unlink(mp3_path)
                
                file_size = output_path.stat().st_size
                estimated_duration = len(text) * 0.08
                
                return {
                    "success": True,
                    "duration": estimated_duration,
                    "sample_rate": AUDIO_CONFIG['sample_rate'],
                    "channels": AUDIO_CONFIG['channels'],
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
                "audioEncoding": "LINEAR16",
                "sampleRateHertz": AUDIO_CONFIG['sample_rate'],
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
                audio_content = base64.b64decode(result['audioContent'])
                
                # Save audio file
                with open(output_path, 'wb') as f:
                    f.write(audio_content)
                
                file_size = output_path.stat().st_size
                estimated_duration = len(text) * 0.09
                
                return {
                    "success": True,
                    "duration": estimated_duration,
                    "sample_rate": AUDIO_CONFIG['sample_rate'],
                    "channels": AUDIO_CONFIG['channels'],
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
            tts = gTTS(text=text, lang='tr', slow=False)
            
            # Save as MP3 first
            mp3_path = output_path.with_suffix('.mp3')
            tts.save(str(mp3_path))
            
            # Convert to WAV
            audio = AudioSegment.from_mp3(str(mp3_path))
            audio = audio.set_frame_rate(AUDIO_CONFIG['sample_rate'])
            audio = audio.set_channels(AUDIO_CONFIG['channels'])
            audio.export(str(output_path), format="wav")
            
            # Clean up MP3
            os.unlink(mp3_path)
            
            file_size = output_path.stat().st_size
            estimated_duration = len(text) * 0.1
            
            return {
                "success": True,
                "duration": estimated_duration,
                "sample_rate": AUDIO_CONFIG['sample_rate'],
                "channels": AUDIO_CONFIG['channels'],
                "file_size": file_size,
                "provider": "gtts",
                "quality": "basic"
            }
            
        except Exception as e:
            return {"success": False, "error": f"gTTS error: {str(e)}"}
    
    def generate_audio(self, text: str, speaker_id: str, output_path: pathlib.Path) -> Dict[str, any]:
        """Generate audio using HIGH-QUALITY providers only (ElevenLabs or Google Cloud TTS)"""
        
        voice_config = ENHANCED_VOICE_CONFIGS.get(speaker_id, {
            "provider": "elevenlabs",
            "voice_id": "pNInz6obpgDQGcFmaJgB"
        })
        
        # TRY ELEVENLABS FIRST (HIGHEST QUALITY)
        if self.providers_status.get("elevenlabs", False):
            voice_id = voice_config.get("voice_id", "pNInz6obpgDQGcFmaJgB")
            result = self._generate_elevenlabs_audio(text, voice_id, output_path)
            if result["success"]:
                return result
            print(f"⚠️  ElevenLabs failed: {result.get('error', 'Unknown error')}")
        
        # FALLBACK TO GOOGLE CLOUD TTS (HIGH QUALITY)
        if self.providers_status.get("google_cloud", False):
            print("🔄 Using Google Cloud TTS as high-quality fallback...")
            google_voice = "tr-TR-Wavenet-A" if "user" in speaker_id else "tr-TR-Wavenet-B"
            result = self._generate_google_cloud_audio(text, google_voice, output_path)
            if result["success"]:
                return result
            print(f"⚠️  Google Cloud TTS failed: {result.get('error', 'Unknown error')}")
        
        # NO LOW-QUALITY FALLBACKS - FAIL IF HIGH-QUALITY OPTIONS UNAVAILABLE
        return {"success": False, "error": "No high-quality TTS providers available (ElevenLabs quota exceeded, Google Cloud TTS failed)"}

# ---- GENDER-AWARE SPEAKER MANAGEMENT ----
class SpeakerManager:
    """Manages gender-aware speaker IDs for consistent voice assignment across conversations"""
    
    def __init__(self):
        self.conversation_speakers = {}
        self.conversation_agent_names = {}  # Track agent names per conversation
        self.voice_manager = EnhancedVoiceManager()
    
    def assign_speakers(self, conversation_id: int, agent_name: str) -> Tuple[str, str]:
        if conversation_id not in self.conversation_speakers:
            # Get gender-appropriate agent voice based on agent name
            agent_voice = get_voice_for_agent(agent_name)
            
            # Get random gender for user (diverse dataset)
            user_voice = get_voice_for_user()
            
            self.conversation_speakers[conversation_id] = (agent_voice, user_voice)
            self.conversation_agent_names[conversation_id] = agent_name
            
            # Log gender matching
            agent_gender = ENHANCED_VOICE_CONFIGS[agent_voice]["gender"]
            user_gender = ENHANCED_VOICE_CONFIGS[user_voice]["gender"]
            print(f"🎭 Conv {conversation_id}: Agent '{agent_name}' ({agent_gender}) → {agent_voice}")
            print(f"🎭 Conv {conversation_id}: User ({user_gender}) → {user_voice}")
            
        return self.conversation_speakers[conversation_id]
    
    def get_speaker_id(self, conversation_id: int, role: str, agent_name: str = None) -> str:
        if agent_name is None:
            agent_name = self.conversation_agent_names.get(conversation_id, "Ahmet")
            
        agent_voice, user_voice = self.assign_speakers(conversation_id, agent_name)
        return agent_voice if role == "agent" else user_voice
    
    def generate_audio_for_turn(self, text: str, speaker_id: str, audio_filepath: str) -> Dict[str, any]:
        """Generate audio file for a conversation turn"""
        audio_path = pathlib.Path(audio_filepath)
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        return self.voice_manager.generate_audio(text, speaker_id, audio_path)

# ---- LLM SETUP ----
agent_llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE_AGENT,
    google_api_key=GOOGLE_API_KEY,
    max_retries=3,
)

user_llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE_USER,
    google_api_key=GOOGLE_API_KEY,
    max_retries=3,
)

# ---- HELPER FUNCTIONS ----
def clean_and_parse_json(response_content: str) -> Optional[Dict]:
    """Extract and parse JSON from LLM response"""
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_content, re.DOTALL)
    if not match:
        match = re.search(r'\{.*\}', response_content, re.DOTALL)
    
    if not match:
        return None
    
    json_str = match.group(1) if '```json' in match.group(0) else match.group(0)
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

def generate_audio_filepath(conversation_id: int, turn_number: int, role: str) -> str:
    """Generate unique audio file path (prevents duplicates)"""
    base_filename = f"{conversation_id:04d}_{turn_number:02d}"
    audio_dir = pathlib.Path(f"data/audio/{role}")
    
    # Check if file already exists for this conversation_id and turn_number
    existing_files = list(audio_dir.glob(f"{base_filename}_*.wav"))
    
    if existing_files:
        # Return existing file path to prevent duplicates
        return str(existing_files[0])
    
    # Generate new unique file path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"data/audio/{role}/{base_filename}_{timestamp}_{unique_id}.wav"

def check_turn_already_exists(conversation_id: int, turn_number: int, role: str) -> bool:
    """Check if a turn already exists in the manifest"""
    manifest_path = OUT_DIR / "training_manifest_with_audio.jsonl"
    
    if not manifest_path.exists():
        return False
    
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if (data.get("conversation_id") == conversation_id and
                        data.get("role") == role and
                        f"_{turn_number:02d}_" in data.get("audio_filepath", "")):
                        return True
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    
    return False

def create_generation_prompt(context: Dict) -> str:
    """Create prompt for conversation generation"""
    
    scenario_info = TELECOM_SCENARIOS[context['scenario_name']]
    
    prompt_template = f"""Sen {context['agent_name']} adında Türk telekom şirketinde çalışan bir müşteri hizmetleri temsilcisisin. Gerçekçi bir telefon görüşmesi için tek bir konuşma turu oluşturuyorsun.

# ZORUNLU ÇIKTI FORMATI
Sadece aşağıdaki JSON formatında yanıt ver, başka hiçbir açıklama yapma:

{{
    "conversation_id": {context['conversation_id']},
    "audio_filepath": "ses_dosyasi_yolu",
    "transcript": "konuşma_metni",
    "speaker_id": "konuşmacı_kimliği", 
    "role": "agent_veya_user",
    "intent": "niyet_etiketi",
    "slot": {{anahtar: "değer"}}
}}

# SENARYO BİLGİLERİ
- **Senaryo**: {context['scenario_name']} - {scenario_info['description']}
- **Akış**: {scenario_info['flow']}
- **Görüşme ID**: {context['conversation_id']}
- **Tur**: {context['turn_number']}/{context['total_turns']}

# KONUŞMA GEÇMİŞİ
{context['history_str']}

# BU TUR İÇİN TALİMATLAR
- **Rolün**: {context['role']}
- **Görevin**: {context['turn_instruction']}

# TÜRKÇE DİL KURALLARI
- Doğal, günlük Türkçe kullan
- Telekom terminolojisini doğru kullan
- Gerektiğinde dolgu kelimeler ekle: {', '.join(random.sample(TURKISH_FILLERS, 3))}
- Konuşma metni 40-150 karakter arası olmalı
- Ses dosyası için uygun, akıcı konuşma

# NİYET VE SLOT KURALLARI
- **info_request**: slot = {{"requested": "istenen_bilgi"}}
- **info_provide**: slot = {{"sağlanan_bilgi": "değer"}}
- **solution**: slot = {{"solution_type": "çözüm_türü", "details": "detaylar"}}
- **Diğer niyetler**: slot = {{}}

# SES DOSYASI KURALLARI
- audio_filepath: Gerçekçi dosya yolu oluştur
- speaker_id: {context['speaker_id']} kullan
- role: "{context['role']}" olmalı

JSON YANITI:"""

    return prompt_template

def get_turn_instruction(role: str, history: List[Dict], total_turns: int, turn_number: int, scenario_name: str, agent_name: str) -> str:
    """Get instruction for current turn"""
    
    scenario_info = TELECOM_SCENARIOS[scenario_name]
    
    if turn_number == 1:
        return f'Sen {agent_name} adındaki ajansın. Sıcak bir selamlama yap ve nasıl yardımcı olabileceğini sor. Intent: "greeting"'
    
    last_turn = history[-1] if history else {}
    
    if turn_number == total_turns - 1:
        return 'Sen ajansın. Sorunu çözdün, nazikçe görüşmeyi sonlandır. Intent: "closing"'
    if turn_number == total_turns:
        return 'Sen kullanıcısın. Ajana teşekkür et. Intent: "thanks"'
    
    if role == "agent":
        if scenario_name == "billing_dispute":
            if last_turn.get('intent') == 'complaint':
                return 'Fatura detaylarını öğrenmek için bilgi iste. Intent: "info_request"'
            elif last_turn.get('intent') == 'info_provide' and turn_number > 4:
                return 'Soruna çözüm öner (iade, düzeltme vb.). Intent: "solution"'
        
        elif scenario_name == "technical_support":
            if last_turn.get('intent') == 'complaint':
                return 'Teknik detayları öğrenmek için soru sor. Intent: "info_request"'
            elif last_turn.get('intent') == 'info_provide' and turn_number > 4:
                return 'Teknik çözüm öner (reset, teknisyen vb.). Intent: "solution"'
        
        if last_turn.get('intent') in ['complaint', 'info_request']:
            return 'Daha fazla bilgi toplamak için soru sor. Intent: "info_request"'
        elif last_turn.get('intent') == 'info_provide':
            return 'Bilgiyi işle ve uygun yanıt ver. Intent: "info_provide" veya "solution"'
        
        return 'Görüşmeyi ilerletmek için uygun yanıt ver.'
    
    else:  # role == "user"
        if last_turn.get('intent') == 'greeting':
            if scenario_name in ['billing_dispute', 'technical_support']:
                return 'Sorununuzu açıklayın. Intent: "complaint"'
            else:
                return 'Neye ihtiyacınız olduğunu belirtin. Intent: "info_request"'
        
        elif last_turn.get('intent') == 'info_request':
            return 'İstenen bilgiyi sağlayın. Intent: "info_provide"'
        
        elif last_turn.get('intent') in ['solution', 'options_presentation']:
            return 'Önerilen çözümü kabul edin veya soru sorun. Intent: "confirmation" veya "info_request"'
        
        return 'Doğal şekilde görüşmeye devam edin.'

def validate_conversation_with_audio(history: List[Dict], conv_id: int, scenario_name: str) -> bool:
    """Validate conversation including audio metadata"""
    
    if not (TURNS_PER_DIALOG_MIN <= len(history) <= TURNS_PER_DIALOG_MAX):
        print(f"  [FAIL] Conv {conv_id}: Turn count ({len(history)}) out of range.")
        return False
    
    for i, turn in enumerate(history):
        expected_role = "agent" if (i + 1) % 2 != 0 else "user"
        if turn['role'] != expected_role:
            print(f"  [FAIL] Conv {conv_id}: Turn {i + 1} wrong role '{turn['role']}'.")
            return False
        
        # Check audio file exists
        audio_path = pathlib.Path(turn.get('audio_filepath', ''))
        if not audio_path.exists():
            print(f"  [FAIL] Conv {conv_id}: Turn {i + 1} audio file missing: {audio_path}")
            return False
        
        # Check audio metadata
        if 'audio_duration' not in turn or turn['audio_duration'] <= 0:
            print(f"  [FAIL] Conv {conv_id}: Turn {i + 1} missing or invalid audio duration.")
            return False
        
        # Transcript length check
        transcript_len = len(turn.get('transcript', ''))
        if transcript_len < 20 or transcript_len > 200:
            print(f"  [FAIL] Conv {conv_id}: Turn {i + 1} transcript length ({transcript_len}) invalid.")
            return False
    
    # Check ending
    if history[-2]['role'] != 'agent' or history[-2]['intent'] != 'closing':
        print(f"  [FAIL] Conv {conv_id}: Missing proper agent closing.")
        return False
    
    if history[-1]['role'] != 'user' or history[-1]['intent'] not in ['thanks', 'confirmation']:
        print(f"  [FAIL] Conv {conv_id}: Missing proper user thanks.")
        return False
    
    print(f"  [PASS] Conv {conv_id} validation successful with audio.")
    return True

def get_next_conversation_id():
    """Get the next conversation ID by checking ALL existing data files (audio + text)"""
    max_id = 0
    
    # Check all possible data directories and files
    data_paths = [
        # Audio data files (current generator's output)
        OUT_DIR / "training_manifest_with_audio.jsonl",
        OUT_DIR / "asr_training_data_with_audio.jsonl",
        OUT_DIR / "tts_training_data_with_audio.jsonl",
        # Text-only data files
        pathlib.Path("data/text_only/text_conversations.jsonl"),
        pathlib.Path("data/text_only/text_asr_data.jsonl"),
        pathlib.Path("data/text_only/text_tts_data.jsonl"),
    ]
    
    for file_path in data_paths:
        if file_path.exists():
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            max_id = max(max_id, data.get("conversation_id", 0))
            except (json.JSONDecodeError, FileNotFoundError):
                continue
    
    return max_id + 1

def reset_training_data():
    """Reset all training data files (use with caution!)"""
    import shutil
    
    print("🚨 RESETTING ALL TRAINING DATA...")
    
    # Remove manifest files
    files_to_remove = [
        OUT_DIR / "training_manifest_with_audio.jsonl",
        OUT_DIR / "asr_training_data_with_audio.jsonl",
        OUT_DIR / "tts_training_data_with_audio.jsonl"
    ]
    
    for file_path in files_to_remove:
        if file_path.exists():
            file_path.unlink()
            print(f"🗑️  Removed: {file_path}")
    
    # Remove audio directories
    audio_dir = OUT_DIR / "audio"
    if audio_dir.exists():
        shutil.rmtree(audio_dir)
        print(f"🗑️  Removed: {audio_dir}")
    
    print("✅ All training data reset. Next run will start from conversation ID 1.")

# Uncomment the line below to reset data before generation
# reset_training_data()

def generate_synthetic_data_with_audio():
    """Main function to generate synthetic training data with audio files (INCREMENTAL)"""
    
    print("🎤 TURKISH TELECOM SYNTHETIC DATA GENERATOR WITH AUDIO (INCREMENTAL)")
    print("=" * 70)
    
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        print("❌ Configuration errors:")
        for error in config_errors:
            print(f"   • {error}")
        return
    
    speaker_manager = SpeakerManager()
    all_manifest_rows = []
    OUT_DIR.mkdir(exist_ok=True)
    
    # Create audio directories
    (OUT_DIR / "audio" / "agent").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "audio" / "user").mkdir(parents=True, exist_ok=True)
    
    # Get starting conversation ID (incremental)
    starting_conversation_id = get_next_conversation_id()
    print(f"📊 Starting from conversation ID: {starting_conversation_id}")
    
    # Check if files exist
    manifest_path = OUT_DIR / "training_manifest_with_audio.jsonl"
    if manifest_path.exists():
        print(f"📁 Existing data found - will APPEND new conversations")
    else:
        print(f"📁 No existing data - creating new files")
    
    # Get scenario distribution
    scenario_distribution = get_scenario_distribution()
    
    pbar = tqdm(total=NUM_CONVERSATIONS, desc="Generating Conversations with Audio")
    
    successful_conversations = 0
    total_audio_duration = 0
    
    for conv_idx in range(NUM_CONVERSATIONS):
        conversation_id = starting_conversation_id + conv_idx
        scenario_name = scenario_distribution[conv_idx]
        
        max_retries = MAX_RETRIES_PER_CONVERSATION
        for attempt in range(max_retries):
            try:
                history = []
                agent_name = random.choice(AGENT_NAMES)
                num_turns = random.randint(TURNS_PER_DIALOG_MIN, TURNS_PER_DIALOG_MAX)
                
                if num_turns % 2 != 0:
                    num_turns += 1
                
                generation_successful = True
                
                for turn_number in range(1, num_turns + 1):
                    role = "agent" if turn_number % 2 != 0 else "user"
                    
                    # Skip if this turn already exists (prevents duplicates)
                    if check_turn_already_exists(conversation_id, turn_number, role):
                        print(f"⏭️  Skipping Conv {conversation_id}, Turn {turn_number} ({role}) - already exists")
                        continue
                    
                    speaker_id = speaker_manager.get_speaker_id(conversation_id, role, agent_name)
                    audio_filepath = generate_audio_filepath(conversation_id, turn_number, role)
                    
                    context = {
                        "conversation_id": conversation_id,
                        "agent_name": agent_name,
                        "scenario_name": scenario_name,
                        "role": role,
                        "turn_number": turn_number,
                        "total_turns": num_turns,
                        "speaker_id": speaker_id,
                        "history_str": "\n".join([json.dumps(t, ensure_ascii=False) for t in history[-3:]]),
                        "turn_instruction": get_turn_instruction(role, history, num_turns, turn_number, scenario_name, agent_name)
                    }
                    
                    # Generate text
                    prompt = create_generation_prompt(context)
                    llm_to_use = agent_llm if role == "agent" else user_llm
                    
                    response = llm_to_use.invoke(prompt)
                    llm_output = clean_and_parse_json(response.content)
                    
                    if not llm_output:
                        print(f"\nJSON parse failed for Conv {conversation_id}, Turn {turn_number}")
                        generation_successful = False
                        break
                    
                    transcript = llm_output.get("transcript", "").strip()
                    
                    # Generate audio (only if file doesn't exist)
                    audio_path = pathlib.Path(audio_filepath)
                    if audio_path.exists():
                        print(f"🔄 Reusing existing audio: {audio_filepath}")
                        # Get file info for existing audio
                        file_size = audio_path.stat().st_size
                        estimated_duration = len(transcript) * 0.08
                        audio_result = {
                            'success': True,
                            'duration': estimated_duration,
                            'sample_rate': 16000,
                            'channels': 1,
                            'file_size': file_size
                        }
                    else:
                        audio_result = speaker_manager.generate_audio_for_turn(
                            transcript, speaker_id, audio_filepath
                        )
                        
                        if not audio_result['success']:
                            print(f"\nAudio generation failed for Conv {conversation_id}, Turn {turn_number}")
                            generation_successful = False
                            break
                    
                    # Create final turn data with audio metadata
                    final_turn_data = {
                        "conversation_id": conversation_id,
                        "audio_filepath": audio_filepath,
                        "transcript": transcript,
                        "speaker_id": speaker_id,
                        "role": role,
                        "intent": llm_output.get("intent", ""),
                        "slot": llm_output.get("slot", {}),
                        "audio_duration": audio_result['duration'],
                        "sample_rate": audio_result['sample_rate'],
                        "channels": audio_result['channels'],
                        "file_size": audio_result.get('file_size', 0)
                    }
                    
                    history.append(final_turn_data)
                    total_audio_duration += audio_result['duration']
                    
                    time.sleep(RATE_LIMIT_DELAY)
                
                # Validate conversation
                if generation_successful and validate_conversation_with_audio(history, conversation_id, scenario_name):
                    all_manifest_rows.extend(history)
                    successful_conversations += 1
                    pbar.update(1)
                    break
                
            except Exception as e:
                print(f"\nError in Conv {conversation_id}, Attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    print(f"Skipping conversation {conversation_id} after {max_retries} attempts")
    
    pbar.close()
    
    # APPEND to existing manifest files (incremental)
    manifest_path = OUT_DIR / "training_manifest_with_audio.jsonl"
    with manifest_path.open("a", encoding="utf-8") as f:  # "a" for append
        for row in all_manifest_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Generate separate files for ASR and TTS (append mode)
    asr_data = all_manifest_rows
    tts_data = [row for row in all_manifest_rows if row['role'] == 'agent']
    
    asr_path = OUT_DIR / "asr_training_data_with_audio.jsonl"
    with asr_path.open("a", encoding="utf-8") as f:  # "a" for append
        for row in asr_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    tts_path = OUT_DIR / "tts_training_data_with_audio.jsonl"
    with tts_path.open("a", encoding="utf-8") as f:  # "a" for append
        for row in tts_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Calculate statistics for this session
    new_agent_utterances = len(tts_data)
    new_user_utterances = len(asr_data) - new_agent_utterances
    new_unique_agent_voices = len(set(row['speaker_id'] for row in tts_data))
    new_unique_user_voices = len(set(row['speaker_id'] for row in asr_data if row['role'] == 'user'))
    new_audio_hours = total_audio_duration / 3600
    
    # Calculate total statistics from all files
    total_conversations = 0
    total_utterances = 0
    total_agent_utterances = 0
    total_user_utterances = 0
    
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            all_conversation_ids = set()
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    all_conversation_ids.add(data.get("conversation_id", 0))
                    total_utterances += 1
                    if data.get("role") == "agent":
                        total_agent_utterances += 1
                    else:
                        total_user_utterances += 1
            total_conversations = len(all_conversation_ids)
    except (json.JSONDecodeError, FileNotFoundError):
        total_conversations = successful_conversations
        total_utterances = len(all_manifest_rows)
        total_agent_utterances = new_agent_utterances
        total_user_utterances = new_user_utterances
    
    print(f"\n{'='*70}")
    print(f"🎤 INCREMENTAL DATA GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"📊 THIS SESSION:")
    print(f"   ✅ New conversations: {successful_conversations}/{NUM_CONVERSATIONS}")
    print(f"   📊 New utterances: {len(all_manifest_rows)}")
    print(f"   🤖 New agent utterances: {new_agent_utterances}")
    print(f"   👤 New user utterances: {new_user_utterances}")
    print(f"   ⏱️  New audio duration: {new_audio_hours:.2f} hours")
    print(f"\n📊 TOTAL DATASET:")
    print(f"   💬 Total conversations: {total_conversations}")
    print(f"   📊 Total utterances: {total_utterances}")
    print(f"   🤖 Total agent utterances: {total_agent_utterances}")
    print(f"   👤 Total user utterances: {total_user_utterances}")
    print(f"\n📁 Updated files:")
    print(f"   • {manifest_path} (Complete manifest with audio)")
    print(f"   • {asr_path} (ASR training data)")
    print(f"   • {tts_path} (TTS training data)")
    print(f"   • data/audio/agent/ (Agent audio files)")
    print(f"   • data/audio/user/ (User audio files)")
    print(f"\n🎯 Ready for ASR/TTS model training with incremental data!")
    print(f"💡 Run again to add more conversations without losing existing data!")

if __name__ == "__main__":
    generate_synthetic_data_with_audio()