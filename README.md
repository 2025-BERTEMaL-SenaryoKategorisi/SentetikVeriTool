# Turkish Telecom Synthetic Data Generator

🎤 **Professional synthetic data generation tool for TEKNOFEST 2025 Turkish Natural Language Processing competition**

Generate high-quality training data for both ASR (Automatic Speech Recognition) and TTS (Text-to-Speech) models with proper speaker identification and role labeling for Turkish telecom customer service conversations.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run generators
python generators/main_generator.py      # With audio generation
python generators/text_only_generator.py # Text-only (faster)
python generators/gcp_generator.py       # GCP version (higher limits)

# 4. Test demos
python demos/enhanced_tts_demo.py        # Enhanced TTS demo
python demos/text_only_demo.py           # Text-only demo
```

## 📁 Project Structure

```
SentetikVeri/
├── generators/           # Main generation scripts
│   ├── main_generator.py      # Standard Google AI generator (with audio)
│   ├── text_only_generator.py # Fast text-only generator (no audio)
│   └── gcp_generator.py       # GCP Vertex AI version (higher limits)
├── demos/               # Demo and test scripts
│   ├── enhanced_tts_demo.py   # High-quality TTS demo
│   ├── text_only_demo.py      # Text-only generation demo
│   ├── audio_demo.py          # Basic audio demo
│   └── simple_audio_demo.py   # Simple TTS test
├── config/              # Configuration files
│   └── config.py           # Main configuration
├── data/                # Generated data
│   ├── outputs/            # Training manifests (JSONL)
│   ├── text_only/          # Text-only conversation data
│   └── audio/              # Generated audio files
│       ├── agent/          # Agent voice files
│       └── user/           # User voice files
├── docs/                # Documentation
│   ├── README.md           # Main documentation
│   ├── USAGE_GUIDE.md      # Usage instructions
│   └── INSTALL_GUIDE.md    # Installation guide
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎯 Features

### Core Functionality

- ✅ **Turkish Telecom Scenarios**: 5 realistic conversation types
- ✅ **Speaker Management**: Consistent agent voices per conversation
- ✅ **Role Labeling**: Proper agent/user role assignment
- ✅ **Intent & Slot Extraction**: NLU training data
- ✅ **Audio Generation**: Real WAV files with voice variations
- ✅ **Text-Only Generation**: Fast conversation generation without audio
- ✅ **JSONL Manifests**: Competition-compliant format

### Audio Quality

- 🎤 **Multiple TTS Providers**: ElevenLabs, Google Cloud TTS, Azure, gTTS
- 🎵 **Voice Variations**: Pitch shifting, speed control, background noise
- 📊 **Audio Metadata**: Duration, sample rate, file size tracking
- 🔊 **Quality Control**: Validation and error handling

### Technical Features

- ⚡ **Rate Limiting**: API-friendly generation
- 🔄 **Retry Logic**: Robust error handling
- 📈 **Progress Tracking**: Real-time generation status
- 💾 **Efficient Storage**: Organized file structure

## 🎤 Audio Generation Process

**Your question: "Does audio come from AI-generated JSON scripts?"**

**Answer: YES!** Here's the complete workflow:

1. **AI generates JSON** with conversation text:

   ```json
   {
     "transcript": "Merhaba, size nasıl yardımcı olabilirim?",
     "speaker_id": "agent_voice_001",
     "role": "agent"
   }
   ```

2. **TTS converts text to audio**:

   - Takes the `transcript` field
   - Uses `speaker_id` for voice selection
   - Generates WAV audio file

3. **Audio path added back to JSON**:

   ```json
   {
     "transcript": "Merhaba, size nasıl yardımcı olabilirim?",
     "audio_filepath": "data/audio/agent/0001_01_20250129_abc123.wav",
     "speaker_id": "agent_voice_001",
     "role": "agent",
     "audio_duration": 3.2,
     "sample_rate": 16000
   }
   ```

4. **Final JSONL includes both text and audio** for training.

## 📊 Generated Data Format

### Training Manifest (JSONL)

```json
{
  "conversation_id": 1,
  "audio_filepath": "data/audio/agent/0001_01_20250129_abc123.wav",
  "transcript": "Merhaba, size nasıl yardımcı olabilirim?",
  "speaker_id": "agent_voice_001",
  "role": "agent",
  "intent": "greeting",
  "slot": {},
  "audio_duration": 3.2,
  "sample_rate": 16000,
  "channels": 1,
  "file_size": 51200
}
```

### Output Files

**Audio Generation:**

- `data/outputs/training_manifest.jsonl` - Complete training data with audio
- `data/outputs/asr_training_data.jsonl` - ASR-specific data
- `data/outputs/tts_training_data.jsonl` - TTS-specific data (agents only)
- `data/audio/agent/` - Agent voice files
- `data/audio/user/` - User voice files

