class Movie:
	def __init__(self):
		self._title = None
		self._genre = []
		self._director = []
		self._actor = []

	@property
	def title(self):
		return self._title
	@title.setter
	def title(self, title):
		self._title = title
	@property
	def genre(self):
	    return self._genre
	@genre.setter
	def genre(self, genre):
		self._genre = genre
	@property
	def director(self):
	    return self._director
	@director.setter
	def director(self, director):
		self._director = director
	@property
	def actor(self):
	    return self._actor
	@actor.setter
	def actor(self, actor):
		self._actor = actor

class Music:
	def __init__(self):
		self._album = None
		self._genre = []
		self._artist = []

	@property
	def album(self):
		return self._album
	@album.setter
	def album(self, album):
		self._album = album
	@property
	def genre(self):
	    return self._genre
	@genre.setter
	def genre(self, genre):
		self._genre = genre
	@property
	def artist(self):
	    return self._artist
	@artist.setter
	def artist(self, artist):
		self._artist = artist
