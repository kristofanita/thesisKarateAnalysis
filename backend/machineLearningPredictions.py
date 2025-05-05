import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
#from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
#import matplotlib.pyplot as plt
from backend import global_vars


#model = tf.keras.models.Sequential()
def get_current_punch_scores():
    minmax_sc_fit = joblib.load("/home/karate/karateProjectFullstack/machine_learning_models/min_max_scaler.pkl")
    scores_model = tf.keras.models.load_model("machine_learning_models/tensorflow_karateScoring_regression_model_directory.keras")
    #print(scores_model)

    #x_test_scaled = pd.read_excel("data/X_test_scaled.xlsx")
    x_test = global_vars.currentMeasurementStats.copy()
    #cols_not_needed = [col for col in x_test.columns if 'Acc' in col]
    #print(cols_not_needed)
    #x_test.drop(columns=cols_not_needed, inplace=True)
    print(x_test)
    
    x_test.drop(columns=['name'], inplace=True)
    print(x_test.columns)
    try:
        x_test_scaled = pd.DataFrame(minmax_sc_fit.transform(x_test), columns=x_test.columns)
    except  ValueError as e:
        print(e)
    #TODO: x_test helyett kell: global_vars.currentMeasurementStats
    #TODO: scalelni kell a: global_vars.currentMeasurementStats-t (standard scale, fittrain... de majd ugyanarra kell scalelni mint a training datasetet)

    #TODO: nem kell az y_test, sem a confusion matrixek....
    #TODO: csak vissza kell terni az uj utesek score-jainak listajaval, ebbol valszeg egy atlagot kene visszaadjak
    make_prediction = scores_model.predict(x_test_scaled)
    predictions = np.round(make_prediction.ravel()).astype(int)

    """
    y_test = pd.read_excel("data/y_test.xlsx")
    all_labels = np.arange(11)
    cm = confusion_matrix(predictions, y_test, labels=all_labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=all_labels)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion matrix of scores")
    plt.show()
    """
    return predictions
