"""Bundle Tool Suite — PySide6 arayüzü."""
import json
import os
import platform
import shutil
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QProcess, QSettings, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QDialog, QFileDialog, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget,
)

import errors
from theme import TOKENS, stylesheet


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


APP_DIR = get_app_dir()
ICON_PATH = APP_DIR / "assets" / "icon.png"


class I18n:
    def __init__(self, lang="tr"):
        self.set_lang(lang)

    def set_lang(self, lang):
        self.lang = lang
        path = APP_DIR / "i18n" / f"{lang}.json"
        self.strings = json.loads(path.read_text(encoding="utf-8"))

    def __call__(self, key, **kw):
        text = self.strings.get(key, key)
        return text.format(**kw) if kw else text


t = I18n()


def row(*widgets, spacing=8, margins=(0, 0, 0, 0)):
    w = QWidget()
    lay = QHBoxLayout(w)
    lay.setContentsMargins(*margins)
    lay.setSpacing(spacing)
    for x in widgets:
        lay.addWidget(x) if isinstance(x, QWidget) else lay.addLayout(x)
    return w, lay


def col(parent=None, spacing=14, margins=(0, 0, 0, 0)):
    lay = QVBoxLayout(parent)
    lay.setContentsMargins(*margins)
    lay.setSpacing(spacing)
    return lay


def label(text, obj="label"):
    lbl = QLabel(text)
    lbl.setObjectName(obj)
    return lbl


class Field(QWidget):
    def __init__(self, key, placeholder="", browse=None, password=False, browse_callback=None, from_file=False):
        super().__init__()
        self.browse_callback = browse_callback
        self._password = password
        self._placeholder = placeholder
        self._txt_path = ""

        lay = col(self, spacing=5)
        self.head, head_lay = row(spacing=8)
        self.label = label(t(key))
        head_lay.addWidget(self.label)
        head_lay.addStretch(1)

        self.from_file_cb = None
        if from_file:
            self.from_file_cb = QCheckBox(t("field.from_txt"))
            self.from_file_cb.setObjectName("fieldToggle")
            self.from_file_cb.toggled.connect(self._on_from_file_toggled)
            head_lay.addWidget(self.from_file_cb)

        lay.addWidget(self.head)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        if password:
            self.input.setEchoMode(QLineEdit.Password)
        line, line_lay = row(spacing=8)
        line_lay.addWidget(self.input, 1)

        self.browse_btn = None
        if browse or from_file:
            self.browse_btn = QPushButton(t("action.browse"))
            self.browse_btn.clicked.connect(self._on_browse)
            line_lay.addWidget(self.browse_btn)
            if from_file and not browse:
                self.browse_btn.hide()

        self.eye_btn = None
        if password:
            self.eye_btn = QPushButton("👁")
            self.eye_btn.setToolTip(t("action.show_pass"))
            self.eye_btn.setFixedWidth(38)
            self.eye_btn.clicked.connect(self.toggle_echo)
            line_lay.addWidget(self.eye_btn)
        lay.addWidget(line)

        self.error = label("", "fieldError")
        self.error.hide()
        lay.addWidget(self.error)
        self.input.textChanged.connect(lambda _: self.clear_error())

    def _on_from_file_toggled(self, checked):
        self.clear_error()
        if checked:
            self.input.setEchoMode(QLineEdit.Normal)
            self.input.setReadOnly(True)
            self.input.setPlaceholderText(t("field.pass_txt.ph"))
            self.input.setText(self._txt_path)
            if self.browse_btn:
                self.browse_btn.show()
            if self.eye_btn:
                self.eye_btn.hide()
        else:
            self.input.setReadOnly(False)
            if self._password:
                self.input.setEchoMode(QLineEdit.Password)
            self.input.setPlaceholderText(self._placeholder)
            self.input.clear()
            if self.browse_btn:
                self.browse_btn.hide()
            if self.eye_btn:
                self.eye_btn.show()

    def _on_browse(self):
        if self.from_file_cb and self.from_file_cb.isChecked():
            path, _ = QFileDialog.getOpenFileName(self, "", "", "Text (*.txt)")
            if path:
                self._txt_path = path
                self.input.setText(path)
                self.clear_error()
            return
        if self.browse_callback:
            self.browse_callback()

    def toggle_echo(self):
        mode = QLineEdit.Normal if self.input.echoMode() == QLineEdit.Password else QLineEdit.Password
        self.input.setEchoMode(mode)

    def set_error(self, message):
        self.input.setProperty("state", "error")
        self.input.style().unpolish(self.input)
        self.input.style().polish(self.input)
        self.error.setText(message)
        self.error.show()

    def clear_error(self):
        if self.input.property("state") == "error":
            self.input.setProperty("state", "")
            self.input.style().unpolish(self.input)
            self.input.style().polish(self.input)
        self.error.hide()

    def value(self):
        return self.input.text().strip()

    def resolve_password(self):
        if self.from_file_cb and self.from_file_cb.isChecked():
            path = self._txt_path.strip()
            if not path:
                return False, "", t("valid.pass_file")
            file_path = Path(path)
            if not file_path.is_file():
                return False, "", t("valid.pass_file")
            try:
                raw = file_path.read_text(encoding="utf-8-sig")
            except OSError:
                return False, "", t("valid.pass_file_read")
            lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
            if not lines:
                return False, "", t("valid.pass_file_empty")
            return True, lines[0], ""
        return True, self.input.text().strip(), ""

    def reset(self):
        self._txt_path = ""
        if self.from_file_cb and self.from_file_cb.isChecked():
            self.from_file_cb.setChecked(False)
        else:
            self.input.clear()
        self.clear_error()


