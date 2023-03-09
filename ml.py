import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the data from the file
data = np.loadtxt('C:/Users/MatthewCurreri/Documents/3n+1/high_scores.txt', delimiter=',')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[:, 0], data[:, 1], test_size=0.2, random_state=42)

# Train a Random Forest regression model on the training set
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train.reshape(-1, 1), y_train)

# Evaluate the model on the testing set
score = model.score(X_test.reshape(-1, 1), y_test)
print('R^2 score:', score)

import tkinter as tk

# Define a function to run the prediction and update the label
def predict():
    start_num = int(entry.get())
    prediction = model.predict([[start_num]])
    result_label.config(text='Predicted accompanying number: ' + str(int(prediction[0])))

# Create the main window
window = tk.Tk()
window.title('Collatz Conjecture Predictor')

# Create the label and entry box for the starting number
start_label = tk.Label(window, text='Starting number:')
start_label.grid(row=0, column=0)
entry = tk.Entry(window)
entry.grid(row=0, column=1)

# Create the button to run the prediction
button = tk.Button(window, text='Predict', command=predict)
button.grid(row=1, column=0, columnspan=2)

# Create the label to display the predicted accompanying number
result_label = tk.Label(window, text='Predicted accompanying number:')
result_label.grid(row=2, column=0, columnspan=2)

# Start the main event loop
window.mainloop()
