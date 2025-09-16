"""
Audio Summarizer UI (Gradio)

Features
- Upload a .wav file and summarize
- Record audio from your microphone and summarize
- Paste a URL to a .wav file; the app downloads then summarizes
- Batch summarize multiple .wav files
- Optional: persist input audio to a chosen folder

How to run
1) pip install -U gradio requests
2) python app.py
3) Open the local URL shown in your terminal

Integrate your summarizer
- Replace the `summarize_audio` stub with your real function.
  It receives a local file path to a WAV and should return a summary string.

Notes
- This app expects WAV input. If your backend supports other formats, you can
  extend `ensure_wav` to convert to WAV before summarization.
- Recording uses the browser’s microphone permission.
"""
from __future__ import annotations

import os
import io
import sys
import time
import shutil
import tempfile
import pathlib
from typing import List, Tuple

import gradio as gr
import requests

# ===============================
# 🔧 Configuration
# ===============================
DEFAULT_SAVE_DIR = os.environ.get("AUDIO_SAVE_DIR", "./saved_audio")
pathlib.Path(DEFAULT_SAVE_DIR).mkdir(parents=True, exist_ok=True)

# ===============================
# ✨ Your summarizer goes here
# ===============================

def summarize_audio(wav_path: str, *, system_prompt: str | None = None) -> str:
    """Stub: Replace with your LLM-powered summarizer.

    Args:
        wav_path: Local filesystem path to a WAV file
        system_prompt: Optional extra instruction to steer the summary

    Returns:
        A concise textual summary of the audio content.
    """
    # TODO: call your existing pipeline here.
    # For now, return a placeholder including the file name.
    name = os.path.basename(wav_path)
    return f"[DEMO] Summarized contents of {name}. (Plug in your LLM here.)"

# ===============================
# 🧰 Helpers
# ===============================

def _persist_copy(src_path: str, save_dir: str | None) -> str:
    """Optionally copy the source file to save_dir and return the path we used."""
    if not save_dir:
        return src_path
    save_dir = os.path.abspath(save_dir)
    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    dest = os.path.join(save_dir, os.path.basename(src_path))
    # Avoid clobbering: add a timestamp if exists
    if os.path.exists(dest):
        stem = pathlib.Path(dest).stem
        suffix = pathlib.Path(dest).suffix
        dest = os.path.join(save_dir, f"{stem}-{int(time.time())}{suffix}")
    shutil.copy2(src_path, dest)
    return dest


def _download_wav(url: str) -> str:
    """Download a WAV from URL to a temporary file and return local path."""
    if not url or not url.strip():
        raise gr.Error("Please provide a non-empty URL.")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        raise gr.Error(f"Failed to download file: {e}")

    # Derive a filename
    filename = None
    # Try Content-Disposition first
    cd = resp.headers.get("content-disposition", "")
    if "filename=" in cd:
        filename = cd.split("filename=")[-1].strip('"')
    if not filename:
        # Fallback from URL path
        filename = pathlib.PurePosixPath(requests.utils.urlparse(url).path).name or "download.wav"

    # Ensure .wav extension
    if not filename.lower().endswith(".wav"):
        filename += ".wav"

    tmpdir = tempfile.mkdtemp(prefix="dlwav_")
    local = os.path.join(tmpdir, filename)
    with open(local, "wb") as f:
        f.write(resp.content)

    return local


def ensure_wav(input_path: str) -> str:
    """Placeholder: confirm/convert to WAV if needed.

    Currently assumes input is already WAV and returns the same path.
    You can extend this to transcode other formats to WAV using ffmpeg/pydub.
    """
    if not input_path.lower().endswith(".wav"):
        # You can convert here; for now, we enforce WAV-only.
        raise gr.Error("This demo expects .wav files. Please upload or provide a WAV URL.")
    return input_path

# ===============================
# 🚀 Inference endpoints used by the UI
# ===============================

def summarize_single(
    wav_path: str | None,
    save_toggle: bool,
    save_dir: str,
    system_prompt: str,
) -> Tuple[str, str]:
    """Summarize a single file (uploaded or recorded)."""
    if not wav_path:
        raise gr.Error("No audio provided.")

    wav_path = ensure_wav(wav_path)
    used_path = _persist_copy(wav_path, save_dir if save_toggle else None)
    summary = summarize_audio(used_path, system_prompt=system_prompt or None)
    return used_path, summary


