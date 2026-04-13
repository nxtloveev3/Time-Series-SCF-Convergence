import pandas as pd
import numpy as np
from pathlib import Path
import os
from sklearn import preprocessing as p
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, classification_report, f1_score, roc_auc_score, roc_curve, precision_recall_curve, auc, precision_score, recall_score, average_precision_score, r2_score, mean_squared_error

def train_gbc(model_size, optimized_params='default'):
    # 1. Path Management
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent 
    data_path = str(project_root/"Data"/"feature_sets")

    train = pd.read_csv(os.path.join(data_path, model_size + '_train.csv'))

    X_train = train.iloc[:, :-1]
    y_train = train.iloc[:, -1]
    
    min_max_scaler = p.MinMaxScaler() 
    min_max_scaler.fit(X_train)  

    X_train_scaled = min_max_scaler.transform(X_train)

    if optimized_params == 'optimized':
        optimized_params = {'iSmall': {'n_estimators': 100, 'learning_rate': 0.05, 'max_depth': 4, 'min_samples_leaf': 6, 'random_state': 523},
                            'iMedium': {'n_estimators': 200, 'learning_rate': 0.05, 'max_depth': 6, 'subsample': 0.8, 'min_samples_leaf': 4, 'random_state': 523},
                            'iLarge': {'n_estimators': 200, 'learning_rate': 0.05, 'max_depth': 8, 'subsample': 0.9, 'min_samples_leaf': 4, 'random_state': 523}}
        params = optimized_params[model_size]
    elif optimized_params == 'default':
        params == None
    else:
        params = optimized_params[model_size]

    gbc = GradientBoostingClassifier(params)

    gbc.fit(X_train_scaled, y_train)

    return gbc, min_max_scaler

def finetune_threshold(model_size, gbc, min_max_scaler):
    # 1. Path Management
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent 
    data_path = str(project_root/"Data"/"feature_sets")

    val = pd.read_csv(os.path.join(data_path, model_size + '_train.csv'))
    test = pd.read_csv(os.path.join(data_path, model_size + '_test.csv'))

    X_val = val.iloc[:, :-1]
    y_val = val.iloc[:, -1]

    X_test = test.iloc[:, :-1]
    y_test = test.iloc[:, -1]

    # Scale using the **original** scaler -------------------------------
    X_val = min_max_scaler.transform(X_val)
    X_test  = min_max_scaler.transform(X_test)

    p_val  = gbc.predict_proba(X_val )[:, 1]
    p_test = gbc.predict_proba(X_test)[:, 1]

    precision, recall, thr = precision_recall_curve(y_val, p_val)
    f1_scores = 2*precision*recall / (precision+recall + 1e-12)
    best_thr  = thr[np.argmax(f1_scores)]
    print(f"chosen threshold = {best_thr:.3f}")

    y_pred = (p_test >= best_thr).astype(int)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred, digits=3))
    print("ROC-AUC =", roc_auc_score(y_test, p_test),
        " PR-AUC =", average_precision_score(y_test, p_test))

def main():