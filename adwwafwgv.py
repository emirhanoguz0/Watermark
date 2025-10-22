import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip
from PIL import Image, ImageDraw, ImageFont
try:
    # FFmpeg'i ilk çalıştırmada otomatik indirip yolunu ayarlar
    from imageio_ffmpeg import get_ffmpeg_exe  # type: ignore
    _ffmpeg_path = get_ffmpeg_exe()
except Exception:
    # İndirme/tespit başarısız olsa bile MoviePy kendi hatasını yükseltir
    pass

# --- Filigran Varsayılan Ayarları ---
FONT_SIZE = 20  # Yazı tipi boyutu
FONT_COLOR = 'white'  # Yazı tipi rengi
POSITION = ('center', 'center')  # Konum

def process_video_thread(file_path, text):
    """Video işleme işlemini ayrı thread'de çalıştırır."""
    try:
        video_clip = VideoFileClip(file_path)

        # PIL ile şeffaf metin görseli üret (ImageMagick bağımlılığı yok)
        def build_text_clip(txt: str, font_size: int, color: str) -> ImageClip:
            # Font yükle (Windows varsayılan arial, yoksa fallback)
            font: ImageFont.FreeTypeFont | ImageFont.ImageFont
            # Font seçimini al
            selected_font = font_var.get()
            font_size = int(size_var.get())
            
            try:
                if selected_font == "DM Sans":
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\DMSans-Regular.ttf", font_size)
                elif selected_font == "Arial":
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
                elif selected_font == "Times New Roman":
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\times.ttf", font_size)
                elif selected_font == "Calibri":
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", font_size)
                elif selected_font == "Verdana":
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\verdana.ttf", font_size)
                else:
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
            except Exception:
                font = ImageFont.load_default()

            # Metin boyutunu ölç
            tmp_img = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
            tmp_draw = ImageDraw.Draw(tmp_img)
            try:
                left, top, right, bottom = tmp_draw.textbbox((0, 0), txt, font=font)
                text_w, text_h = right - left, bottom - top
            except Exception:
                text_w, text_h = tmp_draw.textsize(txt, font=font)

            # Şeffaf tuval oluştur ve metni çiz
            img = Image.new("RGBA", (max(1, text_w), max(1, text_h)), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), txt, font=font, fill=color)

            np_img = np.array(img)
            # RGBA'yı RGB'ye dönüştür (şeffaflık korunur)
            rgb_with_alpha = np_img
            
            txt_clip = ImageClip(rgb_with_alpha).with_duration(video_clip.duration)
            return txt_clip

        watermark_clip = build_text_clip(text, int(size_var.get()), FONT_COLOR).with_position(POSITION)

        final_clip = CompositeVideoClip([video_clip, watermark_clip])

        base_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(base_name)
        output_filename = f"{file_name}_filigranli{file_ext}"

        # Çıktı konumunu al (varsayılan Desktop)
        output_dir = output_dir_var.get().strip()
        if not output_dir:
            output_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        output_path = os.path.join(output_dir, output_filename)

        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )

        # UI güncellemeleri ana thread'de yapılmalı
        root.after(0, lambda: status_label.config(text="Processing completed. You can select a new video."))
        
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error!", f"An error occurred:\n{e}"))
        root.after(0, lambda: status_label.config(text="Error occurred. Please try again."))
    finally:
        root.after(0, lambda: progress_bar.stop())
        root.after(0, lambda: progress_bar.config(mode='determinate', value=100))
        root.after(0, lambda: progress_label.config(text="100%"))
        root.after(0, lambda: process_button.config(state='normal'))

def browse_output_directory():
    """Çıktı klasörü seçme penceresini açar."""
    directory = filedialog.askdirectory(title="Select Output Directory")
    if directory:
        output_dir_var.set(directory)

def browse_input_file():
    """Video dosyası seçme penceresini açar."""
    file_path = filedialog.askopenfilename(
        title="Select MP4 Video File to Add Watermark",
        filetypes=[("MP4 Video Files", "*.mp4")]
    )
    if file_path:
        input_file_var.set(file_path)

