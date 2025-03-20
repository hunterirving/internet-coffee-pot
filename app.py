from flask import Flask, send_file, Response
import subprocess
import os
import time
from PIL import Image, ImageEnhance

app = Flask(__name__)

WEBCAM_DEVICE = "/dev/video0"  # This may need to be changed depending on your webcam
IMAGE_PATH = "/tmp/coffee_pot.jpg"
TEMP_IMAGE_PATH = "/tmp/coffee_pot_temp.jpg"
PROCESSED_IMAGE_PATH = "/tmp/coffee_pot_processed.jpg"
WARMUP_FRAMES = 3  # Number of warmup frames to capture
CONTRAST_FACTOR = 1.5  # Adjust this value to control contrast enhancement

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

def enhance_image():
	"""Enhance the contrast of the captured image"""
	try:
		# Open the original image
		img = Image.open(IMAGE_PATH)
		
		# Create an enhancer and boost the contrast
		enhancer = ImageEnhance.Contrast(img)
		enhanced_img = enhancer.enhance(CONTRAST_FACTOR)
		
		# Save the enhanced image
		enhanced_img.save(PROCESSED_IMAGE_PATH)
		
		return True
	except Exception as e:
		print(f"Error enhancing image: {e}")
		return False

@app.route('/')
def coffee_pot():
	"""Serve a fresh image of the coffee pot"""
	if capture_image() and os.path.exists(IMAGE_PATH):
		if enhance_image() and os.path.exists(PROCESSED_IMAGE_PATH):
			return send_file(PROCESSED_IMAGE_PATH, mimetype='image/jpeg')
		else:
			# Fall back to the original image if enhancement fails
			return send_file(IMAGE_PATH, mimetype='image/jpeg')
	else:
		return Response("Error capturing image", status=500)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)