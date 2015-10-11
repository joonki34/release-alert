import os
from datetime import date

class Config(object):
	"""docstring for Config"""
	urls = {
		"movie_naver" : "http://movie.naver.com/movie/running/premovie.nhn",
		"music_wiki" : "https://en.wikipedia.org/wiki/List_of_" + str(date.today().year) + "_albums"
	}

	data_dir = os.path.dirname(os.path.realpath("__file__")) + "/data"

	def __init__(self):
		super(Config, self).__init__()

