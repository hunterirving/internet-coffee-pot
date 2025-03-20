# Internet Coffee Pot

An homage to the famous [Trojan Room Coffee Pot](https://en.wikipedia.org/wiki/Trojan_Room_coffee_pot), the first webcam on the Internet.

## About the Original Trojan Room Coffee Pot

<img src="readme_images/webcamcoffee.jpeg"><br>

As Quentin Stafford-Fraser, one of project's creators, [described it](https://www.cl.cam.ac.uk/coffee/qsf/coffee.html):

> <i>Some members of the 'coffee club' lived in other parts of the building and had to navigate several flights of stairs to get to the coffee pot; a trip which often proved fruitless if the all-night hackers of the Trojan Room had got there first. This disruption to the progress of Computer Science research obviously caused us some distress, and so XCoffee was born.</i>

<br><img src="readme_images/xcoffee.gif">

## About This Project

This implementation uses a USB webcam and a Raspberry Pi Zero W (or any other machine you have lying around) to serve images of your coffee pot (or anything else) over your local network.

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hunterirving/internet-coffee-pot.git
cd internet-coffee-pot
```

### 2. Run the Setup Script

```bash
chmod +x setup.sh
sudo ./setup.sh
```

The setup script will:
- Install all required dependencies
- Configure the service to start on boot
- Start the service immediately

### 3. Access Your Coffee Pot

Open a web browser and navigate to:

```
http://[your-pi-ip-address]
```

That's it! Your days of walking upstairs to check for fresh coffee should now be well behind you.

## Manual Installation (Alternative)

If you prefer to install manually:

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-flask fswebcam

# Clone the repository
git clone https://github.com/hunterirving/internet-coffee-pot.git
cd internet-coffee-pot

# Set up the service
sudo cp coffee_cam.service /etc/systemd/system/
sudo systemctl enable coffee_cam.service
sudo systemctl start coffee_cam.service
```

## Troubleshooting

### Check Webcam Detection

```bash
ls -l /dev/video*
```

If no devices are listed:

```bash
sudo apt install -y v4l-utils
v4l2-ctl --list-devices
```

### Check Service Status

```bash
sudo systemctl status coffee_cam.service
```

### View Service Logs

```bash
sudo journalctl -u coffee_cam.service
```

### Changing Webcam Device

If your webcam isn't detected at `/dev/video0`, you'll need to edit the `app.py` file:

```bash
sudo nano app.py
```

Change the `WEBCAM_DEVICE` variable to match your camera (e.g., `/dev/video1`).

### Modifying Image Resolution

To change the image resolution, modify the `-r` parameter in the `fswebcam` commands within `app.py`. The default is 640x480.

## License

<a href="LICENSE">GPLv3</a>
