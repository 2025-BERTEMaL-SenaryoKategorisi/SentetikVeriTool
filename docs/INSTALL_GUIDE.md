# 🚀 Installation Guide - Turkish Telecom Audio Generator

Bu rehber, audio-enhanced synthetic data generator'ı kurmanız ve çalıştırmanız için adım adım talimatlar içerir.

## 📋 Sistem Gereksinimleri

- **Python**: 3.8 veya üzeri
- **İşletim Sistemi**: Windows, macOS, Linux
- **İnternet**: API çağrıları ve TTS için
- **Disk Alanı**: En az 500 MB boş alan

## 🔧 Adım 1: Python Kurulumu Kontrolü

```bash
# Python versiyonunu kontrol edin
python --version
# veya
python3 --version

# Pip kurulu mu kontrol edin
pip --version
# veya
pip3 --version
```

**Beklenen çıktı**: Python 3.8+ ve pip versiyonu görünmeli.

## 📦 Adım 2: Dependencies Kurulumu

### Temel Paketler

```bash
# Temel paketleri yükle
pip install python-dotenv
pip install langchain-google-genai
pip install tqdm
```

### Audio Paketleri

```bash
# TTS için Google Text-to-Speech
pip install gTTS

# Audio processing için
pip install pydub

# Audio analysis için
pip install librosa

# Audio I/O için
pip install soundfile

# Numerical computing için
pip install numpy
```

### Tek Komutla Tüm Paketler

```bash
# Tüm paketleri tek seferde yükle
pip install -r requirements.txt
```

## 🔑 Adım 3: API Anahtarı Ayarı

### Google Gemini API Anahtarı Alma

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın
3. API anahtarınızı kopyalayın

### .env Dosyası Oluşturma

```bash
# .env dosyası oluşturun
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

**Önemli**: `your_actual_api_key_here` yerine gerçek API anahtarınızı yazın!

## 🎤 Adım 4: Audio Demo Çalıştırma

### Hızlı Test

```bash
# Audio demo'yu çalıştır
python audio_demo.py
```

### Beklenen Çıktı

```
🎤 AUDIO GENERATION DEMO
==================================================
✅ Voice manager initialized successfully

🔄 Generating 6 audio samples...

   🎵 Generating: Merhaba, ben Ahmet. Size nasıl yardımcı olabilirim?...
      Speaker: agent_voice_001
      Role: agent
      ✅ Success! Duration: 3.2s, Size: 102400 bytes

   🎵 Generating: Merhaba, faturamda bir hata olduğunu düşünüyorum...
      Speaker: user_voice_001
      Role: user
      ✅ Success! Duration: 2.8s, Size: 89600 bytes

📊 AUDIO DEMO RESULTS:
   ✅ Successful: 6/6
   ⏱️  Total audio duration: 18.5 seconds
   📁 Audio files saved to: data/demo_audio
```

## 🚨 Olası Sorunlar ve Çözümler

### 1. Python Bulunamadı Hatası

```bash
# Windows'ta
py --version
py -m pip install -r requirements.txt

# macOS/Linux'ta
python3 --version
python3 -m pip install -r requirements.txt
```

### 2. Permission Denied Hatası

```bash
# macOS/Linux'ta
sudo pip install -r requirements.txt

# Windows'ta (Admin olarak CMD açın)
pip install -r requirements.txt
```

### 3. Audio Library Hataları

#### macOS için

```bash
# Homebrew ile ffmpeg yükle
brew install ffmpeg

# Sonra paketleri tekrar yükle
pip install pydub librosa soundfile
```

#### Ubuntu/Debian için

```bash
# System dependencies
sudo apt-get update
sudo apt-get install ffmpeg libsndfile1

# Python packages
pip install pydub librosa soundfile
```

#### Windows için

```bash
# Chocolatey ile ffmpeg (opsiyonel)
choco install ffmpeg

