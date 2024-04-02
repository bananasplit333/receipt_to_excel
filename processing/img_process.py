import base64

def encode64(file):
	#Read file data 
	file_data = file.read()

	#Encode the file data as base64
	encoded_data = base64.b64encode(file_data).decode('utf-8')
	
	return encoded_data