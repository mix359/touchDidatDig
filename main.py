#from flask import Flask, jsonify, render_template
from casioProjectorSerialCom import CasioProjectorSerialCom
from videoMatrixCom import VideoMatrixCom

#app = Flask(__name__, static_folder='assets', static_url_path='/assets')
#@app.route('/')
#def root():
#    return render_template('index.html')

if __name__ == '__main__':
    mqttServer = "rdisplay1.local"
    proj1 = CasioProjectorSerialCom("3","test/proj/1",mqttServer)
    proj1.start()

    mtrx1 = VideoMatrixCom("00:91:66:e1:d7:b4", "192.168.1.239","test/matrix/1",mqttServer)
    mtrx1.start()
    #app.run(port=5000)
