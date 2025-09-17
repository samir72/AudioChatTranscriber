# Audio Summarizer UI (Azure OpenAI + Gradio)

A simple web app to **summarize audio** from three sources—**file upload**, **microphone recording**, or **URL download**—using **Azure OpenAI** via the `azure.ai.projects` client and a friendly **Gradio** UI.

---

## ✨ Features

- Upload a local WAV file, record from mic, or provide a WAV/MP3 URL
- Converts audio to Base64 and sends it to Azure OpenAI as multimodal input
- Configurable **system** and **user** prompts
- Clean, minimal Gradio UI
- Environment-based configuration; uses `DefaultAzureCredential` (no raw keys required)

---

## 🧭 Architecture Overview

```
 ┌───────────────┐     file/mic/url     ┌───────────────────────┐
 │   Gradio UI   │  ──────────────────▶ │  process_audio(...)    │
 └──────┬────────┘                      └──────────┬─────────────┘
        │                                        validates/reads
        │                             ┌───────────────────────────┐
        │                             │ encode_audio(...),        │
        │                             │ download_wav_from_url(...)│
        │                             └──────────┬────────────────┘
        │                                        │ base64 audio
        ▼                                        ▼
 ┌───────────────────────────┐        ┌─────────────────────────────┐
 │ summarize_audio(audio,...)│  ───▶  │ Azure AIProjectClient →     │
 └───────────────────────────┘        │ OpenAI Chat Completions     │
                                      │ (multimodal: text + audio)  │
                                      └─────────────────────────────┘
```

---

## 📦 Requirements

- Python 3.10+
- An Azure subscription with access to **Azure OpenAI** and an **AI Project** endpoint
- Local login to Azure (for `DefaultAzureCredential`) or another supported credential method

### Python Dependencies

Create a `requirements.txt` (or copy/paste below):

```txt
azure-identity>=1.17.1
azure-ai-projects>=1.0.0b6
gradio>=4.44.0
python-dotenv>=1.0.1
requests>=2.32.3
```

Install:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔐 Configuration

This app uses environment variables loaded via `.env` and authenticates with `DefaultAzureCredential` (with environment and managed identity explicitly **disabled**). You’ll typically authenticate with **Azure CLI** locally.

1) **Create `.env`** at the project root:

```ini
# Azure AI Project endpoint (from Azure AI Foundry / Project details)
AC_PROJECT_ENDPOINT=https://<your-project>.projects.azure.com

# Your Azure OpenAI model deployment name (e.g., gpt-4o-realtime-preview, gpt-4o-mini, etc.)
AC_MODEL_DEPLOYMENT=<your-model-deployment-name>

# Optional: Gradio host/port customization (if you modify demo.launch)
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860
```

2) **Login to Azure** (since `DefaultAzureCredential` will fall back to CLI auth):

```bash
az login
az account set --subscription "<YOUR SUBSCRIPTION NAME OR ID>"
```

---

## ▶️ Running the App

Save the provided Python code as, for example, `app.py`, then:

```bash
python app.py
```

Open the URL printed by Gradio (by default http://127.0.0.1:7860).

---

## 🧪 How to Use

1. **Choose an input method**:
   - **Upload WAV File** – select a local file.
   - **Record Audio** – record from your microphone.
   - **Enter URL** – paste a direct link to an audio file (WAV/MP3).

2. **Prompts**:
   - **System Prompt** (defaults provided): sets assistant behavior.
   - **User Prompt** (e.g., “Summarize the audio content”).  

3. Click **Summarize**. The summary text appears in the **Summary** box.

---

## 🧩 Code Walkthrough (key parts)

- **process_audio(...)** → orchestrates input selection, reads/encodes audio, calls summarizer  
- **encode_audio(...)** → handles base64 encoding for file or memory  
- **download_wav_from_url(...)** → fetches bytes from URL  
- **summarize_audio(...)** → calls Azure OpenAI Chat Completions with text + audio input  

---

## ✅ Environment & Azure Setup Checklist

- [ ] `.env` contains valid `AC_PROJECT_ENDPOINT` and `AC_MODEL_DEPLOYMENT`  
- [ ] Your Azure identity has **Reader/Contributor** on the AI Project and **can access** the model deployment  
- [ ] `az login` succeeded and the correct subscription is selected  
- [ ] The chosen **model deployment** supports **audio input** (multimodal)

---

## 🔧 Troubleshooting

- **Credential errors** → ensure `az login` and subscription are set  
- **Model/Deployment not found** → verify deployment name & multimodal support  
- **HTTP 403/401** → check Azure RBAC roles (e.g., Cognitive Services OpenAI User)  
- **Temp file issues** → adjust code to manage downloaded audio as files

---

## 🧹 Improvements & TODOs

- Align audio format (`wav` vs `mp3`) in UI and request  
- Handle temp files more robustly  
- Add better error handling and user feedback  
- Support multi-turn conversations instead of single prompts  

---

## 🧰 Project Structure (suggested)

```
.
├─ app.py
├─ requirements.txt
├─ .env
├─ README.md
└─ LICENSE
```

---

## 📄 License

MIT License

Copyright (c) 2025 Sayed Amir Rizvi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
