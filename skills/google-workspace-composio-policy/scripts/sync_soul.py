"""Safely synchronize a narrow policy block in the current instance's SOUL.

Run only after independently verifying the current runtime/profile and SOUL path.
This tool cannot discover that identity or grant permissions to a process.
"""
import argparse
import os
from pathlib import Path
import stat
import tempfile

START = "<!-- composio-cli-first:begin -->"
END = "<!-- composio-cli-first:end -->"
BLOCK = (START + "\n"
         "Para cualquier aplicación conectada, comprueba primero Composio CLI en este runtime/perfil. "
         "Solo si no es utilizable por ausencia del ejecutable, autenticación no disponible, "
         "conexión no operativa o fallo técnico, considera MCP de la misma cuenta y tenant, "
         "tras verificar identidad y lectura real. Permisos insuficientes, cuenta equivocada, "
         "denegación de autorización o política bloquean el cambio de ruta; ante causa o "
         "identidad incierta, detente y pide aclaración. Una skill no proporciona terminal ni CLI "
         "a un API server que no los exponga.\n" + END)


def sync(home, profile):
    """Return (changed, backup_path); fail closed before any write on uncertain scope."""
    env_home = os.environ.get("HERMES_HOME")
    env_profile = os.environ.get("HERMES_PROFILE")
    if not env_home or not env_profile or env_profile != profile or not profile:
        raise ValueError("runtime_profile_unverified")
    root = Path(home)
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        raise ValueError("home_unverified")
    if root.resolve() != root or root.resolve() != Path(env_home).resolve() or Path(env_home).is_symlink():
        raise ValueError("home_mismatch")
    if root.stat().st_uid != os.getuid():
        raise ValueError("home_owner_mismatch")
    target = root / "SOUL.md"
    if target.is_symlink() or not target.is_file() or target.stat().st_uid != os.getuid():
        raise ValueError("soul_unverified")
    mode = target.stat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError("soul_not_regular")
    original = target.read_bytes()
    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("soul_not_utf8") from exc
    starts, ends = text.count(START), text.count(END)
    if starts != ends or starts > 1:
        raise ValueError("malformed_or_duplicate_markers")
    if starts:
        begin = text.index(START)
        finish = text.index(END) + len(END)
        if finish <= begin or text.find(END) < begin:
            raise ValueError("marker_order_invalid")
        updated = text[:begin] + BLOCK + text[finish:]
    else:
        updated = text + ("" if text.endswith("\n") else "\n") + "\n" + BLOCK + "\n"
    if updated == text:
        return False, None
    # Before writing, retain an exclusive, byte-exact backup in the same instance.
    fd, name = tempfile.mkstemp(prefix="SOUL.md.backup-", dir=root)
    backup = Path(name)
    try:
        os.fchmod(fd, stat.S_IMODE(mode))
        with os.fdopen(fd, "wb") as out:
            out.write(original)
            out.flush()
            os.fsync(out.fileno())
        if target.is_symlink() or target.read_bytes() != original:
            raise ValueError("soul_changed_during_sync")
        replacement_fd, replacement_name = tempfile.mkstemp(prefix=".SOUL.md.sync-", dir=root)
        replacement = Path(replacement_name)
        try:
            os.fchmod(replacement_fd, stat.S_IMODE(mode))
            with os.fdopen(replacement_fd, "wb") as out:
                out.write(updated.encode("utf-8"))
                out.flush()
                os.fsync(out.fileno())
            os.replace(replacement, target)
            if target.read_bytes() != updated.encode("utf-8") or backup.read_bytes() != original:
                raise RuntimeError("post_write_readback_failed")
        finally:
            replacement.unlink(missing_ok=True)
    except Exception:
        # Keep a valid backup if a post-write validation fails; never undo unverified state.
        raise
    return True, backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True, help="verified absolute HERMES_HOME")
    parser.add_argument("--profile", required=True, help="verified active HERMES_PROFILE")
    args = parser.parse_args()
    try:
        changed, backup = sync(args.home, args.profile)
    except (OSError, ValueError, RuntimeError) as exc:
        print("blocked: " + str(exc))
        return 2
    print("updated; backup=" + str(backup) if changed else "already_current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
