import os
import base64
import tempfile
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import AzureOpenAI  # official OpenAI SDK, works with Azure endpoints

# --- LLM call (Azure OpenAI with API key) -----------------------------------

def summarize_audio_b64(audio_b64: str, sys_prompt: str, user_prompt: str) -> str:
    """
    Calls Azure OpenAI Chat Completions with audio input (base64 mp3).
    """
    load_dotenv()

    endpoint = os.getenv("AC_OPENAI_ENDPOINT")
    api_key = os.getenv("AC_OPENAI_API_KEY")
    deployment = os.getenv("AC_MODEL_DEPLOYMENT")
    api_version = os.getenv("AC_OPENAI_API_VERSION")

    if not endpoint or not api_key or not deployment:
        return "Server misconfiguration: required env vars missing."

    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint,
        )

        system_message = sys_prompt.strip() if sys_prompt else (
            "You are an AI assistant with a charter to clearly analyze the customer enquiry."
        )
        user_text = user_prompt.strip() if user_prompt else "Summarize the audio content."

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_text},
                        {
                            "type": "input_audio",
                            "input_audio": {"data": audio_b64, "format": "mp3"},
                        },
                    ],
                },
            ],
        )

        return response.choices[0].message.content

    except Exception as ex:
        return f"Error from Azure OpenAI: {ex}"


# --- I/O helpers ------------------------------------------------------------

def encode_audio_from_path(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def download_to_temp_mp3(url: str) -> str:
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                tmp.write(chunk)
        return tmp.name


def process_audio(upload_path, record_path, url, sys_prompt, user_prompt):
    tmp_to_cleanup = []
    try:
        audio_path = None
        if upload_path:
            audio_path = upload_path
        elif record_path:
            audio_path = record_path
        elif url and url.strip():
            audio_path = download_to_temp_mp3(url.strip())
            tmp_to_cleanup.append(audio_path)

        if not audio_path:
            return "Please provide an audio file via upload, recording, or URL."

        audio_b64 = encode_audio_from_path(audio_path)
        return summarize_audio_b64(audio_b64, sys_prompt, user_prompt)

    finally:
        for p in tmp_to_cleanup:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass


# --- UI ---------------------------------------------------------------------

with gr.Blocks(title="Audio Summarizer") as demo:
    gr.Markdown("# Audio File Summarizer (Azure OpenAI)")
    gr.Markdown("Upload a mp3, record audio, or paste a URL. The app sends base64 audio to Azure OpenAI.")

    with gr.Row():
        with gr.Column():
            upload_audio = gr.Audio(sources=["upload"], type="filepath", label="Upload mp3")
        with gr.Column():
            record_audio = gr.Audio(sources=["microphone"], type="filepath", label="Record Audio")
        with gr.Column():
            url_input = gr.Textbox(label="mp3 URL", placeholder="https://example.com/audio.mp3")

    with gr.Row():
        userprompt_input = gr.Textbox(
            label="User Prompt",
            value="Summarize the audio content",
            placeholder="e.g., Extract key points and action items",
        )
        sysprompt_input = gr.Textbox(
            label="System Prompt",
            value="You are an AI assistant with a listening charter to clearly analyze the customer enquiry.",
        )

    submit_btn = gr.Button("Summarize")
    output = gr.Textbox(label="Summary", lines=12)

    submit_btn.click(
        fn=process_audio,
        inputs=[upload_audio, record_audio, url_input, sysprompt_input, userprompt_input],
        outputs=output,
    )

if __name__ == "__main__":
    demo.launch()
