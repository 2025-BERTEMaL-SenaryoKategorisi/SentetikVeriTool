# Turkish Telecom Synthetic Data Generator for ASR/TTS Training

Bu araç, TEKNOFEST 2025 Türkçe Doğal Dil İşleme yarışması için ASR (Automatic Speech Recognition) ve TTS (Text-to-Speech) model eğitimi amacıyla sentetik telefon görüşmesi verileri üretir.

## 🎯 Özellikler

### 🎤 Konuşmacı Yönetimi

- **Agent Voices**: Her görüşme için tutarlı ajan sesi (TTS eğitimi için)
- **User Voices**: Çeşitli kullanıcı sesleri (ASR eğitimi için çeşitlilik)
- **Speaker ID**: Benzersiz konuşmacı kimlikleri (`agent_voice_001`, `user_voice_001` vb.)

### 📞 Türk Telekom Senaryoları

1. **Fatura İtirazı** (`billing_dispute`) - Ödeme sorunları ve fatura hataları
2. **Teknik Destek** (`technical_support`) - İnternet, modem ve sinyal sorunları
3. **Paket Değişikliği** (`package_change`) - Tarife upgrade/downgrade talepleri
4. **Roaming Bilgileri** (`roaming_inquiry`) - Yurt dışı kullanım sorguları
5. **Hesap Yönetimi** (`account_management`) - Bakiye, fatura geçmişi sorguları

### 🏷️ Etiketleme Sistemi

- **Role**: `agent` (ajan) / `user` (kullanıcı)
- **Intent**: `greeting`, `complaint`, `info_request`, `info_provide`, `solution`, `closing`, `thanks`
- **Slot**: Yapılandırılmış bilgi çıkarımı için anahtar-değer çiftleri

### 📊 Çıktı Formatları

- **Complete Manifest**: Tüm görüşme verileri (`training_manifest.jsonl`)
- **ASR Data**: Tüm konuşmacılar için eğitim verisi (`asr_training_data.jsonl`)
- **TTS Data**: Sadece ajan konuşmaları (`tts_training_data.jsonl`)

## 🚀 Kurulum

```bash
# Gerekli paketleri yükle
pip install -r requirements.txt

# .env dosyasında Google API anahtarını ayarla
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## 📋 Gereksinimler

- Python 3.8+
- Google Gemini API anahtarı
- İnternet bağlantısı (LLM API çağrıları için)

## 🔧 Kullanım

### Temel Kullanım

```bash
python main3.py
```

### Konfigürasyon Seçenekleri

`main3.py` dosyasındaki konfigürasyon değişkenlerini düzenleyebilirsiniz:

```python
NUM_CONVERSATIONS = 100          # Üretilecek görüşme sayısı
TURNS_PER_DIALOG_MIN = 6        # Minimum tur sayısı
TURNS_PER_DIALOG_MAX = 16       # Maksimum tur sayısı
TEMPERATURE_AGENT = 0.7         # Ajan yaratıcılık seviyesi
TEMPERATURE_USER = 0.9          # Kullanıcı yaratıcılık seviyesi
```

## 📁 Çıktı Dosyaları

### 1. training_manifest.jsonl

Tüm görüşme verilerini içeren ana manifest dosyası.

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

### 2. asr_training_data.jsonl

ASR model eğitimi için tüm konuşmacı verilerini içerir.

### 3. tts_training_data.jsonl

TTS model eğitimi için sadece ajan konuşmalarını içerir.

## 🎯 Veri Kalitesi Özellikleri

### Konuşma Doğallığı

- Türkçe dolgu kelimeleri ("tabii ki", "bir saniye lütfen")
- Telekom terminolojisi
- Gerçekçi görüşme akışları
- Bağlamsal geçişler

### Teknik Özellikler

- **Transcript Uzunluğu**: 40-150 karakter
- **Speaker Consistency**: Görüşme boyunca aynı ajan sesi
- **Role Alternation**: Ajan-kullanıcı sıralaması
- **Intent Validation**: Doğru niyet etiketlemesi

## 📊 İstatistikler

Araç çalıştırıldıktan sonra aşağıdaki istatistikleri gösterir:

```
✅ Successful conversations: 95/100
📊 Total utterances: 1,045
🤖 Agent utterances (TTS): 523
👤 User utterances: 522
🎤 Unique agent voices: 10
🎤 Unique user voices: 20
```

## 🔍 Doğrulama Sistemi

Araç, üretilen her görüşme için şu kontrolleri yapar:

- ✅ Tur sayısı sınırları (6-16 tur)
- ✅ Rol sıralaması (ajan-kullanıcı-ajan...)
- ✅ Transcript uzunluk kontrolü
- ✅ Audio filepath formatı
- ✅ Speaker ID geçerliliği
- ✅ Intent-slot uyumluluğu
- ✅ Görüşme kapanış kontrolü

## 🎨 Senaryo Örnekleri

### Fatura İtirazı

```
Agent: "Merhaba, ben Ayşe. Size nasıl yardımcı olabilirim?"
User: "Merhaba, faturamda hata olduğunu düşünüyorum."
Agent: "Tabii, fatura numaranızı alabilir miyim?"
User: "Fatura numaram 1234567890."
...
```

### Teknik Destek

```
Agent: "Merhaba, ben Mehmet. Nasıl yardımcı olabilirim?"
User: "İnternetim iki saattir kesildi, yardım lütfen."
Agent: "Anlıyorum. Modem ışıkları nasıl yanıyor?"
User: "DSL ışığı yanıp sönüyor."
...
```

## 🔧 Gelişmiş Özellikler

### Speaker Manager Sınıfı

```python
speaker_manager = SpeakerManager()
agent_voice, user_voice = speaker_manager.assign_speakers(conversation_id)
```

### Senaryo Bazlı Talimatlar

Her senaryo için özelleştirilmiş görüşme akışları ve talimatlar.

### Türkçe Dil Desteği

- Doğal Türkçe ifadeler
- Telekom sektörü terminolojisi
- Bölgesel konuşma kalıpları

## 🚨 Hata Ayıklama

### Yaygın Sorunlar

1. **JSON Parse Hatası**

   ```
   JSON parse failed for Conv 1, Turn 3
   ```

   **Çözüm**: API yanıtlarında JSON formatı kontrol edilir, otomatik retry mekanizması devreye girer.

2. **Validation Hatası**

   ```
   [FAIL] Conv 5: Turn count (4) out of range.
   ```

   **Çözüm**: Minimum/maksimum tur sayıları ayarlanabilir.

3. **API Rate Limiting**
   ```
   Error in Conv 10, Attempt 2: Rate limit exceeded
   ```
   **Çözüm**: `time.sleep(0.1)` ile rate limiting uygulanır.

## 📈 Performans Optimizasyonu

- **Batch Processing**: Görüşmeler paralel işlenebilir
- **Caching**: Tekrarlanan API çağrıları önlenir
- **Memory Management**: Büyük veri setleri için bellek optimizasyonu

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje TEKNOFEST 2025 yarışması kapsamında Apache 2.0 lisansı ile lisanslanmıştır.

## 📞 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**🎯 TEKNOFEST 2025 Türkçe Doğal Dil İşleme Yarışması için hazırlanmıştır.**
