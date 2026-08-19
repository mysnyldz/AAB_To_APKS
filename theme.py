"""Bundle Tool Suite — tasarım token'ları ve uygulama QSS'i.

Tek tema: koyu mavi. Renkleri buradan alın; başka yerde hex yazmayın.
"""
import sys
from pathlib import Path
from string import Template

from PySide6.QtGui import QFontDatabase


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


TOKENS = {
    "bg":        "#1b1e23",
    "surf":      "#23272e",
    "panel":     "#2b3038",
    "log":       "#15181c",
    "ink":       "#e9ebee",
    "muted":     "#9a9da1",
    "line":      "#34383e",
    "acc":       "#5d9bd6",
    "acc_ink":   "#b3d0ea",
    "acc_soft":  "#24303c",
    "acc_edge":  "#344e67",
    "on_acc":    "#10161c",
    "ok":        "#6cae8c",
    "ok_soft":   "#273433",
    "ok_ink":    "#b6dcc6",
    "err":       "#e0655c",
    "err_soft":  "#35272a",
    "err_edge":  "#6e3c3b",
    "err_ink":   "#ffada5",
    "r_lg": "12px", "r_md": "10px", "r_sm": "8px", "r_xs": "6px",
    "font": "Figtree",
    "mono": "Menlo, Consolas, 'DejaVu Sans Mono', monospace",
}

FONT_DIR = get_app_dir() / "assets" / "fonts"


def load_fonts() -> str:
    loaded = False
    for f in ("Figtree-Regular.ttf", "Figtree-SemiBold.ttf", "Figtree-Bold.ttf"):
        p = FONT_DIR / f
        if p.exists() and QFontDatabase.addApplicationFont(str(p)) != -1:
            loaded = True
    return "Figtree" if loaded else "Segoe UI, -apple-system, system-ui, sans-serif"


