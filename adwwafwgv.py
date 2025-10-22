import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
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

def select_file_and_add_watermark():
    """Dosya seçme penceresini açar ve filigran ekleme işlemini başlatır."""
    # Kullanıcıdan watermark metnini al
    text = watermark_var.get().strip()
    if not text:
        messagebox.showwarning("Uyarı", "Lütfen bir filigran metni girin.")
        return

    file_path = filedialog.askopenfilename(
        title="Filigran Eklenecek MP4 Dosyasını Seçin",
        filetypes=[("MP4 Video Dosyaları", "*.mp4")]
    )

    if not file_path:
        status_label.config(text="İşlem iptal edildi.")
        return

    status_label.config(text="İşlem başladı, lütfen bekleyin...")
    root.update_idletasks()

    try:
        video_clip = VideoFileClip(file_path)

        # PIL ile şeffaf metin görseli üret (ImageMagick bağımlılığı yok)
        def build_text_clip(txt: str, font_size: int, color: str) -> ImageClip:
            # Font yükle (Windows varsayılan arial, yoksa fallback)
            font: ImageFont.FreeTypeFont | ImageFont.ImageFont
            try:
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
            rgb = np_img[..., :3]
            alpha = np_img[..., 3] / 255.0

            txt_clip = ImageClip(rgb).set_duration(video_clip.duration)
            mask_clip = ImageClip(alpha, ismask=True).set_duration(video_clip.duration)
            txt_clip = txt_clip.set_mask(mask_clip)
            return txt_clip

        watermark_clip = build_text_clip(text, FONT_SIZE, FONT_COLOR).set_position(POSITION)

        final_clip = CompositeVideoClip([video_clip, watermark_clip])

        base_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(base_name)
        output_filename = f"{file_name}_filigranli{file_ext}"

        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_path = os.path.join(desktop_path, output_filename)

        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )

        messagebox.showinfo(
            "Başarılı!",
            f"Video başarıyla işlendi!\n\nYeni dosyanız Masaüstüne kaydedildi:\n{output_filename}"
        )
        status_label.config(text="İşlem tamamlandı. Yeni video seçebilirsiniz.")
    except Exception as e:
        messagebox.showerror("Hata!", f"Bir hata oluştu:\n{e}")
        status_label.config(text="Hata oluştu. Lütfen tekrar deneyin.")

# --- Grafik Arayüz (GUI) Kurulumu ---
root = tk.Tk()
root.title("Hızlı Filigran Ekleme Aracı")
root.geometry("500x220")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

# Filigran metni girişi
watermark_var = tk.StringVar(value="© Benim Filigranım")
wm_label = tk.Label(main_frame, text="Filigran Metni:", font=("Helvetica", 10))
wm_label.pack(anchor="w")
wm_entry = tk.Entry(main_frame, textvariable=watermark_var, font=("Helvetica", 12))
wm_entry.pack(fill=tk.X, pady=(0, 10))

# Buton
process_button = tk.Button(
    main_frame,
    text="MP4 Video Seç ve Filigran Ekle",
    command=select_file_and_add_watermark,
    font=("Helvetica", 12),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=10
)
process_button.pack(pady=5)

# Durum etiketi
status_label = tk.Label(main_frame, text="Lütfen bir video dosyası seçin.", font=("Helvetica", 10))
status_label.pack(pady=10)

root.mainloop()