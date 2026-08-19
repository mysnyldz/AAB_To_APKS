# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

Una aplicación GUI multiplataforma para convertir archivos AAB (Android App Bundle) al formato APKs usando bundletool, y firmar APKs para distribución en plataformas como Xiaomi GetApps.

**Idiomas:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## Características

### Conversión AAB a APKs
- Convierte archivos AAB al formato APKs usando bundletool de Google
- Soporte de firma basado en keystore
- Entrada de contraseña mediante campo de texto o archivo TXT
- Registro de salida en tiempo real

### Firma y renombrado de APK
- Firma archivos APK con keystore personalizado
- Renombrado automático a `com.xiaomi.getapps.signature.verification.apk`
- Compatible con los requisitos de envío de Xiaomi GetApps

### General
- Interfaz multiidioma (8 idiomas: EN, TR, DE, ES, FR, JA, ZH-CN, RU)
- Interfaz con pestañas
- Diálogos de selección de archivos
- Indicadores de progreso
- Multiplataforma (Windows, macOS, Linux)
- Detección automática de Android SDK
- Soporte de bundletool JAR integrado

---

## Requisitos

### Sistema
- **Python 3.10+** (para ejecutar desde el código fuente)
- **Java Runtime Environment (JRE)** (requerido por bundletool)
- **PySide6** (framework GUI Qt6) — los scripts de build lo instalan automáticamente, o manualmente: `pip install PySide6`

### Herramientas externas
- **bundletool** - Herramienta oficial de Google para conversión AAB
  - Descarga: https://github.com/google/bundletool/releases
  - Coloca `bundletool-all-x.x.x.jar` en la carpeta `tools/` o agrégalo al PATH
- **Android SDK build-tools** - Requerido para firma de APK
  - Incluido con Android Studio
  - Detectado automáticamente en todas las plataformas

---

## Instalación

### Opción A: Inicio rápido (Recomendado)

Haga doble clic en el lanzador para su plataforma (en la carpeta `scripts/`):

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

El lanzador automáticamente:
1. Crea un entorno virtual (`.venv`) en la primera ejecución
2. Instala las dependencias (PySide6 ~100 MB)
3. Inicia la aplicación

### Opción B: Ejecutar desde el código fuente

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### Opción C: Ejecutable independiente

#### Windows:
```bash
scripts/build_windows.bat
# Salida: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# Salida: dist/BundleToolSuite
```

> **Nota:** Crear ejecutables requiere [PyInstaller](https://pyinstaller.org/):
> ```bash
> pip install pyinstaller
> ```

### Limpieza / instalación limpia

Para eliminar `.venv`, `dist` y `build` (el código fuente se conserva):

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

Estas carpetas están en `.gitignore` y no se suben a GitHub.

---

## Uso

### AAB a APKs

1. Selecciona tu archivo `.aab`
2. Establece la ruta del archivo `.apks` de salida
3. Proporciona keystore, contraseña, alias de clave y contraseña de clave
4. Haz clic en **Convertir a APKs**

### Firma de APK

1. Selecciona tu archivo `.apk` fuente
2. Establece el directorio de salida
3. Proporciona keystore, contraseña, alias de clave y contraseña de clave
4. Haz clic en **Firmar y renombrar APK**
5. Salida: `com.xiaomi.getapps.signature.verification.apk`

### Contraseña desde archivo TXT

Ambas pestañas soportan leer contraseñas desde un archivo TXT. Marca la opción **"Leer desde TXT"** y selecciona tu archivo de contraseña.

---

## Estructura del proyecto

```
AAB-To-APKs/
├── main_window.py           # GUI principal PySide6
├── theme.py                 # Tokens de diseño y QSS
├── errors.py                # Clasificación de errores y mensajes
├── run.py                   # Lanzador de la aplicación
├── requirements.txt         # Dependencias Python (PySide6)
├── README.md                # Inglés
├── .gitignore
├── i18n/                    # Traducciones
│   ├── tr.json              # Turco
│   └── en.json              # Inglés
├── assets/                  # Iconos y fuentes
│   ├── icon.png             # Icono de la aplicación
│   └── icons/               # Iconos SVG
├── docs/                    # Documentación
│   ├── BUILD.md             # Instrucciones de compilación
│   ├── README_TR.md         # Turco
│   ├── README_DE.md         # Alemán
│   ├── README_ES.md         # Este archivo (Español)
│   ├── README_FR.md         # Francés
│   ├── README_JA.md         # Japonés
│   ├── README_ZH-CN.md      # Chino (simplificado)
│   └── README_RU.md         # Ruso
├── scripts/                 # Scripts de compilación y lanzadores
│   ├── build_simple.sh      # Compilación (macOS/Linux)
│   ├── build_macos.sh       # Compilación macOS .app
│   ├── build_windows.bat    # Compilación Windows .exe
│   ├── start_windows.bat    # Lanzador Windows
│   ├── start_macos.command  # Lanzador macOS
│   ├── start_linux.sh       # Lanzador Linux
│   ├── clean_windows.bat    # Eliminar .venv / dist / build (Windows)
│   └── clean.sh             # Eliminar .venv / dist / build (macOS/Linux)
├── tools/                   # Herramientas externas
│   └── bundletool-all-*.jar # Coloca bundletool JAR aquí
└── examples/                # Comandos CLI de ejemplo
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## Solución de problemas

### bundletool no encontrado
- Asegúrate de que bundletool esté en el PATH o en la carpeta `tools/`
- Verifica que Java esté instalado: `java -version`
- Prueba manual: `bundletool` o `java -jar tools/bundletool-all-x.x.x.jar`

### apksigner no encontrado
- Instala Android Studio o Android SDK
- Asegúrate de que build-tools esté instalado
- La app detecta automáticamente las rutas del SDK en Windows, macOS y Linux

### Errores de keystore
- Verifica el formato del archivo keystore (`.keystore` o `.jks`)
- Verifica la contraseña y el alias
- Asegúrate de que el archivo keystore no esté dañado

### Errores de archivo AAB
- Asegúrate de que el archivo AAB sea válido y no esté dañado
- Evita caracteres especiales o espacios en las rutas de archivos

---

## Soporte de plataforma

| Plataforma | Soporte    |
|------------|------------|
| Windows    | Completo   |
| macOS      | Completo   |
| Linux      | Completo   |

---

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](../LICENSE).

## Contribuir

Los reportes de errores y sugerencias son bienvenidos. Por favor abre un issue en GitHub.
