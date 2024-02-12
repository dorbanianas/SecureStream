# Define variables
VENV_NAME := venv
REQUIREMENTS_FILE := requirements.txt

# Create Python virtual environment
venv:
	@echo "Creating Python virtual environment $(VENV_NAME)..."
	python3 -m venv $(VENV_NAME)
	@echo "Python virtual environment $(VENV_NAME) created successfully."

# Install required libraries from requirements.txt
install:
	@echo "Installing required libraries from $(REQUIREMENTS_FILE)..."
	@$(VENV_NAME)/bin/pip install -r $(REQUIREMENTS_FILE)
	@echo "Required libraries installed successfully."

# Shortcut target for setting up the project
setup: venv install
	@echo "Project setup completed successfully."

# Run the anomaly detection script
run_anomaly_detection:
	sh src/run_anomaly_detection.sh

# Help target to display available Makefile targets
help:
	@echo "Available targets:"
	@echo "  - venv: Create Python virtual environment"
	@echo "  - install: Install required libraries from requirements.txt"
	@echo "  - setup: Set up the project (create venv, install libraries, and perform configuration)"
	@echo "  - run_anomaly_detection: Run the anomaly detection script"
	@echo "  - help: Display available Makefile targets"
