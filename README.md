# 🇹🇷 Turkish Telecom Synthetic Data Generator

## 📋 İçindekiler | Table of Contents

- [🇹🇷 Türkçe](#türkçe-tr)
- [🇺🇸 English](#english-en)

---

<!-- --Türkçe start -->

# Türkçe (TR)

# 🇹🇷 Türk Telekom Sentetik Veri Üretici

🎤 **TEKNOFEST 2025 Türkçe Doğal Dil İşleme yarışması için profesyonel sentetik veri üretim aracı**

Türk telekom müşteri hizmetleri görüşmeleri için ASR (Otomatik Konuşma Tanıma) ve TTS (Metinden Sese) modellerine yönelik yüksek kaliteli eğitim verisi üretir. Doğru konuşmacı tanımlama ve rol etiketleme özelliklerine sahiptir.

## 🚀 Hızlı Başlangıç

```bash
# 1. Gerekli paketleri yükleyin
pip install -r requirements.txt

# 2. Çevre değişkenlerini yapılandırın
cp .env.example .env
# .env dosyasını API anahtarlarınızla düzenleyin

# 3. Üreticileri çalıştırın
python generators/main_generator.py      # Ses üretimi ile
python generators/text_only_generator.py # Sadece metin (daha hızlı)
python generators/gcp_generator.py       # GCP versiyonu (yüksek limitler)

# 4. Demo testleri çalıştırın
python demos/enhanced_tts_demo.py        # Gelişmiş TTS demo
python demos/text_only_demo.py           # Sadece metin demo
```

## 📁 Proje Yapısı

```
SentetikVeri/
├── generators/           # Ana üretim scriptleri
│   ├── main_generator.py      # Standart Google AI üretici (ses ile)
│   ├── text_only_generator.py # Hızlı sadece metin üretici (ses yok)
│   └── gcp_generator.py       # GCP Vertex AI versiyonu (yüksek limitler)
├── demos/               # Demo ve test scriptleri
│   ├── enhanced_tts_demo.py   # Yüksek kaliteli TTS demo
│   ├── text_only_demo.py      # Sadece metin üretim demo
│   ├── audio_demo.py          # Temel ses demo
│   └── simple_audio_demo.py   # Basit TTS test
├── config/              # Yapılandırma dosyaları
│   └── config.py           # Ana yapılandırma
├── data/                # Üretilen veri
│   ├── outputs/            # Eğitim manifestleri (JSONL)
│   ├── text_only/          # Sadece metin görüşme verisi
│   └── audio/              # Üretilen ses dosyaları
│       ├── agent/          # Ajan ses dosyaları
│       └── user/           # Kullanıcı ses dosyaları
├── docs/                # Dokümantasyon
│   ├── README.md           # Ana dokümantasyon
│   ├── USAGE_GUIDE.md      # Kullanım talimatları
│   └── INSTALL_GUIDE.md    # Kurulum rehberi
├── .env                 # Çevre değişkenleri
├── requirements.txt     # Python bağımlılıkları
└── README.md           # Bu dosya
```

## 🎯 Özellikler

### Temel İşlevsellik

- ✅ **Türk Telekom Senaryoları**: 5 gerçekçi görüşme türü
- ✅ **Konuşmacı Yönetimi**: Görüşme başına tutarlı ajan sesleri
- ✅ **Rol Etiketleme**: Doğru ajan/kullanıcı rol ataması
- ✅ **Niyet ve Slot Çıkarımı**: NLU eğitim verisi
- ✅ **Ses Üretimi**: Ses varyasyonları ile gerçek WAV dosyaları
- ✅ **Sadece Metin Üretimi**: Ses olmadan hızlı görüşme üretimi
- ✅ **JSONL Manifestleri**: Yarışma uyumlu format

### Ses Kalitesi

- 🎤 **Çoklu TTS Sağlayıcılar**: ElevenLabs, Google Cloud TTS, Azure, gTTS
- 🎵 **Ses Varyasyonları**: Pitch değiştirme, hız kontrolü, arka plan gürültüsü
- 📊 **Ses Metadata**: Süre, örnekleme hızı, dosya boyutu takibi
- 🔊 **Kalite Kontrolü**: Doğrulama ve hata yönetimi

### Teknik Özellikler

- ⚡ **Hız Sınırlama**: API dostu üretim
- 🔄 **Yeniden Deneme Mantığı**: Sağlam hata yönetimi
- 📈 **İlerleme Takibi**: Gerçek zamanlı üretim durumu
- 💾 **Verimli Depolama**: Düzenli dosya yapısı

## 🎤 Ses Üretim Süreci

**Sorunuz: "Ses, AI tarafından üretilen JSON scriptlerinden mi geliyor?"**

**Cevap: EVET!** İşte tam iş akışı:

1. **AI JSON üretir** görüşme metni ile:

   ```json
   {
     "transcript": "Merhaba, size nasıl yardımcı olabilirim?",
     "speaker_id": "agent_voice_001",
     "role": "agent"
   }
   ```

2. **TTS metni sese dönüştürür**:

   - `transcript` alanını alır
   - Ses seçimi için `speaker_id` kullanır
   - WAV ses dosyası üretir

3. **Ses yolu JSON'a geri eklenir**:

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

4. **Son JSONL hem metin hem de ses içerir** eğitim için.

## 📊 Üretilen Veri Formatı

### Eğitim Manifestosu (JSONL)

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

### Çıktı Dosyaları

**Ses Üretimi:**

- `data/outputs/training_manifest.jsonl` - Ses ile tam eğitim verisi
- `data/outputs/asr_training_data.jsonl` - ASR'ye özgü veri
- `data/outputs/tts_training_data.jsonl` - TTS'ye özgü veri (sadece ajanlar)
- `data/audio/agent/` - Ajan ses dosyaları
- `data/audio/user/` - Kullanıcı ses dosyaları

**Sadece Metin Üretimi:**

- `data/text_only/text_conversations.jsonl` - Tam metin görüşmeleri
- `data/text_only/text_asr_data.jsonl` - Metin ASR eğitim verisi
- `data/text_only/text_tts_data.jsonl` - Metin TTS eğitim verisi

## 🔧 Yapılandırma

### Çevre Değişkenleri (.env)

```bash
# Google AI (Ücretsiz katman)
GOOGLE_API_KEY=your_google_api_key

# GCP Vertex AI (Daha yüksek limitler)
GCP_PROJECT_ID=your_project_id
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Gelişmiş TTS Sağlayıcılar (İsteğe bağlı)
ELEVENLABS_API_KEY=your_elevenlabs_key
GOOGLE_CLOUD_TTS_API_KEY=your_gcp_tts_key
AZURE_SPEECH_KEY=your_azure_key
```

### Üretim Ayarları

```python
NUM_CONVERSATIONS = 50          # Üretilecek görüşme sayısı
TURNS_PER_DIALOG_MIN = 6       # Görüşme başına minimum tur
TURNS_PER_DIALOG_MAX = 12      # Görüşme başına maksimum tur
RATE_LIMIT_DELAY = 1.0         # API çağrıları arası gecikme (saniye)
```

## 🎯 Telekom Senaryoları

1. **Fatura İtirazı** - Müşteri ücret sorgular
2. **Teknik Destek** - İnternet/telefon sorunları
3. **Paket Değişikliği** - Plan yükseltme/düşürme
4. **Roaming Sorgusu** - Uluslararası kullanım soruları
5. **Hesap Yönetimi** - Profil güncellemeleri, ödemeler

Her senaryo şunları içerir:

- Gerçekçi görüşme akışı
- Türk telekom terminolojisi
- Doğru niyet ilerlemesi
- Doğal dil kalıpları

## 🎵 Ses Sistemi

### Ajan Sesleri (Profesyonel)

- 10 farklı ajan sesi
- Görüşme başına tutarlı
- Profesyonel, yardımcı ton
- Çeşitlilik için pitch varyasyonları

### Kullanıcı Sesleri (Doğal)

- 20 çeşitli kullanıcı sesi
- Farklı yaş, cinsiyet, duygular
- Hız ve pitch varyasyonları
- Gerçekçi müşteri endişeleri

## 📈 Kullanım Örnekleri

### Ses Üretimi (Tam Pipeline)

```bash
# Ses dosyaları ile görüşmeler üret
python generators/main_generator.py

# Gelişmiş TTS sağlayıcıları kullan
python demos/enhanced_tts_demo.py

# GCP ile üret (yüksek hız limitleri)
python generators/gcp_generator.py
```

### Sadece Metin Üretimi (Hızlı ve Verimli)

```bash
# Sadece metin görüşmeler üret (ses yok)
python generators/text_only_generator.py

# Sadece metin üretimi test et
python demos/text_only_demo.py
```

**Ne zaman sadece metin üretimi kullanılır:**

- ⚡ **Hızlı prototipleme**: Büyük veri setlerini hızla üret
- 💰 **Maliyet etkin**: TTS API maliyeti yok
- 🔄 **Yinelemeli geliştirme**: Görüşme mantığını test et
- 📊 **Büyük ölçekli veri setleri**: Binlerce görüşme üret

### Özel Yapılandırma

```python
# config/config.py'yi düzenle
NUM_CONVERSATIONS = 100
TURNS_PER_DIALOG_MAX = 15
```

## 🔍 Kalite Doğrulama

Sistem kapsamlı doğrulama içerir:

- ✅ Görüşme yapısı (ajan başlar, kullanıcı bitirir)
- ✅ Ses dosyası varlığı ve metadata
- ✅ Transcript uzunluğu (20-200 karakter)
- ✅ Doğru niyet ilerlemesi
- ✅ Konuşmacı ID tutarlılığı

## 📊 İstatistik Örneği

```
🎤 SENTETİK VERİ ÜRETİMİ TAMAMLANDI
===================================
✅ Başarılı görüşmeler: 50/50
📊 Toplam ifade: 420
🤖 Ajan ifadeleri (TTS): 210
👤 Kullanıcı ifadeleri: 210
🎤 Benzersiz ajan sesleri: 10
🎤 Benzersiz kullanıcı sesleri: 20
⏱️  Toplam ses süresi: 2.3 saat
📁 Üretilen ses dosyaları: 420
```

## 🚀 Sonraki Adımlar

### Ses Eğitim Verisi İçin

1. **Ses üretimi çalıştır**: `python generators/main_generator.py`
2. **Ses kalitesini test et**: `python demos/enhanced_tts_demo.py`
3. **Sesleri geliştir**: Premium kalite için ElevenLabs API ekle

### Sadece Metin Eğitim Verisi İçin

1. **Metin üretimi çalıştır**: `python generators/text_only_generator.py`
2. **Metin kalitesini test et**: `python demos/text_only_demo.py`
3. **Ölçeklendir**: Binlerce görüşmeyi hızla üret

### Genel

4. **Ayarları yapılandır**: İhtiyaçlarınız için `config/config.py`'yi düzenle
5. **Modelleri eğit**: ASR/TTS eğitimi için üretilen JSONL dosyalarını kullan

## 🏆 TEKNOFEST 2025 Uyumluluğu

Bu araç, Türkçe Doğal Dil İşleme yarışması için gereken tam formatta veri üretir:

- ✅ Türkçe dil görüşmeleri
- ✅ Telekom alan özgüllüğü
- ✅ Konuşmacı tanımlama
- ✅ Rol etiketleme (ajan/kullanıcı)
- ✅ Niyet ve slot açıklamaları
- ✅ Ses dosyası üretimi
- ✅ JSONL manifest formatı

## 🤝 Destek

Sorular veya sorunlar için:

1. `docs/` içindeki dokümantasyonu kontrol edin
2. `config/config.py` içindeki yapılandırmayı gözden geçirin
3. `demos/` içindeki demolarla test edin
4. `.env` içindeki API anahtarlarını doğrulayın

<!-- --Türkçe end -->

---

<!-- --English start -->

# English (EN)

# 🇺🇸 Turkish Telecom Synthetic Data Generator

🎤 **Professional synthetic data generation tool for TEKNOFEST 2025 Turkish Natural Language Processing competition**

Generates high-quality training data for ASR (Automatic Speech Recognition) and TTS (Text-to-Speech) models focused on Turkish telecom customer service conversations. Features accurate speaker identification and role labeling.

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
- ✅ **Role Labeling**: Accurate agent/user role assignment
- ✅ **Intent & Slot Extraction**: NLU training data
- ✅ **Audio Generation**: Real WAV files with voice variations
- ✅ **Text-Only Generation**: Fast conversation generation without audio
- ✅ **JSONL Manifests**: Competition-compatible format

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

<!-- --English end -->

---

**Ready to generate professional Turkish telecom training data! 🎯**
