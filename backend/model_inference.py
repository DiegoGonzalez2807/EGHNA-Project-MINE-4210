from tensorflow import keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image
import numpy as np

FIBROSIS_CLASSES = ["F0", "F1", "F2", "F3", "F4"]

MODEL_PATH = "model/model.keras"

_model = None
_input_size = (224, 224)


def load_eghna_model():
    global _model

    if _model is None:
        _model = keras.models.load_model(MODEL_PATH)
        print("Modelo cargado.")
    return _model


def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.resize(_input_size)

    arr = np.array(image).astype("float32")

    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)

    arr = np.expand_dims(arr, axis=0)  # (1, H, W, C)

    arr = preprocess_input(arr)

    return arr


def predict_fibrosis_stage(image: Image.Image) -> str:
    model = load_eghna_model()
    x = preprocess_image(image)

    preds = model.predict(x)
    class_idx = int(np.argmax(preds, axis=1)[0])

    fibrosis_stage = FIBROSIS_CLASSES[class_idx]

    return fibrosis_stage