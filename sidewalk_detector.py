"""
Splits raw image folders into train/val/test structure for jetson-inference classification training.
"""

import os
import random
import shutil

random.seed(42)

SIDEWALK_SRC = "images_v2"
NOT_SIDEWALK_SRC = "raw_not_sidewalk"

SPLIT = {"train": 0.8, "val": 0.1, "test": 0.1}

def find_images(folder):
    exts = (".jpg", ".jpeg", ".png")
    paths = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(exts):
                paths.append(os.path.join(root, f))
    return paths

def split_and_copy(paths, class_name):
    random.shuffle(paths)
    n = len(paths)
    n_train = int(n * SPLIT["train"])
    n_val = int(n * SPLIT["val"])

    buckets = {
        "train": paths[:n_train],
        "val": paths[n_train:n_train + n_val],
        "test": paths[n_train + n_val:],
    }

    for split_name, file_list in buckets.items():
        out_dir = os.path.join(split_name, class_name)
        os.makedirs(out_dir, exist_ok=True)
        for i, src_path in enumerate(file_list):
            ext = os.path.splitext(src_path)[1]
            dst_path = os.path.join(out_dir, f"{class_name}_{i:05d}{ext}")
            shutil.copyfile(src_path, dst_path)
        print(f"{class_name} -> {split_name}: {len(file_list)} images")

def main():
    if not os.path.isdir(SIDEWALK_SRC):
        raise SystemExit(f"ERROR: '{SIDEWALK_SRC}' folder not found. Run this script from data/sidewalks/")
    if not os.path.isdir(NOT_SIDEWALK_SRC):
        raise SystemExit(f"ERROR: '{NOT_SIDEWALK_SRC}' folder not found. Run this script from data/sidewalks/")

    sidewalk_images = find_images(SIDEWALK_SRC)
    not_sidewalk_images = find_images(NOT_SIDEWALK_SRC)

    print(f"Found {len(sidewalk_images)} sidewalk images")
    print(f"Found {len(not_sidewalk_images)} not_sidewalk images")

    if len(sidewalk_images) == 0 or len(not_sidewalk_images) == 0:
        raise SystemExit("ERROR: one of the source folders has no images. Check paths/extensions.")

    split_and_copy(sidewalk_images, "sidewalk")
    split_and_copy(not_sidewalk_images, "not_sidewalk")

    with open("labels.txt", "w") as f:
        f.write("sidewalk\nnot_sidewalk\n")

    print("\nDone. Folder structure created: train/ val/ test/ and labels.txt written.")

if __name__ == "__main__":
    main()
