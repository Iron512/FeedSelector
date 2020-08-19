from flask import Flask, request, session, redirect, url_for

task = Flask(__name__)
task.secret_key = "p0biYbC[Ebq2lKn"

@task.route('/')
def serve():
	if 'value' in session:
		return "Ciao, flask! Il valore è " + session['value']
	else:
		return "Purtroppo il valore non è definito"

@task.route('/set/<val>', methods=['GET'])
def set_val(val):
	session['value'] = val
	return redirect(url_for('serve'))

if __name__ == '__main__':
	task.run()