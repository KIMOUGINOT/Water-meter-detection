import os

import numpy as np

from src.utils import get_file_list


def crop_images(image_dir: str, label_dir: str, output_dir: str, limit=None) -> None:
    os.makedirs(output_dir, exist_ok=True)
    image_files = get_file_list(image_dir, limit=limit)

    for image_file in image_files:
        image_path = 


def crop_image(image: np.ndarray, rect: tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = rect
    return image[y : y + h, x : x + w]
