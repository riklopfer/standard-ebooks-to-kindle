import hashlib
import shutil
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, NamedTuple, Self
from zipfile import ZipFile

import typer
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn

app = typer.Typer()

__all__ = ["app"]


_BLOCK_SIZE = 100


class FingerPrint(NamedTuple):
    size: int
    sha1: str


@cache
def _finger_print(path: Path) -> FingerPrint:
    digest = hashlib.sha1()
    size = 0
    with path.open("rb") as fp:
        while data := fp.read(_BLOCK_SIZE):
            size += len(data)
            digest.update(data)
    return FingerPrint(size=size, sha1=digest.hexdigest())


def _should_copy(source: Path, target: Path) -> bool:
    if not target.exists():
        return True

    if source.name != target.name:
        return True

    source_content, target_content = _finger_print(source), _finger_print(target)

    if source_content == target_content:
        return False

    return source_content.size > target_content.size


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

        if not (force or _should_copy(file, target_path)):
            return False

        shutil.copyfile(file, target_path)
        return True


def mk_pbar() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        expand=True,
    )


def _copy_to_kindle(source: Path, kindle: KindlePaths, force: bool, _desc: str = ""):
    kindle.prepare(force)
    all_files = [f for f in source.glob("**/*") if f.is_file()]

    with mk_pbar() as pbar:
        for file in pbar.track(
            all_files, total=len(all_files), description=_desc or f"{source}"
        ):
            if file.suffix == ".zip":
                with TemporaryDirectory() as tmp_dir:
                    ZipFile(file).extractall(tmp_dir)
                    _copy_to_kindle(
                        Path(tmp_dir), kindle=kindle, force=force, _desc=file.name
                    )
            else:
                kindle.copy_file(file, force)


@app.command()
def main(
    source: Annotated[Path, typer.Argument(help="Path containing downloaded ebooks")],
    kindle_root: Annotated[Path, typer.Argument(help="Kindle mount point")] = Path(
        "/Volumes/Kindle"
    ),
    force: Annotated[
        bool,
        typer.Option(
            help="Force directory creation. Will attempt to create kindle_root if it doesn't exist."
        ),
    ] = False,
) -> None:
    _copy_to_kindle(source=source, kindle=KindlePaths(kindle_root), force=force)


if __name__ == "__main__":
    app()
