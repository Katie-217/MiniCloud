"""Build the pinned Flutter demo without launching it or accessing Firebase."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from lab import ROOT

flutter = shutil.which("flutter")
if not flutter:
    raise SystemExit("Flutter SDK required for source build; the published runtime image needs no SDK.")
source = ROOT / "elearning-web/source"
# Native Flutter font/shader tools on Windows can fail with accented paths.
# Stage the source in a fresh ASCII path; keep it for diagnosing build failures.
stage = Path(tempfile.mkdtemp(prefix="minicloud-flutter-"))
assert stage.resolve().parent == Path(tempfile.gettempdir()).resolve()
shutil.copytree(source, stage, dirs_exist_ok=True,
    ignore=shutil.ignore_patterns("build", ".dart_tool", ".flutter-plugins-dependencies"))
for command in ([flutter, "pub", "get"], [flutter, "build", "web", "--release", "--no-pub",
    "--no-wasm-dry-run", "--no-web-resources-cdn", "--dart-define=MINICLOUD_LOCAL_EMULATORS=true",
    "--base-href", "/elearning/"]):
    subprocess.run(command, cwd=stage, check=True)
shutil.copytree(stage / "build/web", source / "build/web", dirs_exist_ok=True)
shutil.copy2(stage / "pubspec.lock", source / "pubspec.lock")
assert (source / "build/web/main.dart.js").exists()
print("Built E-learning Web for /elearning/; no application launched.")
