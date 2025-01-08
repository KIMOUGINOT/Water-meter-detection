import numpy as np


def get_yolo_rect(image: np.ndarray, label_path: str) -> tuple[int, int, int, int]:
    img_height, img_width = image.shape[:2]
    with open(label_path, "r") as f:
        line = f.readline()
        _, x_center, y_center, width, height = map(float, line.split())

        x_center_px = int(x_center * img_width)
        y_center_px = int(y_center * img_height)
        w_pixel = int(width * img_width)
        h_pixel = int(height * img_height)

        x = x_center_px - w_pixel // 2
        y = y_center_px - h_pixel // 2

        return x, y, w_pixel, h_pixel
