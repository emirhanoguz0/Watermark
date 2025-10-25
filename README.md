# Quick Watermark Tool

MP4 videolarına filigran eklemek için geliştirilmiş basit ve kullanıcı dostu bir uygulama.

## Özellikler

- **Kolay Kullanım**: Sürükle-bırak ile video seçimi
- **Özelleştirilebilir Filigran**: Metin, font ve boyut seçimi
- **Çıktı Kontrolü**: İstediğiniz klasöre kaydetme
- **Gerçek Zamanlı Progress**: İşlem durumu takibi
- **Threading**: UI donmadan video işleme
- **Tek Dosya**: Kurulum gerektirmez

## Kullanım

1. **Watermark Text**: Filigran metnini girin
2. **Input Video**: Video dosyasını seçin (Browse ile)
3. **Output Directory**: Çıktı klasörünü belirleyin
4. **Font & Size**: Font ve boyut seçin
5. **Process Video**: İşlemi başlatın

## Teknik Detaylar

- **Python**: 3.12
- **GUI**: Tkinter
- **Video İşleme**: MoviePy
- **Font İşleme**: Pillow (PIL)
- **Derleme**: PyInstaller

## Gereksinimler

- Windows 10/11
- FFmpeg (otomatik indirilir)

## Kurulum

### Geliştirici Kurulumu
```bash
git clone <repo-url>
cd Watermark
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python adwwafwgv.py
```

### Son Kullanıcı
`dist/Watermark.exe` dosyasını çalıştırın. Kurulum gerekmez.

## Desteklenen Formatlar

- **Giriş**: MP4
- **Çıkış**: MP4 (H.264/AAC)

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
