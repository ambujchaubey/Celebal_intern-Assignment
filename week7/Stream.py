import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt

# Load data and train a simple model for demonstration
boston = load_boston()
X = boston.data
y = boston.target

model = RandomForestRegressor()
model.fit(X, y)

# Streamlit app
st.title('Boston House Price Prediction')

# Sidebar inputs
st.sidebar.header('User Input Features')

def user_input_features():
    data = {}
    for feature_name in boston.feature_names:
        data[feature_name] = st.sidebar.slider(feature_name, float(X[:, boston.feature_names == feature_name].min()), float(X[:, boston.feature_names == feature_name].max()))
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display input features
st.subheader('User Input features')
st.write(input_df)

# Make predictions
prediction = model.predict(input_df)

# Display prediction
st.subheader('Prediction')
st.write(f'Predicted price: ${prediction[0]*1000:.2f}')

# Feature importance
st.subheader('Feature Importance')
importance = model.feature_importances_
indices = np.argsort(importance)

plt.figure(figsize=(8, 6))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importance[indices], align='center')
plt.yticks(range(len(indices)), [boston.feature_names[i] for i in indices])
plt.xlabel('Relative Importance')

st.pyplot(plt)