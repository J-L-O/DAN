import os
import pickle
import shutil

from PIL import Image


def format_wpi():
    dataset_name = "WPI"
    level = "double_page"
    extra_name = "_sem"

    source_fold_path = os.path.join("../raw", dataset_name)
    target_fold_path = os.path.join("../formatted", "{}_{}{}".format(dataset_name, level, extra_name))

    if not os.path.exists(target_fold_path):
        os.mkdir(target_fold_path)

    image_list = find_images(source_fold_path)

    image_splits = image_list[:40], image_list[40:50], image_list[50:]
    splits = {"train": image_splits[0], "valid": image_splits[1], "test": image_splits[2]}

    for split, images in splits.items():
        split_path = os.path.join(target_fold_path, split)
        if not os.path.exists(split_path):
            os.mkdir(split_path)

        copy_images(images, split_path)

    create_pickle(splits, target_fold_path)


def find_images(folder):
    image_list = []
    for root, dirs, files in os.walk(folder):
        images = [os.path.join(root, file) for file in files]
        image_list += images

    return image_list


def copy_images(image_list, target_folder):
    for image_path in image_list:
        image = Image.open(image_path)

        new_size = image.size[0] // 2, image.size[1] // 2
        resized = image.resize(new_size)

        new_path = os.path.join(target_folder, os.path.basename(image_path))
        resized.save(new_path)


def create_pickle(splits, target_folder):
    gt_dict = {}

    for split, images in splits.items():
        gt_dict[split] = {}

        names_only = [os.path.basename(image_path) for image_path in images]

        for name in names_only:
            gt_dict[split][name] = {}

    charset = ['ā', 'e', '.', 'T', 'l', 'ä', '9', 'ß', ' ', 'm', 'Y', '/', 'ⓑ', 'V', '5', '+', 'w', '[', 'ⓐ', 'C',
               'W', 'a', ',', 'J', '2', 'q', '0', 'N', 'R', 'L', '6', 'Ⓢ', 'ⓢ', ':', 'ū', '̈', 'Ⓑ', 'B', 's', 'ⓟ',
               ')', 'M', 'Ⓟ', 'x', 'O', 'y', 'U', 'p', '3', 'Z', 'ⓝ', 'n', 'P', 'G', 'K', '-', '4', '7', 'ē', 'k',
               'z', 'f', 'ÿ', 'r', 'ȳ', 'ü', '¾', 'Ⓝ', '8', '(', 'D', 'h', 'A', '—', 'o', 'u', 'H', 'v', '¬', 'Q',
               ']', 'c', 'ö', 'S', 'ō', 't', 'i', 'b', 'g', 'I', '1', '\n', 'F', 'd', 'E', 'j', '̄', 'Ⓐ', 'Ö']
    output = {"ground_truth": gt_dict, "charset": charset}

    pickle_path = os.path.join(target_folder, "labels.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(output, f)


if __name__ == "__main__":
    format_wpi()
