#import SimpleHTTPServer
#import SocketServer
import http.server
import socketserver
import themoviedb
import os
import configparser


def initialization():
	global defaultPage;
	global mainFile;

	config = configparser.ConfigParser();
	#relDir = os.path.dirname(os.path.abspath(__file__))
	#config.read(relDir+'\conf\configuration.cfg');	
	print('avavava:'+os.path.dirname(os.path.abspath(__file__)));
	files = os.listdir(os.path.dirname(os.path.abspath(__file__)))
	for name in files:
		print(name)	
	config.read(os.path.join(os.path.dirname(__file__)+'/conf', r"configuration.cfg"))
	defaultPage = config.get('System','defaultPage');
	mainFile = config.get('System','mainFile');

def breakdownParams(link):
	returnedParams = '';
	questionMarkPos = link.find('?');
	if questionMarkPos>0:
		return link[questionMarkPos+1:].replace("&", ",");	
	else:
		return '';

def ifnull(var, val):
  if var is None:
    return val
  return var

def findWrapper(var,charToFind):
	if var.find('?') == -1:
		return len(var);
	return var.find(charToFind); 
	
def decideURL(requestURL):
	if requestURL == "/":
		return mainFile  + defaultPage +'()';
	else:
		return mainFile +requestURL[1:findWrapper(requestURL,'?')]+'('+breakdownParams(requestURL)+')'	
  
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		 return http.server.SimpleHTTPRequestHandler.do_GET(self.wfile.write(eval(decideURL(self.path))));

initialization()
Handler = MyRequestHandler;
server = socketserver.TCPServer(('', int(os.environ['PORT'])), Handler);

server.serve_forever();	

		
