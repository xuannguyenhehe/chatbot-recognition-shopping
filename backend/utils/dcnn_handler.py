import tensorflow as tf
import numpy as np

from backend.process.PretrainedModel import PretrainedModel
from backend.utils.utils import text_cleaner, clean_tweet

models = PretrainedModel()

def predict_dcnn(message):
    """Predict message intent with dcnn model

    Args:
        message (String): Message

    Returns:
        String: Intent of message
    """
    if isinstance(message, str):
        message = [message]
    
    X = [text_cleaner(clean_tweet(_)) for _ in message]
    X = [models.tokenizer.encode(_) for _ in X]
    X = tf.keras.preprocessing.sequence.pad_sequences(
        X, value=0, padding="post", maxlen=121)
    
    pred = models.dcnn_model.predict(X)
    y = [models.classes[np.argmax(_)] for _ in pred]
    return y