class DropZone(QFrame):
    picked = Signal(str)

    def __init__(self, ext, title_key, hint_key):
        super().__init__()
        self.setObjectName("dropZone")
        self.ext = ext
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        box = QHBoxLayout(self)
        box.setContentsMargins(24, 22, 24, 22)
        box.setSpacing(16)

        art = QLabel()
        art.setFixedSize(46, 46)
        art.setAlignment(Qt.AlignCenter)
        art.setStyleSheet(
            f"background: {TOKENS['acc_soft']}; border-radius: 10px; font-size: 20px;")
        art.setText("📁")
        box.addWidget(art)

        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(label(t(title_key), "dropTitle"))
        text.addWidget(label(t(hint_key), "dropHint"))
        box.addLayout(text)
        box.addStretch(1)

    def _set_state(self, state):
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, _):
        path, _f = QFileDialog.getOpenFileName(
            self, "", "", f"*{self.ext}")
        if path:
            self.picked.emit(path)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self._set_state("over")

    def dragLeaveEvent(self, _):
        self._set_state("")

    def dropEvent(self, e):
        self._set_state("")
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(self.ext):
                self.picked.emit(path)
                return
        self.window().flash_hint(t("drop.wrong_ext", ext=self.ext))


class Card(QFrame):
    def __init__(self, number, title_key, hint=None):
        super().__init__()
        self.setObjectName("card")
        self.body = col(self, spacing=14, margins=(24, 20, 24, 22))

        head, head_lay = row(spacing=10)
        num = label(str(number), "stepNum")
        num.setAlignment(Qt.AlignCenter)
        num.setFixedSize(24, 24)
        head_lay.addWidget(num)
        head_lay.addWidget(label(t(title_key), "cardTitle"))
        head_lay.addStretch(1)
        self.tag = label("", "errorTag")
        self.tag.hide()
        head_lay.addWidget(self.tag)
        if hint:
            head_lay.addWidget(label(hint, "hint"))
        self.body.addWidget(head)

    def add(self, widget):
        self.body.addWidget(widget)


class Worker(QProcess):
    line = Signal(str)
    step = Signal(int, str)
    percent = Signal(int)
    finished_ok = Signal(str)
    failed = Signal(str)

    def __init__(self):
        super().__init__()
        self.buffer = []
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.readyReadStandardOutput.connect(self._read)
        self.finished.connect(self._done)

    def build_command(self, mode, values):
        raise NotImplementedError

    def run(self, mode, values):
        self.buffer.clear()
        program, args = self.build_command(mode, values)
        self.start(program, args)

    def _read(self):
        for raw in bytes(self.readAllStandardOutput()).decode(errors="replace").splitlines():
            self.buffer.append(raw)
            self.line.emit(raw)

    def _done(self, code, _status):
        raw = "\n".join(self.buffer)
        self.finished_ok.emit(raw) if code == 0 else self.failed.emit(raw)


