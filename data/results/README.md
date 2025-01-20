# Output Directory

This directory contains the output of the model.

## Structure
- `images/`: Contains the raw images of the dataset.
  - Each image corresponds to a specific sample and is used as input for the training and testing of models.
  - Supported formats: `.jpg`, `.jpeg`, `.png`.

- `labels/`: Contains the annotation files for the corresponding images.
  - Each annotation file is a `.txt` file with the same name as the corresponding image.
  - The file contains bounding box information in YOLO format:
    ```
    <class_id> <x_center> <y_center> <width> <height>
    ```
    Where:
      - `class_id` is the integer representing the class.
      - `x_center`, `y_center`, `width`, and `height` are normalized values (between 0 and 1).

## Example
- Image file: `images/sample.jpg`
- Corresponding label file: `labels/sample.txt`
