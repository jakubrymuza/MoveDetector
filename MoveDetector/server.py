from flask import Flask, request, render_template

app = Flask(__name__)
correctPassword = "1234"

class alarmInfo:
    def __init__(self):
      self.isAlarm = False

info = alarmInfo()

@app.route('/', methods=["GET", "POST"])
def renderMain():
    
    if(info.isAlarm == False):
        return render_template('mainT.html')
    else:
        return render_template('alarm.html')

@app.route('/alarm', methods=["GET", "POST"])
def renderAlarm():
    info.isAlarm = True
    return render_template('alarm.html')

@app.route('/cancelled', methods=["GET", "POST"])
def renderCancel():
    info.isAlarm = False
    return render_template('cancel.html')

@app.route('/verify', methods=["GET", "POST"])
def verifyPassword():
    password = request.form.get("password")
    if correctPassword == password:
        return renderCancel()
    else:
        return renderWrong()

@app.route('/wrong', methods=["GET", "POST"])
def renderWrong():
    return render_template('wrong.html')   

@app.route('/state', methods=["GET"])
def checkState():
    return str(info.isAlarm)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
    