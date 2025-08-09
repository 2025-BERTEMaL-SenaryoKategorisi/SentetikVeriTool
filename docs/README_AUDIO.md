# 🎤 Turkish Telecom Synthetic Data Generator with Audio Generation

Bu araç, TEKNOFEST 2025 Türkçe Doğal Dil İşleme yarışması için **gerçek ses dosyaları** ile birlikte ASR (Automatic Speech Recognition) ve TTS (Text-to-Speech) model eğitimi amacıyla sentetik telefon görüşmesi verileri üretir.

## 🆕 Audio Version Özellikleri

### 🎵 Gerçek Ses Dosyası Üretimi

- **TTS Entegrasyonu**: Google Text-to-Speech ile gerçek ses dosyaları
- **Çoklu Ses Karakteristikleri**: Her speaker_id için farklı ses özellikleri
- **Ses Kalitesi Kontrolü**: 16kHz, mono, WAV format
- **Ses Metadata**: Duration, sample rate, file size bilgileri

### 🎭 Gelişmiş Ses Yönetimi

- **Agent Voices**: Tutarlı pitch ve tempo özellikleri
- **User Voices**: Çeşitli konuşma hızları ve ses tonları
- **Pitch Shifting**: Her ses için farklı ton ayarları
- **Background Noise**: Gerçekçilik için hafif arka plan gürültüsü

### 📊 Audio Metadata

Her konuşma turu için ek bilgiler:

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

## 🚀 Kurulum ve Kullanım

### 1. Gelişmiş Gereksinimler

```bash
# Temel paketler
pip install -r requirements.txt

# Ek audio paketleri (otomatik yüklenir)
# - gTTS: Google Text-to-Speech
# - pydub: Audio processing
# - librosa: Audio analysis
# - soundfile: Audio I/O
```

### 2. API Anahtarı Ayarı

```bash
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
```

### 3. Audio Demo (Önerilen İlk Adım)

```bash
# Küçük audio demo çalıştır (6 ses dosyası)
python audio_demo.py
```

### 4. Tam Audio Veri Seti

```bash
# 100 görüşme + gerçek ses dosyaları üret
python main3_with_audio.py
```

## 📁 Çıktı Dosyaları

### Audio Dosya Yapısı

```
data/
├── audio/
│   ├── agent/
│   │   ├── 0001_01_20250129_a1b2c3d4.wav
│   │   ├── 0001_03_20250129_b2c3d4e5.wav
│   │   └── ...
│   └── user/
│       ├── 0001_02_20250129_c3d4e5f6.wav
│       ├── 0001_04_20250129_d4e5f6g7.wav
│       └── ...
├── training_manifest_with_audio.jsonl
├── asr_training_data_with_audio.jsonl
└── tts_training_data_with_audio.jsonl
```

### Manifest Formatı

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

## 🎨 Ses Karakteristikleri

### Agent Voices (TTS Eğitimi İçin)

- **agent_voice_001**: Normal pitch, normal tempo
- **agent_voice_002**: +2 semitone pitch shift
- **agent_voice_003**: Yavaş konuşma
- **agent_voice_004**: +1 semitone pitch shift
- **agent_voice_005**: -2 semitone pitch shift
- **agent_voice_006**: Yavaş konuşma, normal pitch
- **agent_voice_007**: +3 semitone pitch shift
- **agent_voice_008**: -1 semitone pitch shift
- **agent_voice_009**: Yavaş konuşma, +1 pitch
- **agent_voice_010**: -3 semitone pitch shift

### User Voices (ASR Çeşitliliği İçin)

- **Çeşitli konuşma hızları**: 0.8x - 1.2x
- **Farklı pitch değerleri**: -3 ile +3 semitone arası
- **Tempo varyasyonları**: Yavaş ve normal konuşma
- **20 farklı user voice**: Maksimum çeşitlilik

## 🔧 Audio Konfigürasyonu

### config.py İçinde Audio Ayarları

```python
AUDIO_CONFIG = {
    'sample_rate': 16000,    # ASR için standart
    'channels': 1,           # Mono
    'bit_depth': 16,         # 16-bit
    'format': 'wav',         # WAV format
    'normalize': True,       # Ses seviyesi normalizasyonu
    'add_noise': True,       # Arka plan gürültüsü
    'speed_variation': True, # Konuşma hızı varyasyonu
}
```

### Ses Kalitesi Kontrolü

```python
# Pitch shifting aralığı
PITCH_RANGE = (-3, 3)  # semitone

# Konuşma hızı aralığı
SPEED_RANGE = (0.8, 1.2)  # multiplier

# Background noise seviyesi
NOISE_LEVEL = 0.005  # very subtle
```

## 📊 Performans Metrikleri

### Tipik Üretim Süreleri

- **Text Generation**: ~2-3 saniye/tur
- **Audio Generation**: ~1-2 saniye/tur
- **Total per Turn**: ~3-5 saniye
- **100 Conversation**: ~30-60 dakika

### Disk Kullanımı

- **Ortalama Audio Dosyası**: ~50-100 KB
- **100 Görüşme (~1000 tur)**: ~50-100 MB
- **1000 Görüşme**: ~500MB - 1GB

### Audio Kalitesi

- **Sample Rate**: 16 kHz (ASR standart)
- **Bit Depth**: 16-bit
- **Format**: WAV (lossless)
- **Channels**: Mono
- **Duration Range**: 1-8 saniye/tur

