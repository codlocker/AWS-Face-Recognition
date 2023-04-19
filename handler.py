import boto3
import colorama
import face_recognition
import glob
import os
import pickle
from botocore.exceptions import ClientError
from termcolor import cprint

colorama.init()
input_bucket = 'cse546-grp-dynamo-project3-ingress-bucket'
output_bucket = "cse546-grp-dynamo-project3-result-bucket"
encoding_filename = "encoding.dat"

# Validate whether you are in a docker or machine.
environ_key = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

# Initialize variables data_folder for storing files, upload_status to output bucket, CSV File name if created.
data_folder = None
upload_status = False
csvFileName = None

print("Environ Key:", environ_key)

if environ_key:
	cprint("I am in a docker container.", "green")
	data_folder = "/tmp/"
else:
	cprint("I am in a machine.", "blue")
	data_folder = os.getcwd() + "/"

# Function to read the 'encoding' file
def open_encoding(filename):
	file_path = os.path.join(os.getcwd(), filename)
	cprint(f"Encoding file path : {file_path}", "blue")
	file = open(file_path, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):
	try:
		print(event)

		if type(event) == dict:
			file_name = event['queryStringParameters']['file_name']
		else:
			file_name = event

		# 0. Build the baseline
		frames_path = os.path.join(data_folder, "Frames") + "/"
		if not os.path.exists(frames_path):
			os.makedirs(frames_path)


		local_file_path = download_file_s3(file_name)
		encoded_data = open_encoding(encoding_filename)

		cprint(f"Frames folder: {frames_path}", "magenta")
		cmd = f'''ffmpeg -i "{str(local_file_path)}" -r 1 "{str(frames_path)}image-%3d.jpeg" -hide_banner -loglevel error'''

		cprint(f"Executing: {cmd}", "blue")

		# 1. Split video into frames
		os.system(cmd)

		# 2. Face-recog each frame file to get the first face

		fileList = os.listdir(frames_path)

		faceName = ""

		for file in fileList:
			print(f"Located image file : {frames_path}{file}")
			unknown_image = face_recognition.load_image_file(f"{frames_path}{file}")
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

		# 3. Search facename in DynamoDB
		
		result = search_in_dynamodb(facename=faceName)

		# 4. Upload CSV file to S3 bucket.
		if result:
			csvFileName = file_name.split('.')[0] + ".csv"
			csv_file_path = f"{data_folder}{csvFileName}"
			print(f"CSV file at {csv_file_path}")

			with open(f'{csv_file_path}', 'w') as f:
				f.writelines(result)

			upload_csv_to_bucket(
				csv_file=csvFileName)
			upload_status = True

		return result

	except Exception as e:
		print(e)
	finally:
		# 5. Clean Up if Step 4 succeeds
		# Remove all files in Frames folder
		print("Clean up script starts...")
		files = glob.glob(frames_path + "/*")
		for f in files:
			cprint(f"Deleting file {f}", "red")
			os.remove(f)

		# Delete video file
		if file_name:
			cprint(f"Deleting Video file {file_name}", "red")
			os.remove(os.path.join(data_folder, file_name))
		# Delete CSV file
		if csvFileName:
			cprint(f"Deleting CSV file {csvFileName}", "red")
			os.remove(os.path.join(data_folder, csvFileName))


# Define function to download file from S3 bucket
def download_file_s3(file_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(input_bucket)
	local_file_path = os.path.join(data_folder, file_name)

	cprint(f"Local video path : {local_file_path}", "magenta")
	if not os.path.exists(local_file_path):
		cprint("Downloading file...", "blue")
		bucket.download_file(file_name, local_file_path)
	return local_file_path


# Search for facename in Dynamo DB
def search_in_dynamodb(facename):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Student_data')
	if facename:
		response = table.get_item(Key={
			"name": facename
		})

		return f"{response['Item']['name']},{response['Item']['major']},{response['Item']['year']}"
	else:
		return None

# Upload csv file to S3 bucket
def upload_csv_to_bucket(csv_file):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(output_bucket)

	local_file_path = os.path.join(data_folder, csv_file)
	cprint(f"Local CSV path : {local_file_path}", "white")

	if os.path.exists(local_file_path):
		cprint(f'Uploading file to S3 : {output_bucket}', "blue")
		try:
			response = bucket.upload_file(local_file_path, csv_file)
		except ClientError as e:
			cprint(e, "red")
			exit(-1)
	else:
		cprint(f"CSV file : {local_file_path} not found.", "red")
		exit(-1)



# print(face_recognition_handler('test_7.mp4', None))


