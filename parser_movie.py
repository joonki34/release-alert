import datetime
import pickle
from bs4 import BeautifulSoup
from bs4.element import Tag
from collections import OrderedDict
from models import Movie

class MovieParser:
	def __init__(self, html_doc):
		soup = BeautifulSoup(html_doc, 'html.parser')
		self.lists = soup.find_all("div", class_="lst_wrap")
		self.result = OrderedDict()

	def save_to_file(self, file_path):
		with open(file_path, 'wb') as output:
			pickle.dump(self.get_upcoming_list(), output, pickle.HIGHEST_PROTOCOL)

	def parse(self):
		for list in self.lists:
			dt = self.get_date_from_tag(list.div.strong)
			if dt is None:
				continue

			movie_list = []
			for child in list.ul.find_all('li'):
				contents = child.dl.find_all('span', 'link_txt')
				movie = Movie()
				movie.title = self.get_title_from_tag(child)
				movie.genre = self.get_genre_list_from_tag(contents[0])
				movie.director = self.get_director_list_from_tag(contents[1])
				try:
					movie.actor = self.get_actor_list_from_tag(contents[2])
				except IndexError:
					movie.actor = ""
				movie_list.append(movie)

			self.result[dt] = movie_list

	def get_date_from_tag(self, tag):
		dt_string = ''
		for child in tag.children:
			if child == '\n':
				continue
			elif child['class'][0] == 'blind' or child['class'][0] == 'dot' or child['class'][0].startswith('w'):
				continue
			else:
				dt_string += child['class'][0][1]
		if len(dt_string) < 8:
			return None
		return datetime.datetime.strptime(dt_string, "%Y%m%d")

	def get_max_date(self):
		max_dt = datetime.datetime.now()
		while max_dt.weekday() != 6:
			max_dt += datetime.timedelta(1)
		max_dt += datetime.timedelta(weeks=1)
		max_dt = max_dt.replace(hour=23, minute=59, second=59, microsecond=0)
		return max_dt

	def get_title_from_tag(self, tag):
		return str(tag.dl.dt.a.string)

	def get_genre_list_from_tag(self, tag):
		return [str(genre.string) for genre in tag.children if type(genre) is Tag]

	def get_director_list_from_tag(self, tag):
		return [str(director.string) for director in tag.children if type(director) is Tag]

	def get_actor_list_from_tag(self, tag):
		return [str(actor.string) for actor in tag.children if type(actor) is Tag]

	def get_upcoming_list(self):
		max_dt = self.get_max_date()
		result = {key: value for key, value in self.result.items() if datetime.datetime.now() < key < max_dt}
		return OrderedDict(sorted(result.items()))

if __name__ == '__main__':
	html_doc = open("/Users/joonki/Downloads/movie2.html",'r').read()
	movie_parser = MovieParser(html_doc)
	movie_parser.parse()
	print(movie_parser.save_to_file())