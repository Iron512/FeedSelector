from flask import Flask

app = Flask(__name__)

@app.route('/')
def serve():
	return "Ciao, flask!"

if __name__ == '__main__':
	app.run()