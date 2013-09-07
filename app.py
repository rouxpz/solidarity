import os
import urllib2
import json
import markov
import twitter
from flask import Flask, request, render_template

app = Flask(__name__)

api = twitter.Api(consumer_key="83I2XxBCw89VpvJzuAySqA",
	consumer_secret="BtCTOAIkX3JhxB5wxZVtKC7JqZS4aUfMuzVVF9Tc8",
	access_token_key="1591338780-eGbh2VC3lglSfehg4bZ0sLXGdqXDnX6G0ua6gKR",
	access_token_secret="WCjZdxeqMTU4pwFb3Us5AxFizRwuszvH3LvfcugQrQ")

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
	app.run()





