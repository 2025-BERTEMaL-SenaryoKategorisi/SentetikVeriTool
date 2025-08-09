# 🎯 Turkish Telecom Synthetic Data Generator - Complete Project Overview

Bu proje, TEKNOFEST 2025 Türkçe Doğal Dil İşleme yarışması için geliştirilmiş kapsamlı bir sentetik veri üretim aracıdır. Hem metin tabanlı hem de gerçek ses dosyalı ASR/TTS model eğitimi için veri üretir.

## 📁 Proje Dosya Yapısı

```
SentetikVeri/
├── 📄 Temel Dosyalar
│   ├── main2.py                    # Orijinal versiyon (referans)
│   ├── main3.py                    # Gelişmiş metin tabanlı versiyon
│   ├── main3_with_audio.py         # Audio-enhanced versiyon ⭐
│   ├── demo.py                     # Hızlı metin demo (3 görüşme)
│   ├── audio_demo.py               # Audio demo ve test
│   ├── config.py                   # Kapsamlı konfigürasyon
│   ├── test_generator.py           # Kalite kontrol ve validasyon
│   └── requirements.txt            # Tüm dependencies
│
├── 📚 Dokümantasyon
│   ├── README.md                   # Ana dokümantasyon
│   ├── README_AUDIO.md             # Audio versiyon rehberi ⭐
│   ├── USAGE_GUIDE.md              # Detaylı kullanım kılavuzu
│   └── PROJECT_OVERVIEW.md         # Bu dosya
│
├── 📊 Veri Dosyaları
│   ├── seeds.json                  # Başlangıç örnekleri
│   ├── .env                        # API anahtarları
│   └── data/                       # Üretilen veriler
│       ├── manifest.jsonl
│       ├── training_manifest.jsonl
│       ├── training_manifest_with_audio.jsonl ⭐
│       ├── asr_training_data.jsonl
│       ├── tts_training_data.jsonl
│       └── audio/                  # Ses dosyaları ⭐
│           ├── agent/
│           └── user/
│
└── 🎤 Audio Özellikler
    ├── TTS entegrasyonu
    ├── Çoklu ses karakteristikleri
    ├── Audio metadata
    └── Kalite kontrolü
```

## 🚀 İki Ana Versiyon

### 1. 📝 Text-Only Version (`main3.py`)

**En İyi Kullanım**: Hızlı prototipleme, yarışma teslimi, NLU eğitimi

**Özellikler**:

- ⚡ Hızlı üretim (~2-3 saniye/tur)
- 💾 Düşük disk kullanımı
- 🎯 Yarışma gereksinimlerine uygun
- 📊 100+ görüşme kapasitesi

**Çıktı Örneği**:

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

### 2. 🎤 Audio-Enhanced Version (`main3_with_audio.py`) ⭐

**En İyi Kullanım**: Tam ASR/TTS pipeline, üretim kullanımı

**Özellikler**:

- 🎵 Gerçek TTS ses dosyaları
- 🎭 10 farklı agent + 20 farklı user sesi
- 📊 Audio metadata (duration, sample rate, file size)
- 🔊 Pitch shifting, speed variation, background noise
- 📁 Organize edilmiş audio dosya yapısı

**Çıktı Örneği**:

```json
{
  "conversation_id": 1,
  "audio_filepath": "data/audio/agent/0001_01_20250129_a1b2c3d4.wav",
  "transcript": "Merhaba, ben Ahmet. Size nasıl yardımcı olabilirim?",
  "speaker_id": "agent_voice_001",
  "role": "agent",
  "intent": "greeting",
  "slot": {},
  "audio_duration": 3.2,
  "sample_rate": 16000,
  "channels": 1,
  "file_size": 102400
}
```

## 🎯 Kullanım Senaryoları

### 🏆 TEKNOFEST 2025 Yarışması İçin

