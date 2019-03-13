# mini-overflow
A Flask Web Application which fetches code snippet or JAVA Project (.jar) file based on the requirement provided by the User.
<br>
Dependencies installation

```
pip install -r requirements.txt
```

Run the Flask Application

```
python app.py
```
To Run this service as an API run 
```
python api_server.py
```
Now use any API testing tool like POSTMAN to test the api

Or use the Requests library 
```
import requests
code = input('Enter your requirement :')
#test ip. Change it to your own ip
resp = requests.get('http://18.204.37.207:8080/fetch/{}'.format(code))
print 'code: ', resp.text 
```


To build a Docker Image ( cd onto the directory and run the below command or specify the path to the Dockerfile )
```
$ cd ./mini-overflow-master
$ docker build .
```
