#!/usr/bin/env python3
"""
Turkish Telecom Text-Only Synthetic Data Generator
Generates conversation transcripts without audio files for fast data generation
"""

import json
import os
import random
import re
import pathlib
import time
import uuid
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tqdm import tqdm

# ---- LOAD ENVIRONMENT FIRST ----
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path, verbose=True)

# Import configuration after loading environment
sys.path.append(project_root)
from config.config import *

# ---- TEXT-ONLY CONFIGURATION ----
TEXT_OUT_DIR = Path("data/text_only")
TEXT_MANIFEST_FILENAME = "text_conversations.jsonl"
TEXT_ASR_FILENAME = "text_asr_data.jsonl"
TEXT_TTS_FILENAME = "text_tts_data.jsonl"

# Turkish Name Gender Classification (reused from main generator)
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

def get_speaker_id_for_text(agent_name: str, role: str, conversation_id: int) -> str:
    """Generate speaker ID for text-only generation"""
    if role == "agent":
        gender = get_gender_from_name(agent_name)
        return f"agent_{gender}_{conversation_id:03d}"
    else:
        # Random gender for users to create diversity
        gender = random.choice(["male", "female"])
        return f"user_{gender}_{conversation_id:03d}"

# ---- TEXT-ONLY SPEAKER MANAGEMENT ----
class TextOnlySpeakerManager:
    """Manages speaker IDs for text-only generation"""
    
    def __init__(self):
        self.conversation_speakers = {}
        self.conversation_agent_names = {}
    
    def assign_speakers(self, conversation_id: int, agent_name: str) -> Tuple[str, str]:
        if conversation_id not in self.conversation_speakers:
            agent_speaker = get_speaker_id_for_text(agent_name, "agent", conversation_id)
            user_speaker = get_speaker_id_for_text(agent_name, "user", conversation_id)
            
            self.conversation_speakers[conversation_id] = (agent_speaker, user_speaker)
            self.conversation_agent_names[conversation_id] = agent_name
            
        return self.conversation_speakers[conversation_id]
    
    def get_speaker_id(self, conversation_id: int, role: str, agent_name: str = None) -> str:
        if agent_name is None:
            agent_name = self.conversation_agent_names.get(conversation_id, "Ahmet")
            
        agent_speaker, user_speaker = self.assign_speakers(conversation_id, agent_name)
        return agent_speaker if role == "agent" else user_speaker

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

def create_text_generation_prompt(context: Dict) -> str:
    """Create prompt for text-only conversation generation"""
    
    scenario_info = TELECOM_SCENARIOS[context['scenario_name']]
    
    prompt_template = f"""Sen {context['agent_name']} adında Türk telekom şirketinde çalışan bir müşteri hizmetleri temsilcisisin. Gerçekçi bir telefon görüşmesi için tek bir konuşma turu oluşturuyorsun.

# ZORUNLU ÇIKTI FORMATI
Sadece aşağıdaki JSON formatında yanıt ver, başka hiçbir açıklama yapma:

{{
    "conversation_id": {context['conversation_id']},
    "transcript": "konuşma_metni",
    "speaker_id": "{context['speaker_id']}", 
    "role": "{context['role']}",
    "intent": "niyet_etiketi",
    "slot": {{"anahtar": "değer"}}
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
- Konuşma metni 15-250 karakter arası olmalı
- Doğal konuşma dili kullan

# NİYET VE SLOT KURALLARI
- **info_request**: slot = {{"requested": "istenen_bilgi"}}
- **info_provide**: slot = {{"sağlanan_bilgi": "değer"}}
- **solution**: slot = {{"solution_type": "çözüm_türü", "details": "detaylar"}}
- **Diğer niyetler**: slot = {{}}

JSON YANITI:"""

    return prompt_template

def get_turn_instruction(role: str, history: List[Dict], total_turns: int, turn_number: int, scenario_name: str, agent_name: str) -> str:
    """Get instruction for current turn (reused from main generator)"""
    
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

def validate_text_conversation(history: List[Dict], conv_id: int, scenario_name: str) -> bool:
    """Validate text-only conversation"""
    
    if not (TURNS_PER_DIALOG_MIN <= len(history) <= TURNS_PER_DIALOG_MAX):
        print(f"  [FAIL] Conv {conv_id}: Turn count ({len(history)}) out of range.")
        return False
    
    for i, turn in enumerate(history):
        expected_role = "agent" if (i + 1) % 2 != 0 else "user"
        if turn['role'] != expected_role:
            print(f"  [FAIL] Conv {conv_id}: Turn {i + 1} wrong role '{turn['role']}'.")
            return False
        
        # Transcript length check (more lenient for text-only)
        transcript_len = len(turn.get('transcript', ''))
        if transcript_len < 15 or transcript_len > 300:
            print(f"  [FAIL] Conv {conv_id}: Turn {i + 1} transcript length ({transcript_len}) invalid.")
            return False
    
    # Check ending
    if history[-2]['role'] != 'agent' or history[-2]['intent'] != 'closing':
        print(f"  [FAIL] Conv {conv_id}: Missing proper agent closing.")
        return False
    
    if history[-1]['role'] != 'user' or history[-1]['intent'] not in ['thanks', 'confirmation']:
        print(f"  [FAIL] Conv {conv_id}: Missing proper user thanks.")
        return False
    
    print(f"  [PASS] Conv {conv_id} text validation successful.")
    return True

