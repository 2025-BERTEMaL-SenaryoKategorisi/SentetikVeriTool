"""
Configuration file for Turkish Telecom Synthetic Data Generator
Customize these settings based on your training requirements
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    
    # Get the project root directory (parent of config directory)
    config_dir = Path(__file__).parent
    project_root = config_dir.parent
    env_path = project_root / '.env'
    
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print(f"⚠️  .env file not found at: {env_path}")
        
except ImportError:
    print("⚠️  python-dotenv not installed. Environment variables from .env file will not be loaded.")
    print("   Install with: pip install python-dotenv")

# ---- API CONFIGURATION ----
# Choose API provider: "free_gemini" or "gcp_vertex"
API_PROVIDER = os.getenv("API_PROVIDER", "free_gemini")

# Free Gemini API (rate limited)
MODEL_NAME = "gemini-1.5-pro"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# GCP Vertex AI (higher limits with credits)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GCP_MODEL_NAME = os.getenv("GCP_MODEL_NAME", "gemini-1.5-pro")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ---- DATA GENERATION SETTINGS ----
NUM_CONVERSATIONS = 10  # Total number of conversations to generate
TURNS_PER_DIALOG_MIN = 6  # Minimum turns per conversation
TURNS_PER_DIALOG_MAX = 16  # Maximum turns per conversation

# ---- LLM TEMPERATURE SETTINGS ----
TEMPERATURE_AGENT = 0.7  # Lower = more consistent agent responses
TEMPERATURE_USER = 0.9   # Higher = more varied user responses

# ---- OUTPUT CONFIGURATION ----
OUT_DIR = Path("data")
MANIFEST_FILENAME = "training_manifest.jsonl"
ASR_FILENAME = "asr_training_data.jsonl"
TTS_FILENAME = "tts_training_data.jsonl"

# ---- SPEAKER VOICE CONFIGURATION ----
# Agent voices - should be consistent per conversation for TTS training
AGENT_VOICES = [
    "agent_voice_001", "agent_voice_002", "agent_voice_003", "agent_voice_004",
    "agent_voice_005", "agent_voice_006", "agent_voice_007", "agent_voice_008",
    "agent_voice_009", "agent_voice_010", "agent_voice_011", "agent_voice_012"
]

# User voices - should be diverse for ASR training
USER_VOICES = [
    "user_voice_001", "user_voice_002", "user_voice_003", "user_voice_004",
    "user_voice_005", "user_voice_006", "user_voice_007", "user_voice_008",
    "user_voice_009", "user_voice_010", "user_voice_011", "user_voice_012",
    "user_voice_013", "user_voice_014", "user_voice_015", "user_voice_016",
    "user_voice_017", "user_voice_018", "user_voice_019", "user_voice_020",
    "user_voice_021", "user_voice_022", "user_voice_023", "user_voice_024",
    "user_voice_025", "user_voice_026", "user_voice_027", "user_voice_028"
]

# ---- TURKISH LANGUAGE SETTINGS ----
AGENT_NAMES = [
    "Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Veli", "Zeynep", "Elif",
    "Burak", "Cem", "Deniz", "Ece", "Furkan", "Gül", "Hakan", "İrem",
    "Kemal", "Leyla", "Murat", "Nalan", "Oğuz", "Pınar", "Rıza", "Seda",
    "Tolga", "Ufuk", "Volkan", "Yasemin", "Zeki", "Aslı"
]

TURKISH_FILLERS = [
    "tabii ki", "elbette", "memnuniyetle", "bir saniye lütfen", "hemen bakıyorum",
    "anlıyorum", "haklısınız", "kesinlikle", "doğru söylüyorsunuz", "tamamdır",
    "peki", "tamam", "iyi", "güzel", "süper", "mükemmel", "harika", "çok güzel",
    "şöyle", "yani", "işte", "böyle", "hemen", "derhal", "şimdi", "bir dakika",
    "nasıl istersen", "öyle", "doğru", "aynen", "kesin", "mutlaka", "herhalde"
]

# ---- TELECOM VOCABULARY ----
TELECOM_PACKAGES = [
    "Süper Paket", "Mega Paket", "Ultra Paket", "Ekonomik Paket", "Aile Paketi",
    "Gençlik Paketi", "İş Paketi", "Premium Paket", "Standart Paket", "Özel Paket"
]

INTERNET_SPEEDS = [
    "16 Mbps", "25 Mbps", "35 Mbps", "50 Mbps", "100 Mbps", "200 Mbps",
    "500 Mbps", "1 Gbps", "2 Gbps"
]

TELECOM_SERVICES = [
    "Fiber internet", "ADSL", "VDSL", "Mobil internet", "Sabit hat",
    "Dijital TV", "Roaming", "SMS paketi", "Konuşma paketi", "Data paketi"
]

COMMON_ISSUES = [
    "bağlantı sorunu", "yavaş internet", "kesinti", "fatura hatası",
    "ödeme problemi", "modem sorunu", "sinyal problemi", "hat arızası"
]

# ---- SCENARIO CONFIGURATION ----
SCENARIO_WEIGHTS = {
    "billing_dispute": 0.25,      # 25% of conversations
    "technical_support": 0.30,    # 30% of conversations
    "package_change": 0.20,       # 20% of conversations
    "roaming_inquiry": 0.15,      # 15% of conversations
    "account_management": 0.10    # 10% of conversations
}

# ---- TELECOM SCENARIOS ----
TELECOM_SCENARIOS = {
    "billing_dispute": {
        "description": "Fatura itirazı ve ödeme sorunları",
        "flow": "Müşteri fatura hatası bildiriyor → Ajan bilgi topluyor → Çözüm sunuyor",
        "common_intents": ["complaint", "info_request", "info_provide", "solution"],
        "typical_duration": "8-12 turns"
    },
    "technical_support": {
        "description": "İnternet ve teknik destek sorunları",
        "flow": "Müşteri teknik sorun bildiriyor → Ajan troubleshooting → Çözüm/teknisyen",
        "common_intents": ["complaint", "info_request", "solution", "confirmation"],
        "typical_duration": "10-16 turns"
    },
    "package_change": {
        "description": "Paket değişikliği ve yükseltme talepleri",
        "flow": "Müşteri paket değişikliği istiyor → Ajan seçenekleri sunuyor → Onay",
        "common_intents": ["info_request", "options_presentation", "confirmation"],
        "typical_duration": "6-10 turns"
    },
    "roaming_inquiry": {
        "description": "Roaming ve yurtdışı kullanım sorguları",
        "flow": "Müşteri roaming bilgisi istiyor → Ajan tarife/paket bilgisi → Aktivasyon",
        "common_intents": ["info_request", "info_provide", "confirmation"],
        "typical_duration": "6-8 turns"
    },
    "account_management": {
        "description": "Hesap yönetimi ve genel bilgi talepleri",
        "flow": "Müşteri hesap bilgisi istiyor → Ajan bilgi sağlıyor → İşlem tamamlama",
        "common_intents": ["info_request", "info_provide", "confirmation"],
        "typical_duration": "6-10 turns"
    }
}

# ---- QUALITY CONTROL SETTINGS ----
MIN_TRANSCRIPT_LENGTH = 20   # Minimum characters in transcript
MAX_TRANSCRIPT_LENGTH = 200  # Maximum characters in transcript
MAX_RETRIES_PER_CONVERSATION = 3  # Max attempts to generate valid conversation
RATE_LIMIT_DELAY = 2.0       # Seconds between API calls (increased for free tier)

# ---- VALIDATION SETTINGS ----
REQUIRED_INTENTS = [
    "greeting", "complaint", "info_request", "info_provide",
    "solution", "closing", "thanks", "confirmation"
]

REQUIRED_FIELDS = [
    "conversation_id", "audio_filepath", "transcript",
    "speaker_id", "role", "intent", "slot"
]

# ---- AUDIO FILE SETTINGS ----
AUDIO_FORMAT = "wav"
AUDIO_SAMPLE_RATE = 16000  # Hz
AUDIO_CHANNELS = 1         # Mono
AUDIO_BIT_DEPTH = 16       # bits

# ---- ADVANCED SETTINGS ----
CONTEXT_SWITCH_PROBABILITY = 0.15  # 15% chance of context switch in conversation
ENABLE_ADVANCED_VALIDATION = True
ENABLE_STATISTICS_LOGGING = True
ENABLE_ERROR_RECOVERY = True

# ---- EXPORT SETTINGS ----
EXPORT_FORMATS = {
    "jsonl": True,    # Export as JSONL
    "csv": False,     # Export as CSV (optional)
    "parquet": False  # Export as Parquet (optional)
}

# ---- LOGGING CONFIGURATION ----
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "generator.log"
ENABLE_CONSOLE_LOGGING = True
ENABLE_FILE_LOGGING = False

# ---- PERFORMANCE SETTINGS ----
BATCH_SIZE = 10           # Process conversations in batches
PARALLEL_PROCESSING = False  # Enable parallel processing (experimental)
MAX_WORKERS = 4           # Number of worker threads if parallel processing enabled

# ---- CUSTOM PROMPTS (Advanced) ----
CUSTOM_AGENT_PROMPT_SUFFIX = ""
CUSTOM_USER_PROMPT_SUFFIX = ""

# ---- VALIDATION FUNCTIONS ----
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Validate API configuration based on provider
    if API_PROVIDER == "gcp_vertex":
        if not GCP_PROJECT_ID:
            errors.append("GCP_PROJECT_ID environment variable not set for Vertex AI")
        if not GOOGLE_APPLICATION_CREDENTIALS:
            errors.append("GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Vertex AI")
        elif not os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
            errors.append(f"GCP credentials file not found: {GOOGLE_APPLICATION_CREDENTIALS}")
    else:  # free_gemini
        if not GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY environment variable not set")
    
    if NUM_CONVERSATIONS <= 0:
        errors.append("NUM_CONVERSATIONS must be positive")
    
    if TURNS_PER_DIALOG_MIN >= TURNS_PER_DIALOG_MAX:
        errors.append("TURNS_PER_DIALOG_MIN must be less than TURNS_PER_DIALOG_MAX")
    
    if not (0.0 <= TEMPERATURE_AGENT <= 2.0):
        errors.append("TEMPERATURE_AGENT must be between 0.0 and 2.0")
    
    if not (0.0 <= TEMPERATURE_USER <= 2.0):
        errors.append("TEMPERATURE_USER must be between 0.0 and 2.0")
    
    if abs(sum(SCENARIO_WEIGHTS.values()) - 1.0) > 0.01:
        errors.append("SCENARIO_WEIGHTS must sum to 1.0")
    
    if MIN_TRANSCRIPT_LENGTH >= MAX_TRANSCRIPT_LENGTH:
        errors.append("MIN_TRANSCRIPT_LENGTH must be less than MAX_TRANSCRIPT_LENGTH")
    
    return errors

def get_scenario_distribution():
    """Get scenario distribution based on weights"""
    import random
    
    scenarios = []
    for scenario, weight in SCENARIO_WEIGHTS.items():
        count = int(NUM_CONVERSATIONS * weight)
        scenarios.extend([scenario] * count)
    
    # Fill remaining slots with random scenarios
    while len(scenarios) < NUM_CONVERSATIONS:
        scenarios.append(random.choice(list(SCENARIO_WEIGHTS.keys())))
    
    # Shuffle for randomness
    random.shuffle(scenarios)
    return scenarios[:NUM_CONVERSATIONS]

# ---- CONFIGURATION SUMMARY ----
def print_config_summary():
    """Print configuration summary"""
    print("🔧 CONFIGURATION SUMMARY")
    print("=" * 50)
    print(f"📊 Conversations: {NUM_CONVERSATIONS}")
    print(f"🔄 Turns per dialog: {TURNS_PER_DIALOG_MIN}-{TURNS_PER_DIALOG_MAX}")
    print(f"🎤 Agent voices: {len(AGENT_VOICES)}")
    print(f"👤 User voices: {len(USER_VOICES)}")
    print(f"🌡️  Agent temperature: {TEMPERATURE_AGENT}")
    print(f"🌡️  User temperature: {TEMPERATURE_USER}")
    print(f"📁 Output directory: {OUT_DIR}")
    print(f"🎯 Scenario distribution:")
    for scenario, weight in SCENARIO_WEIGHTS.items():
        count = int(NUM_CONVERSATIONS * weight)
        print(f"   • {scenario}: {count} ({weight*100:.1f}%)")
    print("=" * 50)

if __name__ == "__main__":
    # Validate configuration when run directly
    errors = validate_config()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   • {error}")
    else:
        print("✅ Configuration is valid")
        print_config_summary()