"""Ham alt süreç çıktısını kullanıcıya gösterilecek sade mesaja çevirir."""
import re

RULES = [
    (r"keystore password was incorrect|Keystore was tampered with|"
     r"password verification failed",                       "err.ks_password"),
    (r"[Aa]lias .*(does not exist|not found)|"
     r"No key with alias",                                  "err.alias_missing"),
    (r"(java|JAVA_HOME).*(not found|No such file|is not recognized)|"
     r"UnsupportedClassVersionError",                       "err.java_missing"),
    (r"Permission denied|Access is denied|EACCES",          "err.permission"),
    (r"No such file or directory|cannot find the (file|path)", "err.file_missing"),
    (r"not a valid zip|Unable to read bundle|"
     r"AndroidManifest|Bundle is invalid",                  "err.not_a_bundle"),
    (r"zipalign.*(failed|error)",                           "err.zipalign"),
    (r"No space left on device|not enough space",           "err.disk_full"),
    (r"(SDK|build-tools).*(not found|missing)",             "err.sdk_missing"),
]

FALLBACK = "err.unknown"


def classify(raw_output: str) -> str:
    text = raw_output or ""
    for pattern, key in RULES:
        if re.search(pattern, text, re.IGNORECASE):
            return key
    return FALLBACK


def message(raw_output: str, t) -> dict:
    key = classify(raw_output)
    return {
        "key": key,
        "title": t(f"{key}.title"),
        "body": t(f"{key}.body"),
        "action": t(f"{key}.action"),
        "raw": raw_output,
    }
