"""Deterministic package exporters (.pack/.zip/.tar.gz) and import helper."""

from __future__ import annotations

import io
import logging
import shutil
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# Fixed archive member timestamp for reproducibility.
_FIXED_DT = datetime(2026, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
_FIXED_EPOCH = int(_FIXED_DT.timestamp())


class PackageExporter:
    """Export a built package directory to distributable archive formats."""

    def export_all(self, package_dir: Path, output_stem: Path) -> dict[str, Path]:
        """Write .zip, .pack, and .tar.gz next to output_stem."""
        output_stem.parent.mkdir(parents=True, exist_ok=True)
        # Avoid Path.with_suffix — versions like 1.0.0 would truncate to 1.0.
        zip_path = Path(str(output_stem) + ".zip")
        pack_path = Path(str(output_stem) + ".pack")
        tar_path = Path(str(output_stem) + ".tar.gz")
        self.export_zip(package_dir, zip_path)
        # .pack is a zip container with pack semantics.
        shutil.copy2(zip_path, pack_path)
        self.export_tar_gz(package_dir, tar_path)
        logger.info("Exported package archives for %s", output_stem.name)
        return {"zip": zip_path, "pack": pack_path, "tar.gz": tar_path}

    def export_zip(self, package_dir: Path, destination: Path) -> Path:
        """Create a deterministic zip archive."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        files = sorted(
            path for path in package_dir.rglob("*") if path.is_file()
        )
        with zipfile.ZipFile(
            destination,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in files:
                rel = path.relative_to(package_dir).as_posix()
                data = path.read_bytes()
                info = zipfile.ZipInfo(rel, date_time=(2026, 8, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 0
                archive.writestr(info, data)
        return destination

    def export_tar_gz(self, package_dir: Path, destination: Path) -> Path:
        """Create a deterministic tar.gz archive."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        files = sorted(
            path for path in package_dir.rglob("*") if path.is_file()
        )
        with tarfile.open(destination, mode="w:gz", format=tarfile.USTAR_FORMAT) as archive:
            for path in files:
                rel = path.relative_to(package_dir).as_posix()
                data = path.read_bytes()
                info = tarfile.TarInfo(name=rel)
                info.size = len(data)
                info.mtime = _FIXED_EPOCH
                info.mode = 0o644
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                archive.addfile(info, io.BytesIO(data))
        return destination

    def import_archive(self, archive_path: Path, destination_dir: Path) -> Path:
        """Import/extract a package archive into destination_dir."""
        if destination_dir.exists():
            shutil.rmtree(destination_dir)
        destination_dir.mkdir(parents=True, exist_ok=True)
        if archive_path.name.endswith(".tar.gz") or archive_path.suffixes[-2:] == [".tar", ".gz"]:
            with tarfile.open(archive_path, "r:gz") as handle:
                handle.extractall(destination_dir)
        else:
            with zipfile.ZipFile(archive_path, "r") as handle:
                handle.extractall(destination_dir)
        logger.info("Imported package archive into %s", destination_dir)
        return destination_dir
