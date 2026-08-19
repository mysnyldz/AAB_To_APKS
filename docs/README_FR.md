# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

Une application GUI multiplateforme pour convertir les fichiers AAB (Android App Bundle) au format APKs en utilisant bundletool, et signer les APKs pour la distribution sur des plateformes comme Xiaomi GetApps.

**Langues:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## Fonctionnalités

### Conversion AAB vers APKs
- Convertit les fichiers AAB au format APKs en utilisant bundletool de Google
- Support de signature basé sur le keystore
- Saisie de mot de passe via champ texte ou fichier TXT
- Journalisation de sortie en temps réel

### Signature et renommage APK
- Signe les fichiers APK avec un keystore personnalisé
- Renommage automatique en `com.xiaomi.getapps.signature.verification.apk`
- Compatible avec les exigences de soumission Xiaomi GetApps

### Général
- Interface multilingue (8 langues: EN, TR, DE, ES, FR, JA, ZH-CN, RU)
- Interface à onglets
- Boîtes de dialogue de sélection de fichiers
- Indicateurs de progression
- Multiplateforme (Windows, macOS, Linux)
- Détection automatique du SDK Android
- Support JAR bundletool intégré

---

## Prérequis

### Système
- **Python 3.10+** (pour exécuter depuis le code source)
- **Java Runtime Environment (JRE)** (requis par bundletool)
- **PySide6** (framework GUI Qt6) — installé automatiquement par les scripts de build, ou manuellement : `pip install PySide6`

### Outils externes
- **bundletool** - Outil officiel de Google pour la conversion AAB
  - Téléchargement: https://github.com/google/bundletool/releases
  - Placez `bundletool-all-x.x.x.jar` dans le dossier `tools/` ou ajoutez-le au PATH
- **Android SDK build-tools** - Requis pour la signature APK
  - Inclus avec Android Studio
  - Détecté automatiquement sur toutes les plateformes

---

## Installation

### Option A: Démarrage rapide (Recommandé)

Double-cliquez sur le lanceur pour votre plateforme (dans le dossier `scripts/`) :

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

Le lanceur :
1. crée un environnement virtuel (`.venv`) au premier lancement
2. installe les dépendances (PySide6 ~100 MB)
3. démarre l'application

### Option B: Exécuter depuis le code source

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### Option C: Exécutable autonome

#### Windows:
```bash
scripts/build_windows.bat
# Sortie: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# Sortie: dist/BundleToolSuite
```

> **Note:** La création d'exécutables nécessite [PyInstaller](https://pyinstaller.org/):
> ```bash
> pip install pyinstaller
> ```

### Nettoyage / installation propre

Pour supprimer `.venv`, `dist` et `build` (le code source est conservé) :

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

Ces dossiers sont dans `.gitignore` et ne sont pas envoyés sur GitHub.

---

## Utilisation

### AAB vers APKs

1. Sélectionnez votre fichier `.aab`
2. Définissez le chemin du fichier `.apks` de sortie
3. Fournissez le keystore, le mot de passe, l'alias de clé et le mot de passe de clé
4. Cliquez sur **Convertir en APKs**

### Signature APK

1. Sélectionnez votre fichier `.apk` source
2. Définissez le répertoire de sortie
3. Fournissez le keystore, le mot de passe, l'alias de clé et le mot de passe de clé
4. Cliquez sur **Signer et renommer APK**
5. Sortie: `com.xiaomi.getapps.signature.verification.apk`

### Mot de passe depuis un fichier TXT

Les deux onglets supportent la lecture des mots de passe depuis un fichier TXT. Cochez l'option **"Lire depuis TXT"** et sélectionnez votre fichier de mot de passe.

---

## Structure du projet

```
AAB-To-APKs/
├── main_window.py           # Interface PySide6 principale
├── theme.py                 # Tokens de design et QSS
├── errors.py                # Classification des erreurs et messages
├── run.py                   # Lanceur d'application
├── requirements.txt         # Dépendances Python (PySide6)
├── README.md                # Anglais
├── .gitignore
├── i18n/                    # Traductions
│   ├── tr.json              # Turc
│   └── en.json              # Anglais
├── assets/                  # Icônes et polices
│   ├── icon.png             # Icône de l'application
│   └── icons/               # Icônes SVG
├── docs/                    # Documentation
│   ├── BUILD.md             # Instructions de compilation
│   ├── README_TR.md         # Turc
│   ├── README_DE.md         # Allemand
│   ├── README_ES.md         # Espagnol
│   ├── README_FR.md         # Ce fichier (Français)
│   ├── README_JA.md         # Japonais
│   ├── README_ZH-CN.md      # Chinois (simplifié)
│   └── README_RU.md         # Russe
├── scripts/                 # Scripts de compilation et lanceurs
│   ├── build_simple.sh      # Compilation (macOS/Linux)
│   ├── build_macos.sh       # Compilation macOS .app
│   ├── build_windows.bat    # Compilation Windows .exe
│   ├── start_windows.bat    # Lanceur Windows
│   ├── start_macos.command  # Lanceur macOS
│   ├── start_linux.sh       # Lanceur Linux
│   ├── clean_windows.bat    # Supprimer .venv / dist / build (Windows)
│   └── clean.sh             # Supprimer .venv / dist / build (macOS/Linux)
├── tools/                   # Outils externes
│   └── bundletool-all-*.jar # Placez le JAR bundletool ici
└── examples/                # Commandes CLI d'exemple
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## Dépannage

### bundletool introuvable
- Assurez-vous que bundletool est dans le PATH ou dans le dossier `tools/`
- Vérifiez que Java est installé: `java -version`
- Test manuel: `bundletool` ou `java -jar tools/bundletool-all-x.x.x.jar`

### apksigner introuvable
- Installez Android Studio ou le SDK Android
- Assurez-vous que build-tools est installé
- L'application détecte automatiquement les chemins SDK sur Windows, macOS et Linux

### Erreurs de keystore
- Vérifiez le format du fichier keystore (`.keystore` ou `.jks`)
- Vérifiez le mot de passe et l'alias
- Assurez-vous que le fichier keystore n'est pas corrompu

### Erreurs de fichier AAB
- Assurez-vous que le fichier AAB est valide et non corrompu
- Évitez les caractères spéciaux ou les espaces dans les chemins de fichiers

---

## Support de plateforme

| Plateforme | Support    |
|------------|------------|
| Windows    | Complet    |
| macOS      | Complet    |
| Linux      | Complet    |

---

## Licence

Ce projet a été développé à des fins éducatives.

## Contribuer

Les rapports de bugs et suggestions sont les bienvenus. Veuillez ouvrir un issue sur GitHub.
