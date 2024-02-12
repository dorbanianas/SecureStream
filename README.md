# SecureStream Project

This repository contains the source code and notebooks for the SecureStream project, which focuses on anomaly detection in network traffic. The project utilizes Python scripts and Jupyter notebooks for creating models and running anomaly detection algorithms.

## Setup

### Virtual Environment

To set up the project environment, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.

```bash
cd securestream
```

3. Create a Python virtual environment.

```bash
make venv
```

4. Install the required libraries from the `requirements.txt` file.

```bash
make install
```

### Run Anomaly Detection

To run the anomaly detection script, use the following command:

```bash
make run_anomaly_detection
```

This will execute the script responsible for detecting anomalies in network traffic.

### Makefile Targets

- `venv`: Create Python virtual environment.
- `install`: Install required libraries from `requirements.txt`.
- `setup`: Set up the project (create venv, install libraries, and perform configuration).
- `run_anomaly_detection`: Run the anomaly detection script.
- `help`: Display available Makefile targets.

## Notebooks

The repository also contains Jupyter notebooks for creating models and analyzing network traffic data. Feel free to explore these notebooks for further insights into the project.

## Usage of Data and Tools

- **Dataset**: This project utilizes the [`CSE-CIC-IDS2018 dataset`](https://www.unb.ca/cic/datasets/ids-2018.html) for training and evaluating the anomaly detection models. The dataset provides a comprehensive collection of network traffic data with labeled instances of various attacks and normal behavior.

- **cicflowmeter**: Real-time tracking of network traffic is achieved using the [`cicflowmeter`](https://pypi.org/project/cicflowmeter/) tool. This tool captures traffic data and feeds it into the anomaly detection system for analysis and detection of anomalies in real-time.

## Contributors

- [Anas Dorbani](https://github.com/dorbanianas)

If you have any further questions or need additional information, feel free to ask!