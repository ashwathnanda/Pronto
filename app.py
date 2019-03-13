'''

Flask Application which fetches required project based on the requirement provided by the user

'''

from flask import Flask, render_template, request
from flashtext import KeywordProcessor
import pandas as pd
import requests
 
app = Flask(__name__)
 
#renders the index file
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/fetch_code_api', methods = ['GET'])
def fetch_code_api():
	sentence = request.args.get['input']
	#ip is dynamic and wont be the same everytime. Changes everytime EC2 instance is boooted
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
	for i in range(len(l)):
		m = l[i]
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
	for i in range(len(l)):
		if(c == l[i]):
			answer = data['Snippet'][i]
			flag = 1
	if( flag == 0):
		answer = 'File not found'
	
	return render_template('index.html',answer=answer)

#runs the web application with the appropriate port and host
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8080)
