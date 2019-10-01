import os
import json
import requests
from tqdm import tqdm

from utils import *


class Model:

	def __init__(self, api_key, model_type):
		self.api_key = api_key
		self.model_type = model_type
		self.host = "https://app.nanonets.com/api/v2/"

	def _create_model(self, categories):

		"""
		function to create model given the categories and model type

		Parameters
		----------
		categories: List[str]
		    List of categories for our model

		Returns
		-------
		server response for the request for uploading urls. You can find response information
		from response.text
		"""

		self.categories = categories
		url = self.host + self.model_type + '/Model/' 
		if not self.model_type == 'ImageCategorization':
			headers = {'Content-Type': "application/json"}
			payload = json.dumps({"categories": categories})
		else: 
			headers = {'Accept': "application/x-www-form-urlencoded"}
			payload = {"categories": categories}
		response =  requests.request("POST", url, 
					     headers=headers, 
					     data=payload,
					     auth=requests.auth.HTTPBasicAuth(self.api_key, ''))
		self.model_id = response.json()["model_id"]
		print("Your Model ID is: ", self.model_id)
		return response

	def _upload_image_file(self, img_path, annotation):

		"""
		function to upload a single file and it's labels for training to a model that 
		has been created.

		Parameters
		----------
		img_path: str
		    path to the image we want to upload

		annotation: 
			list of all labels associated with the image (MLC) or JSON format for OD/OCR 

		Returns
		-------
		server response for the request for uploading urls. You can find response information
		from response.text
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id + '/UploadFile/'
		img_name = img_path.split('/')[-1]
		params = {'file': open(image_path, 'rb'),
				  'modelId': ('', self.model_id),
				  'data' :('', annotation)}
		response = requests.post(url,
					files=params, 
					auth=requests.auth.HTTPBasicAuth(self.api_key, ''))
		return response

	def _train(self):

		"""
		function to create model given the categories and model type as a calss attribute

		Parameters
		----------
		categories: List[str]
		    List of categories for our model

		Returns
		-------
		server response for the request for uploading urls. You can find response information
		from response.text
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id + '/Train/'
		headers = {'authorization': 'Basic %s'%self.api_key}
		params = {'modelId': self.model_id}
		response = requests.request("POST", url,
					    params=params,
					    auth=requests.auth.HTTPBasicAuth(self.api_key, ''))
		print(response.text)
		return response

	def _check_model_state(self):

		"""
		function to check model state given you have the model id as a class attribute

		Parameters
		----------
		None

		Returns
		-------
		server response for the request for uploading urls. You can find response information
		from response.text
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id
		response = requests.request("GET", url,
					auth=requests.auth.HTTPBasicAuth(self.api_key,''))
		state = response.json()["state"]
		status = response.json()["status"]
		if state != 5:
			print("The model isn't ready yet, it's status is:", status)
			print("We will send you an email when the model is ready.")
		else:
			print("Model is ready for predictions.")
		return response

	def _predict_urls(self, image_urls):

		"""
		function to get predictions for images using urls

		Parameters
		----------
		image_urls: List[str]
			urls of the images you want to get predictions for

		Returns
		-------
		JSON repsonse of the prediction 
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id + '/LabelUrls/'
		params = {'modelId': self.model_id, 'urls': image_urls}
		response = requests.post(url,
					auth=requests.auth.HTTPBasicAuth(self.api_key, ''),
					data=params) 
		return response
