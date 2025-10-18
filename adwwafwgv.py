import tkinter as tk
from tkinter import filedialog, messagebox
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# --- Filigran Ayarları (Burayı Değiştirebilirsiniz) ---
WATERMARK_TEXT = "airfryerhost.exe"  # Ekranda görünecek metin
FONT_SIZE = 20  # Yazı tipi boyutu
FONT_COLOR = 'white'  # Yazı tipi rengi
POSITION = ('center', 'center')


# ---------------------------------------------------------

def select_file_and_add_watermark():
    """Dosya seçme penceresini açar ve filigran ekleme işlemini başlatır."""

    # Sadece mp4 dosyalarını göstermek için dosya türlerini filtrele
    file_path = filedialog.askopenfilename(
        title="Filigran Eklenecek MP4 Dosyasını Seçin",
        filetypes=[("MP4 Video Dosyaları", "*.mp4")]
    )

    # Kullanıcı bir dosya seçtiyse devam et
    if not file_path:
        # Kullanıcı pencereyi kapattıysa veya "İptal"e bastıysa hiçbir şey yapma
        status_label.config(text="İşlem iptal edildi.")
        return

    status_label.config(text="İşlem başladı, lütfen bekleyin...")
    root.update_idletasks()  # Arayüzün güncellenmesini sağla

    try:
        # 1. Video dosyasını yükle
        video_clip = VideoFileClip(file_path)

        # 2. Filigran metnini oluştur
        watermark_clip = TextClip(
            txt=WATERMARK_TEXT,
            fontsize=FONT_SIZE,
            color=FONT_COLOR,
            font='Arial'  # Bilgisayarınızda yüklü olan bir fontu seçebilirsiniz
        )

        # Filigranın süresini videonun süresiyle aynı yap ve konumunu ayarla
        watermark_clip = watermark_clip.set_duration(video_clip.duration).set_position(POSITION)

        # 3. Videoyu ve filigranı birleştir
        final_clip = CompositeVideoClip([video_clip, watermark_clip])

        # 4. Çıktı dosyasının yolunu ve adını belirle
        # Dosya adının sonuna "_filigranli" ekle
        base_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(base_name)
        output_filename = f"{file_name}_filigranli{file_ext}"

        # Masaüstü yolunu bul
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_path = os.path.join(desktop_path, output_filename)

        # 5. Yeni videoyu kaydet
        # codec="libx264" ve audio_codec="aac" en yaygın ve uyumlu formatlardır.
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )

        # İşlem tamamlandığında kullanıcıyı bilgilendir
        messagebox.showinfo("Başarılı!",
                            f"Video başarıyla işlendi!\n\nYeni dosyanız Masaüstüne kaydedildi:\n{output_filename}")
        status_label.config(text="İşlem tamamlandı. Yeni video seçebilirsiniz.")

    except Exception as e:
        messagebox.showerror("Hata!", f"Bir hata oluştu:\n{e}")
        status_label.config(text="Hata oluştu. Lütfen tekrar deneyin.")


# --- Grafik Arayüz (GUI) Kurulumu ---
root = tk.Tk()
root.title("Hızlı Filigran Ekleme Aracı")
root.geometry("450x150")  # Pencere boyutu

# Ana çerçeve
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

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

# Pencereyi çalıştır
root.mainloop()