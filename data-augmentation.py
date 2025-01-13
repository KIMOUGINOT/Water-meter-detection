import os
import random
from PIL import Image, ImageEnhance

# Chemin du dossier contenant les images originales
input_folder = "./data/x_test_augmented/train/images"
# Chemin du dossier où sauvegarder les images augmentées
output_folder = "./data/x_test_augmented/train/augmented_images"

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Paramètres pour l'augmentation
rotation_range = (-30, 30)  # Rotation entre -30 et +30 degrés
brightness_range = (0.5, 1.5)  # Facteur de luminosité entre 0.5 et 1.5
augmentation_factor = 5  # Nombre d'augmentations par image

# Extensions d'images acceptées
valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

# Fonction pour effectuer une rotation aléatoire
def random_rotation(image):
    angle = random.uniform(*rotation_range)
    return image.rotate(angle, resample=Image.BICUBIC, expand=True)

# Fonction pour changer la luminosité
def random_brightness(image):
    factor = random.uniform(*brightness_range)
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Liste des fichiers dans le dossier source
image_files = [
    f for f in os.listdir(input_folder)
    if os.path.isfile(os.path.join(input_folder, f)) and os.path.splitext(f)[1].lower() in valid_extensions
]

# Traitement des images
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    image = Image.open(image_path)

    # Générer plusieurs versions augmentées
    for i in range(augmentation_factor):
        augmented_image = image.copy()

        # Appliquer une rotation aléatoire
        augmented_image = random_rotation(augmented_image)

        # Appliquer un changement de luminosité
        augmented_image = random_brightness(augmented_image)

        # Sauvegarder l'image augmentée
        base_name, ext = os.path.splitext(image_file)
        augmented_image.save(os.path.join(output_folder, f"{base_name}_augmented_{i}{ext}"))

print(f"Augmentation terminée. Images sauvegardées dans {output_folder}")
