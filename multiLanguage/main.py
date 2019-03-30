from app import app
from flask_cors import *
CORS(app, supports_credentials=True)

if __name__ == "__main__":
	app.run(host="192.168.30.9",port=5000)