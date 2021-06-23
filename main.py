import webbrowser 
import serial
import sys
import glob
import time
from flask import Flask, render_template, request
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=["GET"])
def hello_world():
    return render_template("index.html")

@app.route('/getInitData', methods=["GET"])
def get_init_data():
    # return init data of dropdowns
    return "ok"

@app.route('/submitted', methods=["POST"])
def submitted():
    # return init data of dropdowns
    return "ok :)"

@app.route("/flash", methods=["POST"])
def get_post_data():
    data = request.get_json()
    # do something
    print(data)
    return render_template("flashed.html")

def non_match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        if i not in list_b:
            non_match.append(i)
    return non_match

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def findPort():
    originalPorts = serial_ports()
    #prompt user to plug device
    while originalPorts == serial_ports():
        print("Waiting for keypad")
        newPorts = serial_ports()
    #Yeet prompt
    keypadPort = non_match_elements(newPorts, originalPorts)
    if len(keypadPort) > 1:
        raise Exception('Multiple Devices')
    return keypadPort[0]

def write(x):
    arduino.write(bytes(x, 'utf-8'))

def read():
    data = arduino.readline()
    return data

if __name__ == '__main__':
    app.run(port=13004)
    # webbrowser.open_new_tab('http://localhost:13004') 
    arduino = serial.Serial(findPort(), baudrate=9600, timeout=.1)
    if read() != "Welcome to the serial remapper!":
        raise Exception('Unsupported Device')
