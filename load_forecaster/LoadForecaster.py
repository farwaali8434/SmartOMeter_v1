import tensorflow as tf


class Forecaster:
    def __init__(self, model_path):
        self.graph = tf.get_default_graph()
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, dataframe):
        with self.graph.as_default():
            predictions = self.model.predict(dataframe)
            for p in predictions:
                yield float(p)