# Veya conda kullanın
conda install -c conda-forge librosa soundfile
```

### 4. API Anahtarı Hataları

```
❌ GOOGLE_API_KEY not found in environment variables
```

**Çözüm**:

```bash
# .env dosyasını kontrol edin
cat .env

# Doğru format:
GOOGLE_API_KEY=AIzaSyD...your_actual_key...xyz

# Boşluk veya tırnak işareti olmamalı!
```

### 5. Network/TTS Hataları

```
Error generating audio: HTTP Error 429: Too Many Requests
```

**Çözüm**:

```bash
# Biraz bekleyin ve tekrar deneyin
# Veya rate limiting artırın (audio_demo.py içinde)
time.sleep(1.0)  # 0.5 yerine 1.0 saniye
```

## 🔍 Kurulum Doğrulama

### Test Scripti

```bash
# Basit test scripti oluşturun
cat > test_installation.py << 'EOF'
#!/usr/bin/env python3
import sys

print("🧪 Testing installation...")

try:
    import dotenv
    print("✅ python-dotenv: OK")
except ImportError:
    print("❌ python-dotenv: FAILED")

try:
    import langchain_google_genai
    print("✅ langchain-google-genai: OK")
except ImportError:
    print("❌ langchain-google-genai: FAILED")

try:
    import gtts
    print("✅ gTTS: OK")
except ImportError:
    print("❌ gTTS: FAILED")

try:
    import pydub
    print("✅ pydub: OK")
except ImportError:
    print("❌ pydub: FAILED")

try:
    import librosa
    print("✅ librosa: OK")
except ImportError:
    print("❌ librosa: FAILED")

try:
    import soundfile
    print("✅ soundfile: OK")
except ImportError:
    print("❌ soundfile: FAILED")

try:
    import numpy
    print("✅ numpy: OK")
except ImportError:
    print("❌ numpy: FAILED")

print("\n🎯 Installation test complete!")
EOF

# Test'i çalıştır
python test_installation.py
```

### API Anahtarı Testi

```bash
# API anahtarı test scripti
cat > test_api.py << 'EOF'
#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    print("🎯 Ready to run audio demo!")
else:
    print("❌ API Key not found!")
    print("Please create .env file with GOOGLE_API_KEY=your_key")
EOF

python test_api.py
```

## 🎵 Audio Demo Çalıştırma

### Adım Adım

```bash
# 1. Dizine gidin
cd /path/to/SentetikVeri

# 2. Kurulumu test edin
python test_installation.py

# 3. API anahtarını test edin
python test_api.py

# 4. Audio demo'yu çalıştırın
python audio_demo.py

# 5. Sonuçları kontrol edin
ls -la data/demo_audio/
```

### Başarılı Çalışma Göstergeleri

- ✅ 6 audio dosyası oluşturuldu
- ✅ `data/demo_audio/agent/` ve `data/demo_audio/user/` klasörleri var
- ✅ WAV dosyaları çalınabilir durumda
- ✅ `demo_manifest.jsonl` dosyası oluştu

### Audio Dosyalarını Dinleme

```bash
# macOS'ta
afplay data/demo_audio/agent/demo_01_agent_*.wav

# Linux'ta
aplay data/demo_audio/agent/demo_01_agent_*.wav

# Windows'ta
# Windows Media Player ile .wav dosyalarını açın
```

## 🎯 Sonraki Adımlar

### Başarılı Kurulum Sonrası

```bash
# Tam audio generator'ı çalıştır
python main3_with_audio.py

# Sonuçları test et
python test_generator.py
```

### Sorun Yaşıyorsanız

1. **Hata mesajını tam olarak kopyalayın**
2. **Python ve pip versiyonlarını kontrol edin**
3. **İnternet bağlantınızı kontrol edin**
4. **API anahtarınızın doğru olduğunu kontrol edin**
5. **Disk alanınızın yeterli olduğunu kontrol edin**

---

**🎤 Bu rehberi takip ederek audio-enhanced synthetic data generator'ı başarıyla kurabilir ve çalıştırabilirsiniz!**
