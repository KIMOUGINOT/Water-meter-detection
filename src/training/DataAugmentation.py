import os
import random
import yaml
from PIL import Image, ImageEnhance
import shutil

class DataAugmentation:
    def __init__(self, config_path):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

        # Extract parameters from the configuration
        self.input_folder = self.config["input_folder"]
        self.output_folder = self.config["output_folder"]
        os.makedirs(os.path.join(self.output_folder, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.output_folder, "labels"), exist_ok=True)

        self.rotation_range = (
            self.config["augmentation"]["rotation_range"]["min"],
            self.config["augmentation"]["rotation_range"]["max"]
        )
        self.brightness_range = (
            self.config["augmentation"]["brightness_range"]["min"],
            self.config["augmentation"]["brightness_range"]["max"]
        )
        self.augmentation_factor = self.config["augmentation"]["augmentation_factor"]
        self.valid_extensions = set(self.config["valid_extensions"])

    def random_rotation(self, image):
        """Apply random rotation."""
        angle = random.uniform(*self.rotation_range)
        return image.rotate(angle, resample=Image.BICUBIC, expand=True)

    def random_brightness(self, image):
        """Change the brightness of the image."""
        factor = random.uniform(*self.brightness_range)
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    def augment_image(self, image):
        """Apply augmentations to an image."""
        augmented_image = image.copy()
        augmented_image = self.random_rotation(augmented_image)
        augmented_image = self.random_brightness(augmented_image)
        return augmented_image

    def process_images_and_labels(self):
        """Process all images and their labels from the source directory."""
        images_folder = os.path.join(self.input_folder, "images")
        labels_folder = os.path.join(self.input_folder, "labels")
        output_images_folder = os.path.join(self.output_folder, "images")
        output_labels_folder = os.path.join(self.output_folder, "labels")

        # List of valid image files in the source folder
        image_files = [
            f for f in os.listdir(images_folder)
            if os.path.isfile(os.path.join(images_folder, f)) and os.path.splitext(f)[1].lower() in self.valid_extensions
        ]

        # Process each image
        for image_file in image_files:
            image_path = os.path.join(images_folder, image_file)
            label_path = os.path.join(labels_folder, os.path.splitext(image_file)[0] + ".txt")

            # Ensure the label file exists for the current image
            if not os.path.exists(label_path):
                print(f"Warning: Label file not found for {image_file}. Skipping...")
                continue

            # Load the image
            image = Image.open(image_path)

            for i in range(self.augmentation_factor):
                # Augment the image
                augmented_image = self.augment_image(image)

                # Save the augmented image
                base_name, ext = os.path.splitext(image_file)
                augmented_image_name = f"{base_name}_augmented_{i}{ext}"
                augmented_image_path = os.path.join(output_images_folder, augmented_image_name)
                augmented_image.save(augmented_image_path)

                # Duplicate the label file
                augmented_label_name = f"{base_name}_augmented_{i}.txt"
                augmented_label_path = os.path.join(output_labels_folder, augmented_label_name)
                shutil.copy(label_path, augmented_label_path)

        print(f"Data augmentation completed. Images and labels saved in {self.output_folder}")

# Example usage
if __name__ == "__main__":
    config_path = "./src/training/data-augmentation.yaml"  # Path to the configuration file
    augmenter = DataAugmentation(config_path)
    augmenter.process_images_and_labels()
