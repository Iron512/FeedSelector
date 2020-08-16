from flask import Flask

task = Flask(__name__)

@task.route('/')
def serve():
	return "Ciao, flask!"

if __name__ == '__main__':
	task.run()