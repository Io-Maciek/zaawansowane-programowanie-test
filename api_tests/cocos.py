import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="validation",
    label_types=["detections"],    # bounding boxy
    classes=["Person"],            # tylko ludzie
    max_samples=1000,
)
# output z tego znajduje sie w katologu /data
