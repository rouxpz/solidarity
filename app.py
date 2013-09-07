import os
import urllib2
import json
import markov
import twitter
from flask import Flask, request, render_template

app = Flask(__name__)

api = twitter.Api(consumer_key=os.environ['consumer_key'],
	consumer_secret=os.environ['consumer_secret'],
	access_token_key=os.environ['access_key'],
	access_token_secret=os.environ['access_secret'])

generator = markov.MarkovGenerator(n=3, max=25)

url = "http://www.slutsacrossamerica.org/submissions.json"

response = urllib2.urlopen(url)
js = json.load(response)

data = js['content']

for d in data:
	raw = d['statement']
	statement = raw.encode('ascii', 'ignore')
	if statement  != "Why do you use or support birth control? (200 character max.)":
		statement = statement.strip()
		statement = statement.replace(',', '').replace('.', '').replace('?', '').replace('!', '').replace('  ', ' ').replace(')', '').replace('(', '').replace("I'm a slut because", '')
		words = statement.split(' ')
		line = ' '.join(words)
		generator.feed(line)

@app.route("/")
def about():

	for i in range(1):
		output = generator.generate()
		api.PostUpdate(output)

	return render_template('index.html', output=output)

@app.route("/about")
def index():
	return """This site is a sister project to <a href="http://www.slutsacrossamerica.org">'Sluts Across America'</a>.</br>
	We take all of the text that has been submitted via that project and remix it."""


#start the server
if __name__ == "__main__":
	app.debug = True

	port = int(os.environ.get('PORT', 5000)) #locally runs on 5000, heroku assigns own port
	app.run(host='0.0.0.0', port=port)





