
from .extract_embeddings import extract_embeddings
from .recognize_video import recognize_video
from .train_model import train_model


class FaceDetection():

    def __init__(self):
        pass
    def full_model(self):
        extract_embeddings()
        train_model()
    def run_video_test(self,video_input):
        return recognize_video(video_input)
    def run_video(self,video_input):
        return recognize_video(video_input)

