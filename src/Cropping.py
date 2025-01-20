import os
from PIL import Image
import shutil

class Cropping:
    def __init__(self, input_dir, output_dir):
        """
        Initialize the cropping class.

        Args:
            input_dir (str): Path to the input directory containing 'images' and 'labels'.
            output_dir (str): Path to the output directory to save cropped images and labels.
        """
        self.input_images_dir = os.path.join(input_dir, "images")
        self.input_labels_dir = os.path.join(input_dir, "labels")
        self.output_images_dir = os.path.join(output_dir, "images")
        self.output_labels_dir = os.path.join(output_dir, "labels")

        # Create output directories if they don't exist
        os.makedirs(self.output_images_dir, exist_ok=True)
        os.makedirs(self.output_labels_dir, exist_ok=True)

    def crop_image(self, image_path, boxes):
        """
        Crop an image based on the provided bounding boxes.

        Args:
            image_path (str): Path to the input image.
            boxes (list): List of bounding boxes in YOLO format [x_center, y_center, width, height].

        Returns:
            list: A list of cropped images.
        """
        image = Image.open(image_path)
        image_width, image_height = image.size
        cropped_images = []

        for box in boxes:
            x_center, y_center, width, height = box

            # Convert YOLO format to pixel format
            x1 = int((x_center - width / 2) * image_width)
            y1 = int((y_center - height / 2) * image_height)
            x2 = int((x_center + width / 2) * image_width)
            y2 = int((y_center + height / 2) * image_height)

            # Crop the image
            cropped = image.crop((x1, y1, x2, y2))
            cropped_images.append(cropped)

        return cropped_images

    def parse_label_file(self, label_path):
        """
        Parse a YOLO label file to extract bounding box information.

        Args:
            label_path (str): Path to the label file.

        Returns:
            list: A list of bounding boxes (class_id, x_center, y_center, width, height).
        """
        boxes = []
        with open(label_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
                boxes.append((class_id, x_center, y_center, width, height))
        return boxes

    def save_cropped_data(self, cropped_images, boxes, image_name):
        """
        Save cropped images and their corresponding labels.

        Args:
            cropped_images (list): List of cropped images.
            boxes (list): List of bounding boxes (class_id, x_center, y_center, width, height).
            image_name (str): Name of the original image.
        """
        for i, (cropped_image, box) in enumerate(zip(cropped_images, boxes)):
            class_id, _, _, _, _ = box

            # Save cropped image
            cropped_image_name = f"{os.path.splitext(image_name)[0]}_crop_{i}.jpg"
            cropped_image_path = os.path.join(self.output_images_dir, cropped_image_name)
            cropped_image.save(cropped_image_path)

            # Save label
            cropped_label_name = f"{os.path.splitext(image_name)[0]}_crop_{i}.txt"
            cropped_label_path = os.path.join(self.output_labels_dir, cropped_label_name)
            with open(cropped_label_path, "w") as label_file:
                label_file.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

    def process_dataset(self):
        """
        Process the dataset: crop images based on labels and save the results.
        """
        for image_file in os.listdir(self.input_images_dir):
            image_path = os.path.join(self.input_images_dir, image_file)
            label_path = os.path.join(self.input_labels_dir, os.path.splitext(image_file)[0] + ".txt")

            if not os.path.exists(label_path):
                print(f"Warning: Label file not found for {image_file}. Skipping...")
                continue

            # Parse label file
            boxes = self.parse_label_file(label_path)

            # Crop the image
            cropped_images = self.crop_image(image_path, [box[1:] for box in boxes])

            # Save cropped images and labels
            self.save_cropped_data(cropped_images, boxes, image_file)

        print(f"Cropping completed. Cropped data saved in {os.path.dirname(self.output_images_dir)}")

# Example usage
if __name__ == "__main__":
    input_dir = "data/augmented"
    output_dir = "data/cropped"
    cropper = Cropping(input_dir, output_dir)
    cropper.process_dataset()
