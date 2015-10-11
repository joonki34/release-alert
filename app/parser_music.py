import datetime
import pickle
from bs4 import BeautifulSoup
from collections import OrderedDict
from pytz import timezone
from app.models import Music

class MusicParser:
	def __init__(self, html_doc):
		soup = BeautifulSoup(html_doc, 'html.parser')
		self.tables = soup.find_all("table", class_="wikitable")
		self.year = next(int(s) for s in soup.title.string.split() if s.isdigit())
		self.result = OrderedDict()

	def save_to_file(self, file_path):
		with open(file_path, 'wb') as output:
			pickle.dump(self.get_upcoming_list(), output, pickle.HIGHEST_PROTOCOL)

	def parse(self):
		header_col_count = 0
		for table in self.tables:
			trs = table.find_all("tr")
			day_list = []
			for idx, tr in enumerate(trs):
				if idx == 0 and tr.find_all("th")[0].string != 'Release date': # if TBD, go onto next table
					break
				if idx == 0: # Skip header (th)
					header_col_count = len(tr.find_all("th"))
					continue
				
				tds = tr.find_all('td')
				music = Music()
				td_start_idx = 0
				if len(tds) == header_col_count:
					day_list = []
					try:
						dt = self.get_date_from_tag(tds[td_start_idx])
					except ValueError:
						dt = None
					td_start_idx += 1

				music.artist = self.get_artist_list_from_tag(tds[td_start_idx]);
				music.album = self.get_album_from_tag(tds[td_start_idx + 1]);
				music.genre = self.get_genre_list_from_tag(tds[td_start_idx + 2]);

				if dt is not None:
					day_list.append(music)
					self.result[dt] = day_list

	def get_max_date(self):
		max_dt = datetime.datetime.now()
		while max_dt.weekday() != 6:
			max_dt += datetime.timedelta(1)
		max_dt += datetime.timedelta(weeks=1)
		max_dt = max_dt.replace(hour=23, minute=59, second=59, microsecond=0)
		return max_dt

	def get_date_from_tag(self, tag):
		result = ''
		date_contents = tag.contents
		for content in date_contents:
			content_string = str(content.string)
			if content_string != 'None':
				result += content_string.strip() + ' '
		result = str(self.year) + ' ' + result.strip()
		dt = datetime.datetime.strptime(result, "%Y %B %d")

		localtz = timezone('US/Pacific') # Assume album release datetime is based on US/Pacific timezone
		dt_aware = localtz.localize(dt)
		dt_localized = dt_aware.astimezone(timezone('Asia/Seoul')) # TODO: localization
		return dt_localized.replace(tzinfo=None)

	def get_artist_list_from_tag(self, tag):
		return [str(x.string) for x in tag.find_all("a")]

	def get_album_from_tag(self, tag):
		return str(tag.string)

	def get_genre_list_from_tag(self, tag):
		return [str(x.string) for x in tag.find_all("a")]

	def get_upcoming_list(self):
		max_dt = self.get_max_date()
		result = {key: value for key, value in self.result.items() if datetime.datetime.now() < key < max_dt}
		return OrderedDict(sorted(result.items()))

if __name__ == '__main__':
	html_doc = open("/Users/joonki/Downloads/music.html",'r').read()
	music_parser = MusicParser(html_doc)
	music_parser.parse()
	print(music_parser.get_upcoming_list())
