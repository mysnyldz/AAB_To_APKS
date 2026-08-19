#!/usr/bin/env python3
import sys
import os
import platform
from pathlib import Path


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


def check_python_version():
    if sys.version_info < (3, 6):
        print(f"ERROR: Python 3.6+ required. Current: {sys.version}")
        return False
    return True


def check_pyside6():
    try:
        import PySide6
        return True
    except ImportError:
        print("ERROR: PySide6 not found!")
        print("Install with: pip install PySide6")
        return False


def check_bundletool():
    import shutil
    if shutil.which("bundletool"):
        return True

    app_dir = get_app_dir()
    bundletool_dir = os.path.join(app_dir, "tools")
    if os.path.exists(bundletool_dir):
        for f in os.listdir(bundletool_dir):
            if f.endswith(".jar"):
                return True

    print("WARNING: bundletool not found!")
    print("1. Download from: https://github.com/google/bundletool/releases")
    print("2. Place bundletool-all-x.x.x.jar in tools/ folder or add to PATH")
    return False


def get_android_sdk_paths():
    system = platform.system()
    possible_paths = []

    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            possible_paths.append(os.path.join(local_app_data, "Android", "Sdk", "build-tools"))
        possible_paths.append(os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Android", "Sdk", "build-tools"))
    elif system == "Darwin":
        possible_paths.append(os.path.expanduser("~/Library/Android/sdk/build-tools"))
    else:
        possible_paths.append(os.path.expanduser("~/Android/Sdk/build-tools"))
        possible_paths.append(os.path.expanduser("~/android-sdk/build-tools"))

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def check_android_sdk():
    build_tools_base = get_android_sdk_paths()

    if build_tools_base:
        versions = [v for v in os.listdir(build_tools_base) if os.path.isdir(os.path.join(build_tools_base, v))]
        if versions:
            print(f"Android SDK build-tools found. Versions: {', '.join(sorted(versions))}")
            return True

    print("WARNING: Android SDK build-tools not found!")
    print("APK Signer feature requires Android SDK.")
    return False


def main():
    print("Starting Bundle Tool Suite...")

    if not check_python_version():
        sys.exit(1)

    if not check_pyside6():
        sys.exit(1)

    check_bundletool()
    check_android_sdk()

    try:
        from main_window import MainWindow
        from theme import stylesheet
        from PySide6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        app.setStyleSheet(stylesheet())
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    except ImportError as e:
        print(f"ERROR: Could not import application module: {e}")
        print("Make sure PySide6 is installed: pip install PySide6")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Application failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