def summarize_from_url(
    url: str,
    save_toggle: bool,
    save_dir: str,
    system_prompt: str,
) -> Tuple[str, str]:
    """Download from URL and summarize."""
    local = _download_wav(url)
    local = ensure_wav(local)
    used_path = _persist_copy(local, save_dir if save_toggle else None)
    summary = summarize_audio(used_path, system_prompt=system_prompt or None)
    return used_path, summary


def summarize_batch(
    wav_paths: List[str] | None,
    save_toggle: bool,
    save_dir: str,
    system_prompt: str,
) -> List[List[str]]:
    """Summarize multiple files. Returns a table [[file, summary], ...]."""
    if not wav_paths:
        raise gr.Error("Please select one or more WAV files.")

    results: List[List[str]] = []
    for p in wav_paths:
        try:
            p2 = ensure_wav(p)
            used_path = _persist_copy(p2, save_dir if save_toggle else None)
            s = summarize_audio(used_path, system_prompt=system_prompt or None)
            results.append([used_path, s])
        except Exception as e:
            results.append([str(p), f"Error: {e}"])
    return results

# ===============================
# 🎛️ UI Layout
# ===============================
with gr.Blocks(title="Audio Summarizer UI") as demo:
    gr.Markdown("""
    # 📝 Audio Summarizer
    Upload, record, or paste a URL to a WAV file, then get a concise summary.
    Replace the summarizer stub in `app.py` with your LLM-powered logic.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            system_prompt = gr.Textbox(
                label="Optional: System/Style Instructions",
                placeholder="e.g., 'Summarize for an executive in 3 bullet points'",
            )
        with gr.Column(scale=1):
            save_toggle = gr.Checkbox(value=False, label="Save input audio to folder")
            save_dir = gr.Textbox(value=DEFAULT_SAVE_DIR, label="Save folder (if enabled)")

    with gr.Tabs():
        # --- Tab 1: Upload a single WAV ---
        with gr.TabItem("Upload .wav"):
            in_upload = gr.Audio(sources=["upload"], type="filepath", label="Upload WAV")
            out_path_u = gr.Textbox(label="Used file path", interactive=False)
            out_sum_u = gr.Textbox(label="Summary", lines=6)
            btn_u = gr.Button("Summarize Upload", variant="primary")
            btn_u.click(
                summarize_single,
                inputs=[in_upload, save_toggle, save_dir, system_prompt],
                outputs=[out_path_u, out_sum_u],
            )

        # --- Tab 2: Record from mic ---
        with gr.TabItem("Record"):
            in_rec = gr.Audio(sources=["microphone"], type="filepath", label="Record")
            out_path_r = gr.Textbox(label="Used file path", interactive=False)
            out_sum_r = gr.Textbox(label="Summary", lines=6)
            btn_r = gr.Button("Summarize Recording", variant="primary")
            btn_r.click(
                summarize_single,
                inputs=[in_rec, save_toggle, save_dir, system_prompt],
                outputs=[out_path_r, out_sum_r],
            )

        # --- Tab 3: URL to WAV ---
        with gr.TabItem("From URL"):
            in_url = gr.Textbox(label="WAV URL", placeholder="https://example.com/audio.wav")
            out_path_url = gr.Textbox(label="Used file path", interactive=False)
            out_sum_url = gr.Textbox(label="Summary", lines=6)
            btn_url = gr.Button("Download & Summarize", variant="primary")
            btn_url.click(
                summarize_from_url,
                inputs=[in_url, save_toggle, save_dir, system_prompt],
                outputs=[out_path_url, out_sum_url],
            )

        # --- Tab 4: Batch multiple WAVs ---
        with gr.TabItem("Batch (.wav files)"):
            in_files = gr.Files(file_count="multiple", type="filepath", label="Select one or more WAV files")
            out_table = gr.Dataframe(
                headers=["File", "Summary"],
                datatype=["str", "str"],
                interactive=False,
                wrap=True,
                row_count=(1, "dynamic"),
                label="Results",
            )
            btn_b = gr.Button("Summarize Batch", variant="primary")
            btn_b.click(
                summarize_batch,
                inputs=[in_files, save_toggle, save_dir, system_prompt],
                outputs=out_table,
            )

    gr.Markdown(
        """
        ---
        **Tip:** If your existing program already handles directories and formats, you can
        call it inside `summarize_audio` and skip the WAV-only restriction.
        """
    )

if __name__ == "__main__":
    # `share=True` creates a temporary public link if you need to try it remotely.
    demo.launch(share=False)
