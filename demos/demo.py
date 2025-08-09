#!/usr/bin/env python3
"""
Demo script for Turkish Telecom Synthetic Data Generator
Generates a small sample dataset to test functionality
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

# ---- DEMO CONFIGURATION ----
load_dotenv(verbose=True)
MODEL_NAME = "gemini-1.5-pro"
NUM_CONVERSATIONS = 3  # Small demo dataset
TURNS_PER_DIALOG_MIN = 6
TURNS_PER_DIALOG_MAX = 10
TEMPERATURE_AGENT = 0.7
TEMPERATURE_USER = 0.9
OUT_DIR = pathlib.Path("data")

# ---- SPEAKER MANAGEMENT ----
class SpeakerManager:
    """Manages speaker IDs for consistent voice assignment"""
    
    def __init__(self):
        self.agent_voices = ["agent_voice_001", "agent_voice_002", "agent_voice_003"]
        self.user_voices = ["user_voice_001", "user_voice_002", "user_voice_003", "user_voice_004"]
        self.conversation_speakers = {}
    
    def assign_speakers(self, conversation_id: int) -> Tuple[str, str]:
        if conversation_id not in self.conversation_speakers:
            agent_voice = random.choice(self.agent_voices)
            user_voice = random.choice(self.user_voices)
            self.conversation_speakers[conversation_id] = (agent_voice, user_voice)
        return self.conversation_speakers[conversation_id]
    
    def get_speaker_id(self, conversation_id: int, role: str) -> str:
        agent_voice, user_voice = self.assign_speakers(conversation_id)
        return agent_voice if role == "agent" else user_voice

# ---- LLM SETUP ----
agent_llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE_AGENT,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_retries=3,
)

user_llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE_USER,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_retries=3,
)

# ---- DEMO SCENARIOS ----
DEMO_SCENARIOS = {
    "billing_dispute": "Fatura itirazı - greeting → complaint → info_gathering → solution → closing",
    "technical_support": "Teknik destek - greeting → problem_report → troubleshooting → solution → closing",
    "package_change": "Paket değişikliği - greeting → request → options → selection → confirmation → closing"
}

AGENT_NAMES = ["Ahmet", "Ayşe", "Mehmet"]
TURKISH_FILLERS = ["tabii ki", "bir saniye lütfen", "anlıyorum", "tamamdır", "peki"]

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
    """Generate realistic audio file path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"audio/{role}/{conversation_id:04d}_{turn_number:02d}_{timestamp}_{unique_id}.wav"

def create_demo_prompt(context: Dict) -> str:
    """Create prompt for demo conversation generation"""
    
    prompt = f"""Sen {context['agent_name']} adında Türk telekom şirketinde çalışan bir müşteri hizmetleri temsilcisisin.

# ÇIKTI FORMATI (Sadece JSON döndür):
{{
    "conversation_id": {context['conversation_id']},
    "audio_filepath": "ses_dosyasi_yolu",
    "transcript": "konuşma_metni",
    "speaker_id": "{context['speaker_id']}",
    "role": "{context['role']}",
    "intent": "niyet",
    "slot": {{}}
}}

# SENARYO: {context['scenario_name']}
# TUR: {context['turn_number']}/{context['total_turns']}
# ROLÜN: {context['role']}

# GEÇMİŞ:
{context['history_str']}

# TALİMAT: {context['turn_instruction']}

# KURALLAR:
- Doğal Türkçe kullan (40-120 karakter)
- Telekom konuşması yap
- Gerekirse dolgu kelime ekle: {', '.join(random.sample(TURKISH_FILLERS, 2))}

JSON:"""
    
    return prompt

def get_demo_instruction(role: str, history: List[Dict], total_turns: int, turn_number: int, agent_name: str) -> str:
    """Get instruction for current turn"""
    
    if turn_number == 1:
        return f'Sen {agent_name} ajansın. Selamla ve nasıl yardımcı olabileceğini sor. Intent: "greeting"'
    
    last_turn = history[-1] if history else {}
    
    if turn_number == total_turns - 1:
        return 'Sen ajansın. Sorunu çözdün, görüşmeyi kapat. Intent: "closing"'
    if turn_number == total_turns:
        return 'Sen kullanıcısın. Teşekkür et. Intent: "thanks"'
    
    if role == "agent":
        if last_turn.get('intent') == 'complaint':
            return 'Daha fazla bilgi iste. Intent: "info_request"'
        elif last_turn.get('intent') == 'info_provide':
            return 'Çözüm öner. Intent: "solution"'
        return 'Uygun yanıt ver.'
    else:  # user
        if last_turn.get('intent') == 'greeting':
            return 'Sorununuzu açıklayın. Intent: "complaint"'
        elif last_turn.get('intent') == 'info_request':
            return 'İstenen bilgiyi verin. Intent: "info_provide"'
        elif last_turn.get('intent') == 'solution':
            return 'Çözümü kabul edin. Intent: "confirmation"'
        return 'Doğal yanıt verin.'

