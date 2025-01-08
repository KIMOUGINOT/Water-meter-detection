import os

from ultralytics import YOLO  # type: ignore


def train_yolo(
    config_path: str,
    output_dir: str,
) -> None:
    os.makedirs(output_dir, exist_ok=True)

    model = YOLO("yolo11n.pt")

    model.train(
        data=config_path,
        epochs=50,
        batch=16,
        imgsz=640,
        project=output_dir,
        name="fine_tuned_yolo",
        pretrained=True,
        device="cpu",
    )


if __name__ == "__main__":
    config_path = os.path.abspath("../../configs/train_config.yaml")
    output_dir = os.path.abspath("../../models/yolo_finetune")

    train_yolo(config_path, output_dir)
