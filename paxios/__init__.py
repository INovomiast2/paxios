#   , __    ___,    _          _    __        
#  /|/  \  /   |   (_\  /     | |  /\_\/   () 
#   |___/ |    |      \/      | | |    |   /\ 
#   |     |    |      /\    _ |/  |    |  /  \
#   |      \__/\_/  _/  \_/ \_/\/  \__/  /(__/
#   ==========================================
#   A supercharged version of the requests module, with more features and better performance.
  
#   _sumary_:
# 	Paxios permits you tu create in a super fast and easy ways a full API for your web application.
	
#   _author_: INovomiast2 (Ivan Novomiast)
#   _version_: 1.0.0
#   _license_: MIT
#   _github_: https://github.com/INovomiast2/paxios

# Here is all the code of paxios, this is going to be a long file, so be prepared.

# Importing the necessary modules
import requests
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Any, Tuple, Type
import ssl
from .middlewares import Middleware

# Defining the main class
class CreatePaxios():
	"""
	To use paxios, you MUST create an instance of this class.
	With this class you can create a full API for your web application.

	Args:
		port (int): The port the API will be using to run itself.
		debug (bool): Enables the debug mode on the API.
		host (str): The host where the API will be running.
		version (str): The version of the API.
		ssl (bool): Enables SSL context on the API.
		ssl_key (str): The route to the SSL Key.
		ssl_cert (str): The route to the SSL Certificate.
		auth (bool): Enables Authentication.
		auth_token (str): The token for the authentication.
	"""
	def __init__(self, host:str='localhost', port:int=3000, debug:bool=False, version:int=0, ssl:bool=False, ssl_key:str=None, ssl_cert:str=None, auth:bool=True, auth_token:str=None) -> None:
		self.host = host
		self.port = port
		self.debug = debug
		self.version = version
		self.ssl = ssl
		self.ssl_key = ssl_key
		self.ssl_cert = ssl_cert
		self.auth = auth
		self.auth_token = auth_token
		self.routes = {}
		self.middlewares = []
  
		@self.route('/', methods=['GET'])
		def index():
			return self.json({'message': 'Welcome to Paxios!'})

		@self.route('/version', methods=['GET'])
		def api_version():
			return self.json({'version': self.version})

		@self.route('/servinfo', methods=['GET'])
		def server_info():
			return self.json({'host': self.host, 'port': self.port, 'ssl': self.ssl == True and 'enabled' or 'disabled', 'auth': self.auth == True and 'enabled' or 'disabled', 'paxios_version': '1.0.0', 'debug': self.debug == True and 'enabled' or 'disabled'})

	class CustomHTTPServer(HTTPServer):
		def __init__(self, server_address, RequestHandlerClass, routes, bind_and_activate=True):
			super().__init__(server_address, RequestHandlerClass, bind_and_activate)
			self.routes = routes
 
	class RequestHandler(BaseHTTPRequestHandler):
		def do_GET(self):
			route = self.server.routes.get(self.path)
			if route is not None and 'GET' in route:
				response = route['GET']()
				self.send_response(200)
				self.send_header('Content-type', 'application/json')
				self.end_headers()
				self.wfile.write(response.encode())
			else:
				response = json.dumps({'message': 'Route not found'})
				self.send_response(404)
				self.end_headers()
				self.wfile.write(response.encode())

		def do_POST(self):
			route = self.server.routes.get(self.path)
			if route is not None and 'POST' in route:
				response = route['POST']()
				self.send_response(200)
				self.send_header('Content-type', 'application/json')
				self.end_headers()
				self.wfile.write(response.encode())
			else:
				response = json.dumps({'message': 'Route not found'})
				self.send_response(404)
				self.end_headers()
				self.wfile.write(response.encode())

		def do_PUT(self):
			route = self.server.routes.get(self.path)
			if route is not None and 'PUT' in route:
				response = route['PUT']()
				self.send_response(200)
				self.send_header('Content-type', 'application/json')
				self.end_headers()
				self.wfile.write(response.encode())
			else:
				response = json.dumps({'message': 'Route not found'})
				self.send_response(404)
				self.end_headers()
				self.wfile.write(response.encode())
	
		def handle_dynamic_routes(self, path):
			route = self.server.routes.get(path)
			if route is not None and 'GET' in route:
				response = route['GET']()
				self.send_response(200)
				self.send_header('Content-type', 'application/json')
				self.end_headers()
				self.wfile.write(response.encode())
			else:
				response = json.dumps({'message': 'Route not found'})
				self.send_response(404)
				self.end_headers()
				self.wfile.write(response.encode())

	def route(self, path: str, methods: List[str]):
		def decorator(f):
			versioned_path = f"/v{self.version}{path}"
			if versioned_path not in self.routes:
				self.routes[versioned_path] = {}
			for method in methods:
				if method in self.routes[versioned_path]:
					raise ValueError(f"La ruta {versioned_path} ya está definida para el método {method}.")
				self.routes[versioned_path][method] = f
			return f
		return decorator

	def run(self) -> None:
		"""
		Inicia la API.
		"""
		if self.ssl:
			server = self.CustomHTTPServer((self.host, self.port), self.RequestHandler)
			server.socket = ssl.wrap_socket(server.socket, keyfile=self.ssl_key, certfile=self.ssl_cert, server_side=True)
			server.serve_forever()
		else:
			print("API running on http://{}:{}/v{}/".format(self.host, self.port, self.version))
			server = self.CustomHTTPServer((self.host, self.port), self.RequestHandler, self.routes)
			server.serve_forever()
   
	def json(self, data:Dict[str, Any]) -> str:
		"""
		Devuelve un objeto JSON.

		Args:
			data (Dict[str, Any]): The data to convert to JSON.
		"""
		return json.dumps(data)

	def list_routes(self):
		route_names = {path: {method: func.__name__ for method, func in funcs.items()} for path, funcs in self.routes.items()}
		return route_names

	def use(self, middleware: Type[Middleware]) -> Middleware:
		if not issubclass(middleware, Middleware):
			raise ValueError("{} is not a valid middleware.".format(middleware))
		instance = middleware()  # Crea una instancia de la subclase de Middleware
		self.middlewares.append(instance)
		return instance  # Devuelve la instancia

class fromFile:
	def __init__(self, file:str=None) -> None:
		self.file = file
		self.data = None
	
	def read(self) -> dict:
		"""
			Read a JSON file and return it as a dictionary.
		"""
		# Protecting the function from errors
		try:
			# Opening the file
			with open(self.file, 'r') as f:
				# Reading the file
				self.data = json.load(f)
			# Returning the data
			return self.data
		except Exception as e:
			# If an error occurs, return the error
			return e
		
	def write(self, data:dict) -> None:
		"""
			Write a dictionary to a JSON file.
		"""
		# Protecting the function from errors
		try:
			# Opening the file
			with open(self.file, 'w') as f:
				# Writing the data
				json.dump(data, f)
		except Exception as e:
			# If an error occurs, return the error
			return e