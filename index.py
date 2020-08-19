from flask import Flask

task = Flask(__name__)
myval = 50

@task.route('/')
def serve():
	return "Ciao, flask! Il valore è " + str(myval)

@task.route('/set/')
def set_val():
	value = int(request.args.get('val'))

	myval = value

if __name__ == '__main__':
	task.run()