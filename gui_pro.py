import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import json
import whisper

def log(msg):
    console.insert(tk.END, msg + "\n")
    console.see(tk.END)

def transcribe(audio_path):
    log("Loading Whisper model...")
    model = whisper.load_model("base")
    log("Transcribing audio...")
    result = model.transcribe(audio_path)

    segments = []
    for seg in result["segments"]:
        segments.append({
            "text": seg["text"],
            "start": seg["start"],
            "end": seg["end"]
        })
    return segments

def create_scenes(segments, total_prompts):
    total_time = segments[-1]["end"]
    target = total_time / max(total_prompts, 1)

    scenes = []
    current = []
    start_time = None
    scene_id = 1

    for seg in segments:
        if start_time is None:
            start_time = seg["start"]

        current.append(seg)

        if seg["end"] - start_time >= target:
            scene_text = " ".join(s["text"] for s in current).strip()
            scenes.append({
                "scene_id": f"SCENE_{scene_id:03d}",
                "start_time_sec": round(start_time, 2),
                "end_time_sec": round(seg["end"], 2),
                "duration_sec": round(seg["end"] - start_time, 2),
                "transcript": scene_text
            })
            scene_id += 1
            current = []
            start_time = None

    if current and start_time is not None:
        scene_text = " ".join(s["text"] for s in current).strip()
        scenes.append({
            "scene_id": f"SCENE_{scene_id:03d}",
            "start_time_sec": round(start_time, 2),
            "end_time_sec": round(current[-1]["end"], 2),
            "duration_sec": round(current[-1]["end"] - start_time, 2),
            "transcript": scene_text
        })

    return scenes

def save_output(scenes):
    os.makedirs("output", exist_ok=True)
    with open("output/scenes.jsonl", "w", encoding="utf-8") as f:
        for s in scenes:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

def run_pipeline():
    try:
        audio = audio_path.get().strip()
        prompts = int(prompt_count.get().strip() or "30")

        if not audio:
            messagebox.showerror("Error", "Please select an MP3 file.")
            return

        if prompts <= 0:
            messagebox.showerror("Error", "Prompt count must be greater than 0.")
            return

        log("Starting...")
        segments = transcribe(audio)
        scenes = create_scenes(segments, prompts)
        save_output(scenes)
        log(f"Done! Created {len(scenes)} scenes.")
        log("Saved to output/scenes.jsonl")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        log(f"Error: {e}")

def start():
    threading.Thread(target=run_pipeline, daemon=True).start()

def select_audio():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    audio_path.set(file_path)

root = tk.Tk()
root.title("Video Prompt Tool (Whisper Build Ready)")
root.geometry("700x450")

audio_path = tk.StringVar()
prompt_count = tk.StringVar(value="30")

tk.Label(root, text="Audio (.mp3)").pack(pady=(10, 0))
tk.Entry(root, textvariable=audio_path, width=70).pack()
tk.Button(root, text="Select Audio", command=select_audio).pack(pady=(4, 10))

tk.Label(root, text="Number of Prompts").pack()
tk.Entry(root, textvariable=prompt_count).pack()

tk.Button(root, text="Generate", command=start, bg="green", fg="white").pack(pady=12)

tk.Label(root, text="Console").pack()
console = tk.Text(root, height=14)
console.pack(fill="both", expand=True, padx=10, pady=(0, 10))

root.mainloop()