def validate_demo_conversation(history: List[Dict], conv_id: int) -> bool:
    """Simple validation for demo"""
    
    if len(history) < 4:
        print(f"  [FAIL] Conv {conv_id}: Too few turns")
        return False
    
    # Check role alternation
    for i, turn in enumerate(history):
        expected_role = "agent" if i % 2 == 0 else "user"
        if turn['role'] != expected_role:
            print(f"  [FAIL] Conv {conv_id}: Wrong role at turn {i+1}")
            return False
    
    # Check ending
    if history[-2]['intent'] != 'closing' or history[-1]['intent'] != 'thanks':
        print(f"  [FAIL] Conv {conv_id}: Invalid ending")
        return False
    
    print(f"  [PASS] Conv {conv_id}: Valid")
    return True

def run_demo():
    """Run demo generation"""
    
    print("🚀 TURKISH TELECOM SYNTHETIC DATA GENERATOR - DEMO")
    print("=" * 60)
    
    # Validate API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set your API key in .env file:")
        print("GOOGLE_API_KEY=your_api_key_here")
        return
    
    speaker_manager = SpeakerManager()
    all_data = []
    OUT_DIR.mkdir(exist_ok=True)
    
    scenarios = list(DEMO_SCENARIOS.keys())
    
    print(f"📊 Generating {NUM_CONVERSATIONS} demo conversations...")
    
    for conv_idx in range(NUM_CONVERSATIONS):
        conversation_id = conv_idx + 1
        scenario_name = scenarios[conv_idx % len(scenarios)]
        agent_name = random.choice(AGENT_NAMES)
        num_turns = random.randint(TURNS_PER_DIALOG_MIN, TURNS_PER_DIALOG_MAX)
        
        if num_turns % 2 != 0:
            num_turns += 1
        
        print(f"\n🔄 Generating conversation {conversation_id} ({scenario_name})...")
        
        history = []
        success = True
        
        for turn_number in range(1, num_turns + 1):
            role = "agent" if turn_number % 2 != 0 else "user"
            speaker_id = speaker_manager.get_speaker_id(conversation_id, role)
            
            context = {
                "conversation_id": conversation_id,
                "agent_name": agent_name,
                "scenario_name": scenario_name,
                "role": role,
                "turn_number": turn_number,
                "total_turns": num_turns,
                "speaker_id": speaker_id,
                "history_str": "\n".join([json.dumps(t, ensure_ascii=False) for t in history[-2:]]),
                "turn_instruction": get_demo_instruction(role, history, num_turns, turn_number, agent_name)
            }
            
            try:
                prompt = create_demo_prompt(context)
                llm_to_use = agent_llm if role == "agent" else user_llm
                
                response = llm_to_use.invoke(prompt)
                llm_output = clean_and_parse_json(response.content)
                
                if not llm_output:
                    print(f"    ❌ JSON parse failed at turn {turn_number}")
                    success = False
                    break
                
                # Create final turn data
                audio_filepath = generate_audio_filepath(conversation_id, turn_number, role)
                
                final_turn_data = {
                    "conversation_id": conversation_id,
                    "audio_filepath": audio_filepath,
                    "transcript": llm_output.get("transcript", "").strip(),
                    "speaker_id": speaker_id,
                    "role": role,
                    "intent": llm_output.get("intent", ""),
                    "slot": llm_output.get("slot", {})
                }
                
                history.append(final_turn_data)
                print(f"    ✅ Turn {turn_number} ({role}): {final_turn_data['transcript'][:50]}...")
                
                time.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                print(f"    ❌ Error at turn {turn_number}: {e}")
                success = False
                break
        
        if success and validate_demo_conversation(history, conversation_id):
            all_data.extend(history)
            print(f"✅ Conversation {conversation_id} completed successfully")
        else:
            print(f"❌ Conversation {conversation_id} failed validation")
    
    # Save results
    if all_data:
        demo_path = OUT_DIR / "demo_manifest.jsonl"
        with demo_path.open("w", encoding="utf-8") as f:
            for row in all_data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        
        # Separate ASR and TTS data
        asr_data = all_data
        tts_data = [row for row in all_data if row['role'] == 'agent']
        
        asr_demo_path = OUT_DIR / "demo_asr.jsonl"
        tts_demo_path = OUT_DIR / "demo_tts.jsonl"
        
        with asr_demo_path.open("w", encoding="utf-8") as f:
            for row in asr_data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        
        with tts_demo_path.open("w", encoding="utf-8") as f:
            for row in tts_data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        
        # Statistics
        print(f"\n📊 DEMO RESULTS:")
        print(f"   ✅ Total utterances: {len(all_data)}")
        print(f"   🤖 Agent utterances (TTS): {len(tts_data)}")
        print(f"   👤 User utterances: {len(asr_data) - len(tts_data)}")
        print(f"   🎤 Unique agent voices: {len(set(row['speaker_id'] for row in tts_data))}")
        print(f"   🎤 Unique user voices: {len(set(row['speaker_id'] for row in asr_data if row['role'] == 'user'))}")
        
        print(f"\n📁 Generated files:")
        print(f"   • {demo_path}")
        print(f"   • {asr_demo_path}")
        print(f"   • {tts_demo_path}")
        
        print(f"\n🎯 Demo completed! Check the generated files.")
        
        # Show sample data
        print(f"\n📝 SAMPLE DATA:")
        for i, row in enumerate(all_data[:4]):
            print(f"   {i+1}. [{row['role']}] {row['transcript']}")
    
    else:
        print("❌ No valid data generated")

if __name__ == "__main__":
    run_demo()