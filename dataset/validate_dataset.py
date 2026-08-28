from pathlib import Path
from PIL import Image


# =========================
# Configuration
# =========================

DATASET_DIR = Path("dataset")

SPLITS = ["train", "valid", "test"]

VALID_CLASSES = {0, 1}

CLASS_NAMES = {
    0: "open_palm",
    1: "peace_sign"
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# =========================
# Helper Functions
# =========================

def get_images(images_dir):
    """Return all supported image files."""
    return [
        file
        for file in images_dir.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def validate_label(label_path):
    """
    Validate one YOLO label file.

    YOLO format:
    class_id x_center y_center width height
    """

    errors = []

    try:
        lines = label_path.read_text().splitlines()
    except Exception as e:
        return [f"Cannot read label file: {e}"]

    for line_number, line in enumerate(lines, start=1):

        # Ignore empty lines
        if not line.strip():
            continue

        parts = line.split()

        # YOLO detection must contain exactly 5 values
        if len(parts) != 5:
            errors.append(
                f"Line {line_number}: expected 5 values, got {len(parts)}"
            )
            continue

        # Check class ID
        try:
            class_id = int(parts[0])
        except ValueError:
            errors.append(
                f"Line {line_number}: invalid class ID '{parts[0]}'"
            )
            continue

        if class_id not in VALID_CLASSES:
            errors.append(
                f"Line {line_number}: invalid class ID {class_id}"
            )

        # Check coordinates
        try:
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
        except ValueError:
            errors.append(
                f"Line {line_number}: coordinates must be numbers"
            )
            continue

        values = {
            "x_center": x_center,
            "y_center": y_center,
            "width": width,
            "height": height
        }

        # YOLO normalized coordinates must be between 0 and 1
        for name, value in values.items():
            if not 0 <= value <= 1:
                errors.append(
                    f"Line {line_number}: {name}={value} is outside [0, 1]"
                )

        # Width and height should be greater than zero
        if width <= 0:
            errors.append(
                f"Line {line_number}: width must be > 0"
            )

        if height <= 0:
            errors.append(
                f"Line {line_number}: height must be > 0"
            )

    return errors


def validate_split(split):
    """Validate one dataset split."""

    images_dir = DATASET_DIR / split / "images"
    labels_dir = DATASET_DIR / split / "labels"

    print("\n" + "=" * 60)
    print(f"Checking: {split.upper()}")
    print("=" * 60)

    # Check directories
    if not images_dir.exists():
        print(f"ERROR: Missing directory: {images_dir}")
        return

    if not labels_dir.exists():
        print(f"ERROR: Missing directory: {labels_dir}")
        return

    images = get_images(images_dir)
    labels = list(labels_dir.glob("*.txt"))

    print(f"Images : {len(images)}")
    print(f"Labels : {len(labels)}")

    # -------------------------
    # Check image/label matching
    # -------------------------

    image_names = {
        image.stem
        for image in images
    }

    label_names = {
        label.stem
        for label in labels
    }

    missing_labels = image_names - label_names
    missing_images = label_names - image_names

    if missing_labels:
        print("\nImages without labels:")
        for name in sorted(missing_labels):
            print(f"  - {name}")

    if missing_images:
        print("\nLabels without images:")
        for name in sorted(missing_images):
            print(f"  - {name}")

    if not missing_labels and not missing_images:
        print("✓ Every image has a matching label.")

    # -------------------------
    # Validate label contents
    # -------------------------

    total_errors = 0

    for label_path in labels:

        errors = validate_label(label_path)

        if errors:
            print(f"\nERROR in {label_path}:")
            for error in errors:
                print(f"  - {error}")

            total_errors += len(errors)

    if total_errors == 0:
        print("✓ All labels have valid YOLO format.")
    else:
        print(f"✗ Found {total_errors} label errors.")

    # -------------------------
    # Count classes
    # -------------------------

    class_counts = {
        0: 0,
        1: 0
    }

    for label_path in labels:

        try:
            lines = label_path.read_text().splitlines()

            for line in lines:

                if not line.strip():
                    continue

                parts = line.split()

                if len(parts) != 5:
                    continue

                try:
                    class_id = int(parts[0])
                except ValueError:
                    continue

                if class_id in class_counts:
                    class_counts[class_id] += 1

        except Exception:
            pass

    print("\nClass distribution:")

    for class_id, count in class_counts.items():
        print(
            f"  {class_id} ({CLASS_NAMES[class_id]}): {count}"
        )

    # -------------------------
    # Validate images
    # -------------------------

    corrupted_images = []

    for image_path in images:

        try:
            with Image.open(image_path) as img:
                img.verify()

        except Exception:
            corrupted_images.append(image_path.name)

    if corrupted_images:

        print("\nCorrupted images:")

        for image in corrupted_images:
            print(f"  - {image}")

    else:
        print("✓ All images can be opened.")


# =========================
# Main
# =========================

def main():

    print("\n")
    print("=" * 60)
    print(" YOLO DATASET VALIDATION")
    print("=" * 60)

    if not DATASET_DIR.exists():
        print(f"\nERROR: Dataset directory not found: {DATASET_DIR}")
        return

    for split in SPLITS:
        validate_split(split)

    print("\n" + "=" * 60)
    print(" VALIDATION FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()