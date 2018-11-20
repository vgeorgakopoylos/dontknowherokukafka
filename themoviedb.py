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
	global imageWidthGeneral;
	global imageWidthDetail;
	global imageWidthThump;
	
	config = configparser.ConfigParser();
	config.read(os.path.join(os.path.dirname(__file__), 'conf', 'configuration.cfg'));
	version = config.get('General','version3');
	mainURL = config.get('General','mainurl');
	apiKey = config.get('General','apikeyV3');
	language = config.get('General','language');
	imageURL = config.get('General','imageURL');
	imageWidthGeneral = config.get('General','imageWidthGeneral');
	imageWidthDetail = config.get('General','imageWidthDetail');
	imageWidthThump = config.get('General','imageWidthThump');

def urlBuilder(methodName, searchId , idSuffix, paramerers):
	if config.get('Method Types',methodName) == 'General':
		url = mainURL + version + config.get('Method Suffix',methodName)+config.get('Methods',methodName)+'?'+'api_key='+apiKey+'&language='+config.get('General','language')+paramerers;
	elif config.get('Method Types',methodName) == 'SearchById':
		url = mainURL + version + config.get('Method Suffix',methodName)+str(searchId)+idSuffix+'?'+'api_key='+apiKey+'&language='+config.get('General','language')+paramerers;		
	
	return url;

def apiCalls(url):
	response = requests.get(url);
	if (response.status_code!=200):
		raise Exception("API Call was not completed correctly. Status Code returned:"+str(response.status_code));

	return response;

def producePagingHTML(totalViewPages, pageTag, placeholder, overallPages, moviePage, showPrevNext):	
	currentPage = 1;
	htmlPage = '';
	
	if moviePage != 1 and showPrevNext==True:
		htmlPage = htmlPage + pageTag.replace(placeholder,str(int(moviePage-1)),1).replace(placeholder,'Previous');
			
	for i in range(1,totalViewPages+1):
		if totalViewPages >= overallPages:
			currentPage = i;
		else:
			if moviePage+(totalViewPages/2)<=overallPages and moviePage-(math.floor(totalViewPages/2))>0:
				currentPage = moviePage-(totalViewPages/2)+i;
			elif moviePage+(totalViewPages/2)>overallPages and moviePage-(math.floor(totalViewPages/2))>0:
				currentPage = moviePage -(totalViewPages-(overallPages-moviePage))+i;
			elif moviePage+(totalViewPages/2)<=overallPages and moviePage-(math.floor(totalViewPages/2))<=0:
				currentPage = i;				
			
		htmlPage = htmlPage + pageTag.replace(placeholder,str(int(currentPage)));
		if currentPage==overallPages:
			break;
	if moviePage != overallPages:
		htmlPage = htmlPage + pageTag.replace(placeholder,str(int(moviePage+1)),1).replace(placeholder,'Next');	
	
	return htmlPage;
	
def initHTML(cssFilesConc,jsFilesConc):
	intiHTMLvar = '<html><head><meta charset="utf-8"/>';
	cssFilesSplit = cssFilesConc.split(':')
	for cssFile in cssFilesSplit:
		if cssFile is not None:
			intiHTMLvar = intiHTMLvar+'<link rel="stylesheet" type="text/css" href="'+cssFile+'">';
	intiHTMLvar = intiHTMLvar+'<link rel="shortcut icon" href="favicon.ico"/></head><body>'
	jsFilesSplit = jsFilesConc.split(':')
	for jsFile in jsFilesSplit:
		if jsFile is not None:
			intiHTMLvar = intiHTMLvar+'<script src="'+jsFile+'"></script>';
			
	return intiHTMLvar

def finalizeHTML():	
	return '</body></html>';
	
def getData(methodName, searchId , idSuffix, paramerers):
	URL = urlBuilder(methodName, searchId, idSuffix, paramerers);
	response = apiCalls(URL);
	
	return json.loads(response.text);
	
#function definitions end