def select_file_and_add_watermark():
    """Video işleme işlemini başlatır."""
    # Kullanıcıdan watermark metnini al
    text = watermark_var.get().strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter a watermark text.")
        return

    # Video dosyası yolunu al
    file_path = input_file_var.get().strip()
    if not file_path:
        messagebox.showwarning("Warning", "Please select a video file.")
        return

    if not os.path.exists(file_path):
        messagebox.showerror("Error!", "Selected video file does not exist.")
        return

    status_label.config(text="Processing started, please wait...")
    progress_bar.config(mode='determinate', value=0)
    progress_label.config(text="0%")
    process_button.config(state='disabled')
    
    # Video işleme işlemini ayrı thread'de başlat
    thread = threading.Thread(target=process_video_thread, args=(file_path, text))
    thread.daemon = True
    thread.start()

# --- Grafik Arayüz (GUI) Kurulumu ---
root = tk.Tk()
root.title("Quick Watermark Tool")
root.geometry("500x320")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

# Watermark text input
watermark_var = tk.StringVar(value="©")
wm_frame = tk.Frame(main_frame)
wm_frame.pack(fill=tk.X, pady=(0, 10))

wm_label = tk.Label(wm_frame, text="Watermark Text:", font=("DM Sans", 10), width=15, anchor="w")
wm_label.pack(side=tk.LEFT)

wm_entry = tk.Entry(wm_frame, textvariable=watermark_var, font=("DM Sans", 10))
wm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

# Input video file
input_file_var = tk.StringVar()
input_frame = tk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

input_label = tk.Label(input_frame, text="Input Video:", font=("DM Sans", 10), width=15, anchor="w")
input_label.pack(side=tk.LEFT)

input_entry_frame = tk.Frame(input_frame)
input_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

input_entry = tk.Entry(input_entry_frame, textvariable=input_file_var, font=("DM Sans", 10))
input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

input_browse_button = tk.Button(
    input_entry_frame,
    text="",
    command=browse_input_file,
    font=("DM Sans", 9),
    bg="white",
    fg="black",
    padx=10,
    width=3
)
input_browse_button.pack(side=tk.RIGHT, padx=(10, 0))

# Output directory input
output_dir_var = tk.StringVar(value=os.path.join(os.path.expanduser('~'), 'Desktop'))
output_frame = tk.Frame(main_frame)
output_frame.pack(fill=tk.X, pady=(0, 10))

output_label = tk.Label(output_frame, text="Output Directory:", font=("DM Sans", 10), width=15, anchor="w")
output_label.pack(side=tk.LEFT)

output_entry_frame = tk.Frame(output_frame)
output_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

output_entry = tk.Entry(output_entry_frame, textvariable=output_dir_var, font=("DM Sans", 10))
output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

browse_button = tk.Button(
    output_entry_frame,
    text="",
    command=browse_output_directory,
    font=("DM Sans", 9),
    bg="white",
    fg="black",
    padx=10,
    width=3
)
browse_button.pack(side=tk.RIGHT, padx=(10, 0))

# Font and size selection
font_frame = tk.Frame(main_frame)
font_frame.pack(fill=tk.X, pady=(0, 10))

font_label = tk.Label(font_frame, text="Font:", font=("DM Sans", 10), width=15, anchor="w")
font_label.pack(side=tk.LEFT)

font_var = tk.StringVar(value="DM Sans")
font_combo = ttk.Combobox(font_frame, textvariable=font_var, font=("DM Sans", 10), width=12)
font_combo['values'] = ('DM Sans', 'Arial', 'Times New Roman', 'Calibri', 'Verdana')
font_combo.pack(side=tk.LEFT, padx=(10, 20))

size_label = tk.Label(font_frame, text="Size:", font=("DM Sans", 10))
size_label.pack(side=tk.LEFT)

size_var = tk.StringVar(value="20")
size_combo = ttk.Combobox(font_frame, textvariable=size_var, font=("DM Sans", 10), width=8)
size_combo['values'] = ('12', '16', '20', '24', '28', '32', '36', '40')
size_combo.pack(side=tk.LEFT, padx=(10, 0))

# Progress bar with percentage
progress_frame = tk.Frame(main_frame)
progress_frame.pack(fill=tk.X, pady=(0, 10))

progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=250)
progress_bar.pack(side=tk.LEFT)

progress_label = tk.Label(progress_frame, text="0%", font=("DM Sans", 10))
progress_label.pack(side=tk.LEFT, padx=(10, 0))

# Button
process_button = tk.Button(
    main_frame,
    text="Process Video",
    command=select_file_and_add_watermark,
    font=("DM Sans", 10),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=10
)
process_button.pack(pady=5)

# Status label
status_label = tk.Label(main_frame, text="Please select a video file.", font=("DM Sans", 10))
status_label.pack(pady=10)

root.mainloop()