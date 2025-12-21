import cv2

def get_model() -> cv2.dnn.Net:
    return cv2.dnn.readNetFromTensorflow(model="model/frozen_inference_graph.pb", config="model/model.pbtxt")