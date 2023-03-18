import boto3
import face_recognition
import os
import pickle
from termcolor import cprint
import colorama

colorama.init()
input_bucket = 'inputbucket-cse546'
output_bucket = "546proj2output"
encoding_filename = "encoding"
frames_path = os.path.join(os.getcwd(), "Frames")

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(file_name):	
	local_file_path = download_file_s3(file_name)
	encoded_data = open_encoding(encoding_filename)

	cprint(f"Frames folder: {frames_path}", "magenta")
	cmd = f'''ffmpeg -i "{str(local_file_path)}" -r 1 "{str(frames_path)}\image-%3d.jpeg" -hide_banner -loglevel error'''

	cprint(f"Executing: {cmd}", "blue")

	# 1. Split video into frames
	os.system(cmd)

	# 2. Face-recog each frame file to get the first face

	fileList = os.listdir(frames_path)

	faceName = ""

	for file in fileList:
		unknown_image = face_recognition.load_image_file(f"{frames_path}/{file}")
		unknown_image_face_encoding = face_recognition.face_encodings(unknown_image)[0]

		cprint(f"Comparing the encoding for file name : {file}", "yellow")

		for name, encoded_value in zip(encoded_data["name"], encoded_data["encoding"]):
			results = face_recognition.compare_faces(unknown_image_face_encoding, [encoded_value])
			# print(name, bool(results[0]))
			if results[0] == True:

				faceName = name
				break
		if faceName:
			break
	

	# Search facename in DynamoDB
	return faceName


# Define function to download file from S3 bucket
def download_file_s3(file_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(input_bucket)
	local_file_path = os.path.join(os.getcwd(), file_name)

	cprint(f"Local video path : {local_file_path}", "magenta")
	if not os.path.exists(local_file_path):
		cprint("Downloading file...", "blue")
		bucket.download_file(file_name, local_file_path)
	return local_file_path


if not os.path.exists(frames_path):
	os.makedirs(frames_path)


# This will change to actual format
# face_recognition_handler(event, context)
print(face_recognition_handler('test_0.mp4'))