```bash
# Hızlı başlangıç - metin tabanlı
python demo.py              # 3 görüşme demo
python main3.py             # 100 görüşme üretimi
python test_generator.py    # Kalite kontrolü
```

### 🎓 ASR Model Eğitimi İçin

```bash
# Audio versiyon - tam pipeline
python audio_demo.py        # Audio test
python main3_with_audio.py  # Ses dosyalı üretim
```

### 🔬 Araştırma ve Geliştirme İçin

```bash
# Konfigürasyon özelleştirme
vim config.py              # Ayarları düzenle
python main3_with_audio.py # Özel ayarlarla üret
```

## 📊 Performans Karşılaştırması

| Özellik              | Text-Only           | Audio-Enhanced         |
| -------------------- | ------------------- | ---------------------- |
| **Üretim Hızı**      | ~2-3 sn/tur         | ~3-5 sn/tur            |
| **Disk Kullanımı**   | ~1-2 MB/100 görüşme | ~50-100 MB/100 görüşme |
| **Ses Dosyası**      | ❌ Placeholder      | ✅ Gerçek WAV          |
| **ASR Eğitimi**      | ❌ Sadece metin     | ✅ Tam pipeline        |
| **TTS Eğitimi**      | ❌ Sadece metin     | ✅ Tam pipeline        |
| **Yarışma Uyumu**    | ✅ Mükemmel         | ✅ Mükemmel            |
| **Üretim Hazırlığı** | ⚠️ Kısıtlı          | ✅ Tam hazır           |

## 🎨 Ses Karakteristikleri (Audio Version)

### 🤖 Agent Voices (TTS Eğitimi)

- **Tutarlılık**: Her görüşmede aynı ajan sesi
- **Çeşitlilik**: 10 farklı ses karakteristiği
- **Özellikler**: Pitch shifting (-3 ile +3 semitone)
- **Tempo**: Normal ve yavaş konuşma seçenekleri

### 👤 User Voices (ASR Çeşitliliği)

- **Çeşitlilik**: 20 farklı kullanıcı sesi
- **Hız Varyasyonu**: 0.8x - 1.2x konuşma hızı
- **Pitch Range**: -3 ile +3 semitone
- **Gerçekçilik**: Hafif arka plan gürültüsü

## 🔧 Konfigürasyon Seçenekleri

### Temel Ayarlar

```python
NUM_CONVERSATIONS = 100      # Görüşme sayısı
TURNS_PER_DIALOG_MIN = 6    # Min tur sayısı
TURNS_PER_DIALOG_MAX = 16   # Max tur sayısı
TEMPERATURE_AGENT = 0.7     # Ajan yaratıcılığı
TEMPERATURE_USER = 0.9      # Kullanıcı yaratıcılığı
```

### Audio Ayarları

```python
AUDIO_CONFIG = {
    'sample_rate': 16000,    # ASR standart
    'channels': 1,           # Mono
    'format': 'wav',         # WAV format
    'normalize': True,       # Ses normalizasyonu
    'add_noise': True,       # Arka plan gürültüsü
}
```

### Senaryo Dağılımı

```python
SCENARIO_WEIGHTS = {
    "billing_dispute": 0.25,     # Fatura itirazları
    "technical_support": 0.30,   # Teknik destek
    "package_change": 0.20,      # Paket değişiklikleri
    "roaming_inquiry": 0.15,     # Roaming sorguları
    "account_management": 0.10   # Hesap yönetimi
}
```

## 🎯 Hangi Versiyonu Seçmeli?

### 📝 Text-Only Version Seç Eğer:

- ✅ Hızlı prototip istiyorsun
- ✅ TEKNOFEST yarışması için yeterli
- ✅ Disk alanı kısıtlı
- ✅ Sadece NLU/NLP eğitimi yapacaksın
- ✅ İlk kez deniyorsun

### 🎤 Audio-Enhanced Version Seç Eğer:

