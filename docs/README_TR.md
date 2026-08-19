# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

AAB (Android App Bundle) dosyalarını bundletool kullanarak APKs formatına dönüştüren ve Xiaomi GetApps gibi platformlarda dağıtım için APK imzalayan çapraz platformlu bir GUI uygulaması.

**Diller:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## Özellikler

### AAB'den APKs'e Dönüştürme
- Google'ın bundletool aracı ile AAB dosyalarını APKs formatına dönüştürme
- Keystore tabanlı imzalama desteği
- Metin alanı veya TXT dosyasından şifre girişi
- Gerçek zamanlı çıktı günlüğü

### APK İmzalama ve Yeniden Adlandırma
- Özel keystore ile APK dosyalarını imzalama
- Otomatik olarak `com.xiaomi.getapps.signature.verification.apk` olarak yeniden adlandırma
- Xiaomi GetApps gönderim gereksinimleriyle uyumlu

### Genel
- Çok dilli arayüz (8 dil: EN, TR, DE, ES, FR, JA, ZH-CN, RU)
- Sekmeli arayüz
- Dosya tarayıcı diyalogları
- İlerleme göstergeleri
- Çapraz platform (Windows, macOS, Linux)
- Otomatik Android SDK algılama
- Dahili bundletool JAR desteği

---

## Gereksinimler

### Sistem
- **Python 3.10+** (kaynaktan çalıştırmak için)
- **Java Runtime Environment (JRE)** (bundletool için gerekli)
- **PySide6** (Qt6 GUI framework) — build scriptleri otomatik kurar, veya manuel: `pip install PySide6`

### Harici Araçlar
- **bundletool** - Google'ın resmi AAB dönüştürme aracı
  - İndirme: https://github.com/google/bundletool/releases
  - `bundletool-all-x.x.x.jar` dosyasını `tools/` klasörüne koyun veya PATH'e ekleyin
- **Android SDK build-tools** - APK imzalama için gerekli
  - Android Studio ile birlikte gelir
  - Tüm platformlarda otomatik olarak algılanır

---

## Kurulum

### Seçenek A: Hızlı Başlangıç (Önerilen)

`scripts/` klasöründeki, platformunuza uygun başlatıcıya çift tıklayın:

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

Başlatıcı otomatik olarak:
1. İlk çalıştırmada sanal ortam (`.venv`) oluşturur
2. Bağımlılıkları kurar (PySide6 ~100 MB)
3. Uygulamayı başlatır

### Seçenek B: Kaynaktan Çalıştırma

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### Seçenek C: Bağımsız Çalıştırılabilir Dosya

#### Windows:
```bash
scripts/build_windows.bat
# Çıktı: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# Çıktı: dist/BundleToolSuite
```

