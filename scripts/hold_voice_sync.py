#!/usr/bin/env python3
#!/usr/bin/env python3
"""Push voice profile, meta, and voice.md to Cloudflare R2 for backup.

Cost design: R2 has no egress fees. This script uses S3-compatible PUT only
(no Workers, no compute). Typical payload: 5-20KB. At $0.015/GB stored with
1 sync/day, annual cost is essentially zero.

Requires: pip install boto3

Env vars (set once):
  HYV_R2_ACCESS_KEY_ID
  HYV_R2_SECRET_ACCESS_KEY
  HYV_R2_ENDPOINT (e.g. https://<account>.r2.cloudflarestorage.com)
  HYV_R2_BUCKET (e.g. hyv-voice-profiles)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sync_profile(
    profile_path: Path,
    meta_path: Path | None = None,
    voice_md_path: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """push files to R2. returns summary dict."""
    try:
        import boto3
    except ImportError:
        return {"synced": False, "error": "boto3 not installed. pip install boto3"}

    required = ["HYV_R2_ACCESS_KEY_ID", "HYV_R2_SECRET_ACCESS_KEY", "HYV_R2_ENDPOINT", "HYV_R2_BUCKET"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        return {"synced": False, "error": f"missing env vars: {', '.join(missing)}"}

    if not profile_path.exists():
        return {"synced": False, "error": f"profile not found: {profile_path}"}

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["HYV_R2_ENDPOINT"],
        aws_access_key_id=os.environ["HYV_R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["HYV_R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    bucket = os.environ["HYV_R2_BUCKET"]
    profile_name = profile_path.stem  # e.g. "voice-profile"

    files_to_sync: list[tuple[Path, str]] = [
        (profile_path, f"{profile_name}/{profile_path.name}"),
    ]
    if meta_path and meta_path.exists():
        files_to_sync.append((meta_path, f"{profile_name}/{meta_path.name}"))
    if voice_md_path and voice_md_path.exists():
        files_to_sync.append((voice_md_path, f"{profile_name}/{voice_md_path.name}"))

    total_size = sum(f.stat().st_size for f, _ in files_to_sync if f.exists())
    if total_size > 1_000_000:  # 1MB safety cap
        return {"synced": False, "error": f"payload too large: {total_size} bytes"}

    if dry_run:
        return {"synced": False, "dry_run": True, "would_sync": [k for _, k in files_to_sync], "size": total_size}

    sync_time = _now_iso()
    uploaded = []
    for local_path, remote_key in files_to_sync:
        if not local_path.exists():
            continue
        s3.upload_file(
            str(local_path),
            bucket,
            remote_key,
            ExtraArgs={"ContentType": "application/json" if local_path.suffix == ".json" else "text/markdown"},
        )
        uploaded.append(remote_key)

    return {"synced": True, "uploaded": uploaded, "size": total_size, "time": sync_time}


def was_synced_recently(meta: dict[str, Any], max_hours: int = 24) -> bool:
    """check if a sync happened within max_hours."""
    last = meta.get("last_sync")
    if not last:
        return False
    try:
        last_dt = datetime.fromisoformat(last)
        hours_since = (datetime.now(timezone.utc) - last_dt.replace(tzinfo=timezone.utc)).total_seconds() / 3600
        return hours_since < max_hours
    except (ValueError, TypeError):
        return False


def try_auto_sync(
    profile_path: str,
    meta_path: str | None = None,
    voice_md_path: str | None = None,
) -> bool:
    """called by profile-evolve after saving. syncs if env is configured and
    last sync was > 24h ago. returns True if sync happened."""
    p = Path(profile_path).expanduser()
    if not p.exists():
        return False

    m = Path(meta_path).expanduser() if meta_path else p.with_suffix(".meta.json")
    meta: dict[str, Any] = {}
    if m.exists():
        try:
            meta = json.loads(m.read_text(encoding="utf-8", errors="ignore"))
        except (json.JSONDecodeError, OSError):
            meta = {}

    if was_synced_recently(meta, max_hours=23):
        return False

    vm = Path(voice_md_path).expanduser() if voice_md_path else p.with_suffix(".voice.md")
    result = sync_profile(p, meta_path=m, voice_md_path=vm)

    if result.get("synced"):
        meta["last_sync"] = result.get("time", _now_iso())
        m.parent.mkdir(parents=True, exist_ok=True)
        m.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    return False


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Sync voice profile to Cloudflare R2")
    parser.add_argument("--profile", required=True, help="voice profile JSON file")
    parser.add_argument("--meta", help="meta JSON file (default: profile path with .meta.json)")
    parser.add_argument("--voice-md", help="voice.md file (default: profile path with .voice.md)")
    parser.add_argument("--dry-run", action="store_true", help="print what would be synced without uploading")
    parser.add_argument("--force", action="store_true", help="sync even if recently synced")
    args = parser.parse_args()

    profile_path = Path(args.profile).expanduser()
    meta_path = Path(args.meta).expanduser() if args.meta else profile_path.with_suffix(".meta.json")
    voice_md_path = Path(args.voice_md).expanduser() if args.voice_md else profile_path.with_suffix(".voice.md")

    if not args.force:
        meta: dict[str, Any] = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8", errors="ignore"))
            except (json.JSONDecodeError, OSError):
                pass
        if was_synced_recently(meta):
            print("sync skipped — already synced within 24h (use --force to override)")
            return 0

    result = sync_profile(profile_path, meta_path=meta_path, voice_md_path=voice_md_path, dry_run=args.dry_run)

    if args.dry_run:
        print(json.dumps(result, indent=2))
        return 0

    if result.get("synced"):
        meta: dict[str, Any] = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8", errors="ignore"))
            except (json.JSONDecodeError, OSError):
                meta = {}
        meta["last_sync"] = result.get("time", _now_iso())
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"synced {len(result.get('uploaded', []))} files ({result.get('size', 0)} bytes)")
        for f in result.get("uploaded", []):
            print(f"  {f}")
        return 0

    print(f"sync failed: {result.get('error', 'unknown')}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
