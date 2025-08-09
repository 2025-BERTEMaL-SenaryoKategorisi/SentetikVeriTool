# 🚀 GCP Vertex AI Setup Guide for High-Volume Data Generation

Since you have GCP credits, we can use **Google Cloud Vertex AI** which has much higher rate limits than the free Gemini API.

## 📋 **Step-by-Step Setup**

### **STEP 1: Enable Required APIs**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Go to **APIs & Services** → **Library**
4. Enable these APIs:
   - **Vertex AI API**
   - **Generative Language API**
   - **Cloud Resource Manager API**

### **STEP 2: Create Service Account**

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"Create Service Account"**
3. **Name**: `synthetic-data-generator`
4. **Description**: `Service account for Turkish telecom data generation`
5. Click **"Create and Continue"**

### **STEP 3: Grant Permissions**

Add these roles to your service account:

- **Vertex AI User** (`roles/aiplatform.user`)
- **AI Platform Developer** (`roles/ml.developer`)
- **Service Account Token Creator** (`roles/iam.serviceAccountTokenCreator`)

### **STEP 4: Create and Download Key**

1. Click on your service account
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Select **JSON** format
5. Download the JSON file
6. **Save it securely** (e.g., `~/gcp-service-account.json`)

### **STEP 5: Set Up Authentication**

**Option A: Environment Variable (Recommended)**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

**Option B: Add to .env file**

```bash
# Add this line to your .env file
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
```

### **STEP 6: Install Required Dependencies**

```bash
pip install google-cloud-aiplatform
```

### **STEP 7: Test Your Setup**

Run this test script to verify everything works:

```bash
python tools/test_gcp_setup.py
```

## 🎯 **Benefits of GCP Vertex AI**

### **Higher Rate Limits:**

- **Requests per minute**: 300+ (vs 15 for free tier)
- **Requests per day**: No daily limit with credits
- **Concurrent requests**: Much higher
- **Token limits**: Much more generous

### **Better Models:**

- **Gemini 1.5 Pro**: Latest model with better performance
- **Gemini 1.5 Flash**: Faster, cheaper option
- **Better Turkish language support**

### **Cost with Credits:**

- **Gemini 1.5 Pro**: ~$0.00125 per 1K input tokens
- **Gemini 1.5 Flash**: ~$0.000125 per 1K input tokens
- **Your GCP credits will cover thousands of conversations**

## 🚀 **Ready to Generate!**

Once set up, you can generate:

- **1000+ conversations** without rate limits
- **10,000+ utterances** for training
- **20+ hours of audio** for your competition dataset

Your synthetic data generator will run at **full speed** with GCP credits! 🏆
