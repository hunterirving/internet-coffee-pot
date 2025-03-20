from flask import Flask, send_file, Response
import subprocess
import os
import time

app = Flask(__name__)

WEBCAM_DEVICE = "/dev/video0"  # This may need to be changed depending on your webcam
IMAGE_PATH = "/tmp/coffee_pot.jpg"
TEMP_IMAGE_PATH = "/tmp/coffee_pot_temp.jpg"
WARMUP_FRAMES = 3  # Number of warmup frames to capture

def capture_image():
	"""Capture an image from the webcam with warmup phase"""
	try:
		# Warmup phase - take a few throwaway images to let the camera adjust
		for i in range(WARMUP_FRAMES):
			subprocess.run([
				"fswebcam",
				"--no-banner",
				"-r", "640x480",
				"-d", WEBCAM_DEVICE,
				TEMP_IMAGE_PATH
			], check=True, stderr=subprocess.DEVNULL)  # Hide output during warmup
			
		# Now capture the actual image we'll use
		subprocess.run([
			"fswebcam",
			"--no-banner",
			"-r", "640x480",
			"-d", WEBCAM_DEVICE,
			"-S", "10",  # Skip 10 frames for better quality
			IMAGE_PATH
		], check=True)
		
		return True
	except Exception as e:
		print(f"Error capturing image: {e}")
		return False

@app.route('/')
def coffee_pot():
	"""Serve a fresh image of the coffee pot"""
	if capture_image() and os.path.exists(IMAGE_PATH):
		return send_file(IMAGE_PATH, mimetype='image/jpeg')
	else:
		return Response("Error capturing image", status=500)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)