# -*- coding: utf-8 -*-
"""ANN

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hsSNw2JYhqSJxRfs0amukD1YIE02rkMl
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

data = pd.read_csv('survey lung cancer.csv')
data.columns = data.columns.str.strip()
print(data.columns)
print(data.head)
if 'Gender' not in data.columns:
    raise ValueError("The column 'Gender' is not found in the dataset.")

label_encoder_gender = LabelEncoder()
label_encoder_lung_cancer = LabelEncoder()

data['Gender'] = label_encoder_gender.fit_transform(data['Gender'])
data['Lung_Cancer'] = label_encoder_lung_cancer.fit_transform(data['Lung_Cancer'])

X = data.drop('Lung_Cancer', axis=1)
y = data['Lung_Cancer']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(16, input_dim=X.shape[1], activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=0)

y_pred = (model.predict(X_test) > 0.5).astype("int32")

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
print(confusion_matrix(y_test, y_pred))

new_data = {
    'Gender': 'M',
    'Age': 15,
    'Smoking': 0,
    'Yellow': 0,
    'Anxiety': 1,
    'Peer_pressure': 0,
    'Chronic Disease': 0,
    'Fatigue': 0,
    'Allergy': 0,
    'Wheezing': 0,
    'Alcohol': 0,
    'Coughing': 0,
    'Shortness of Breath': 2,
    'Swallowing Difficulty': 0,
    'Chest Pain': 0
}

input_df = pd.DataFrame([new_data])

input_df['Gender'] = label_encoder_gender.transform(input_df['Gender'])
input_df = scaler.transform(input_df)

prediction = (model.predict(input_df) > 0.5).astype("int32")
prediction_label = label_encoder_lung_cancer.inverse_transform(prediction.flatten())

print(f'Lung Cancer Prediction: {prediction_label[0]}')