class BundleToolWorker(Worker):
    def build_command(self, mode, values):
        if mode == "aab":
            return self._build_aab_command(values)
        else:
            return self._build_sign_command(values)

    def _get_bundletool_command(self):
        bundletool_path = shutil.which("bundletool")
        if bundletool_path:
            return "bundletool", []

        bundletool_dir = APP_DIR / "tools"
        if bundletool_dir.exists():
            for f in bundletool_dir.iterdir():
                if f.suffix == ".jar":
                    return "java", ["-jar", str(f)]
        return None, []

    def _get_apksigner_command(self):
        apksigner_path = shutil.which("apksigner")
        if apksigner_path:
            return "apksigner", []

        build_tools_base = self._get_android_sdk_paths()
        if build_tools_base:
            versions = sorted(
                [v for v in os.listdir(build_tools_base) if os.path.isdir(os.path.join(build_tools_base, v))],
                reverse=True
            )
            for version in versions:
                apksigner = os.path.join(build_tools_base, version, "apksigner")
                apksigner_bat = os.path.join(build_tools_base, version, "apksigner.bat")
                if os.path.exists(apksigner_bat):
                    return apksigner_bat, []
                if os.path.exists(apksigner):
                    return apksigner, []
        return None, []

    def _get_android_sdk_paths(self):
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

    def _build_aab_command(self, values):
        program, extra_args = self._get_bundletool_command()
        if not program:
            raise FileNotFoundError("bundletool not found")

        args = extra_args + [
            "build-apks",
            f"--bundle={values['bundle']}",
            f"--output={values['output']}",
            f"--ks={values['keystore']}",
            f"--ks-pass={values['ks_pass']}",
            f"--ks-key-alias={values['alias']}",
            f"--key-pass={values['key_pass']}"
        ]
        return program, args

    def _build_sign_command(self, values):
        program, extra_args = self._get_apksigner_command()
        if not program:
            raise FileNotFoundError("apksigner not found")

        output_dir = values['output']
        singer_apk = os.path.join(output_dir, "singer.apk")

        args = extra_args + [
            "sign",
            "--ks", values['keystore'],
            "--ks-pass", values['ks_pass'],
            "--ks-key-alias", values['alias'],
            "--key-pass", values['key_pass'],
            "--out", singer_apk,
            values['apk']
        ]
        return program, args


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("BundleToolSuite", "ui")
        self.setWindowTitle(t("app.title"))
        self.setMinimumSize(980, 720)
        self.resize(1140, 800)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = col(root, spacing=0, margins=(0, 0, 0, 0))

        outer.addWidget(self._header())
        outer.addWidget(self._tabs())

        self.pages = QStackedWidget()
        self.pages.addWidget(self._page("aab"))
        self.pages.addWidget(self._page("sign"))
        outer.addWidget(self.pages, 1)

        self.worker = BundleToolWorker()
        self.worker.line.connect(self._on_log_line)
        self.worker.finished_ok.connect(self._on_finished)
        self.worker.failed.connect(self._on_failed)

        self.current_mode = "aab"
        self.log_line_count = 0
        self.picked_files = {"aab": None, "sign": None}

    def _header(self):
        wrap = QWidget()
        lay = col(wrap, spacing=4, margins=(34, 24, 34, 12))
        top, top_lay = row(spacing=20)
        left = QVBoxLayout()
        left.setSpacing(3)
        left.addWidget(label(t("app.title"), "h1"))
        left.addWidget(label(t("app.subtitle"), "sub"))
        top_lay.addLayout(left)
        top_lay.addStretch(1)

        lang_frame = QWidget()
        lang_lay = QHBoxLayout(lang_frame)
        lang_lay.setContentsMargins(0, 0, 0, 0)
        lang_lay.setSpacing(6)
        lang_lay.addWidget(label("🌐"))
        
        languages = [
            ("tr", "TR"), ("en", "EN"), ("de", "DE"), ("es", "ES"),
            ("fr", "FR"), ("ja", "JA"), ("zh_cn", "ZH"), ("ru", "RU")
        ]
        self.lang_buttons = []
        for code, display in languages:
            btn = QPushButton(display)
            btn.setObjectName("chip")
            btn.setCheckable(True)
            btn.setChecked(code == "tr")
            btn.clicked.connect(lambda checked, c=code: self._switch_lang(c))
            lang_lay.addWidget(btn)
            self.lang_buttons.append((code, btn))
        
        top_lay.addWidget(lang_frame, 0, Qt.AlignTop)

        self.env = label("bundletool · Java hazır", "envPill")
        top_lay.addWidget(self.env, 0, Qt.AlignTop)
        lay.addWidget(top)
        return wrap

    def _switch_lang(self, lang):
        t.set_lang(lang)
        self.settings.setValue("language", lang)
        self._rebuild_ui()
        
        for code, btn in self.lang_buttons:
            btn.setChecked(code == lang)

    def _rebuild_ui(self):
        self.setWindowTitle(t("app.title"))
        
        old_pages = self.pages
        current_index = old_pages.currentIndex()
        
        new_pages = QStackedWidget()
        new_pages.addWidget(self._page("aab"))
        new_pages.addWidget(self._page("sign"))
        new_pages.setCurrentIndex(current_index)
        
        root = self.centralWidget()
        outer = root.layout()
        
        outer.removeWidget(old_pages)
        old_pages.deleteLater()
        
        outer.addWidget(new_pages, 1)
        self.pages = new_pages
        
        for i, key in enumerate(("tab.aab", "tab.sign")):
            self.tab_buttons[i].setText(t(key))

    def _tabs(self):
        strip = QWidget()
        strip.setObjectName("tabStrip")
        lay, lay_h = row(margins=(34, 12, 34, 0), spacing=6)
        self.tab_buttons = []
        for i, key in enumerate(("tab.aab", "tab.sign")):
            b = QPushButton(t(key))
            b.setObjectName("tab")
            b.setCheckable(True)
            b.setChecked(i == 0)
            b.clicked.connect(lambda _c, idx=i: self.switch_tab(idx))
            lay_h.addWidget(b)
            self.tab_buttons.append(b)
        lay_h.addStretch(1)
        return lay

    def switch_tab(self, index):
        for i, b in enumerate(self.tab_buttons):
            b.setChecked(i == index)
        self.pages.setCurrentIndex(index)
        self.current_mode = "aab" if index == 0 else "sign"

    def _page(self, mode):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        inner = QWidget()
        lay = col(inner, spacing=16, margins=(34, 22, 34, 28))

        files = Card(1, "card.files")
        zone = DropZone(".aab" if mode == "aab" else ".apk",
                        f"drop.{mode if mode == 'aab' else 'apk'}.title",
                        f"drop.{mode if mode == 'aab' else 'apk'}.hint")
        zone.picked.connect(lambda path, m=mode: self._on_file_picked(path, m))
        files.add(zone)

        if mode == "aab":
            output_field = Field("field.output", t("field.output.ph"), browse="folder",
                               browse_callback=lambda: self._browse_output_file())
        else:
            output_field = Field("field.output", t("field.output.ph"), browse="folder",
                               browse_callback=lambda: self._browse_output_dir())
        output_field.setObjectName("outputField")
        files.add(output_field)
        lay.addWidget(files)

        signing = Card(2, "card.signing", hint=t("card.signing_hint"))
        ks_field = Field("field.keystore", t("field.keystore.ph"), browse="key",
                        browse_callback=lambda: self._browse_keystore())
        ks_field.setObjectName("keystoreField")
        signing.add(ks_field)
        ks_pass_field = Field("field.ks_pass", "••••••••", password=True, from_file=True)
        ks_pass_field.setObjectName("ksPassField")
        signing.add(ks_pass_field)
        alias_field = Field("field.alias", t("field.alias.ph"))
        alias_field.setObjectName("aliasField")
        signing.add(alias_field)
        key_pass_field = Field("field.key_pass", "••••••••", password=True, from_file=True)
        key_pass_field.setObjectName("keyPassField")
        signing.add(key_pass_field)
        remember = QCheckBox(t("field.remember"))
        remember.setChecked(True)
        signing.add(remember)
        lay.addWidget(signing)

        cta_row, cta_lay = row(spacing=12)
        cta = QPushButton(t("cta.convert") if mode == "aab" else t("cta.sign"))
        cta.setObjectName("primary")
        cta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cta.clicked.connect(lambda: self._on_cta_clicked(mode))
        reset = QPushButton(t("cta.reset"))
        reset.clicked.connect(lambda: self._reset_form(mode))
        cta_lay.addWidget(cta, 1)
        cta_lay.addWidget(reset)
        lay.addWidget(cta_row)

        progress_box = self._create_progress_box(mode)
        success_box = self._create_success_box(mode)
        error_box = self._create_error_box(mode)
        log_box = self._create_log_box(mode)
        
        lay.addWidget(progress_box)
        lay.addWidget(success_box)
        lay.addWidget(error_box)
        lay.addWidget(log_box)
        lay.addStretch(1)
        scroll.setWidget(inner)
        return scroll

    def _browse_output_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "", "", "APK Set (*.apks)")
        if path:
            page = self.pages.currentWidget()
            output_field = page.findChild(Field, "outputField")
            if output_field:
                output_field.input.setText(path)

    def _browse_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "")
        if path:
            page = self.pages.currentWidget()
            output_field = page.findChild(Field, "outputField")
            if output_field:
                output_field.input.setText(path)

    def _browse_keystore(self):
        path, _ = QFileDialog.getOpenFileName(self, "", "", "Keystore (*.keystore *.jks)")
        if path:
            page = self.pages.currentWidget()
            ks_field = page.findChild(Field, "keystoreField")
            if ks_field:
                ks_field.input.setText(path)

    def _on_file_picked(self, path, mode):
        self.picked_files[mode] = path
        page = self.pages.widget(0 if mode == "aab" else 1)
        card = page.findChild(Card)
        zone = card.findChild(DropZone)
        zone.hide()

        file_row = QFrame()
        file_row.setObjectName("fileRow")
        row_lay = QHBoxLayout(file_row)
        row_lay.setContentsMargins(16, 12, 16, 12)
        row_lay.setSpacing(12)

        check = QLabel("✓")
        check.setStyleSheet(f"background: {TOKENS['ok_soft']}; color: {TOKENS['ok']}; "
                           f"border-radius: 10px; font-size: 16px; font-weight: bold;")
        check.setFixedSize(38, 38)
        check.setAlignment(Qt.AlignCenter)
        row_lay.addWidget(check)

        info = QVBoxLayout()
        info.setSpacing(2)
        info.addWidget(label(Path(path).name))
        info.addWidget(label(t(f"file.meta.{mode}", size="", modules=""), "fileMeta"))
        row_lay.addLayout(info)
        row_lay.addStretch(1)

        change_btn = QPushButton(t("file.change"))
        change_btn.clicked.connect(lambda: self._change_file(mode))
        row_lay.addWidget(change_btn)

        card.body.insertWidget(1, file_row)

        output_field = card.findChild(Field, "outputField")
        if output_field and not output_field.value():
            if mode == "aab":
                output_field.input.setText(path.replace('.aab', '.apks'))
            else:
                output_field.input.setText(str(Path(path).parent))

    def _change_file(self, mode):
        self.picked_files[mode] = None
        page = self.pages.widget(0 if mode == "aab" else 1)
        card = page.findChild(Card)
        file_row = card.findChild(QFrame, "fileRow")
        if file_row:
            file_row.deleteLater()
        zone = card.findChild(DropZone)
        zone.show()

    def _on_cta_clicked(self, mode):
        page = self.pages.widget(0 if mode == "aab" else 1)
        cards = page.findChildren(Card)
        files_card = cards[0]
        signing_card = cards[1]

        ks_field = signing_card.findChild(Field, "keystoreField")
        ks_pass_field = signing_card.findChild(Field, "ksPassField")
        alias_field = signing_card.findChild(Field, "aliasField")
        key_pass_field = signing_card.findChild(Field, "keyPassField")

        output_field = files_card.findChild(Field, "outputField")

        errors = []
        zone = files_card.findChild(DropZone)
        if zone.isVisible() or not self.picked_files.get(mode):
            errors.append(("file", t("valid.file")))
        if not output_field.value():
            errors.append(("output", t("valid.output")))
        if not ks_field.value():
            errors.append(("keystore", t("valid.keystore")))

        ks_ok, ks_pass, ks_err = ks_pass_field.resolve_password()
        if not ks_ok:
            errors.append(("ks_pass", ks_err))
        elif not ks_pass:
            errors.append(("ks_pass", t("valid.ks_pass")))

        key_ok, key_pass, key_err = key_pass_field.resolve_password()
        if not key_ok:
            errors.append(("key_pass", key_err))
        elif not key_pass:
            key_pass = ks_pass

        if errors:
            for field_name, msg in errors:
                if field_name == "file":
                    pass
                elif field_name == "output":
                    output_field.set_error(msg)
                elif field_name == "keystore":
                    ks_field.set_error(msg)
                elif field_name == "ks_pass":
                    ks_pass_field.set_error(msg)
                elif field_name == "key_pass":
                    key_pass_field.set_error(msg)

            signing_card.tag.setText(t("valid.tag", count=len(errors)))
            signing_card.tag.show()
            return

        values = {
            'keystore': ks_field.value(),
            'ks_pass': f"pass:{ks_pass}",
            'alias': alias_field.value(),
            'key_pass': f"pass:{key_pass}",
            'output': output_field.value(),
        }

        if mode == "aab":
            values['bundle'] = self.picked_files[mode]
        else:
            values['apk'] = self.picked_files[mode]

        self._start_process(mode, values)

    def _start_process(self, mode, values):
        page = self.pages.widget(0 if mode == "aab" else 1)
        cta = page.findChild(QPushButton, "primary")
        cta.setEnabled(False)
        cta.setText(t("cta.running"))

        progress_box = page.findChild(QFrame, "progressBox")
        success_box = page.findChild(QFrame, "successBox")
        error_box = page.findChild(QFrame, "errorBox")
        log_box = page.findChild(QFrame, "logBox")
        log = page.findChild(QPlainTextEdit, "log")
        
        progress_box.show()
        success_box.hide()
        error_box.hide()
        log_box.show()
        log.clear()
        self.log_line_count = 0

        try:
            self.worker.run(mode, values)
        except FileNotFoundError as e:
            self._on_failed(str(e))

    def _on_log_line(self, line):
        page = self.pages.currentWidget()
        log = page.findChild(QPlainTextEdit, "log")
        log_count = page.findChild(QLabel, "logCount")
        log.appendPlainText(line)
        self.log_line_count += 1
        log_count.setText(t("log.count", n=self.log_line_count))

    def _on_finished(self, raw):
        page = self.pages.widget(0 if self.current_mode == "aab" else 1)
        cta = page.findChild(QPushButton, "primary")
        cta.setEnabled(True)
        cta.setText(t("cta.convert") if self.current_mode == "aab" else t("cta.sign"))

        progress_box = page.findChild(QFrame, "progressBox")
        success_box = page.findChild(QFrame, "successBox")
        success_title = page.findChild(QLabel, "successTitle")
        
        progress_box.hide()
        success_box.show()
        success_title.setText(t("done.title", duration=""))

    def _on_failed(self, raw):
        page = self.pages.widget(0 if self.current_mode == "aab" else 1)
        cta = page.findChild(QPushButton, "primary")
        cta.setEnabled(True)
        cta.setText(t("cta.convert") if self.current_mode == "aab" else t("cta.sign"))

        progress_box = page.findChild(QFrame, "progressBox")
        error_box = page.findChild(QFrame, "errorBox")
        error_title = page.findChild(QLabel, "errorTitle")
        error_body = page.findChild(QLabel, "errorBody")

        progress_box.hide()
        error_box.show()

        info = errors.message(raw, t)
        error_title.setText(info["title"])
        error_body.setText(info["body"])

    def _reset_form(self, mode):
        self.picked_files[mode] = None
        page = self.pages.widget(0 if mode == "aab" else 1)
        cards = page.findChildren(Card)

        for card in cards:
            fields = card.findChildren(Field)
            for field in fields:
                field.reset()
            card.tag.hide()

            file_row = card.findChild(QFrame, "fileRow")
            if file_row:
                file_row.deleteLater()
            zone = card.findChild(DropZone)
            zone.show()

        progress_box = page.findChild(QFrame, "progressBox")
        success_box = page.findChild(QFrame, "successBox")
        error_box = page.findChild(QFrame, "errorBox")
        progress_box.hide()
        success_box.hide()
        error_box.hide()

    def _create_progress_box(self, mode):
        box = QFrame()
        box.setObjectName("progressBox")
        box.hide()
        lay = col(box, spacing=10, margins=(22, 18, 22, 18))
        head, head_lay = row(spacing=10)
        step_label = label(t(f"step.{mode}.2"))
        head_lay.addWidget(step_label)
        head_lay.addStretch(1)
        pct = label("0%", "pct")
        head_lay.addWidget(pct)
        lay.addWidget(head)
        bar = QProgressBar()
        bar.setTextVisible(False)
        bar.setRange(0, 0)
        lay.addWidget(bar)
        lay.addWidget(label(t("progress.meta", i=2, n=4, eta=""), "hint"))
        return box

    def _create_success_box(self, mode):
        box = QFrame()
        box.setObjectName("successBox")
        box.hide()
        lay = col(box, spacing=8, margins=(22, 18, 22, 18))
        head, head_lay = row(spacing=12)
        check = QLabel("✓")
        check.setStyleSheet(f"background: {TOKENS['ok']}; color: {TOKENS['ok_soft']}; "
                           f"border-radius: 20px; font-size: 20px; font-weight: bold;")
        check.setFixedSize(40, 40)
        check.setAlignment(Qt.AlignCenter)
        head_lay.addWidget(check)
        info = QVBoxLayout()
        info.setSpacing(2)
        success_title = label(t("done.title", duration=""), "successTitle")
        success_title.setObjectName("successTitle")
        info.addWidget(success_title)
        success_meta = label("", "successMeta")
        info.addWidget(success_meta)
        head_lay.addLayout(info)
        head_lay.addStretch(1)
        open_btn = QPushButton(t("done.open"))
        open_btn.clicked.connect(self._open_output_folder)
        head_lay.addWidget(open_btn)
        lay.addWidget(head)
        return box

    def _create_error_box(self, mode):
        box = QFrame()
        box.setObjectName("errorBox")
        box.hide()
        lay = col(box, spacing=8, margins=(22, 18, 22, 18))
        error_title = label("", "errorTitle")
        error_title.setObjectName("errorTitle")
        lay.addWidget(error_title)
        error_body = label("", "errorBody")
        error_body.setObjectName("errorBody")
        lay.addWidget(error_body)
        return box

    def _create_log_box(self, mode):
        box = QFrame()
        box.setObjectName("logBox")
        lay = col(box, spacing=0, margins=(14, 12, 14, 14))
        head, head_lay = row(spacing=10)
        toggle = QPushButton(t("log.title"))
        toggle.setObjectName("logHeader")
        toggle.setCheckable(True)
        toggle.setChecked(True)
        head_lay.addWidget(toggle)
        log_count = label(t("log.count", n=0), "hint")
        log_count.setObjectName("logCount")
        head_lay.addWidget(log_count)
        head_lay.addStretch(1)
        copy = QPushButton(t("log.copy"))
        copy.setObjectName("chip")
        copy.clicked.connect(self.copy_log)
        head_lay.addWidget(copy)
        lay.addWidget(head)

        log = QPlainTextEdit()
        log.setObjectName("log")
        log.setReadOnly(True)
        log.setMaximumHeight(168)
        log.setPlaceholderText(t("log.empty"))
        lay.addWidget(log)
        toggle.toggled.connect(log.setVisible)
        return box

    def copy_log(self):
        page = self.pages.currentWidget()
        log = page.findChild(QPlainTextEdit, "log")
        QApplication.clipboard().setText(log.toPlainText())

    def flash_hint(self, message):
        self.env.setText(message)

    def _open_output_folder(self):
        page = self.pages.currentWidget()
        output_field = page.findChild(Field, "outputField")
        if output_field and output_field.value():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(output_field.value()).parent)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet())
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
