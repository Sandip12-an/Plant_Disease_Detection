"""
PlantVillage Dataset Preparation Script
========================================
Downloads the PlantVillage dataset (38-class) and splits it into
train / val / test sets at data/processed/{train,val,test}/.

Supports three download modes (auto-detected in order):
  1. Kaggle API  -- fastest if ~/.kaggle/kaggle.json exists
  2. Manual zip  -- pass --zip path/to/downloaded.zip
  3. pip install kaggle + setup guide is printed

Usage:
  python -m ml.prepare_dataset                          # auto-detect
  python -m ml.prepare_dataset --zip ~/Downloads/plantvillage.zip
  python -m ml.prepare_dataset --split-only             # re-split existing raw data
  python -m ml.prepare_dataset --ratios 0.70 0.15 0.15  # custom split ratios

Output structure:
  data/
    raw/plantvillage/        <- original extracted folders
    processed/
      train/<ClassName>/...
      val/<ClassName>/...
      test/<ClassName>/...
"""
import os, sys, json, shutil, zipfile, random, argparse
from pathlib import Path
from typing import List, Tuple

# --- Paths (mirrors ml.src.config) -----------------------------------------
BASE_DIR          = Path(__file__).resolve().parent.parent
RAW_DIR           = BASE_DIR / "data" / "raw" / "plantvillage"
PROCESSED_DIR     = BASE_DIR / "data" / "processed"
TRAIN_DIR         = PROCESSED_DIR / "train"
VAL_DIR           = PROCESSED_DIR / "val"
TEST_DIR          = PROCESSED_DIR / "test"
REGISTRY_DIR      = BASE_DIR / "ml" / "model_registry"
CLASS_LABELS_PATH = REGISTRY_DIR / "class_labels.json"

KAGGLE_DATASET    = "emmarex/plantdisease"   # kaggle datasets download -d emmarex/plantdisease
VALID_EXTS        = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SEED              = 42

# ---------------------------------------------------------------------------

def print_step(msg: str):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def count_images(root: Path) -> int:
    return sum(1 for p in root.rglob("*") if p.suffix.lower() in VALID_EXTS)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_via_kaggle(dest: Path) -> Path:
    """Downloads PlantVillage zip via Kaggle API."""
    try:
        import kaggle
    except ImportError:
        print("[Download] kaggle package not installed. Run: pip install kaggle")
        sys.exit(1)

    dest.mkdir(parents=True, exist_ok=True)
    print(f"[Download] Downloading '{KAGGLE_DATASET}' via Kaggle API...")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(KAGGLE_DATASET, path=str(dest), unzip=False)
    zips = list(dest.glob("*.zip"))
    if not zips:
        raise RuntimeError("Kaggle download completed but no zip file found.")
    return zips[0]


def extract_zip(zip_path: Path, extract_to: Path) -> Path:
    """Extracts a zip archive, returns the root folder of extracted content."""
    print(f"[Extract] Extracting {zip_path.name} -> {extract_to} ...")
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        total = len(zf.namelist())
        for i, member in enumerate(zf.namelist(), 1):
            zf.extract(member, extract_to)
            if i % 5000 == 0 or i == total:
                print(f"  Extracted {i}/{total} files", end="\r")
    print()

    # Find the actual image-root (some zips nest inside a subfolder)
    candidates = [p for p in extract_to.iterdir() if p.is_dir()]
    if len(candidates) == 1:
        inner = candidates[0]
        # If inner contains class sub-folders, use it as root
        sub_candidates = [p for p in inner.iterdir() if p.is_dir()]
        if sub_candidates:
            return inner
    return extract_to


def find_class_dirs(root: Path) -> List[Path]:
    """
    Walks root and finds directories that directly contain image files.
    Handles arbitrary nesting (PlantVillage, PlantDoc, etc.).
    """
    class_dirs = []
    for dirpath in sorted(root.rglob("*")):
        if not dirpath.is_dir():
            continue
        images = [f for f in dirpath.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTS]
        if images:
            class_dirs.append(dirpath)
    return class_dirs


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------

