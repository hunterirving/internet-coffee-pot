#!/bin/bash

# Internet Coffee Pot Setup Script
# https://github.com/hunterirving/internet-coffee-pot

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "Please run as root (use sudo)"
	exit 1
fi

echo "=== Internet Coffee Pot Setup ==="
echo "Installing required packages..."

# Update and install dependencies
apt update
apt install -y python3-flask fswebcam python3-pip python3-pil

# Get the directory where the setup script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create the service file
echo "Creating systemd service..."
cat > /etc/systemd/system/coffee_cam.service << EOF
[Unit]
Description=Coffee Pot Webcam Service
After=network.target

[Service]
User=root
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Check if webcam is present
echo "Checking for webcam..."
if [ ! -e /dev/video0 ]; then
	echo "Warning: No webcam detected at /dev/video0"
	echo "You may need to adjust the WEBCAM_DEVICE variable in app.py"
	
	# Check for other video devices
	OTHER_DEVICES=$(ls /dev/video* 2>/dev/null)
	if [ -n "$OTHER_DEVICES" ]; then
		echo "Found other video devices: $OTHER_DEVICES"
		echo "You may need to update the WEBCAM_DEVICE variable in app.py to one of these."
	fi
else
	echo "Webcam detected at /dev/video0"
fi

# Enable and start the service
echo "Enabling and starting service..."
systemctl enable coffee_cam.service
systemctl start coffee_cam.service

# Get the IP address for easy access
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo "=== Setup Complete! ==="
echo "Your Coffee Pot webcam is now running."
echo "Access it at: http://$IP_ADDRESS"
echo ""
echo "If you need to make changes, edit $SCRIPT_DIR/app.py"
echo "To restart the service: sudo systemctl restart coffee_cam.service"
echo "To view logs: sudo journalctl -u coffee_cam.service"