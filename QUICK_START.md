# 🚀 Quick Start Guide

Get up and running with the Turkish Telecom Synthetic Data Generator in 5 minutes!

## ⚡ Super Quick Start (Text-Only)

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/SentetikVeri.git
cd SentetikVeri
pip install -r requirements.txt

# 2. Configure (minimum setup)
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Generate text conversations (fast!)
python generators/text_only_generator.py
```

**That's it!** You'll have Turkish telecom conversation data in `data/text_only/`

## 🎤 Audio Generation Setup

For high-quality audio generation:

```bash
# 1. Add ElevenLabs API key to .env
ELEVENLABS_API_KEY=your_key_here

# 2. Generate conversations with audio
python generators/main_generator.py
```

## 📊 What You Get

### Text-Only Generation

- **Speed**: ~30 seconds per conversation
- **Cost**: Only LLM API calls
- **Output**: `data/text_only/`
  - `text_conversations.jsonl` - Complete conversations
  - `text_asr_data.jsonl` - ASR training data
  - `text_tts_data.jsonl` - TTS training data

### Audio Generation

- **Speed**: ~2-3 minutes per conversation
- **Quality**: High-quality WAV files with ElevenLabs
- **Output**: `data/outputs/` + `data/audio/`
  - JSONL manifests with audio metadata
  - WAV files for each conversation turn

## 🎯 Sample Output

```json
{
  "conversation_id": 1,
  "transcript": "Merhaba, Türk Telekom'dan Ayşe ben. Size nasıl yardımcı olabilirim?",
  "speaker_id": "agent_female_001",
  "role": "agent",
  "intent": "greeting",
  "slot": {},
  "agent_name": "Ayşe",
  "scenario": "billing_dispute",
  "turn_number": 1
}
```

## 🔧 Configuration

Edit `config/config.py` to customize:

```python
NUM_CONVERSATIONS = 50        # How many conversations to generate
TURNS_PER_DIALOG_MIN = 6     # Minimum turns per conversation
TURNS_PER_DIALOG_MAX = 12    # Maximum turns per conversation
```

## 🎭 Scenarios Available

1. **Billing Dispute** - Customer questions charges
2. **Technical Support** - Internet/phone issues
3. **Package Change** - Plan upgrades/downgrades
4. **Roaming Inquiry** - International usage questions
5. **Account Management** - Profile updates, payments

## 🚀 Demo Scripts

```bash
# Quick text demo (2 conversations)
python demos/text_only_demo.py

# Audio quality demo
python demos/enhanced_tts_demo.py
```

## 📈 Scaling Up

```bash
# Generate 100 text conversations
# Edit config.py: NUM_CONVERSATIONS = 100
python generators/text_only_generator.py

# Generate 50 audio conversations
# Edit config.py: NUM_CONVERSATIONS = 50
python generators/main_generator.py
```

## 🔄 Incremental Generation

Both generators automatically continue from the last conversation ID:

```bash
# First run: generates conversations 1-50
python generators/text_only_generator.py

# Second run: generates conversations 51-100
python generators/text_only_generator.py

# No data overwriting! ✅
```

## 🆘 Troubleshooting

### Common Issues

**"No module named 'config'"**

```bash
# Make sure you're in the project root directory
cd SentetikVeri
python generators/text_only_generator.py
```

**"API key not found"**

```bash
# Check your .env file
cat .env
# Make sure GOOGLE_API_KEY is set
```

**"Permission denied"**

```bash
# Make sure you have write permissions
chmod +w data/
```

### Getting Help

- 📖 **Full Documentation**: Check `README.md`
- 📝 **Text-Only Guide**: See `docs/TEXT_ONLY_GUIDE.md`
- 🐛 **Issues**: Create GitHub issue
- 💬 **Questions**: Use GitHub Discussions

## 🎯 TEKNOFEST 2025 Ready

This tool generates data in the exact format required for the TEKNOFEST 2025 Turkish Natural Language Processing competition:

- ✅ Turkish language conversations
- ✅ Telecom domain specificity
- ✅ Speaker identification
- ✅ Role labeling (agent/user)
- ✅ Intent and slot annotations
- ✅ JSONL manifest format

## 🏃‍♂️ Next Steps

1. **Start Small**: Generate 5-10 conversations to test
2. **Validate Quality**: Check the generated conversations
3. **Scale Up**: Increase `NUM_CONVERSATIONS` for production
4. **Add Audio**: Use `main_generator.py` for audio files
5. **Train Models**: Use generated JSONL files for ASR/TTS training

**Happy generating! 🎉**
