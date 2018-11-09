import SimpleHTTPServer
import SocketServer
import themoviedb
import os


def breakdownParams(link):
	returnedParams = '';
	questionMarkPos = link.find('?');
	if questionMarkPos>0:
		print '**********:'+link[questionMarkPos+1:].replace("&", ",")
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
  
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self.wfile.write(eval("themoviedb."+self.path[1:findWrapper(self.path,'?')]+'('+breakdownParams(self.path)+')')));

Handler = MyRequestHandler;
server = SocketServer.TCPServer(('0.0.0.0', 80), Handler);
server.serve_forever();	

		
