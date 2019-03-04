from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
 
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/fetch_code' , methods = ['POST'])
def fetch_code():
	from flashtext import KeywordProcessor
	import pandas as pd
	key_processor = KeywordProcessor()
	
	data = pd.read_csv('data_tag.csv')
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
	
	return render_template('result.html',answer=answer)

if __name__ == '__main__':
    app.run(host = '0.0.0.0' , debug = True , port = 8080)