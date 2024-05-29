class Middleware:
	def __init__(self):
		pass

	def is_valid(self, middleware):
		# Obtiene todas las subclases anidadas de Middlewares
		subclasses = [attr for attr in Middleware.__dict__.values() if isinstance(attr, type)]
		nested_subclasses = [attr for subclass in subclasses for attr in subclass.__dict__.values() if isinstance(attr, type)]
		# Verifica si el middleware es una instancia de alguna subclase anidada de Middlewares
		return any(isinstance(middleware, subclass) for subclass in nested_subclasses)

	class Databases:
		class MongoDB:
			def __init__(self) -> None:
				pass

			def process_request(self):
				# Implementa la lógica del middleware aquí
				pass

			def connect(self):
				print("Connected to MongoDB")

			def disconnect():
				print("Disconnected from MongoDB")

		class MySQL:
			pass
		
		class SQLite:
			pass
		
		class PostgreSQL:
			pass
		
		class MariaDB:
			pass
		
		class Redis:
			pass
		
		class Firebase:
			pass
		
		class TursoDB:
			pass
		
	class Authentication:
		pass
	
	class Authorization:
		pass
	
	class RateLimit:
		pass
	
	class Cache:
		pass
	
	class Logger:
		pass