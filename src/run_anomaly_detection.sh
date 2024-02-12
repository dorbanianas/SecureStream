#!/bin/bash

# Run cicflowmeter to capture traffic and save it to the flows.csv file
sudo cicflowmeter -i wlan0 -c traffic_data/flows.csv -v > traffic_data/cicflowmeter_output.log 2>&1 &

# remove the checkpoint file if it exists
rm -f traffic_data/last_processed_checkpoint.ckpt

# Activate your Python environment (if necessary)
# source /path/to/your/python/venv/bin/activate

# Run the Python script for anomaly detection
python src/anomaly_detection_script.py

# Deactivate the Python environment (if activated)
# deactivate
