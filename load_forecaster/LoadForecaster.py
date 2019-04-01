import tensorflow as tf


class Forecaster:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, dataframe):
        return [float(p) for p in self.model.predict(dataframe)]
