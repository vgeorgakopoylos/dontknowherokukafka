import json
import configparser
import os
import requests
import json
import SimpleHTTPServer
import SocketServer

#function definitions start
def initialization():
	global relDir;
	global version;
	global mainURL;
	global config;
	global apiKey;
	global language;
	global imageURL;
	global imageWidth;
	config = configparser.ConfigParser();
	relDir = os.path.dirname(__file__);
	config.read(relDir+'\conf\configuration.cfg');	
	version = config.get('General','version3');
	mainURL = config.get('General','mainurl');
	apiKey = config.get('General','apikeyV3');
	language = config.get('General','language');
	imageURL = config.get('General','imageURL');
	imageWidth = config.get('General','imageWidth');

def urlBuilder(methdName, paramerers):
	if config.get('Method Types',methdName) == 'General':
		url = mainURL + version + config.get('Method Suffix',methdName)+config.get('Methods',methdName)+'?'+'api_key='+apiKey+'&language='+config.get('General','language')+paramerers;
		return url;
def apiCalls(url):
	response = requests.get(url);
	if (response.status_code!=200):
		raise Exception("API Call was not completed correctly. Status Code returned:"+str(response.status_code));
	return response;

#function definitions end
def upcomingMovies(moviepage=1):
	initialization();
	
	html = '<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="mystyle.css"></head><body><div class="centered"><table>'
		
	rowChange = 1;

	upcomingURL = urlBuilder('upcoming','&page='+str(moviepage));
	response = apiCalls(upcomingURL);
	upcomingMoviesOverall = json.loads(response.text);
	upcomingMoviesPages = upcomingMoviesOverall['total_pages'];
	upcomingMovies = upcomingMoviesOverall['results'];
		
	for movie in upcomingMovies:
		if rowChange == 1:
			html = html+'<tr>';
		html = html + '<td><a href=\"movieDesc?movieid='+str(movie['id'])+'\">'+movie['title']+'</a></td>';
		#html = html +  "<img src=\""+imageURL+imageWidth+movie['poster_path']+"\"></tr>"
		
		if rowChange==2:
			html = html+'</tr>';
			rowChange = 0;
		rowChange = rowChange+1;
		
	
	html = html + '<tr align="center"><td>';
	
	
	for i in range(1,11):
		if i<=5:
			if upcomingMoviesPages-moviepage<=10 and moviepage-2<=0:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(i)+'\">'+str(i)+'</a>  ';
			if upcomingMoviesPages-moviepage<=10 and moviepage-2>0:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(moviepage-2+i)+'\">'+str(moviepage-2+i)+'</a>  ';				
			if upcomingMoviesPages-moviepage>10 and moviepage-2<=0:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(i)+'\">'+str(i)+'</a>  ';
			if upcomingMoviesPages-moviepage>10 and moviepage-2>0:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(moviepage-2+i)+'\">'+str(moviepage-2+i)+'</a>  ';								
		if i==5 and (upcomingMoviesPages>8 or upcomingMoviesPages-moviepage>8):
			html = html + '.... ';
		if i>5:
			if upcomingMoviesPages-moviepage<=10 or upcomingMoviesPages-10+i<=moviepage+i:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(i)+'\">'+str(i)+'</a>  ';
			if upcomingMoviesPages-moviepage<10 and upcomingMoviesPages-10+i>moviepage+i:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(upcomingMoviesPages-10+i)+'\">'+str(upcomingMoviesPages-10+i)+'</a>  ';								
			if upcomingMoviesPages-moviepage>10 and upcomingMoviesPages-10+i>moviepage+i:
				html = html + '<a href=\"upcomingMovies?moviepage='+str(upcomingMoviesPages-10+i)+'\">'+str(upcomingMoviesPages-10+i)+'</a>  ';				

	html = html + '</tr></td>'	
	html = html + '</table></body></div></html>';
	return html.encode('utf-8');

	






	