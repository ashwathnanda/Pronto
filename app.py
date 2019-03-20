'''
Flask Application which fetches required project based on the requirement provided by the user
'''

from flask import Flask, render_template, request
from flashtext import KeywordProcessor
import pandas as pd
import requests
from logging.handlers import RotatingFileHandler
from time import strftime
import logging
import traceback


app = Flask(__name__)
 
#renders the index file
@app.route('/')
def index():
	return render_template('index.html')

#Change the IP to the one you are using
@app.route('/fetch_code_api', methods = ['GET','POST'])
def fetch_code_api():
	if(requests.methods == 'POST'):
		sentence = request.form['input']
		resp = requests.post('http://3.209.12.194:8080/' , data = {'req':sentence})
	else:
		sentence = request.args.get['input']
		resp = requests.get('http://3.209.12.194:8080/fetch/{}'.format(sentence))
	answer = resp.text
	return render_template('index.html',answer=answer)

#triggers when the user enters his/her requirement
@app.route('/fetch_code' , methods = ['POST'])
def fetch_code():
	key_processor = KeywordProcessor()
	#reading the data 	
	data = pd.read_csv('dataset/data_tag.csv')
	#flag var to ckeck for correct requirement
	flag = 0
	#converting the tags into a list
	l = list(data['Tag'])
	my_list2 = []
	for i,m in enumerate(l):
		my_list2.extend(m.split(','))
	
	#adding the tags onto the processor
	key_processor.add_keywords_from_list(my_list2)
	
	#function to return the keyword from a sentence
	def return_keyword(word):
		ans = key_processor.extract_keywords(word)
		ans.sort()
		return ans
	
	sentence = request.form['input']
	c = return_keyword(sentence.lower())
	c = ','.join(c)
	for i,item in enumerate(l):
		if(c == item):
			answer = data['Snippet'][i]
			flag = 1
	if( flag == 0):
		answer = 'File not found'
	
	return render_template('index.html',answer=answer)

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

#runs the web application with the appropriate port and host
if __name__ == '__main__':
	handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
	logger = logging.getLogger('werkzeug')
	logger.setLevel(logging.ERROR)
	logger.addHandler(handler)
	app.run(debug=True,port = 8080)