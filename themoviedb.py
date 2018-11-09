import json
import configparser
import os
import requests
import logging
import math

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
	relDir = os.path.dirname(os.path.abspath(__file__))
	config.read(relDir+'\conf\configuration.cfg');	
	logging.basicConfig(filename= relDir + '\\logs\\app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s');
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

def producePagingHTML(totalViewPages, pageTag, placeholder, upcomingMoviesPages, moviePage, showPrevNext):	
	currentPage = 1;
	htmlPage = '';
	
	if moviePage != 1 and showPrevNext==True:
		htmlPage = htmlPage + pageTag.replace(placeholder,str(moviePage-1),1).replace(placeholder,'Previous');
			
	for i in range(1,totalViewPages+1):
		if totalViewPages >= upcomingMoviesPages:
			currentPage = i;
		else:
			if moviePage+(totalViewPages/2)<=upcomingMoviesPages and moviePage-(math.floor(totalViewPages/2))>0:
				currentPage = moviePage-(totalViewPages/2)+i;
			elif moviePage+(totalViewPages/2)>upcomingMoviesPages and moviePage-(math.floor(totalViewPages/2))>0:
				currentPage = moviePage -(totalViewPages-(upcomingMoviesPages-moviePage))+i;
			elif moviePage+(totalViewPages/2)<=upcomingMoviesPages and moviePage-(math.floor(totalViewPages/2))<=0:
				currentPage = i;				
			
		htmlPage = htmlPage + pageTag.replace(placeholder,str(currentPage));
		if currentPage==upcomingMoviesPages:
			break;
	if moviePage != upcomingMoviesPages:
		htmlPage = htmlPage + pageTag.replace(placeholder,str(moviePage+1),1).replace(placeholder,'&nbsp&nbspNext');	
	
	return htmlPage;
#function definitions end
def upcomingMovies(moviePage=1):
	initialization();
	
	html = '<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="mystyle.css"></head><body><div class="centered"><table>'
		
	rowChange = 1;

	upcomingURL = urlBuilder('upcoming','&page='+str(moviePage));
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
	
	html = html + producePagingHTML(10, '<a href=\"upcomingMovies?moviePage=@#\">@#</a>  ', '@#', upcomingMoviesPages, moviePage, True);
	
	html = html + '</tr></td>'	
	html = html + '</table></body></div></html>';
	return html.encode('utf-8');

	






	