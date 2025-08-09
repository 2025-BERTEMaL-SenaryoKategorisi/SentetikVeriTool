#!/usr/bin/env python3
"""
Enhanced Turkish Telecom Synthetic Data Generator with TTS Audio Generation
GCP Vertex AI Version - Higher rate limits with GCP credits
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
from tqdm import tqdm
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor

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

# ---- GCP VERTEX AI SETUP ----
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    GCP_AVAILABLE = True
except ImportError:
    print("⚠️  GCP packages not installed. Install with: pip install google-cloud-aiplatform")
    GCP_AVAILABLE = False

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

# ---- VOICE MAPPING SYSTEM ----
class VoiceManager:
    """Manages TTS voice generation with different characteristics for agents and users"""
    
    def __init__(self):
        # Voice characteristics for different speaker types
        self.agent_voice_configs = {
            'agent_voice_001': {'lang': 'tr', 'slow': False, 'pitch_shift': 0},
            'agent_voice_002': {'lang': 'tr', 'slow': False, 'pitch_shift': 2},
            'agent_voice_003': {'lang': 'tr', 'slow': True, 'pitch_shift': -1},
            'agent_voice_004': {'lang': 'tr', 'slow': False, 'pitch_shift': 1},
            'agent_voice_005': {'lang': 'tr', 'slow': False, 'pitch_shift': -2},
            'agent_voice_006': {'lang': 'tr', 'slow': True, 'pitch_shift': 0},
            'agent_voice_007': {'lang': 'tr', 'slow': False, 'pitch_shift': 3},
            'agent_voice_008': {'lang': 'tr', 'slow': False, 'pitch_shift': -1},
            'agent_voice_009': {'lang': 'tr', 'slow': True, 'pitch_shift': 1},
            'agent_voice_010': {'lang': 'tr', 'slow': False, 'pitch_shift': -3},
        }
        
        self.user_voice_configs = {
            'user_voice_001': {'lang': 'tr', 'slow': False, 'pitch_shift': 0, 'speed': 1.0},
            'user_voice_002': {'lang': 'tr', 'slow': True, 'pitch_shift': 2, 'speed': 0.9},
            'user_voice_003': {'lang': 'tr', 'slow': False, 'pitch_shift': -2, 'speed': 1.1},
            'user_voice_004': {'lang': 'tr', 'slow': False, 'pitch_shift': 1, 'speed': 1.0},
            'user_voice_005': {'lang': 'tr', 'slow': True, 'pitch_shift': -1, 'speed': 0.95},
            'user_voice_006': {'lang': 'tr', 'slow': False, 'pitch_shift': 3, 'speed': 1.05},
            'user_voice_007': {'lang': 'tr', 'slow': False, 'pitch_shift': -3, 'speed': 1.0},
            'user_voice_008': {'lang': 'tr', 'slow': True, 'pitch_shift': 0, 'speed': 0.85},
            'user_voice_009': {'lang': 'tr', 'slow': False, 'pitch_shift': 2, 'speed': 1.15},
            'user_voice_010': {'lang': 'tr', 'slow': False, 'pitch_shift': -1, 'speed': 1.0},
            'user_voice_011': {'lang': 'tr', 'slow': True, 'pitch_shift': 1, 'speed': 0.9},
            'user_voice_012': {'lang': 'tr', 'slow': False, 'pitch_shift': -2, 'speed': 1.1},
            'user_voice_013': {'lang': 'tr', 'slow': False, 'pitch_shift': 0, 'speed': 1.2},
            'user_voice_014': {'lang': 'tr', 'slow': True, 'pitch_shift': 2, 'speed': 0.8},
            'user_voice_015': {'lang': 'tr', 'slow': False, 'pitch_shift': -1, 'speed': 1.0},
            'user_voice_016': {'lang': 'tr', 'slow': False, 'pitch_shift': 1, 'speed': 1.05},
            'user_voice_017': {'lang': 'tr', 'slow': True, 'pitch_shift': -2, 'speed': 0.95},
            'user_voice_018': {'lang': 'tr', 'slow': False, 'pitch_shift': 3, 'speed': 1.1},
            'user_voice_019': {'lang': 'tr', 'slow': False, 'pitch_shift': 0, 'speed': 1.0},
            'user_voice_020': {'lang': 'tr', 'slow': True, 'pitch_shift': -3, 'speed': 0.9},
        }
        
        # Create audio output directories
        self.audio_dir = OUT_DIR / "audio"
        self.agent_audio_dir = self.audio_dir / "agent"
        self.user_audio_dir = self.audio_dir / "user"
        
        for dir_path in [self.audio_dir, self.agent_audio_dir, self.user_audio_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_voice_config(self, speaker_id: str) -> Dict:
        """Get voice configuration for a speaker"""
        if speaker_id.startswith('agent_voice_'):
            return self.agent_voice_configs.get(speaker_id, self.agent_voice_configs['agent_voice_001'])
        else:
            return self.user_voice_configs.get(speaker_id, self.user_voice_configs['user_voice_001'])
    
    def add_background_noise(self, audio_data: np.ndarray, noise_level: float = 0.005) -> np.ndarray:
        """Add subtle background noise for realism"""
        if not AUDIO_CONFIG['add_noise']:
            return audio_data
        
        noise = np.random.normal(0, noise_level, audio_data.shape)
        return audio_data + noise
    
    def pitch_shift(self, audio_data: np.ndarray, sample_rate: int, n_steps: float) -> np.ndarray:
        """Shift pitch of audio"""
        if n_steps == 0:
            return audio_data
        
        return librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=n_steps)
    
    def generate_audio(self, text: str, speaker_id: str, output_path: pathlib.Path) -> Dict[str, any]:
        """Generate audio file from text using TTS with voice characteristics"""
        
        try:
            voice_config = self.get_voice_config(speaker_id)
            
            # Generate TTS audio
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                tts = gTTS(
                    text=text,
                    lang=voice_config['lang'],
                    slow=voice_config['slow']
                )
                tts.save(tmp_file.name)
                
                # Load and process audio
                audio = AudioSegment.from_mp3(tmp_file.name)
                
                # Convert to numpy array for processing
                audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
                if audio.channels == 2:
                    audio_data = audio_data.reshape((-1, 2)).mean(axis=1)
                
                # Normalize
                audio_data = audio_data / np.max(np.abs(audio_data))
                
                # Apply voice modifications
                sample_rate = audio.frame_rate
                
                # Pitch shifting
                if voice_config.get('pitch_shift', 0) != 0:
                    audio_data = self.pitch_shift(
                        audio_data, 
                        sample_rate, 
                        voice_config['pitch_shift']
                    )
                
                # Speed variation for users
                if speaker_id.startswith('user_voice_') and 'speed' in voice_config:
                    speed_factor = voice_config['speed']
                    if speed_factor != 1.0:
                        audio_data = librosa.effects.time_stretch(audio_data, rate=speed_factor)
                
                # Add background noise
                audio_data = self.add_background_noise(audio_data)
                
                # Resample to target sample rate
                if sample_rate != AUDIO_CONFIG['sample_rate']:
                    audio_data = librosa.resample(
                        audio_data, 
                        orig_sr=sample_rate, 
                        target_sr=AUDIO_CONFIG['sample_rate']
                    )
                
                # Normalize final audio
                if AUDIO_CONFIG['normalize']:
                    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
                
                # Save as WAV
                sf.write(
                    output_path, 
                    audio_data, 
                    AUDIO_CONFIG['sample_rate'],
                    subtype='PCM_16'
                )
                
                # Clean up temp file
                os.unlink(tmp_file.name)
                
                # Calculate audio metadata
                duration = len(audio_data) / AUDIO_CONFIG['sample_rate']
                
                return {
                    'success': True,
                    'duration': duration,
                    'sample_rate': AUDIO_CONFIG['sample_rate'],
                    'channels': AUDIO_CONFIG['channels'],
                    'file_size': output_path.stat().st_size,
                    'voice_config': voice_config
                }
                
        except Exception as e:
            print(f"Error generating audio for {speaker_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'duration': 0,
                'sample_rate': AUDIO_CONFIG['sample_rate'],
                'channels': AUDIO_CONFIG['channels']
            }

# ---- GCP LLM SETUP ----
class GCPLLMManager:
    """Manages GCP Vertex AI LLM connections"""
    
    def __init__(self):
        self.initialized = False
        self.model = None
        self.setup_gcp()
    
    def setup_gcp(self):
        """Initialize GCP Vertex AI"""
        if not GCP_AVAILABLE:
            print("❌ GCP packages not available")
            return
        
        try:
            # Initialize Vertex AI
            vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
            
            # Initialize model
            self.model = GenerativeModel(GCP_MODEL_NAME)
            self.initialized = True
            
            print(f"✅ GCP Vertex AI initialized: {GCP_PROJECT_ID}/{GCP_LOCATION}")
            print(f"🤖 Using model: {GCP_MODEL_NAME}")
            
        except Exception as e:
            print(f"❌ Failed to initialize GCP Vertex AI: {e}")
            self.initialized = False
    
    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate content using GCP Vertex AI"""
        if not self.initialized:
            raise Exception("GCP Vertex AI not initialized")
        
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": temperature,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"GCP generation error: {e}")

