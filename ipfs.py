import requests
import json

pinata_post_url = 'https://api.pinata.cloud/pinning/pinJSONToIPFS'
pinata_api_key = '32fdd3b9e6c8043dc951'
pinata_api_secret = 'f286a48560509c7108e67e2bd2272f62b0a1ca21bf3f170b87388891887db33e'
pinata_jwt_secret = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI5YTVmZTgwNC05NTViLTQ1NzAtOTIwNC1iMDJmY2U1NDI4OTgiLCJlbWFpbCI6ImthcmVlbWVAc2Vhcy51cGVubi5lZHUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiMzJmZGQzYjllNmM4MDQzZGM5NTEiLCJzY29wZWRLZXlTZWNyZXQiOiJmMjg2YTQ4NTYwNTA5YzcxMDhlNjdlMmJkMjI3MmY2MmIwYTFjYTIxYmYzZjE3MGI4NzM4ODg5MTg4N2RiMzNlIiwiZXhwIjoxNzczNzk5OTE0fQ.wHPlRkUSglKqE5KnwpddCjY7e3vIa6hss5MVZP3zTlM'

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	json_data = json.dumps(data)
	
	# Prepare the request payload
	files = {
		'file': ('data.json', json_data)
	}

	headers = {
		"Content-Type": "application/json",
		"pinata_api_key": pinata_api_key,
		"pinata_secret_api_key": pinata_api_secret
	}
    
    	# Convert the dictionary to JSON and send to Pinata
	response = requests.post(pinata_post_url, headers=headers, json={"pinataContent": data})
	print(response.text)
	
	cid = response.json().get("IpfsHash")  # Retrieve CID (Content Identifier)
	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
