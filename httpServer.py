import http.server
import socketserver
import themoviedb
import os
import configparser


def initialization():
	global defaultPage;
	global mainFile;
	global config;
	global contentType;

	config = configparser.ConfigParser();
	config.read(os.path.join(os.path.dirname(__file__), 'conf', 'configuration.cfg'));
	defaultPage = config.get('System','defaultPage');
	mainFile = config.get('System','mainFile');
	contentType ={"png":"image/png","jpg":"images/jpeg","gif":"images/gif","ico":"image/x-icon"};

def breakdownParams(link):
	returnedParams = '';
	questionMarkPos = link.find('?');
	if questionMarkPos>0:
		return link[questionMarkPos+1:].replace("&", ",");	
	else:
		return '';

def ifnull(var, val):
  if var is None:
    return val;
  return var;

def findWrapper(var,charToFind):
	if var.find('?') == -1:
		return len(var);
	return var.find(charToFind); 
	
def decideURL(requestURL):
	if requestURL == "/":
		return mainFile  + defaultPage +'()';
	else:
		return mainFile +os.path.relpath(requestURL, '/')[:findWrapper(requestURL,'?')-1]+'('+breakdownParams(requestURL)+')';
 	
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200);
		self.send_header('Content-type','text/html');
		self.end_headers();
		if self.path == '/favicon.ico':
			with open(os.path.join(os.path.dirname(__file__), 'images', 'favicon.ico'),'rb') as f:
				self.send_response(200);
				self.wfile.write(f.read());				
				return;
		elif self.path.endswith(".css"):
			with open(os.path.relpath(self.path, '/')) as f:
				self.send_response(200);
				self.send_header('Content-type', 'text/css');
				self.end_headers();
				self.wfile.write(f.read().encode());
				return;
			
		elif contentType.get(self.path[self.path.rfind(".")+1:], 'None')!='None':
			with open(os.path.relpath(self.path, '/'),'rb') as f:
				print ("****:"+self.path);			
				self.send_response(200);
				self.wfile.write(f.read());	
		
				return;		
		else:
			url = decideURL(self.path);
			responseMessage=eval(decideURL(self.path));
			self.wfile.write(responseMessage);
			return;
		 

initialization();
Handler = MyRequestHandler;
server = socketserver.TCPServer(('', int(os.environ['PORT'])), Handler);
server.serve_forever();	

		
