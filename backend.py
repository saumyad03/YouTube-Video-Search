import sys
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import tensorflow_text as text
import tensorflow_addons as tfa
import os
import numpy as np
query = sys.argv[1]
text_encoder = keras.models.load_model("text_encoder")
text_encoder.compile()
embedding = text_encoder.predict(query.split())
aggregated_embedding = np.mean(embedding, axis=0).reshape((1, 256))
files = ["embeddings/" + file for file in os.listdir(os.getcwd() + "/embeddings") if file.endswith(".npy")]
scores = []
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2.T)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    similarity = dot_product / (norm_v1 * norm_v2)
    return similarity
for file in files:
    data = np.load(file)
    if file.endswith("txt.npy"):
        text_embedding = np.mean(data, axis=0).reshape((1, 256))
        scores.append(cosine_similarity(aggregated_embedding, text_embedding))
    else:
        scores.append(cosine_similarity(aggregated_embedding, data))
output = []
while len(output) < 3:
    i = scores.index(max(scores))
    video_id = files[i].split("-")[0].split("/")[1]
    if video_id not in output:
        output.append(video_id)
    scores.pop(i)
    files.pop(i)
for id in output:
    print(id)