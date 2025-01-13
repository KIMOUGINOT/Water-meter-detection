import os
import random
import yaml
from PIL import Image, ImageEnhance

class DataAugmentation:
    def __init__(self, config_path):
        # Charger la configuration
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

        # Extraire les paramètres depuis la configuration
        self.input_folder = self.config["input_folder"]
        self.output_folder = self.config["output_folder"]
        os.makedirs(self.output_folder, exist_ok=True)

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
        """Applique une rotation aléatoire."""
        angle = random.uniform(*self.rotation_range)
        return image.rotate(angle, resample=Image.BICUBIC, expand=True)

    def random_brightness(self, image):
        """Change la luminosité de l'image."""
        factor = random.uniform(*self.brightness_range)
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    def augment_image(self, image):
        """Applique des augmentations à une image."""
        augmented_image = image.copy()
        augmented_image = self.random_rotation(augmented_image)
        augmented_image = self.random_brightness(augmented_image)
        return augmented_image

    def process_images(self):
        """Traite toutes les images du dossier source."""
        # Liste des fichiers valides dans le dossier source
        image_files = [
            f for f in os.listdir(self.input_folder)
            if os.path.isfile(os.path.join(self.input_folder, f)) and os.path.splitext(f)[1].lower() in self.valid_extensions
        ]

        # Traitement des images
        for image_file in image_files:
            image_path = os.path.join(self.input_folder, image_file)
            image = Image.open(image_path)

            for i in range(self.augmentation_factor):
                augmented_image = self.augment_image(image)

                # Sauvegarder l'image augmentée
                base_name, ext = os.path.splitext(image_file)
                augmented_image.save(os.path.join(self.output_folder, f"{base_name}_augmented_{i}{ext}"))

        print(f"Augmentation terminée. Images sauvegardées dans {self.output_folder}")

# Exemple d'utilisation
if __name__ == "__main__":
    config_path = "config.yaml"  # Chemin vers le fichier de configuration
    augmenter = DataAugmentation(config_path)
    augmenter.process_images()