# ---- ENHANCED SPEAKER MANAGEMENT ----
class SpeakerManager:
    """Manages speaker IDs for consistent voice assignment across conversations"""
    
    def __init__(self):
        self.agent_voices = AGENT_VOICES
        self.user_voices = USER_VOICES
        self.conversation_speakers = {}
        self.voice_manager = VoiceManager()
    
    def assign_speakers(self, conversation_id: int) -> Tuple[str, str]:
        if conversation_id not in self.conversation_speakers:
            agent_voice = random.choice(self.agent_voices)
            user_voice = random.choice(self.user_voices)
            self.conversation_speakers[conversation_id] = (agent_voice, user_voice)
        return self.conversation_speakers[conversation_id]
    
    def get_speaker_id(self, conversation_id: int, role: str) -> str:
        agent_voice, user_voice = self.assign_speakers(conversation_id)
        return agent_voice if role == "agent" else user_voice
    
    def generate_audio_for_turn(self, text: str, speaker_id: str, audio_filepath: str) -> Dict[str, any]:
        """Generate audio file for a conversation turn"""
        audio_path = pathlib.Path(audio_filepath)
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        return self.voice_manager.generate_audio(text, speaker_id, audio_path)

# ---- LLM SETUP ----
gcp_llm = GCPLLMManager()

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
    """Generate audio file path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"data/audio/{role}/{conversation_id:04d}_{turn_number:02d}_{timestamp}_{unique_id}.wav"

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

def generate_synthetic_data_with_audio_gcp():
    """Main function to generate synthetic training data with audio files using GCP"""
    
    print("🎤 TURKISH TELECOM SYNTHETIC DATA GENERATOR WITH AUDIO (GCP)")
    print("=" * 70)
    
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        print("❌ Configuration errors:")
        for error in config_errors:
            print(f"   • {error}")
        return
    
    # Check GCP initialization
    if not gcp_llm.initialized:
        print("❌ GCP Vertex AI not initialized. Check your setup.")
        return
    
    speaker_manager = SpeakerManager()
    all_manifest_rows = []
    OUT_DIR.mkdir(exist_ok=True)
    
    # Create audio directories
    (OUT_DIR / "audio" / "agent").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "audio" / "user").mkdir(parents=True, exist_ok=True)
    
    # Get scenario distribution
    scenario_distribution = get_scenario_distribution()
    
    pbar = tqdm(total=NUM_CONVERSATIONS, desc="Generating Conversations with Audio (GCP)")
    
    successful_conversations = 0
    total_audio_duration = 0
    
    for conv_idx in range(NUM_CONVERSATIONS):
        conversation_id = conv_idx + 1
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
                    speaker_id = speaker_manager.get_speaker_id(conversation_id, role)
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
                    
                    # Generate text using GCP
                    prompt = create_generation_prompt(context)
                    temperature = TEMPERATURE_AGENT if role == "agent" else TEMPERATURE_USER
                    
                    response_text = gcp_llm.generate_content(prompt, temperature)
                    llm_output = clean_and_parse_json(response_text)
                    
                    if not llm_output:
                        print(f"\nJSON parse failed for Conv {conversation_id}, Turn {turn_number}")
                        generation_successful = False
                        break
                    
                    transcript = llm_output.get("transcript", "").strip()
                    
                    # Generate audio
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
    
    # Save manifest files
    manifest_path = OUT_DIR / "training_manifest_with_audio_gcp.jsonl"
    with manifest_path.open("w", encoding="utf-8") as f:
        for row in all_manifest_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Generate separate files for ASR and TTS
    asr_data = all_manifest_rows
    tts_data = [row for row in all_manifest_rows if row['role'] == 'agent']
    
    asr_path = OUT_DIR / "asr_training_data_with_audio_gcp.jsonl"
    with asr_path.open("w", encoding="utf-8") as f:
        for row in asr_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    tts_path = OUT_DIR / "tts_training_data_with_audio_gcp.jsonl"
    with tts_path.open("w", encoding="utf-8") as f:
        for row in tts_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Calculate statistics
    agent_utterances = len(tts_data)
    user_utterances = len(asr_data) - agent_utterances
    unique_agent_voices = len(set(row['speaker_id'] for row in tts_data))
    unique_user_voices = len(set(row['speaker_id'] for row in asr_data if row['role'] == 'user'))
    total_audio_hours = total_audio_duration / 3600
    print(f"\n{'='*70}")
    print(f"🎤 SYNTHETIC DATA WITH AUDIO GENERATION COMPLETE (GCP)")
    print(f"{'='*70}")
    print(f"✅ Successful conversations: {successful_conversations}/{NUM_CONVERSATIONS}")
    print(f"📊 Total utterances: {len(all_manifest_rows)}")
    print(f"🤖 Agent utterances (TTS): {agent_utterances}")
    print(f"👤 User utterances: {user_utterances}")
    print(f"🎤 Unique agent voices: {unique_agent_voices}")
    print(f"🎤 Unique user voices: {unique_user_voices}")
    print(f"⏱️  Total audio duration: {total_audio_hours:.2f} hours")
    print(f"📁 Audio files generated: {len(all_manifest_rows)}")
    print(f"💰 Using GCP credits: {GCP_PROJECT_ID}")
    print(f"\n📁 Generated files:")
    print(f"   • {manifest_path} (Complete manifest with audio)")
    print(f"   • {asr_path} (ASR training data)")
    print(f"   • {tts_path} (TTS training data)")
    print(f"   • data/audio/agent/ (Agent audio files)")
    print(f"   • data/audio/user/ (User audio files)")
    print(f"\n🎯 Ready for ASR/TTS model training with real audio data!")

if __name__ == "__main__":
    generate_synthetic_data_with_audio_gcp()
    