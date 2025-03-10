#!/bin/bash

# Define paths
APP_PATH="/PiPaperFrame/app.py"
VENV_PATH="/PiPaperFrame/venv"
SERVICE_PATH="/etc/systemd/system/myapp.service"

# Create systemd service file
echo "Creating systemd service file at $SERVICE_PATH..."
sudo bash -c "cat <<EOF > $SERVICE_PATH
[Unit]
Description=My Python Application
After=network.target

[Service]
Type=simple
User=max
ExecStart=$VENV_PATH/bin/python3 $APP_PATH

[Install]
WantedBy=multi-user.target
EOF"

# Reload systemd to recognize new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service..."
sudo systemctl enable myapp.service

# Optional: Start the service and show status
echo "Starting service..."
sudo systemctl start myapp.service
echo "Service status:"
sudo systemctl status myapp.service