def get_next_text_conversation_id():
    """Get the next conversation ID by checking ALL existing data files (audio + text)"""
    max_id = 0
    
    # Check all possible data directories and files
    data_paths = [
        # Audio data files (correct paths)
        Path("data/outputs/training_manifest_with_audio.jsonl"),
        Path("data/outputs/asr_training_data_with_audio.jsonl"),
        Path("data/outputs/tts_training_data_with_audio.jsonl"),
        Path("data/training_manifest_with_audio.jsonl"),
        Path("data/asr_training_data_with_audio.jsonl"),
        Path("data/tts_training_data_with_audio.jsonl"),
        # Text-only data files
        TEXT_OUT_DIR / TEXT_MANIFEST_FILENAME,
        TEXT_OUT_DIR / TEXT_ASR_FILENAME,
        TEXT_OUT_DIR / TEXT_TTS_FILENAME,
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

def generate_text_only_conversations():
    """Main function to generate text-only conversation data"""
    
    print("📝 TURKISH TELECOM TEXT-ONLY CONVERSATION GENERATOR")
    print("=" * 70)
    
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        print("❌ Configuration errors:")
        for error in config_errors:
            print(f"   • {error}")
        return
    
    speaker_manager = TextOnlySpeakerManager()
    all_manifest_rows = []
    TEXT_OUT_DIR.mkdir(exist_ok=True)
    
    # Get starting conversation ID (incremental)
    starting_conversation_id = get_next_text_conversation_id()
    print(f"📊 Starting from conversation ID: {starting_conversation_id}")
    
    # Check if files exist
    manifest_path = TEXT_OUT_DIR / TEXT_MANIFEST_FILENAME
    if manifest_path.exists():
        print(f"📁 Existing text data found - will APPEND new conversations")
    else:
        print(f"📁 No existing text data - creating new files")
    
    # Get scenario distribution
    scenario_distribution = get_scenario_distribution()
    
    pbar = tqdm(total=NUM_CONVERSATIONS, desc="Generating Text Conversations")
    
    successful_conversations = 0
    
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
                    speaker_id = speaker_manager.get_speaker_id(conversation_id, role, agent_name)
                    
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
                    prompt = create_text_generation_prompt(context)
                    llm_to_use = agent_llm if role == "agent" else user_llm
                    
                    response = llm_to_use.invoke(prompt)
                    llm_output = clean_and_parse_json(response.content)
                    
                    if not llm_output:
                        print(f"\nJSON parse failed for Conv {conversation_id}, Turn {turn_number}")
                        generation_successful = False
                        break
                    
                    transcript = llm_output.get("transcript", "").strip()
                    
                    # Create final turn data (text-only)
                    final_turn_data = {
                        "conversation_id": conversation_id,
                        "transcript": transcript,
                        "speaker_id": speaker_id,
                        "role": role,
                        "intent": llm_output.get("intent", ""),
                        "slot": llm_output.get("slot", {}),
                        "agent_name": agent_name,
                        "scenario": scenario_name,
                        "turn_number": turn_number
                    }
                    
                    history.append(final_turn_data)
                    
                    time.sleep(RATE_LIMIT_DELAY)
                
                # Validate conversation
                if generation_successful and validate_text_conversation(history, conversation_id, scenario_name):
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
    manifest_path = TEXT_OUT_DIR / TEXT_MANIFEST_FILENAME
    with manifest_path.open("a", encoding="utf-8") as f:
        for row in all_manifest_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Generate separate files for ASR and TTS (append mode)
    asr_data = all_manifest_rows
    tts_data = [row for row in all_manifest_rows if row['role'] == 'agent']
    
    asr_path = TEXT_OUT_DIR / TEXT_ASR_FILENAME
    with asr_path.open("a", encoding="utf-8") as f:
        for row in asr_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    tts_path = TEXT_OUT_DIR / TEXT_TTS_FILENAME
    with tts_path.open("a", encoding="utf-8") as f:
        for row in tts_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Calculate statistics for this session
    new_agent_utterances = len(tts_data)
    new_user_utterances = len(asr_data) - new_agent_utterances
    
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
    print(f"📝 TEXT-ONLY CONVERSATION GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"📊 THIS SESSION:")
    print(f"   ✅ New conversations: {successful_conversations}/{NUM_CONVERSATIONS}")
    print(f"   📊 New utterances: {len(all_manifest_rows)}")
    print(f"   🤖 New agent utterances: {new_agent_utterances}")
    print(f"   👤 New user utterances: {new_user_utterances}")
    print(f"\n📊 TOTAL TEXT DATASET:")
    print(f"   💬 Total conversations: {total_conversations}")
    print(f"   📊 Total utterances: {total_utterances}")
    print(f"   🤖 Total agent utterances: {total_agent_utterances}")
    print(f"   👤 Total user utterances: {total_user_utterances}")
    print(f"\n📁 Updated files:")
    print(f"   • {manifest_path} (Complete text manifest)")
    print(f"   • {asr_path} (Text ASR training data)")
    print(f"   • {tts_path} (Text TTS training data)")
    print(f"\n🎯 Ready for text-based model training!")
    print(f"💡 Run again to add more conversations without losing existing data!")
    print(f"⚡ Much faster than audio generation - perfect for large datasets!")

if __name__ == "__main__":
    generate_text_only_conversations()