import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


#model = tf.keras.models.Sequential()

scores_model = tf.keras.models.load_model("machine_learning_models/tensorflow_karateScoring_regression_model_directory.keras")
print(scores_model)

x_test_scaled = pd.read_excel("data/X_test_scaled.xlsx")
y_test = pd.read_excel("data/y_test.xlsx")
make_prediction = scores_model.predict(x_test_scaled)
predictions = np.round(make_prediction).astype(int)

all_labels = np.arange(11)
cm = confusion_matrix(predictions, y_test, labels=all_labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=all_labels)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion matrix of scores")
plt.show()
