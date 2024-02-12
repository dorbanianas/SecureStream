# Import necessary libraries
import os
import pandas as pd
import joblib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

sys.path.append(os.path.abspath('../'))

# Define the path to the traffic file
traffic_file_path = 'traffic_data/flows.csv'
# Define the path to the file where the last processed position or timestamp is stored
checkpoint_file_path = 'traffic_data/last_processed_checkpoint.ckpt'
# Define the path to the anomaly history file
anomaly_history_file = 'traffic_data/anomaly_history.csv'

# Load the trained model
model = joblib.load('models/rf_classifier.pkl')  # Change 'your_trained_model.pkl' to the path of your trained model file

# Function to read the last processed position or timestamp from the checkpoint file
def read_checkpoint():
    if os.path.exists(checkpoint_file_path):
        with open(checkpoint_file_path, 'r') as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    else:
        return 0  # Start from the beginning of the file if checkpoint file doesn't exist

# Function to write the last processed position or timestamp to the checkpoint file
def write_checkpoint(position):
    with open(checkpoint_file_path, 'w') as f:
        f.write(str(position))

# Function to write anomalies to the anomaly history CSV file
def write_anomalies_to_csv(anomalies):
    if not os.path.exists(anomaly_history_file):
        with open(anomaly_history_file, 'w') as f:
            f.write("Index,Anomaly,Timestamp\n")  # Write header if file doesn't exist
    df = pd.DataFrame(anomalies)
    df.to_csv(anomaly_history_file, mode='a', index=False, header=False)  # Append to file without writing header again

# Define function to preprocess data and make predictions
def predict_anomalies(new_data):
    # Preprocess the new data
    df = new_data.drop(columns=['dst_port', 'protocol', 'timestamp', 'src_ip', 'dst_ip', 'src_port', 'cwr_flag_count']).sort_index(axis=1)

    # Make predictions on the new data
    predictions = model.predict(df)  # Assuming 'label' is the target column and is not included in the features
    
    # Initialize list to store anomalies
    anomalies = []

    for i, prediction in enumerate(predictions):
        if prediction != 0:
            anomaly_info = {
                "anomaly": prediction,
                "timestamp": new_data.loc[i, 'timestamp']  # Assuming timestamp column exists
            }
            anomalies.append(anomaly_info)
            print(f"🔴 Anomaly detected: {prediction} at {anomaly_info['timestamp']}")
    if not anomalies:
        print("🟢 No anomalies detected")

    return anomalies

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == traffic_file_path:
            print("File modified. Detecting anomalies...")
            
            # Read the last processed position from the checkpoint file
            last_processed_position = read_checkpoint()
            
            # Read the new data from the traffic file, starting from the last processed position
            with open(traffic_file_path, 'r') as f:
                header = f.readline().strip('\n').split(',')

                # Move the file pointer to the last processed position
                f.seek(last_processed_position)

                # Read the data from the file, starting from the last processed position
                data = f.readlines()

                # Combine header with data
                combined_data = [row.strip('\n').split(',') for row in data]

                # Create a DataFrame from the combined data
                new_data = pd.DataFrame(combined_data, columns=header)

                # Retrieve the current file position
                current_position = f.tell()
            
            # Trigger prediction function
            try:
                anomalies = predict_anomalies(new_data)
                if anomalies:
                    write_anomalies_to_csv(anomalies)
            except Exception as e:
                pass
            
            # Update the last processed position in the checkpoint file
            write_checkpoint(current_position)


# Set up file system event observer
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=traffic_file_path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
