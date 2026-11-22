import shutil
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Self
from zipfile import ZipFile

import typer
from rich import progress

app = typer.Typer()

__all__ = ["app"]


@dataclass(frozen=True)
class KindlePaths:
    root: Path

    @property
    def books_dir(self) -> Path:
        return self.root / "documents"

    @property
    def thumbnails_dir(self) -> Path:
        return self.root / "system/thumbnails"

    def prepare(self, force: bool) -> Self:
        if force:
            self.books_dir.mkdir(parents=True, exist_ok=True)
            self.thumbnails_dir.mkdir(parents=True, exist_ok=True)
        else:
            if not self.books_dir.is_dir():
                raise NotADirectoryError(self.books_dir)
            if not self.thumbnails_dir.is_dir():
                raise NotADirectoryError(self.thumbnails_dir)
        return self

    def copy_file(self, file: Path, force: bool) -> bool:
        file = file.resolve()
        if not file.is_file():
            return False

        if file.suffix == ".azw3":
            target_path = self.books_dir / file.name
        elif file.suffix == ".jpg":
            target_path = self.thumbnails_dir / file.name
        else:
            return False

        if not force and target_path.exists() and target_path.stat().st_mtime >= file.stat().st_mtime:
            return False

        shutil.copyfile(file, target_path)
        return True


def copy_to_kindle(source: Path, kindle: KindlePaths, force: bool):
    kindle.prepare(force)
    all_files = [f for f in source.glob("**/*") if f.is_file()]
    for file in progress.track(all_files, total=len(all_files), description="Copying"):
        if file.suffix == ".zip":
            with TemporaryDirectory() as tmp_dir:
                ZipFile(file).extractall(tmp_dir)
                copy_to_kindle(Path(tmp_dir), kindle=kindle, force=force)
        else:
            kindle.copy_file(file, force)


@app.command()
def main(
    source: Annotated[Path, typer.Argument(help="Path containing downloaded ebooks")],
    kindle_root: Annotated[Path, typer.Argument(help="Kindle mount point")] = Path("/Volumes/Kindle"),
    force: Annotated[bool, typer.Option(help="Force directory creation")] = False,
) -> None:
    copy_to_kindle(source=source, kindle=KindlePaths(kindle_root), force=force)


if __name__ == "__main__":
    app()
