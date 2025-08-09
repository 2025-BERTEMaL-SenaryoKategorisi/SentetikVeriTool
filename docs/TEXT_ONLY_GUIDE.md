# Text-Only Conversation Generator Guide

## Overview

The text-only conversation generator creates Turkish telecom conversations without audio files, making it perfect for:

- ⚡ **Fast prototyping**: Generate large datasets quickly
- 💰 **Cost-effective**: No TTS API costs
- 🔄 **Iterative development**: Test conversation logic
- 📊 **Large-scale datasets**: Generate thousands of conversations

## Quick Start

```bash
# Generate text-only conversations
python generators/text_only_generator.py

# Run demo (3 conversations)
python demos/text_only_demo.py
```

## Output Format

The text-only generator produces the same JSONL format as the audio generator, but without audio-related fields:

```json
{
  "conversation_id": 1,
  "transcript": "Merhaba, size nasıl yardımcı olabilirim?",
  "speaker_id": "agent_male_001",
  "role": "agent",
  "intent": "greeting",
  "slot": {},
  "agent_name": "Ahmet",
  "scenario": "billing_dispute",
  "turn_number": 1
}
```

## Output Files

All files are created in `data/text_only/`:

- **`text_conversations.jsonl`** - Complete conversation data
- **`text_asr_data.jsonl`** - All utterances for ASR training
- **`text_tts_data.jsonl`** - Agent utterances only for TTS training

## Features

### Same Quality as Audio Generator

- ✅ Turkish telecom scenarios
- ✅ Intent and slot labeling
- ✅ Speaker ID consistency
- ✅ Role-based conversation flow
- ✅ Validation and error handling

### Performance Benefits

- ⚡ **10x faster** than audio generation
- 💰 **No TTS costs** - only LLM API calls
- 🔄 **Incremental generation** - append new conversations
- 📊 **Scalable** - generate thousands of conversations

## Configuration

Uses the same configuration as the main generator:

```python
# In config/config.py
NUM_CONVERSATIONS = 100        # Number to generate
TURNS_PER_DIALOG_MIN = 6      # Minimum turns
TURNS_PER_DIALOG_MAX = 12     # Maximum turns
RATE_LIMIT_DELAY = 1.0        # API delay
```

## Use Cases

### 1. Rapid Prototyping

```bash
# Generate 100 conversations quickly
python generators/text_only_generator.py
```

### 2. Large Dataset Creation

```bash
# Edit config.py to increase NUM_CONVERSATIONS
# Then run multiple times to build large datasets
python generators/text_only_generator.py
```

### 3. Conversation Logic Testing

```bash
# Use demo to test small batches
python demos/text_only_demo.py
```

### 4. Text-Based Model Training

```bash
# Use generated JSONL files directly for:
# - Language model fine-tuning
# - Intent classification training
# - Slot extraction training
# - Conversation flow analysis
```

## Comparison: Text vs Audio Generation

| Feature  | Text-Only                      | Audio Generation         |
| -------- | ------------------------------ | ------------------------ |
| Speed    | ⚡ ~30 sec/conversation        | 🐌 ~2-3 min/conversation |
| Cost     | 💰 LLM only                    | 💸 LLM + TTS APIs        |
| Output   | 📝 Text + metadata             | 🎤 Text + audio files    |
| Use Case | 🔄 Prototyping, large datasets | 🎯 Final training data   |

## Best Practices

### 1. Start with Text-Only

```bash
# First, generate and validate conversation logic
python demos/text_only_demo.py

# Then scale up for large text datasets
python generators/text_only_generator.py
```

### 2. Incremental Generation

```bash
# Run multiple times to build large datasets
# Files are automatically appended, not overwritten
python generators/text_only_generator.py  # First batch
python generators/text_only_generator.py  # Second batch
python generators/text_only_generator.py  # Third batch
```

### 3. Quality Validation

```bash
# Check generated files
head -5 data/text_only/text_conversations.jsonl
wc -l data/text_only/text_conversations.jsonl
```

### 4. Convert to Audio Later

```bash
# After validating text conversations, generate audio
python generators/main_generator.py
```

## Troubleshooting

### Common Issues

1. **Empty output files**

   - Check API keys in `.env`
   - Verify internet connection
   - Check rate limits

2. **Validation errors**

   - Review conversation scenarios
   - Check turn count settings
   - Verify intent progression

3. **Performance issues**
   - Reduce `NUM_CONVERSATIONS` for testing
   - Increase `RATE_LIMIT_DELAY` if hitting limits
   - Use GCP version for higher limits

### Debug Commands

```bash
# Check configuration
python -c "from config.config import *; print(f'Conversations: {NUM_CONVERSATIONS}')"

# Verify API access
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print('API OK')"

# Check output directory
ls -la data/text_only/
```

## Integration with Audio Pipeline

The text-only generator is designed to work seamlessly with the audio pipeline:

1. **Generate text conversations** with text-only generator
2. **Validate conversation quality** and logic
3. **Generate audio files** using main generator
4. **Combine datasets** for comprehensive training data

This workflow maximizes efficiency and minimizes costs while ensuring high-quality training data.

---

**Ready to generate fast, cost-effective Turkish telecom conversation data! 🚀**
