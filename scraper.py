import time
import os
import urllib.request
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from parser_movie import MovieParser
from parser_music import MusicParser

class Scraper(object):
	"""docstring for Scraper"""
	def __init__(self):
		super(Scraper, self).__init__()
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.scrape, 'cron', hour=4, minute=0, second=0)

	def scrape(self):
		file_path = Config.data_dir

		try:
			os.mkdir(file_path)
		except Exception:
			pass

		file_ext = ".pkl"
		for name, url in Config.urls.items():
			full_file_path = os.path.join(file_path, name + file_ext)
			html_doc = urllib.request.urlopen(url).read()

			parser = None
			if name == 'movie_naver':
				parser = MovieParser(html_doc)
			elif name == 'music_wiki':
				parser = MusicParser(html_doc)
			else:
				raise Exception('Cannot find parser')

			parser.parse()
			parser.save_to_file(full_file_path)

	def start(self):
		self.scheduler.start()

	def shutdown(self):
		self.scheduler.shutdown()

if __name__ == '__main__':
	scraper = Scraper()
	scraper.start()
	while True:
		time.sleep(10)
	scraper.shutdown()
	#scraper.scrape()