def split_dataset(
    class_dirs: List[Path],
    ratios: Tuple[float, float, float] = (0.70, 0.15, 0.15),
):
    """Copies images from raw class dirs into processed/{train,val,test}."""
    train_r, val_r, _ = ratios
    random.seed(SEED)

    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        split_dir.mkdir(parents=True, exist_ok=True)

    class_names = []
    total_train = total_val = total_test = 0

    for class_dir in class_dirs:
        cls_name = class_dir.name
        class_names.append(cls_name)
        images = sorted([f for f in class_dir.iterdir() if f.suffix.lower() in VALID_EXTS])
        random.shuffle(images)

        n = len(images)
        n_train = int(n * train_r)
        n_val   = int(n * val_r)

        splits = {
            TRAIN_DIR: images[:n_train],
            VAL_DIR:   images[n_train:n_train + n_val],
            TEST_DIR:  images[n_train + n_val:],
        }

        for split_dir, split_imgs in splits.items():
            out_dir = split_dir / cls_name
            out_dir.mkdir(parents=True, exist_ok=True)
            for img_path in split_imgs:
                shutil.copy2(img_path, out_dir / img_path.name)

        n_test = n - n_train - n_val
        total_train += n_train
        total_val   += n_val
        total_test  += n_test
        print(f"  {cls_name:<50s}  train={n_train:4d}  val={n_val:3d}  test={n_test:3d}")

    print(f"\n[Split] Total  train={total_train:,}  val={total_val:,}  test={total_test:,}")
    print(f"[Split] Classes: {len(class_names)}")

    # Save class labels
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    sorted_names = sorted(class_names)
    with open(CLASS_LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_names, f, indent=2)
    print(f"[Split] class_labels.json saved -> {CLASS_LABELS_PATH}")
    return sorted_names


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Prepare PlantVillage dataset")
    parser.add_argument("--zip",        type=str, default=None, help="Path to manually downloaded zip")
    parser.add_argument("--split-only", action="store_true",    help="Skip download; re-split existing raw data")
    parser.add_argument("--ratios",     nargs=3, type=float, default=[0.70, 0.15, 0.15],
                        metavar=("TRAIN", "VAL", "TEST"), help="Train/val/test split ratios")
    args = parser.parse_args()

    ratios = tuple(args.ratios)
    assert abs(sum(ratios) - 1.0) < 1e-6, "Ratios must sum to 1.0"

    # ------------------------------------------------------------------ #
    # Step 1: Locate or download raw data
    # ------------------------------------------------------------------ #
    if args.split_only:
        print_step("Step 1: Skipping download, using existing raw data")
        raw_root = RAW_DIR
    elif args.zip:
        zip_path = Path(args.zip).expanduser().resolve()
        if not zip_path.exists():
            print(f"[Error] Zip not found: {zip_path}")
            sys.exit(1)
        print_step(f"Step 1: Extracting provided zip: {zip_path.name}")
        raw_root = extract_zip(zip_path, RAW_DIR)
    else:
        # Try Kaggle API
        kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
        if kaggle_json.exists():
            print_step("Step 1: Downloading via Kaggle API")
            try:
                zip_path = download_via_kaggle(BASE_DIR / "data" / "raw")
                raw_root = extract_zip(zip_path, RAW_DIR)
            except Exception as e:
                print(f"[Kaggle] Download failed: {e}")
                _print_manual_instructions()
                sys.exit(1)
        else:
            _print_manual_instructions()
            sys.exit(0)

    # ------------------------------------------------------------------ #
    # Step 2: Discover class directories
    # ------------------------------------------------------------------ #
    print_step("Step 2: Discovering class directories")
    class_dirs = find_class_dirs(raw_root)
    if not class_dirs:
        print(f"[Error] No image-containing directories found under: {raw_root}")
        print("  Make sure the zip was extracted correctly.")
        sys.exit(1)
    print(f"[Dataset] Found {len(class_dirs)} class directories  ({count_images(raw_root):,} total images)")

    # ------------------------------------------------------------------ #
    # Step 3: Split into train / val / test
    # ------------------------------------------------------------------ #
    print_step(f"Step 3: Splitting (train={ratios[0]:.0%}  val={ratios[1]:.0%}  test={ratios[2]:.0%})")
    class_names = split_dataset(class_dirs, ratios=ratios)

    # ------------------------------------------------------------------ #
    # Done
    # ------------------------------------------------------------------ #
    print_step("Dataset Ready!")
    print(f"  Train : {TRAIN_DIR}  ({count_images(TRAIN_DIR):,} images)")
    print(f"  Val   : {VAL_DIR}    ({count_images(VAL_DIR):,} images)")
    print(f"  Test  : {TEST_DIR}   ({count_images(TEST_DIR):,} images)")
    print(f"\nNext step -> train the model:")
    print("  python -m ml.src.train --arch mobilenet_v2 --epochs 25 --batch 32\n")


def _print_manual_instructions():
    print("""
  Kaggle API key not found (~/.kaggle/kaggle.json).

  OPTION A — Set up Kaggle API (recommended):
    1. Go to https://www.kaggle.com/settings -> API -> Create New Token
    2. Save the downloaded kaggle.json to: C:\\Users\\SANDIP\\.kaggle\\kaggle.json
    3. pip install kaggle
    4. python -m ml.prepare_dataset

  OPTION B — Download manually:
    1. Go to https://www.kaggle.com/datasets/emmarex/plantdisease
    2. Click Download (plantdisease.zip, ~1.5 GB)
    3. Run: python -m ml.prepare_dataset --zip "C:\\Users\\SANDIP\\Downloads\\plantdisease.zip"
""")


if __name__ == "__main__":
    main()
