import csv
import shutil
import uuid
from pathlib import Path

import pytest
from PIL import Image

from core.date_classifier import build_date_path, get_target_date
from locales import get_texts
from main import validate_paths
from services.organizer import organize_images


def create_media_file(path: Path, content: str = "demo") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def create_image_file(path: Path, color: tuple[int, int, int]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (32, 32), color=color).save(path)
    return path


def expected_target_path(src_file: Path, dst_dir: Path) -> Path:
    target_date = get_target_date(str(src_file))
    return Path(build_date_path(str(dst_dir), target_date)) / src_file.name


def expected_target_dir(src_file: Path, dst_dir: Path) -> Path:
    target_date = get_target_date(str(src_file))
    return Path(build_date_path(str(dst_dir), target_date))


@pytest.fixture
def work_dir() -> Path:
    base_dir = Path.cwd() / "tests_runtime"
    base_dir.mkdir(exist_ok=True)
    temp_dir = base_dir / f"run_{uuid.uuid4().hex}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(autouse=True)
def hash_db_path(work_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMAGE_ORGANIZER_HASH_DB", str(work_dir / "hash_db.json"))


def test_copy_mode_organizes_and_keeps_source(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "copy.log"
    src_file = create_media_file(src_dir / "a.jpg")

    target_path = expected_target_path(src_file, dst_dir)

    organize_images(str(src_dir), str(dst_dir), str(log_path), mode="copy")

    assert src_file.exists()
    assert target_path.exists()
    assert "OK | COPY" in log_path.read_text(encoding="utf-8")


def test_move_mode_organizes_and_removes_source(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "move.log"
    src_file = create_media_file(src_dir / "a.jpg")

    target_path = expected_target_path(src_file, dst_dir)

    organize_images(str(src_dir), str(dst_dir), str(log_path), mode="move")

    assert not src_file.exists()
    assert target_path.exists()
    assert "OK | MOVE" in log_path.read_text(encoding="utf-8")


def test_validate_paths_rejects_missing_source(work_dir: Path) -> None:
    texts = get_texts("en")
    missing_src = work_dir / "missing"
    dst_dir = work_dir / "dst"

    with pytest.raises(ValueError, match="Source directory does not exist"):
        validate_paths(str(missing_src), str(dst_dir), texts)


def test_validate_paths_rejects_destination_inside_source(work_dir: Path) -> None:
    texts = get_texts("en")
    src_dir = work_dir / "src"
    nested_dst = src_dir / "nested" / "dst"
    src_dir.mkdir(parents=True)

    with pytest.raises(ValueError, match="Destination directory must not be"):
        validate_paths(str(src_dir), str(nested_dst), texts)


def test_duplicate_names_get_numeric_suffix(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "duplicate.log"
    src_file_1 = create_media_file(src_dir / "camera1" / "same.jpg", content="first")
    src_file_2 = create_media_file(src_dir / "camera2" / "same.jpg", content="second")

    target_dir = Path(build_date_path(str(dst_dir), get_target_date(str(src_file_1))))

    organize_images(str(src_dir), str(dst_dir), str(log_path), mode="copy")

    first_target = target_dir / "same.jpg"
    second_target = target_dir / "same_1.jpg"

    assert first_target.exists()
    assert second_target.exists()
    assert first_target.read_text(encoding="utf-8") == "first"
    assert second_target.read_text(encoding="utf-8") == "second"


def test_strict_duplicate_detection_keeps_duplicates_within_current_destination(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "strict.log"
    first_file = create_media_file(src_dir / "camera1" / "same.jpg", content="first")
    create_media_file(src_dir / "camera2" / "same.jpg", content="first")
    target_dir = expected_target_dir(first_file, dst_dir)

    organize_images(
        str(src_dir),
        str(dst_dir),
        str(log_path),
        mode="copy",
        duplicate_detection="strict",
    )

    log_text = log_path.read_text(encoding="utf-8")
    assert "DUP | strict=" in log_text
    assert (target_dir / "same.jpg").exists()
    assert (target_dir / "same_dup1.jpg").exists()


def test_duplicate_report_csv_is_written_for_detected_duplicates(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "strict.log"
    first_file = create_media_file(src_dir / "camera1" / "same_name.jpg", content="first")
    create_media_file(src_dir / "camera2" / "different_name.jpg", content="first")
    target_dir = expected_target_dir(first_file, dst_dir)

    organize_images(
        str(src_dir),
        str(dst_dir),
        str(log_path),
        mode="copy",
        duplicate_detection="strict",
    )

    report_path = work_dir / "duplicate_report.csv"
    assert report_path.exists()

    with report_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 1
    row = rows[0]
    assert row["original_name"] == "different_name.jpg"
    assert row["original_path"].endswith(str(Path("camera2") / "different_name.jpg"))
    assert row["kept_path"].endswith(str(target_dir / "same_name.jpg"))
    assert row["duplicate_method"] == "strict"
    assert row["hash"]
    assert row["duplicate_path"].endswith(str(target_dir / "same_name_dup1.jpg"))


def test_duplicate_names_follow_kept_file_name_sequence(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "strict.log"
    first_file = create_media_file(src_dir / "camera1" / "first_name.jpg", content="first")
    create_media_file(src_dir / "camera2" / "second_name.jpg", content="first")
    create_media_file(src_dir / "camera3" / "third_name.jpg", content="first")
    target_dir = expected_target_dir(first_file, dst_dir)

    organize_images(
        str(src_dir),
        str(dst_dir),
        str(log_path),
        mode="copy",
        duplicate_detection="strict",
    )

    assert (target_dir / "first_name.jpg").exists()
    assert (target_dir / "first_name_dup1.jpg").exists()
    assert (target_dir / "first_name_dup2.jpg").exists()


def test_hash_db_does_not_redirect_files_outside_current_destination(work_dir: Path) -> None:
    first_src = work_dir / "src_first"
    first_dst = work_dir / "dst_first"
    second_src = work_dir / "src_second"
    second_dst = work_dir / "dst_second"
    first_log = work_dir / "first.log"
    second_log = work_dir / "second.log"

    create_media_file(first_src / "same.jpg", content="identical")
    second_file = create_media_file(second_src / "same.jpg", content="identical")
    second_target_dir = expected_target_dir(second_file, second_dst)

    organize_images(
        str(first_src),
        str(first_dst),
        str(first_log),
        mode="copy",
        duplicate_detection="strict",
    )
    organize_images(
        str(second_src),
        str(second_dst),
        str(second_log),
        mode="copy",
        duplicate_detection="strict",
    )

    second_log_text = second_log.read_text(encoding="utf-8")
    assert "DUP | strict=" not in second_log_text
    assert "OK | COPY" in second_log_text
    assert (second_target_dir / "same.jpg").exists()


def test_phash_duplicate_detection_uses_distance_threshold(work_dir: Path) -> None:
    src_dir = work_dir / "src"
    dst_dir = work_dir / "dst"
    log_path = work_dir / "phash.log"
    create_image_file(src_dir / "camera1" / "same.png", color=(255, 0, 0))
    create_image_file(src_dir / "camera2" / "same.png", color=(255, 0, 0))

    organize_images(
        str(src_dir),
        str(dst_dir),
        str(log_path),
        mode="copy",
        duplicate_detection="phash",
        phash_threshold=0,
    )

    log_text = log_path.read_text(encoding="utf-8")
    assert "DUP | phash=" in log_text
