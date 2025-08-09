# 🚀 Turkish Telecom Synthetic Data Generator - Usage Guide

Bu rehber, TEKNOFEST 2025 yarışması için geliştirilen sentetik veri üretim aracının nasıl kullanılacağını adım adım açıklar.

## 📋 Hızlı Başlangıç

### 1. Kurulum

```bash
# Projeyi klonlayın veya indirin
git clone <repository-url>
cd SentetikVeri

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# API anahtarınızı ayarlayın
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Demo Çalıştırma (Önerilen İlk Adım)

```bash
# Küçük bir demo veri seti oluşturun (3 görüşme)
python demo.py
```

Bu komut şunları üretir:

- `data/demo_manifest.jsonl` - Tüm demo verileri
- `data/demo_asr.jsonl` - ASR eğitimi için veriler
- `data/demo_tts.jsonl` - TTS eğitimi için veriler

### 3. Tam Veri Seti Üretimi

```bash
# Ana araçla 100 görüşme üretin
python main3.py
```

## 🔧 Konfigürasyon

### Temel Ayarlar (`config.py`)

```python
NUM_CONVERSATIONS = 100          # Üretilecek görüşme sayısı
TURNS_PER_DIALOG_MIN = 6        # Minimum tur sayısı
TURNS_PER_DIALOG_MAX = 16       # Maksimum tur sayısı
TEMPERATURE_AGENT = 0.7         # Ajan yaratıcılık seviyesi
TEMPERATURE_USER = 0.9          # Kullanıcı yaratıcılık seviyesi
```

### Senaryo Dağılımı

```python
SCENARIO_WEIGHTS = {
    "billing_dispute": 0.25,      # Fatura itirazları
    "technical_support": 0.30,    # Teknik destek
    "package_change": 0.20,       # Paket değişiklikleri
    "roaming_inquiry": 0.15,      # Roaming sorguları
    "account_management": 0.10    # Hesap yönetimi
}
```

## 📊 Çıktı Dosyaları

### 1. Ana Manifest (`training_manifest.jsonl`)

Her satır bir konuşma turunu temsil eder:

```json
{
  "conversation_id": 1,
  "audio_filepath": "audio/agent/0001_01_20250129_a1b2c3d4.wav",
  "transcript": "Merhaba, ben Ahmet. Size nasıl yardımcı olabilirim?",
  "speaker_id": "agent_voice_001",
  "role": "agent",
  "intent": "greeting",
  "slot": {}
}
```

### 2. ASR Eğitim Verisi (`asr_training_data.jsonl`)

- Tüm konuşmacılar (ajan + kullanıcı)
- Ses tanıma modeli eğitimi için
- Çeşitli konuşmacı sesleri

### 3. TTS Eğitim Verisi (`tts_training_data.jsonl`)

- Sadece ajan konuşmaları
- Ses sentezi modeli eğitimi için
- Tutarlı ajan sesleri

## 🎯 Veri Kalitesi Kontrolü

### Otomatik Doğrulama

```bash
# Üretilen verileri test edin
python test_generator.py
```

Bu test şunları kontrol eder:

- ✅ JSON format doğruluğu
- ✅ Speaker ID tutarlılığı
- ✅ Görüşme akış yapısı
- ✅ Intent-slot uyumluluğu
- ✅ Türkçe dil kalitesi

### Manuel Kontrol

```bash
# İlk 10 satırı görüntüleyin
head -10 data/training_manifest.jsonl

