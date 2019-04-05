# coding=utf-8
from flask import Flask, json, render_template
from threading import Thread
from flask_socketio import SocketIO
from graphqlclient import GraphQLClient
import serial, time, serial.tools.list_ports, datetime, socket


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET!'
socketio = SocketIO(app)
uuid_last = ''
data = ''
connexion_genius = GraphQLClient('https://##.###.##/')
connexion_genius.inject_token('Bearer ####','Authorization')
REMOTE_SERVER = "##.###.##"


@app.route('/')
def index():
    return render_template('index.html')


def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def getprofilewithbadge(badge):
    tmp = connexion_genius.execute('''{ 
                           profiles(where:{badge:"''' + badge + '''"}){
                           firstName
                           lastName
                         }
                       }
                    ''')
    return tmp

def sethello(badge):
    tmp = connexion_genius.execute('''mutation{terminalHello(data:{badge:"''' + badge + '''",timeOfArrival:"''' + str(datetime.datetime.now().isoformat()) + '''"}){status}}''')
    return tmp


class SerialRead(Thread):
    global j

    def __init__(self):
        Thread.__init__(self)

        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p[1] or "ttyACM0" in p[1]:
                print("Arduino detecte sur le port : ", p[0])
                self.serial = serial.Serial(str(p[0]), 9600, timeout=1)
                socketio.emit('Internet', {'internet': True})

    def init_serial(self):
        ports = list(serial.tools.list_ports.comports())
        self.serial.close()
        for p in ports:
            if "Arduino" in p[1] or "ttyACM0" in p[1]:
                print("Arduino detecte sur le port : ", p[0])
                self.serial = serial.Serial(str(p[0]), 9600, timeout=1)
                socketio.emit('Internet', {'internet': True})
                self.run()

    def run(self):
        global uuid_last
        while True:
            try:
                if self.serial is not None:

                    data = self.serial.readline().strip(b'\n\r')
                    try:
                        if is_connected():
                            j = json.loads(data.decode('UTF-8'))
                            socketio.emit('Internet', {'internet': True})
                            if "ESTIAM" in j['uuid']:
                                if uuid_last != j['uuid']:
                                    uuid_last = j['uuid']
                                    try:
                                        reponse = json.loads(sethello(uuid_last))
                                        try:
                                            if len(reponse['errors']) > 0:
                                                socketio.emit('CardFound', {'error':True,'user': None, 'late':False})
                                        except:
                                            if reponse['data']['terminalHello']['status'] == "OK":
                                                profile = json.loads(getprofilewithbadge(uuid_last))
                                                socketio.emit('CardFound', {'error':False,'user': {'firstName': profile['data']['profiles'][0]['firstName'],'lastName': profile['data']['profiles'][0]['lastName'],'late': None}, 'late':False})
                                            if reponse['data']['terminalHello']['status'] == "ALREADYBADGED":
                                                profile = json.loads(getprofilewithbadge(uuid_last))
                                                socketio.emit('CardFound', {'error':False,'user': {'firstName': profile['data']['profiles'][0]['firstName'],'lastName': profile['data']['profiles'][0]['lastName'],'late': None}, 'late':False})
                                            if reponse['data']['terminalHello']['status'] == "NO_DATE":
                                                profile = json.loads(getprofilewithbadge(uuid_last))
                                                socketio.emit('CardFound', {'error':False,'user': {'firstName': profile['data']['profiles'][0]['firstName'],'lastName': profile['data']['profiles'][0]['lastName'],'late': None}, 'late':False})
                                            if reponse['data']['terminalHello']['status'] == "UNKNOWN_CARD":
                                                socketio.emit('CardFound', {'error':True,'user':False,'late':False})
                                            if reponse['data']['terminalHello']['status'] == "FAILED_SYS_ERROR":
                                                socketio.emit('CardFound', {'error': True, 'user': False, 'late': False})

                                    except:
                                        continue

                        else:
                            socketio.emit('Internet', {'internet': False})

                    except:
                        continue
            except:
                socketio.emit('Internet', {'internet': False})
                print("La liaison serie ne peut etre etablie")
                time.sleep(1)
                self.init_serial()

    def first(self):
        self.run()


if __name__ == '__main__':
    ThreadSerial = SerialRead()
    ThreadSerial.start()
    socketio.run(app,host='0.0.0.0',port=8000)
