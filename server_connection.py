import http.client
import urllib.parse
import json

from logging_class import Loggable

class APIMethods(Loggable):

	def __init__(self):
		self.URL_ADDRES = "api.themoviedb.org"
		self.API_KEY = ""
		self.EXPORT_DATA = {
			"page": "1",
			"language": "ru",
			"api_key": self.API_KEY
		}

		self.connection_api = http.client.HTTPSConnection(self.URL_ADDRES)

		self.image_size = "w300"


	def urlencode_to_send(self, data):
		return urllib.parse.urlencode(data)


	def send_request(self, where_to_send, type_request="GET", payload={}): 
		self.connection_api.request(type_request, where_to_send, payload)
		self.log_it("NEW REQUEST " + where_to_send)
		result = self.connection_api.getresponse().read().decode("utf-8")
		result_json = json.loads(result)
		return result_json


	def get_movie_by_title(self, title):
		current_data = self.EXPORT_DATA.copy()
		current_data["query"] = title
		self.log_it("NEW REQUEST FIND FILM" + title)
		formated = self.urlencode_to_send(current_data)
		curent_url = "/3/search/movie?" + formated

		answer = self.send_request(curent_url)
		print(answer)
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


	def get_movie_upcoming(self):
		current_data = self.EXPORT_DATA.copy()
		formated_data = self.urlencode_to_send(current_data)
		current_url = "/3/movie/upcoming?" + formated_data 
		ans = self.send_request(current_url)

		return ans


	def get_image_url(self, path):
		base_url = "https://image.tmdb.org/t/p/"
		size = self.image_size
		current_url = base_url + size + path
		return current_url


	def get_movie_by_params(self, **params):
		current_data = self.EXPORT_DATA.copy()

		for key in params:
			current_data[key] = params[key]

		formated_data = self.urlencode_to_send(current_data)
		current_url = "/3/discover/movie?" + formated_data
		ans = self.send_request(current_url)
		return ans


	def get_genres(self):
		# Можно сделать иначе. Не нужно постоянно делать запрос, поскольку это будет занимать время
		# А жанры и их id вроде как не меняются
		current_data = self.EXPORT_DATA.copy()
		del current_data["page"]
		formated_data = self.urlencode_to_send(current_data)

		current_url = "/genre/movie/list?" + formated_data
		ans = self.send_request(current_url)


	def get_movies_by_genre(self):
		# Можно использовать get_movie_by_params
		current_data = self.EXPORT_DATA.copy() 
		# TODO: Сформировать нормальную ссылку
		pass

if __name__ == "__main__":
	pass