- ✅ Gerçek ASR/TTS modeli eğiteceksin
- ✅ Üretim kalitesinde veri istiyorsun
- ✅ Ses karakteristikleri önemli
- ✅ Tam pipeline kuruyorsun
- ✅ Araştırma/geliştirme yapıyorsun

## 🚀 Hızlı Başlangıç Rehberi

### 1. İlk Kurulum

```bash
git clone <repository>
cd SentetikVeri
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key" > .env
```

### 2. Hızlı Test

```bash
# Metin demo
python demo.py

# Audio demo (eğer audio istiyorsan)
python audio_demo.py
```

### 3. Tam Üretim

```bash
# Metin tabanlı (hızlı)
python main3.py

# Audio tabanlı (tam özellik)
python main3_with_audio.py
```

### 4. Kalite Kontrolü

```bash
python test_generator.py
```

## 📈 Ölçeklendirme Rehberi

### Küçük Ölçek (Demo/Test)

- **Görüşme**: 3-10
- **Süre**: 1-5 dakika
- **Disk**: <10 MB
- **Kullanım**: `demo.py` veya `audio_demo.py`

### Orta Ölçek (Geliştirme)

- **Görüşme**: 50-100
- **Süre**: 15-60 dakika
- **Disk**: 50-100 MB (audio ile)
- **Kullanım**: `main3.py` veya `main3_with_audio.py`

### Büyük Ölçek (Üretim)

- **Görüşme**: 500-1000+
- **Süre**: 2-8 saat
- **Disk**: 500MB-5GB (audio ile)
- **Kullanım**: `main3_with_audio.py` + paralel işleme

## 🔍 Kalite Kontrol Checklist

### ✅ Temel Kontroller

- [ ] API anahtarı ayarlandı
- [ ] Dependencies yüklendi
- [ ] Demo başarıyla çalıştı
- [ ] Manifest dosyaları oluştu
- [ ] JSON formatı doğru

### ✅ Audio Kontroller (Audio Version)

- [ ] Audio dosyaları oluştu
- [ ] WAV format doğru (16kHz, mono)
- [ ] Ses kalitesi kabul edilebilir
- [ ] Duration metadata doğru
- [ ] Farklı sesler ayırt edilebilir

### ✅ İçerik Kontrolleri

- [ ] Türkçe dil kalitesi iyi
- [ ] Telekom terminolojisi doğru
- [ ] Görüşme akışları mantıklı
- [ ] Intent/slot etiketleri uygun
- [ ] Speaker ID tutarlılığı var

## 🎓 Sonuç ve Öneriler

### 🏆 TEKNOFEST 2025 İçin

1. **İlk adım**: `demo.py` ile test edin
2. **Geliştirme**: `main3.py` ile 100 görüşme üretin
3. **Teslim**: Text-based versiyon yeterli
4. **Bonus**: Audio version ile fark yaratın

### 🚀 Üretim Kullanımı İçin

1. **Başlangıç**: `audio_demo.py` ile test edin
2. **Geliştirme**: `main3_with_audio.py` ile tam pipeline
3. **Ölçeklendirme**: Paralel işleme ve cloud storage
4. **Optimizasyon**: Konfigürasyon fine-tuning

### 📊 Model Eğitimi İçin

1. **ASR**: Audio version ile tam veri seti
2. **TTS**: Agent-only audio dosyaları
3. **NLU**: Text version yeterli
4. **Multimodal**: Audio version şart

---

**🎯 Bu proje, TEKNOFEST 2025 yarışmasından üretim kullanımına kadar her seviyede ihtiyacı karşılayacak şekilde tasarlanmıştır.**

**🎤 Audio-enhanced versiyon ile gerçek ASR/TTS pipeline kurabilir, text-only versiyon ile hızlı prototipleme yapabilirsiniz.**

**📧 Sorularınız için GitHub Issues kullanabilirsiniz.**