**Text-Only Generation:**

- `data/text_only/text_conversations.jsonl` - Complete text conversations
- `data/text_only/text_asr_data.jsonl` - Text ASR training data
- `data/text_only/text_tts_data.jsonl` - Text TTS training data

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Google AI (Free tier)
GOOGLE_API_KEY=your_google_api_key

# GCP Vertex AI (Higher limits)
GCP_PROJECT_ID=your_project_id
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Enhanced TTS Providers (Optional)
ELEVENLABS_API_KEY=your_elevenlabs_key
GOOGLE_CLOUD_TTS_API_KEY=your_gcp_tts_key
AZURE_SPEECH_KEY=your_azure_key
```

### Generation Settings

```python
NUM_CONVERSATIONS = 50          # Number of conversations to generate
TURNS_PER_DIALOG_MIN = 6       # Minimum turns per conversation
TURNS_PER_DIALOG_MAX = 12      # Maximum turns per conversation
RATE_LIMIT_DELAY = 1.0         # Delay between API calls (seconds)
```

## 🎯 Telecom Scenarios

1. **Billing Dispute** - Customer questions charges
2. **Technical Support** - Internet/phone issues
3. **Package Change** - Plan upgrades/downgrades
4. **Roaming Inquiry** - International usage questions
5. **Account Management** - Profile updates, payments

Each scenario includes:

- Realistic conversation flow
- Turkish telecom terminology
- Proper intent progression
- Natural language patterns

## 🎵 Voice System

### Agent Voices (Professional)

- 10 distinct agent voices
- Consistent per conversation
- Professional, helpful tone
- Pitch variations for diversity

### User Voices (Natural)

- 20 diverse user voices
- Different ages, genders, emotions
- Speed and pitch variations
- Realistic customer concerns

## 📈 Usage Examples

### Audio Generation (Full Pipeline)

```bash
# Generate conversations with audio files
python generators/main_generator.py

# Use enhanced TTS providers
python demos/enhanced_tts_demo.py

# Generate with GCP (higher rate limits)
python generators/gcp_generator.py
```

### Text-Only Generation (Fast & Efficient)

```bash
# Generate text conversations only (no audio)
python generators/text_only_generator.py

# Test text-only generation
python demos/text_only_demo.py
```

**When to use text-only generation:**

- ⚡ **Fast prototyping**: Generate large datasets quickly
- 💰 **Cost-effective**: No TTS API costs
- 🔄 **Iterative development**: Test conversation logic
- 📊 **Large-scale datasets**: Generate thousands of conversations

### Custom Configuration

```python
# Edit config/config.py
NUM_CONVERSATIONS = 100
TURNS_PER_DIALOG_MAX = 15
```

## 🔍 Quality Validation

The system includes comprehensive validation:

- ✅ Conversation structure (agent starts, user ends)
- ✅ Audio file existence and metadata
- ✅ Transcript length (20-200 characters)
- ✅ Proper intent progression
- ✅ Speaker ID consistency

## 📊 Statistics Example

```
🎤 SYNTHETIC DATA GENERATION COMPLETE
=====================================
✅ Successful conversations: 50/50
📊 Total utterances: 420
🤖 Agent utterances (TTS): 210
👤 User utterances: 210
🎤 Unique agent voices: 10
🎤 Unique user voices: 20
⏱️  Total audio duration: 2.3 hours
📁 Audio files generated: 420
```

## 🚀 Next Steps

### For Audio Training Data

1. **Run audio generation**: `python generators/main_generator.py`
2. **Test audio quality**: `python demos/enhanced_tts_demo.py`
3. **Enhance voices**: Add ElevenLabs API for premium quality

### For Text-Only Training Data

1. **Run text generation**: `python generators/text_only_generator.py`
2. **Test text quality**: `python demos/text_only_demo.py`
3. **Scale up**: Generate thousands of conversations quickly

### General

4. **Configure settings**: Edit `config/config.py` for your needs
5. **Train models**: Use generated JSONL files for ASR/TTS training

## 🏆 TEKNOFEST 2025 Compliance

This tool generates data in the exact format required for the Turkish Natural Language Processing competition:

- ✅ Turkish language conversations
- ✅ Telecom domain specificity
- ✅ Speaker identification
- ✅ Role labeling (agent/user)
- ✅ Intent and slot annotations
- ✅ Audio file generation
- ✅ JSONL manifest format

## 🤝 Support

For questions or issues:

1. Check the documentation in `docs/`
2. Review configuration in `config/config.py`
3. Test with demos in `demos/`
4. Verify API keys in `.env`

---

**Ready to generate professional Turkish telecom training data! 🎯**
