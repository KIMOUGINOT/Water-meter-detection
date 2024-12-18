import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


class ImageProcessor:
    image_paths: list[str] = []
    image_dir = ""
    image: cv2.UMat = None
    filtered_image: cv2.UMat = None

    def __init__(self, image_index=None):
        self.image = None
        if image_index is not None:
            self.load_image(image_index)

    @classmethod
    def set_image_dir(cls, image_dir, limit=10):
        cls.image_dir = image_dir
        cls.image_paths = list(
            map(
                lambda image_file: os.path.join(image_dir, image_file),
                sorted(os.listdir(image_dir)),
            )
        )

    def load_image(self, image_index):
        if image_index < 0 or image_index >= len(self.image_paths):
            raise IndexError("Image index out of range.")
        image_path = self.image_paths[image_index]
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Image at path {image_path} could not be loaded.")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def apply_threshold(self, threshold_value=128):
        if self.image is None:
            raise ValueError("No image loaded.")

        gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        blurred_image = cv2.GaussianBlur(self.image, ksize, 0)
        _, self.image = cv2.adaptiveThreshold(
            img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

    def apply_blur(self, ksize=(5, 5)):
        if self.image is None:
            raise ValueError("No image loaded.")

    def apply_grid_filter(self, grid_size=(10, 10)):
        if self.image is None:
            raise ValueError("No image loaded.")
        h, w, _ = self.image.shape
        grid_image = self.image.copy()
        for i in range(0, h, grid_size[0]):
            for j in range(0, w, grid_size[1]):
                grid_image[i : i + grid_size[0], j : j + grid_size[1]] = np.mean(
                    grid_image[i : i + grid_size[0], j : j + grid_size[1]], axis=(0, 1)
                )
        self.image = grid_image

    def show_image(self, image=None, title="Image"):
        if image is None:
            image = self.image
        if image is None:
            raise ValueError("No image to display.")
        plt.imshow(image, cmap="gray" if len(image.shape) == 2 else None)
        plt.title(title)
        plt.axis("off")
        plt.show()


# Example usage:
# ImageProcessor.set_image_paths(['image1.jpg', 'image2.jpg'], base_path='/path/to/images/')
# processor = ImageProcessor(0)
# processor.show_image()
# blurred_img = processor.apply_blur()
# processor.show_image(blurred_img, title="Blurred Image")
# thresh_img = processor.apply_threshold(128)
# processor.show_image(thresh_img, title="Thresholded Image")
# grid_img = processor.apply_grid_filter()
# processor.show_image(grid_img, title="Grid Filtered Image")
