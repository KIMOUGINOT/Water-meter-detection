import os
from PIL import Image
from ultralytics import YOLO
from Cropping import Cropping
from shutil import move, rmtree

class Predict:
    def __init__(self, config):
        """
        Initialize the Predict class with configuration parameters.

        Args:
            config (dict): Configuration dictionary containing paths and model information.
        """
        self.water_meter_model_path = config["water_meter_model"]
        self.digit_model_path = config["digit_model"]
        self.input_dir = config["input_dir"]
        self.cropped_dir = config["cropped_dir"]
        self.output_dir = config["output_dir"]

        os.makedirs(self.cropped_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        # Load models
        self.water_meter_model = YOLO(self.water_meter_model_path)
        self.digit_model = YOLO(self.digit_model_path)

    def predict_water_meter(self):
        """
        Predict and detect water meters in images.
        """
        images_dir = os.path.join(self.input_dir, "images")
        labels_dir = os.path.join(self.input_dir, "labels")
        os.makedirs(labels_dir, exist_ok=True)

        # Specify the output directory for the predictions
        results = self.water_meter_model.predict(
            source=images_dir,
            save_txt=True,
            save_conf=False,
            project=self.input_dir,  # Save in the input directory
            name="water_meter_predictions"  # Subdirectory for predictions
        )

        # Move labels to the expected folder
        predictions_dir = os.path.join(self.input_dir, "water_meter_predictions", "labels")
        if os.path.exists(predictions_dir):
            for label_file in os.listdir(predictions_dir):
                move(os.path.join(predictions_dir, label_file), os.path.join(labels_dir, label_file))
            rmtree(os.path.join(self.input_dir, "water_meter_predictions"), ignore_errors=True)

        print(f"Water meter predictions completed. Labels saved in {labels_dir}.")



    def predict_digit(self):
        """
        Predict digits from cropped water meter images.
        """
        cropped_images_dir = os.path.join(self.cropped_dir, "images")
        labels_dir = os.path.join(self.cropped_dir, "labels")
        output_labels_dir = os.path.join(self.output_dir, "labels")
        output_images_dir = os.path.join(self.output_dir, "images")
        os.makedirs(output_labels_dir, exist_ok=True)
        os.makedirs(output_images_dir, exist_ok=True)

        results = self.digit_model.predict(
            source=cropped_images_dir,
            save_txt=True,
            save_conf=True,
            save=True,  # Save annotated images
            project=self.output_dir,  # Save in the output directory
            name="digit_predictions"  # Subdirectory for predictions
        )

        # Move labels to the expected folder
        predictions_dir = os.path.join(self.output_dir, "digit_predictions", "labels")
        if os.path.exists(predictions_dir):
            for label_file in os.listdir(predictions_dir):
                move(os.path.join(predictions_dir, label_file), os.path.join(output_labels_dir, label_file))

        # Move images to the expected folder
        predictions_images_dir = os.path.join(self.output_dir, "digit_predictions")
        for image_file in os.listdir(predictions_images_dir):
            if image_file.endswith(('.jpg', '.jpeg', '.png')):
                move(os.path.join(predictions_images_dir, image_file), os.path.join(output_images_dir, image_file))

        # Clean up the temporary prediction folder
        rmtree(os.path.join(self.output_dir, "digit_predictions"), ignore_errors=True)

        print(f"Digit predictions completed. Labels saved in {output_labels_dir}, and images saved in {output_images_dir}.")


    def predict(self):
        """
        Perform the full pipeline: predict water meters, crop the data, and predict digits.
        """
        print("Starting water meter detection...")
        self.predict_water_meter()

        print("Cropping water meter regions...")
        cropper = Cropping(input_dir=self.input_dir, output_dir=self.cropped_dir)
        cropper.process_dataset()

        print("Starting digit detection...")
        self.predict_digit()

        print("Pipeline completed. All results saved.")

# Example usage
if __name__ == "__main__":
    import yaml

    # Load configuration
    with open("config/predict.yaml", "r") as file:
        config = yaml.safe_load(file)

    predictor = Predict(config)
    predictor.predict()
