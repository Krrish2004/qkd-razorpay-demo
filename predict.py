import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Define the model architecture
class SimpleNN(nn.Module):
    def __init__(self, input_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 1)
        self.dropout = nn.Dropout(p=0.2)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout(x)
        x = torch.tanh(self.fc3(x))
        x = self.fc4(x)
        return x

# Load the dataset to get feature information
df = pd.read_csv('PS_20174392719_1491204439457_log.csv')
df = df.drop(['nameOrig', 'nameDest'], axis=1)
df = pd.concat([df, pd.get_dummies(df['type'], prefix='type')], axis=1)
df = df.drop('type', axis=1)
df['amount_deducted'] = df['oldbalanceOrg'] - df['newbalanceOrig']
df['amount_credited'] = df['newbalanceDest'] - df['oldbalanceDest']
df = df.drop('isFraud', axis=1)

# Load the saved model
input_size = df.shape[1]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNN(input_size).to(device)
model.load_state_dict(torch.load('simple_nn_model_big_dropout_89.pth', map_location=device))
model.eval()

# Load the scaler and fit it to dataset
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# Function to take user input and predict fraud
def predict_fraud():
    print("Enter transaction details:")
    input_data = {}
    for col in df.columns:
        value = float(input(f"Enter {col}: "))
        input_data[col] = value
    
    # Convert input to DataFrame and normalize
    input_df = pd.DataFrame([input_data])
    input_scaled = scaler.transform(input_df)
    input_tensor = torch.tensor(input_scaled, dtype=torch.float32).to(device)
    
    # Get model prediction
    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.sigmoid(output).item()
    
    print("Fraudulent Transaction" if prediction > 0.5 else "Legitimate Transaction")

# Run the prediction function
if __name__ == "__main__":
    print("start")
    predict_fraud()
    print("end")