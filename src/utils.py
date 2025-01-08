import os

import cv2
import matplotlib.pyplot as plt


def get_file_list(image_dir, limit=None):
    image_list = sorted(os.listdir(image_dir))
    if limit:
        image_list = image_list[:limit]
    return image_list


def show_image_with_title(image, title, rectangle=None):
    """Affiche une image avec un titre et un rectangle facultatif."""
    if rectangle:
        x1, y1, x2, y2 = rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(6, 6))
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis("off")
    plt.show()