## 🎯 Model Eğitimi İçin Kullanım

### ASR Model Eğitimi

```python
import json
import librosa

# ASR verilerini yükle
asr_data = []
with open('data/asr_training_data_with_audio.jsonl', 'r') as f:
    for line in f:
        asr_data.append(json.loads(line))

# Audio dosyalarını yükle
for item in asr_data:
    audio_path = item['audio_filepath']
    audio, sr = librosa.load(audio_path, sr=16000)
    transcript = item['transcript']
    speaker_id = item['speaker_id']

    # ASR eğitim pipeline'ına gönder
    # train_asr_model(audio, transcript, speaker_id)
```

### TTS Model Eğitimi

```python
# TTS verilerini yükle (sadece agent)
tts_data = []
with open('data/tts_training_data_with_audio.jsonl', 'r') as f:
    for line in f:
        tts_data.append(json.loads(line))

# Speaker ID'ye göre grupla
from collections import defaultdict
speaker_groups = defaultdict(list)

for item in tts_data:
    speaker_id = item['speaker_id']
    audio_path = item['audio_filepath']
    transcript = item['transcript']

    speaker_groups[speaker_id].append({
        'audio': audio_path,
        'text': transcript,
        'duration': item['audio_duration']
    })

# Her speaker için TTS modeli eğit
for speaker_id, samples in speaker_groups.items():
    print(f"Training TTS for {speaker_id}: {len(samples)} samples")
    # train_tts_model(speaker_id, samples)
```

## 🔍 Audio Kalite Kontrolü

### Otomatik Validasyon

```bash
# Audio dosyalarını doğrula
python test_generator.py
```

Kontrol edilen özellikler:

- ✅ Audio dosyası varlığı
- ✅ Doğru format (WAV, 16kHz, mono)
- ✅ Duration metadata doğruluğu
- ✅ File size makul aralıkta
- ✅ Audio corruption kontrolü

### Manuel Kalite Kontrolü

```bash
# İlk 5 agent ses dosyasını listele
find data/audio/agent -name "*.wav" | head -5

# Ses dosyası bilgilerini görüntüle
ffprobe data/audio/agent/0001_01_*.wav

# Ses dosyasını çal (macOS)
afplay data/audio/agent/0001_01_*.wav
```

## 🚨 Sorun Giderme

### Audio Generation Hataları

#### 1. gTTS API Hatası

```
Error generating audio: HTTP Error 429: Too Many Requests
```

**Çözüm**: Rate limiting artırın:

```python
RATE_LIMIT_DELAY = 1.0  # 1 saniye bekle
```

#### 2. Audio Dependencies Hatası

```
ImportError: No module named 'librosa'
```

**Çözüm**: Audio paketlerini yükleyin:

```bash
pip install librosa soundfile pydub
```

#### 3. Disk Alanı Hatası

```
OSError: [Errno 28] No space left on device
```

**Çözüm**: Disk alanını kontrol edin, eski dosyaları silin.

#### 4. Audio Format Hatası

```
Error: Could not write audio file
```

**Çözüm**: Output dizininin yazma izni olduğunu kontrol edin.

### Performance Optimizasyonu

#### Paralel Audio Generation (Deneysel)

```python
# config.py içinde
PARALLEL_PROCESSING = True
MAX_WORKERS = 4  # CPU core sayısına göre ayarlayın
```

#### Memory Management

```python
# Büyük veri setleri için
BATCH_SIZE = 10  # Aynı anda işlenecek görüşme sayısı
```

## 📈 Gelişmiş Özellikler

### Custom Voice Characteristics

```python
# config.py içinde yeni ses ekle
AGENT_VOICES.append("agent_voice_011")

# main3_with_audio.py içinde ses özelliklerini tanımla
agent_voice_configs['agent_voice_011'] = {
    'lang': 'tr',
    'slow': False,
    'pitch_shift': 4
}
```

### Audio Post-Processing

```python
# Ses dosyalarına ek işlemler
def custom_audio_processing(audio_data, sample_rate):
    # Reverb ekleme
    # Compression
    # EQ ayarları
    return processed_audio
```

## 🎓 Üretim Kullanımı

### Büyük Ölçekli Üretim

```python
# 1000+ görüşme için
NUM_CONVERSATIONS = 1000
PARALLEL_PROCESSING = True
MAX_WORKERS = 8

# Disk alanı hesaplama
# ~1000 conversations = ~10,000 turns = ~500MB-1GB
```

### Cloud Storage Entegrasyonu

```python
# AWS S3, Google Cloud Storage vb. için
def upload_audio_to_cloud(audio_path, cloud_path):
    # Cloud upload logic
    pass
```

## 📞 Destek ve Geliştirme

### Performans İzleme

- Audio generation speed tracking
- Disk usage monitoring
- Memory usage optimization
- Error rate tracking

### Kalite Metrikleri

- Audio duration distribution
- File size consistency
- Voice characteristic validation
- Transcript-audio alignment

---

**🎤 Bu audio-enhanced versiyon, gerçek ses dosyaları ile tam ASR/TTS eğitim pipeline'ı sağlar.**

**🎯 TEKNOFEST 2025 yarışması ve üretim kullanımı için hazırdır.**

**📧 Audio-specific sorular için GitHub Issues kullanabilirsiniz.**
