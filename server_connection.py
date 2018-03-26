import http.client
# import requests
import urllib.parse
import json

# API_KEY = "d03c254e45681731fe6c68a466818160"
# conn = http.client.HTTPSConnection("api.themoviedb.org")


# export_data = {
# 	"page": "1",
# 	"query": "",
# 	"language": "ru",
# 	"api_key":  API_KEY
# }
# payload = "{}"

# export_data["query"] = input()
# data = urllib.parse.urlencode(export_data)

# conn.request("GET", "/3/search/movie?" + data, payload)

# res = conn.getresponse()
# res_data = res.read().decode("utf-8")
# json_load = json.loads(res_data)
# print(json_load)


class APIMethods():

	def __init__(self):
		self.URL_ADDRES = "api.themoviedb.org"
		self.API_KEY = ""
		self.EXPORT_DATA = {
			"page": "1",
			"language": "ru",
			"api_key": self.API_KEY
		}

		self.connection_api = http.client.HTTPSConnection(self.URL_ADDRES)


	def urlencode_to_send(self, data):
		return urllib.parse.urlencode(data)


	def send_request(self, where_to_send, type="GET", payload={}): 
		self.connection_api.request(type, where_to_send, payload)
		result = self.connection_api.getresponse().read().decode("utf-8")
		result_json = json.loads(result)
		return result_json


	def get_movie_by_title(self, title):
		current_data = self.EXPORT_DATA.copy()
		current_data["query"] = title

		formated = self.urlencode_to_send(current_data)
		curent_url = "/3/search/movie?" + formated

		answer = self.send_request(curent_url)
		return answer


	def get_most_popular(self):
		current_data = self.EXPORT_DATA.copy()
		formated_data = self.urlencode_to_send(current_data)
		current_url = "/3/movie/popular?" + formated_data
		answer = self.send_request(current_url)
		return answer

	def get_similar_movie(self, id):
		current_data = self.EXPORT_DATA.copy()
		formated_data = self.urlencode_to_send(current_data)

		current_url = "/3/movie/" + str(id) + "/similar?" + formated_data
		answer = self.send_request(current_url)
		return answer


	def get_now_playing(self):
		current_data = self.EXPORT_DATA.copy()
		formated_data = self.urlencode_to_send(current_data)

		current_url = "/3/movie/now_playing?" + formated_data
		answer = self.send_request(current_url)
		return answer

	# def get_by_

if __name__ == "__main__":
	api = APIMethods()
	birdman_movie = api.get_movie_by_title("Бэтмен")
	bird_id = birdman_movie["results"][0]["id"]

	print()
	print(api.get_similar_movie(bird_id))

	print()
	print(api.get_most_popular())

	print("\n\n")
	print(api.get_now_playing())