# Ajan konuşmalarını filtreleyin
grep '"role": "agent"' data/training_manifest.jsonl | head -5
```

## 📈 Performans İpuçları

### 1. API Rate Limiting

```python
# config.py içinde
RATE_LIMIT_DELAY = 0.1  # API çağrıları arası bekleme (saniye)
MAX_RETRIES_PER_CONVERSATION = 3  # Başarısız görüşme için tekrar sayısı
```

### 2. Bellek Optimizasyonu

```python
# Büyük veri setleri için
BATCH_SIZE = 10  # Toplu işleme boyutu
```

### 3. Hata Ayıklama

```python
# Detaylı log için
LOG_LEVEL = "DEBUG"
ENABLE_CONSOLE_LOGGING = True
```

## 🎨 Özelleştirme

### Yeni Senaryo Ekleme

```python
# config.py içinde TELECOM_SCENARIOS'a ekleyin
"new_scenario": {
    "description": "Yeni senaryo açıklaması",
    "flow": "greeting → custom_flow → closing",
    "intents": ["greeting", "custom_intent", "closing"],
    "common_issues": ["özel sorun 1", "özel sorun 2"]
}
```

### Ajan İsimleri Güncelleme

```python
# config.py içinde
AGENT_NAMES = [
    "Özel İsim 1", "Özel İsim 2", "Özel İsim 3"
]
```

### Ses Sayısını Artırma

```python
# config.py içinde
AGENT_VOICES = [
    "agent_voice_001", "agent_voice_002", # ... daha fazla
]
USER_VOICES = [
    "user_voice_001", "user_voice_002", # ... daha fazla
]
```

## 🔍 Sorun Giderme

### Yaygın Hatalar

#### 1. API Anahtarı Hatası

```
❌ GOOGLE_API_KEY not found in environment variables
```

**Çözüm**: `.env` dosyasında API anahtarınızı ayarlayın.

#### 2. JSON Parse Hatası

```
JSON parse failed for Conv 1, Turn 3
```

**Çözüm**: LLM yanıtları bazen bozuk JSON üretebilir. Araç otomatik retry yapar.

#### 3. Rate Limiting

```
Error: Rate limit exceeded
```

**Çözüm**: `RATE_LIMIT_DELAY` değerini artırın (örn: 0.5).

#### 4. Validation Hatası

```
[FAIL] Conv 5: Turn count (4) out of range
```

**Çözüm**: `TURNS_PER_DIALOG_MIN/MAX` değerlerini kontrol edin.

### Debug Modu

```bash
# Detaylı hata bilgisi için
export DEBUG=1
python main3.py
```

## 📊 Veri Analizi

### Temel İstatistikler

```python
import json

# Manifest dosyasını yükle
with open('data/training_manifest.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]

# İstatistikler
total_utterances = len(data)
agent_utterances = len([d for d in data if d['role'] == 'agent'])
user_utterances = total_utterances - agent_utterances

print(f"Toplam konuşma: {total_utterances}")
print(f"Ajan konuşması: {agent_utterances}")
print(f"Kullanıcı konuşması: {user_utterances}")
```

### Intent Dağılımı

```python
from collections import Counter

intents = [d['intent'] for d in data]
intent_counts = Counter(intents)

for intent, count in intent_counts.most_common():
    print(f"{intent}: {count}")
```

## 🎓 Model Eğitimi İçin Hazırlık

### ASR Model Eğitimi

```python
# ASR verilerini yükle
asr_data = []
with open('data/asr_training_data.jsonl', 'r') as f:
    for line in f:
        asr_data.append(json.loads(line))

# Transcript'leri çıkar
transcripts = [d['transcript'] for d in asr_data]
speaker_ids = [d['speaker_id'] for d in asr_data]
```

### TTS Model Eğitimi

```python
# TTS verilerini yükle (sadece ajan)
tts_data = []
with open('data/tts_training_data.jsonl', 'r') as f:
    for line in f:
        tts_data.append(json.loads(line))

# Ajan konuşmalarını speaker_id'ye göre grupla
from collections import defaultdict
speaker_groups = defaultdict(list)

for d in tts_data:
    speaker_groups[d['speaker_id']].append(d['transcript'])
```

## 🚀 Üretim Kullanımı

### Büyük Veri Setleri

```python
# config.py içinde
NUM_CONVERSATIONS = 1000  # 1000 görüşme
PARALLEL_PROCESSING = True  # Paralel işleme (deneysel)
MAX_WORKERS = 4  # İşçi thread sayısı
```

### Kalite Kontrolü

```bash
# Her 100 görüşmede bir test çalıştır
python test_generator.py

# Başarı oranı %90'ın altındaysa durdurun
```

## 📞 Destek

### Hata Raporlama

1. Hata mesajının tam metnini kaydedin
2. Kullanılan konfigürasyonu paylaşın
3. `generator.log` dosyasını kontrol edin
4. GitHub Issues'da rapor edin

### Performans Optimizasyonu

- API anahtarınızın quota limitlerini kontrol edin
- Büyük veri setleri için batch processing kullanın
- SSD disk kullanın (I/O performansı için)

---

**🎯 Bu araç TEKNOFEST 2025 Türkçe Doğal Dil İşleme yarışması için özel olarak geliştirilmiştir.**

**📧 Sorularınız için GitHub Issues kullanabilirsiniz.**
