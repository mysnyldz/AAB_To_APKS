# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

Кроссплатформенное GUI-приложение для конвертации файлов AAB (Android App Bundle) в формат APKs с помощью bundletool и подписания APK для распространения на платформах, таких как Xiaomi GetApps.

**Языки:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## Возможности

### Конвертация AAB в APKs
- Конвертация файлов AAB в формат APKs с помощью bundletool от Google
- Поддержка подписания на основе хранилища ключей
- Ввод пароля через текстовое поле или TXT-файл
- Журналирование вывода в реальном времени

### Подписание и переименование APK
- Подписание файлов APK с пользовательским хранилищем ключей
- Автоматическое переименование в `com.xiaomi.getapps.signature.verification.apk`
- Совместимость с требованиями подачи Xiaomi GetApps

### Общее
- Многоязычный интерфейс (8 языков: EN, TR, DE, ES, FR, JA, ZH-CN, RU)
- Интерфейс с вкладками
- Диалоги выбора файлов
- Индикаторы прогресса
- Кроссплатформенность (Windows, macOS, Linux)
- Автоматическое обнаружение Android SDK
- Поддержка встроенного bundletool JAR

---

## Требования

### Система
- **Python 3.10+** (для запуска из исходного кода)
- **Java Runtime Environment (JRE)** (требуется для bundletool)
- **PySide6** (Qt6 GUI-фреймворк) — автоматически устанавливается скриптами сборки, или вручную: `pip install PySide6`

### Внешние инструменты
- **bundletool** - Официальный инструмент Google для конвертации AAB
  - Скачать: https://github.com/google/bundletool/releases
  - Поместите `bundletool-all-x.x.x.jar` в папку `tools/` или добавьте в PATH
- **Android SDK build-tools** - Требуется для подписания APK
  - Входит в состав Android Studio
  - Автоматически обнаруживается на всех платформах

---

## Установка

### Вариант A: Быстрый старт (Рекомендуется)

Дважды щёлкните по лаунчеру для вашей платформы (в папке `scripts/`):

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

Лаунчер автоматически:
1. создаёт виртуальное окружение (`.venv`) при первом запуске
2. устанавливает зависимости (PySide6 ~100 МБ)
3. запускает приложение

### Вариант B: Запуск из исходного кода

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### Вариант C: Автономный исполняемый файл

#### Windows:
```bash
scripts/build_windows.bat
# Вывод: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# Вывод: dist/BundleToolSuite
```

> **Примечание:** Для создания исполняемых файлов требуется [PyInstaller](https://pyinstaller.org/):
> ```bash
> pip install pyinstaller
> ```

### Очистка / чистая установка

Чтобы удалить `.venv`, `dist` и `build` (исходный код сохраняется):

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

Эти папки указаны в `.gitignore` и не попадают на GitHub.

---

## Использование

### AAB в APKs

1. Выберите файл `.aab`
2. Укажите путь выходного файла `.apks`
3. Введите хранилище ключей, пароль, псевдоним ключа и пароль ключа
4. Нажмите **Конвертировать в APKs**

### Подписание APK

1. Выберите исходный файл `.apk`
2. Укажите выходную папку
3. Введите хранилище ключей, пароль, псевдоним ключа и пароль ключа
4. Нажмите **Подписать и переименовать APK**
5. Результат: `com.xiaomi.getapps.signature.verification.apk`

### Пароль из TXT-файла

Обе вкладки поддерживают чтение паролей из TXT-файла. Отметьте опцию **"Читать из TXT"** и выберите файл пароля.

---

## Структура проекта

```
AAB-To-APKs/
├── main_window.py           # Основной PySide6 GUI
├── theme.py                 # Токены дизайна и QSS
├── errors.py                # Классификация ошибок и сообщения
├── run.py                   # Запуск приложения
├── requirements.txt         # Зависимости Python (PySide6)
├── README.md                # Английский
├── .gitignore
├── i18n/                    # Переводы
│   ├── tr.json              # Турецкий
│   └── en.json              # Английский
├── assets/                  # Иконки и шрифты
│   ├── icon.png             # Иконка приложения
│   └── icons/               # SVG-иконки
├── docs/                    # Документация
│   ├── BUILD.md             # Инструкции по сборке
│   ├── README_TR.md         # Турецкий
│   ├── README_DE.md         # Немецкий
│   ├── README_ES.md         # Испанский
│   ├── README_FR.md         # Французский
│   ├── README_JA.md         # Японский
│   ├── README_ZH-CN.md      # Китайский (упрощённый)
│   └── README_RU.md         # Этот файл (Русский)
├── scripts/                 # Скрипты сборки и запуска
│   ├── build_simple.sh      # Сборка (macOS/Linux)
│   ├── build_macos.sh       # Сборка macOS .app
│   ├── build_windows.bat    # Сборка Windows .exe
│   ├── start_windows.bat    # Лаунчер Windows
│   ├── start_macos.command  # Лаунчер macOS
│   ├── start_linux.sh       # Лаунчер Linux
│   ├── clean_windows.bat    # Удалить .venv / dist / build (Windows)
│   └── clean.sh             # Удалить .venv / dist / build (macOS/Linux)
├── tools/                   # Внешние инструменты
│   └── bundletool-all-*.jar # Поместите bundletool JAR сюда
└── examples/                # Примеры CLI-команд
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## Устранение неполадок

### bundletool не найден
- Убедитесь, что bundletool находится в PATH или в папке `tools/`
- Проверьте установку Java: `java -version`
- Ручная проверка: `bundletool` или `java -jar tools/bundletool-all-x.x.x.jar`

### apksigner не найден
- Установите Android Studio или Android SDK
- Убедитесь, что build-tools установлены
- Приложение автоматически обнаруживает пути SDK на Windows, macOS и Linux

### Ошибки хранилища ключей
- Проверьте формат файла хранилища ключей (`.keystore` или `.jks`)
- Перепроверьте пароль и псевдоним
- Убедитесь, что файл хранилища ключей не повреждён

### Ошибки файла AAB
- Убедитесь, что файл AAB действителен и не повреждён
- Избегайте специальных символов и пробелов в путях к файлам

---

## Поддержка платформ

| Платформа | Поддержка   |
|-----------|-------------|
| Windows   | Полная      |
| macOS     | Полная      |
| Linux     | Полная      |

---

## Лицензия

Этот проект распространяется под [лицензией MIT](../LICENSE).

## Вклад

Сообщения об ошибках и предложения приветствуются. Пожалуйста, откройте issue на GitHub.
