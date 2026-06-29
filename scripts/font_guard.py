#!/usr/bin/env python3
"""Strict font checks for gongwen-draft Word export."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
from pathlib import Path

try:
    from fontTools.ttLib import TTCollection, TTFont
except ImportError:  # pragma: no cover - optional dependency
    TTFont = None
    TTCollection = None

try:
    import winreg
except ImportError:  # pragma: no cover - non-Windows
    winreg = None

try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11
    tomllib = None


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_FONT_DIR = SKILL_DIR / "assets" / "fonts"
ASSET_FONT_CATALOG = ASSET_FONT_DIR / "catalog.toml"
FRONT_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n?", re.S)

OFFICIAL_FOUNDER_OFFICE_URL = "https://www.foundertype.com/index.php/FontInfo/get_font_office.html"

FONT_PROFILES = {
    "founder-gongwen": {
        "issuer": "方正小标宋简体",
        "title": "方正小标宋简体",
        "body": "仿宋_GB2312",
        "h1": "黑体",
        "h2": "楷体_GB2312",
        "h3": "仿宋_GB2312",
        "footer": "宋体",
    }
}

FONT_OVERRIDE_KEYS = {
    "issuer_font": "issuer",
    "title_font": "title",
    "body_font": "body",
    "h1_font": "h1",
    "h2_font": "h2",
    "h3_font": "h3",
    "footer_font": "footer",
}

FONT_ALIASES = {
    "simsun": {"宋体"},
    "fangsong": {"仿宋"},
    "simfang": {"仿宋"},
    "simhei": {"黑体"},
    "kaiti": {"楷体"},
    "simkai": {"楷体"},
}


def parse_front_matter(text: str) -> dict[str, object]:
    match = FRONT_RE.match(text)
    if not match:
        return {}

    meta: dict[str, object] = {}
    current_list: list[str] | None = None
    current_key: str | None = None

    for raw in match.group("body").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and current_list is not None:
            current_list.append(line.split("- ", 1)[1].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                meta[key] = value
                current_list = None
            else:
                current_list = []
                meta[key] = current_list
        elif current_key:
            meta[current_key] = line.strip()

    return meta


def meta_text(meta: dict[str, object], key: str) -> str:
    value = meta.get(key, "")
    if isinstance(value, list):
        return "；".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def build_font_config(meta: dict[str, object] | None = None) -> dict[str, str]:
    meta = meta or {}
    profile = meta_text(meta, "font_profile") or "founder-gongwen"
    if profile != "custom" and profile not in FONT_PROFILES:
        raise SystemExit(
            f"Unknown font_profile `{profile}`. Use `founder-gongwen` or `custom` with explicit font keys."
        )

    fonts = dict(FONT_PROFILES.get(profile, FONT_PROFILES["founder-gongwen"]))
    for key, role in FONT_OVERRIDE_KEYS.items():
        value = meta_text(meta, key)
        if value:
            fonts[role] = value
    return fonts


def required_fonts(fonts: dict[str, str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for role in ("issuer", "title", "body", "h1", "h2", "h3", "footer"):
        font = fonts.get(role, "").strip()
        if font and font not in seen:
            seen.add(font)
            ordered.append(font)
    return ordered


def clean_registry_name(name: str) -> str:
    return re.sub(r"\s+\((TrueType|OpenType|Type 1)\)\s*$", "", name, flags=re.I).strip()


def add_name(names: set[str], value: str) -> None:
    value = value.strip().strip("\x00")
    if not value:
        return
    names.add(value)
    normalized = value.lower().replace(" ", "")
    for key, aliases in FONT_ALIASES.items():
        if key in normalized:
            names.update(aliases)


def registry_font_files() -> tuple[set[str], set[Path]]:
    names: set[str] = set()
    files: set[Path] = set()
    if winreg is None:
        return names, files

    keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
    ]
    for hive, subkey in keys:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                for idx in range(winreg.QueryInfoKey(key)[1]):
                    name, value, _ = winreg.EnumValue(key, idx)
                    add_name(names, clean_registry_name(str(name)))
                    font_path = Path(str(value))
                    if not font_path.is_absolute():
                        font_path = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / font_path
                    if font_path.exists():
                        files.add(font_path)
        except OSError:
            continue
    return names, files


def system_font_search_dirs() -> list[Path]:
    dirs = [
        Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts",
        Path.home() / "Library" / "Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
        Path.home() / ".local" / "share" / "fonts",
        Path("/usr/local/share/fonts"),
        Path("/usr/share/fonts"),
    ]
    return [path for path in dirs if path and path.exists()]


def asset_font_files() -> list[Path]:
    if not ASSET_FONT_DIR.exists():
        return []
    return sorted(
        path
        for path in ASSET_FONT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in {".ttf", ".otf", ".ttc"}
    )


def iter_font_files() -> set[Path]:
    _, registry_files = registry_font_files()
    files = set(registry_files)
    for directory in system_font_search_dirs():
        files.update(
            path
            for path in directory.rglob("*")
            if path.is_file() and path.suffix.lower() in {".ttf", ".otf", ".ttc"}
        )
    return files


def names_from_font_file(path: Path) -> set[str]:
    names: set[str] = set()
    if TTFont is None:
        add_name(names, path.stem)
        return names

    def collect(ttfont) -> None:
        for record in ttfont["name"].names:
            if record.nameID in {1, 2, 4, 6, 16, 17}:
                try:
                    add_name(names, record.toUnicode())
                except UnicodeDecodeError:
                    continue

    try:
        if path.suffix.lower() == ".ttc":
            collection = TTCollection(str(path), lazy=True)
            for font in collection.fonts:
                collect(font)
            collection.close()
        else:
            font = TTFont(str(path), lazy=True)
            collect(font)
            font.close()
    except Exception:
        add_name(names, path.stem)
    return names


def installed_font_names() -> set[str]:
    names, _ = registry_font_files()
    for path in iter_font_files():
        names.update(names_from_font_file(path))
    return names


def asset_font_inventory() -> list[tuple[Path, set[str]]]:
    return [(path, names_from_font_file(path)) for path in asset_font_files()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def catalog_entries() -> list[dict[str, object]]:
    if not ASSET_FONT_CATALOG.exists():
        return []
    if tomllib is not None:
        with ASSET_FONT_CATALOG.open("rb") as handle:
            data = tomllib.load(handle)
        entries = data.get("fonts", [])
    else:
        entries = parse_simple_font_catalog(ASSET_FONT_CATALOG.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise SystemExit("Invalid assets/fonts/catalog.toml: `fonts` must be a list.")
    return [entry for entry in entries if isinstance(entry, dict)]


def parse_simple_font_catalog(text: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[[fonts]]":
            current = {}
            entries.append(current)
            continue
        if current is None or "=" not in line:
            continue
        key, value = line.split("=", 1)
        current[key.strip()] = value.strip().strip('"').strip("'")
    return entries


def verify_asset_catalog() -> None:
    errors: list[str] = []
    for entry in catalog_entries():
        file_name = str(entry.get("file", "")).strip()
        font_name = str(entry.get("font_name", "")).strip()
        expected_hash = str(entry.get("sha256", "")).strip().upper()
        if not file_name or not font_name or not expected_hash:
            errors.append(f"Incomplete catalog entry: {entry}")
            continue
        path = ASSET_FONT_DIR / file_name
        if not path.exists():
            errors.append(f"Missing font asset: {file_name}")
            continue
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            errors.append(f"SHA256 mismatch for {file_name}: expected {expected_hash}, got {actual_hash}")
        names = names_from_font_file(path)
        if font_name not in names:
            errors.append(f"Font name mismatch for {file_name}: `{font_name}` not found in name table")
    if errors:
        raise SystemExit("Font asset verification failed:\n" + "\n".join(f"- {error}" for error in errors))


def missing_fonts(fonts: dict[str, str]) -> list[str]:
    available = installed_font_names()
    return [font for font in required_fonts(fonts) if font not in available]


def official_channel_message(missing: list[str]) -> str:
    lines = [
        "Missing required official-document fonts:",
        *[f"- {font}" for font in missing],
        "",
        "Official channel checked:",
        f"- 方正字库公文写作个人（家庭）版授权: {OFFICIAL_FOUNDER_OFFICE_URL}",
        "",
        "This official page requires account authorization/payment before a font package can be obtained.",
        "Do not download these fonts from random font mirrors. Install authorized fonts locally, or place authorized font files in assets/fonts and run:",
        "  python scripts/check_fonts.py --install-assets",
    ]
    return "\n".join(lines)


def ensure_required_fonts(fonts: dict[str, str]) -> None:
    missing = missing_fonts(fonts)
    if missing:
        raise SystemExit(official_channel_message(missing))


def install_assets_for_missing(fonts: dict[str, str]) -> list[Path]:
    if sys.platform != "win32":
        raise SystemExit("--install-assets is only supported on Windows.")
    if winreg is None:
        raise SystemExit("Windows registry access is unavailable.")
    verify_asset_catalog()

    missing = set(missing_fonts(fonts))
    if not missing:
        return []

    local_dir = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
    local_dir.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []

    for path in asset_font_files():
        names = names_from_font_file(path)
        matched = sorted(missing.intersection(names))
        if not matched:
            continue
        dest = local_dir / path.name
        shutil.copy2(path, dest)
        font_type = "OpenType" if path.suffix.lower() == ".otf" else "TrueType"
        with winreg.CreateKeyEx(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            for font_name in matched:
                winreg.SetValueEx(key, f"{font_name} ({font_type})", 0, winreg.REG_SZ, str(dest))
        installed.append(dest)

    if installed:
        try:
            import ctypes

            HWND_BROADCAST = 0xFFFF
            WM_FONTCHANGE = 0x001D
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)
        except Exception:
            pass
    return installed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", help="Controlled Markdown draft whose font front matter should be checked")
    parser.add_argument("--install-assets", action="store_true", help="Install matching authorized fonts from assets/fonts for the current Windows user")
    parser.add_argument("--list", action="store_true", help="List detected font names")
    parser.add_argument("--list-assets", action="store_true", help="List font assets bundled with this skill")
    parser.add_argument("--verify-assets", action="store_true", help="Verify assets/fonts/catalog.toml hashes and font names")
    args = parser.parse_args()

    if args.list:
        for name in sorted(installed_font_names()):
            print(name)
        return
    if args.verify_assets:
        verify_asset_catalog()
        print("OK: font assets match catalog hashes and font names.")
        return
    if args.list_assets:
        for path, names in asset_font_inventory():
            print(f"{path.name}: {', '.join(sorted(names))}")
        return

    meta = {}
    if args.draft:
        meta = parse_front_matter(Path(args.draft).read_text(encoding="utf-8-sig"))
    fonts = build_font_config(meta)

    if args.install_assets:
        installed = install_assets_for_missing(fonts)
        for path in installed:
            print(f"Installed authorized asset font: {path}")

    ensure_required_fonts(fonts)
    print("OK: required official-document fonts are installed.")


if __name__ == "__main__":
    main()