def upcomingMovies(moviePage=1):
	initialization();
	html = initHTML('css/themoviedb.css','');
	html = html + '<div class="upcomingAll"><table>'
	rowChange = 1;
	rowChangeNum = 3
	upcomingMoviesOverall = getData('upcoming', '', '', '&page='+str(moviePage));
	upcomingTotalPages = upcomingMoviesOverall['total_pages'];
	upcomingMovies = upcomingMoviesOverall['results'];
	
	for movie in upcomingMovies:
		if rowChange == 1:
			html = html+'<tr>';
		html = html + '<td>';
		if movie['poster_path'] is not None:
			html = html +  '<a href="movieDesc?movieid='+str(movie['id'])+'"><img src='+imageURL+imageWidthGeneral+movie['poster_path']+'></a><br>';
		else:
			html = html +  '<a href="movieDesc?movieid='+str(movie['id'])+'"><img src="images/noposter.jpg"></a><br>';	
		html = html + '<a href="movieDesc?movieid='+str(movie['id'])+'">'+movie['title']+'</a>';
		html = html + '</td>';
		
	
		if rowChange==rowChangeNum:
			html = html+'</tr>';
			rowChange = 0;
		rowChange = rowChange+1;
	
	html = html + '<tr><td colspan="'+str(rowChangeNum)+'">';
	html = html + producePagingHTML(10, '<a href="upcomingMovies?moviePage=@#">@#</a>  ', '@#', upcomingTotalPages, moviePage, True);
	html = html + '</td></tr></table></div>';
	html = html + finalizeHTML();	
	
	return html;

def movieDesc(movieid,relatedMoviePage=1):
	initialization();
	html = initHTML('css/themoviedb.css','js/asyncCallEvents.js:js/jquery-3.3.1.min.js');
	movieInfo = getData('searchMovieById', movieid, '', '');
	html = html + '<div class="movieDesc"><table>'
	html = html + '<tr>';
	if movieInfo['poster_path'] is not None:
		html = html + '<td><img src="'+imageURL+imageWidthDetail+movieInfo['poster_path']+'"></td>';
	if movieInfo['backdrop_path'] is not None:
		html = html + '<td><img src="'+imageURL+imageWidthDetail+movieInfo['backdrop_path']+'"></td>';
	html = html + '</tr>';
	html = html + '<tr>';
	html = html + '<td>Overview:</td>';
	html = html + '<td>'+movieInfo['overview']+'</td>';
	html = html + '</tr>';
	html = html + '<tr>';
	html = html + '<td>Rank:</td>';
	html = html + '<td>'+str(movieInfo['vote_average'])+'</td>'	;
	html = html + '</tr>';
	html = html + '</table></div>';
	html = html +  movieRelated(movieid, relatedMoviePage);
	html = html +  finalizeHTML();

	return html;
	
def movieRelated(movieid, moviePage=1):	
	relatedMovies= getData('movieRelated', movieid, '/similar', '&page='+str(moviePage));
	relatedMoviesRes = relatedMovies['results'];

	if len(relatedMoviesRes) == 0:
		return '';
	relatedTotalPages = relatedMovies['total_pages'];
	html = '<div id="movieRelated" name="movieRelated" class="upcomingAll"><div name="movieRelatedHorizontal" class="horizontalMovies"><table>'
	descriptionRow = '';
	imageRow = '';
	for relatedMovieRes in relatedMoviesRes:
		descriptionRow = descriptionRow + '<td>'
		descriptionRow = descriptionRow + '<a href="movieDesc?movieid='+str(relatedMovieRes['id'])+'">'+relatedMovieRes['title']+'</a>'
		descriptionRow = descriptionRow + '</td>'
		imageRow = imageRow + '<td>'
		if relatedMovieRes['poster_path'] is not None:
			imageRow = imageRow +  '<a href="movieDesc?movieid='+str(relatedMovieRes['id'])+'"><img src='+imageURL+imageWidthThump+relatedMovieRes['poster_path']+'></a>';
		else:
			imageRow = imageRow +  '<a href="movieDesc?movieid='+str(relatedMovieRes['id'])+'"><img src="images/noposter.jpg"></a>';
		imageRow = imageRow + '</td>'
	
	html = html + '<tr>' + descriptionRow + '</tr>'
	html = html + '<tr>' + imageRow + '</tr>'	
	html = html + '</table></div>'
	html = html + producePagingHTML(10, '<a href="/" onClick="changePageAsynch(\'movieRelated\', \'movieRelated?movieid='+str(movieid)+'&moviePage=@#\'); return false;">@#</a>  ', '@#', relatedTotalPages, moviePage, True);
	html = html + '</div>'

	return  html;
	
	

	
	






	