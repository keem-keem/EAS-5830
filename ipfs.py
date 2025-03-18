import requests
import json

post_url = 'https://ipfs.infura.io:5001/api/v0/add'
api_key = '5099618b27de4148a4046b00a73e0a9e'
api_key_secret = 'JtUcZRbUDpnf4w2rw3pjYWSU+8nvYIeJc+ku+Sn1kUADFQgddOOq5Q'

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	json_data = json.dumps(data)
	
	# Prepare the request payload
	files = {
		'file': ('data.json', json_data)
	}
    
    	# Send a request to Infura's IPFS API to add the file
	response = requests.post(post_url, files=files, auth= (api_key, api_key_secret))
	print(response.text)
	
	cid = response.json().get("Hash")  # Retrieve CID (Content Identifier)
	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