QSS = Template("""
* { font-family: $font; font-size: 13px; color: $ink; outline: none; }
QMainWindow, #root { background: $bg; }

#titleBar { background: $surf; }
#titleText { color: $muted; font-size: 12px; }
#winBtn { background: transparent; border: 0; border-radius: $r_xs; }
#winBtn:hover { background: $acc_soft; }
#winClose:hover { background: $acc; }

#h1 { font-size: 26px; font-weight: 700; letter-spacing: -0.4px; }
#sub { color: $muted; font-size: 13px; }
#envPill { background: $ok_soft; color: $ok_ink; border-radius: $r_xs;
           padding: 6px 12px; font-size: 11px; }
#envPillWarn { background: $err_soft; color: $err_ink; border-radius: $r_xs;
               padding: 6px 12px; font-size: 11px; }

#tabStrip { border-bottom: 1px solid $line; }
QPushButton#tab { background: transparent; border: 0; color: $muted;
                  padding: 11px 20px; font-size: 14px; font-weight: 600;
                  border-top-left-radius: $r_sm; border-top-right-radius: $r_sm; }
QPushButton#tab:hover { background: $acc_soft; color: $acc_ink; }
QPushButton#tab:checked { background: $surf; color: $acc_ink;
                          border-bottom: 3px solid $acc; }

#card { background: $surf; border: 1px solid $line; border-radius: $r_lg; }
#cardTitle { font-size: 17px; font-weight: 700; }
#stepNum { background: $acc_soft; border: 1px solid $acc_edge; color: $acc_ink;
           border-radius: 7px; font-size: 12px; font-weight: 700;
           min-width: 24px; min-height: 24px; }
#hint { color: $muted; font-size: 11px; }

QLabel#label { color: $muted; font-size: 12px; }
QLineEdit { background: $panel; border: 1px solid $line; border-radius: $r_sm;
            padding: 8px 12px; min-height: 20px; selection-background-color: $acc; }
QLineEdit:hover { border-color: $acc_edge; }
QLineEdit:focus { border-color: $acc; }
QLineEdit[state="error"] { background: $err_soft; border-color: $err; }
QLineEdit:disabled { color: $muted; }

QPushButton { background: transparent; border: 1px solid $line; border-radius: $r_sm;
              padding: 8px 14px; font-weight: 600; }
QPushButton:hover { border-color: $acc; color: $acc_ink; background: $acc_soft; }
QPushButton:pressed { background: $acc_edge; }
QPushButton:focus { border-color: $acc; }
QPushButton:disabled { color: $muted; border-color: $line; background: transparent; }

QPushButton#primary { background: $acc; color: $on_acc; border: 0;
                      padding: 15px 20px; font-size: 15px; font-weight: 700; }
QPushButton#primary:hover { background: #6da8de; }
QPushButton#primary:pressed { background: #4d87bd; }
QPushButton#primary:disabled { background: $acc_soft; color: $muted; }

QPushButton#chip { border: 1px solid $line; border-radius: $r_xs; color: $muted;
                   padding: 4px 10px; font-size: 11px; font-weight: 400; }
QPushButton#chip:checked { background: $acc_soft; border-color: $acc_edge; color: $acc_ink; }

#dropZone { background: $panel; border: 2px dashed $line; border-radius: $r_md; }
#dropZone[state="over"] { border: 2px solid $acc; background: $acc_soft; }
#dropTitle { font-size: 15px; font-weight: 600; }
#dropHint { color: $muted; font-size: 12px; }
#fileRow { background: $panel; border: 1px solid $line; border-radius: $r_md; }
#fileMeta { color: $muted; font-size: 11px; }

#progressBox { background: $surf; border: 1px solid $line; border-radius: $r_md; }
QProgressBar { background: $panel; border: 1px solid $line; border-radius: 4px;
               height: 8px; text-align: center; color: transparent; }
QProgressBar::chunk { background: $acc; border-radius: 3px; }
#pct { color: $acc_ink; font-size: 19px; font-weight: 700; }

#successBox { background: $ok_soft; border-radius: $r_md; }
#successTitle { color: $ok_ink; font-size: 15px; font-weight: 700; }
#successMeta { color: $ok_ink; font-size: 12px; }

#errorBox { background: $err_soft; border: 1px solid $err_edge; border-radius: $r_md; }
#errorTitle { color: $err_ink; font-size: 14px; font-weight: 700; }
#errorBody { color: $err_ink; font-size: 12px; }
#fieldError { color: $err_ink; font-size: 11px; }
#errorTag { background: $err_soft; border: 1px solid $err_edge; color: $err_ink;
            border-radius: $r_xs; padding: 3px 9px; font-size: 11px; }

#logBox { background: $surf; border: 1px solid $line; border-radius: $r_md; }
#logHeader { font-size: 14px; font-weight: 600; background: transparent; border: 0;
             text-align: left; padding: 4px; }
QPlainTextEdit#log { background: $log; border: 0; border-radius: $r_sm;
                     font-family: $mono; font-size: 12px; color: $muted;
                     padding: 12px 14px; }

QScrollBar:vertical { background: transparent; width: 10px; margin: 4px; }
QScrollBar::handle:vertical { background: $line; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: $acc_edge; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }

QCheckBox { spacing: 9px; font-size: 13px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 5px;
                       border: 1.5px solid $line; background: $panel; }
QCheckBox::indicator:hover { border-color: $acc; }
QCheckBox::indicator:checked { background: $acc; border-color: $acc; }
QCheckBox#fieldToggle { font-size: 12px; color: $muted; spacing: 6px; }
QCheckBox#fieldToggle::indicator { width: 15px; height: 15px; border-radius: 4px; }

QDialog { background: $surf; }
#dialogTitle { font-size: 19px; font-weight: 700; }
#dialogBody { color: $muted; font-size: 13px; }
""")


def stylesheet() -> str:
    return QSS.substitute({**TOKENS, "font": load_fonts()})
