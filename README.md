# Water Meter Digit Detection

This project focuses on automating the detection of water meter digits using YOLO-based object detection models. The pipeline is designed to first detect water meters in images and then recognize the digits displayed on them. The project includes data augmentation, fine-tuning of YOLO models, and evaluation of their performance.

---

## Project Structure

The repository is organized as follows:

```
.
├── data/
│   ├── augmented/         # Augmented dataset (images and labels)
│   ├── cropped/           # Cropped data containing only digits
│   ├── output/            # Output files from the trained models (predictions, metrics, etc.)
│   ├── raw/               # Original dataset (images and labels)
│   └── README.md          # Documentation for the dataset directories
├── models/                # YOLO models used for detection and digit recognition
├── src/                   # Scripts for data augmentation, training, and evaluation
├── README.md              # Main project documentation
└── requirements.txt       # Python dependencies
```

---

## Objectives

1. **Water Meter Detection**:
   - Detect the location of the water meter in the image using a YOLO model fine-tuned on labeled data.
   
2. **Digit Recognition**:
   - Recognize and classify the digits displayed on the water meter using another YOLO model.
   - Address the challenges of digit recognition through data augmentation and fine-tuning.

3. **Data Augmentation**:
   - Generate additional data to improve model robustness using transformations like rotation, brightness adjustments, and more.

---

## Prerequisites

- **Python**: Ensure Python 3.8 or higher is installed.
- **Dependencies**: Install required packages using:
  ```bash
  pip install -r requirements.txt
  ```

---

## Usage

### 1. Data Preparation
- Place the original dataset in `data/raw/`:
  - Images in `data/raw/images/`.
  - Corresponding YOLO format labels in `data/raw/labels/`.

### 2. Data Augmentation
Run the augmentation script to generate augmented images and labels:
```bash
python scripts/data_augmentation.py --config data-augmentation.yaml
```
The augmented data will be saved in `data/augmented/`.

### 3. Model Training
Train the YOLO models using the prepared dataset:
```bash
python scripts/train_yolo.py --config config.yaml
```

### 4. Model Evaluation
Evaluate the trained model's performance:
```bash
python scripts/evaluate_model.py --model models/yolo_finetuned.pt
```

### 5. Prediction
Use the trained model to predict on new images:
```bash
python scripts/predict.py --model models/yolo_finetuned.pt --input ./data/new_images
```

---

## Results

- **Water Meter Detection**: 
  - High accuracy in detecting water meters under various conditions.
  - Precision, recall, and F1-scores achieved during evaluation.

- **Digit Recognition**: 
  - Performance was limited due to the lack of fine-tuning on our specific dataset.
  - Future improvements will focus on proper labeling and model refinement.

---

## Improvement

 **Model Optimization**:
   - Experiment with other architectures or transfer learning techniques to improve detection accuracy.

---

## Contributors

- Kilian Mouginot
- Romain Bourdain
- Enzo Bergamini
- Florin Baumann

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments

- YOLO models were fine-tuned using the framework provided by [Ultralytics](https://github.com/ultralytics/yolov5).
- Special thanks to open datasets and GitHub repositories for pre-trained digit recognition models.