> **Not:** Çalıştırılabilir dosya oluşturmak için [PyInstaller](https://pyinstaller.org/) gerekir:
> ```bash
> pip install pyinstaller
> ```

### Temiz kurulum

`.venv`, `dist` ve `build` klasörlerini silmek için (kaynak kod durur):

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

Bu klasörler `.gitignore` içinde olduğu için GitHub'a gönderilmez.

---

## Kullanım

### AAB'den APKs'e

1. `.aab` dosyanızı seçin
2. Çıktı `.apks` dosya yolunu belirleyin
3. Keystore dosyası, şifre, key alias ve key şifresini girin
4. **APKs'e Dönüştür** butonuna tıklayın

### APK İmzalama

1. Kaynak `.apk` dosyanızı seçin
2. Çıktı klasörünü belirleyin
3. Keystore dosyası, şifre, key alias ve key şifresini girin
4. **APK'yı İmzala ve Yeniden Adlandır** butonuna tıklayın
5. Çıktı: `com.xiaomi.getapps.signature.verification.apk`

### TXT Dosyasından Şifre

Her iki sekme de şifreleri doğrudan yazmak yerine TXT dosyasından okumayı destekler. **"TXT'den oku"** seçeneğini işaretleyin ve şifre dosyanızı seçin.

---

## Proje Yapısı

```
AAB-To-APKs/
├── main_window.py           # Ana PySide6 GUI uygulaması
├── theme.py                 # Tasarım token'ları ve QSS
├── errors.py                # Hata sınıflandırma ve kullanıcı mesajları
├── run.py                   # Uygulama başlatıcı
├── requirements.txt         # Python bağımlılıkları (PySide6)
├── README.md                # İngilizce README
├── .gitignore
├── i18n/                    # Çeviriler
│   ├── tr.json              # Türkçe
│   └── en.json              # İngilizce
├── assets/                  # İkonlar ve fontlar
│   ├── icon.png             # Uygulama ikonu
│   └── icons/               # SVG ikonlar
├── docs/                    # Belgeler
│   ├── BUILD.md             # Derleme talimatları
│   ├── README_TR.md         # Bu dosya (Türkçe)
│   ├── README_DE.md         # Almanca
│   ├── README_ES.md         # İspanyolca
│   ├── README_FR.md         # Fransızca
│   ├── README_JA.md         # Japonca
│   ├── README_ZH-CN.md      # Çince (Basitleştirilmiş)
│   └── README_RU.md         # Rusça
├── scripts/                 # Derleme ve başlatıcı scriptleri
│   ├── build_simple.sh      # Derleme (macOS/Linux)
│   ├── build_macos.sh       # macOS .app derleme
│   ├── build_windows.bat    # Windows .exe derleme
│   ├── start_windows.bat    # Windows başlatıcı
│   ├── start_macos.command  # macOS başlatıcı
│   ├── start_linux.sh       # Linux başlatıcı
│   ├── clean_windows.bat    # .venv / dist / build temizle (Windows)
│   └── clean.sh             # .venv / dist / build temizle (macOS/Linux)
├── tools/                   # Harici araçlar
│   └── bundletool-all-*.jar # bundletool JAR buraya
└── examples/                # Örnek CLI komutları
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## Sorun Giderme

### bundletool bulunamadı
- bundletool'un PATH'de veya `tools/` klasöründe olduğundan emin olun
- Java'nın yüklü olduğunu doğrulayın: `java -version`
- Manuel test: `bundletool` veya `java -jar tools/bundletool-all-x.x.x.jar`

### apksigner bulunamadı
- Android Studio veya Android SDK'yı yükleyin
- build-tools'un yüklü olduğundan emin olun
- Uygulama, Windows, macOS ve Linux'ta SDK yollarını otomatik algılar

### Keystore hataları
- Keystore dosya formatını doğrulayın (`.keystore` veya `.jks`)
- Şifre ve alias bilgilerini kontrol edin
- Keystore dosyasının bozuk olmadığından emin olun

### AAB dosyası hataları
- AAB dosyasının geçerli ve bozuk olmadığından emin olun
- Dosya yollarında özel karakter veya boşluk kullanmaktan kaçının

---

## Teknik Detaylar

Uygulama aşağıdaki komutları çalıştırır:

**AAB'den APKs'e:**
```bash
bundletool build-apks \
  --bundle=/yol/app.aab \
  --output=/yol/app.apks \
  --ks=/yol/keystore.keystore \
  --ks-pass=pass:SIFRE \
  --ks-key-alias=ALIAS \
  --key-pass=pass:SIFRE
```

**APK İmzalama:**
```bash
apksigner sign \
  --ks /yol/keystore.keystore \
  --ks-pass pass:SIFRE \
  --ks-key-alias ALIAS \
  --key-pass pass:SIFRE \
  --out singer.apk \
  kaynak.apk
```

---

## Platform Desteği

| Platform | Destek  |
|----------|---------|
| Windows  | Tam     |
| macOS    | Tam     |
| Linux    | Tam     |

---

## Lisans

Bu proje [MIT Lisansı](../LICENSE) altında lisanslanmıştır.

## Katkıda Bulunma

Hata bildirimleri ve önerileriniz için GitHub'da issue açabilirsiniz.
