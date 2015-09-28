from flask import Flask
from flask import render_template
from config import Config
from scraper import Scraper
import pickle
scraper = Scraper()
app = Flask(__name__)

@app.route('/')
def index():
	try:
		input = open("data/movie_naver.pkl", 'rb')
	except FileNotFoundError:
		scraper.scrape()
		input = open("data/movie_naver.pkl", 'rb')
	finally:
		upcoming_list = pickle.load(input)
		input.close()

	return render_template('movie_naver.html', upcoming_list=upcoming_list)

@app.route('/music/wiki')
def music_wiki():
	try:
		input = open("data/music_wiki.pkl", 'rb')
	except FileNotFoundError:
		scraper.scrape()
		input = open("data/music_wiki.pkl", 'rb')
	finally:
		upcoming_list = pickle.load(input)
		input.close()

	return render_template('music_wiki.html', upcoming_list=upcoming_list)

if __name__ == '__main__':
	scraper.start()
	app.run(debug=True)