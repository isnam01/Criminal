from flask import Flask, render_template, Response,redirect, url_for, request
from camera import VideoCamera
import sqlite3
import hashlib
app = Flask(__name__)

#def check_password(hashed_password,user_password):
#    return hashed_password==hashlib.md5(user_password.encode()).hexdigest()

def validate(username,password):
    con=sqlite3.connect('Static/trydb.db')
    complition=False
    with con:
        cur=con.cursor()
        cur.execute('SELECT * FROM info')
        rows=cur.fetchall()
        for row in rows:
            dbUser=row[0]
            dbPass=row[1]
            if dbUser==username:
                if dbPass==password:
                    complition=True

    return complition


@app.route('/',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        completion=validate(username,password)
        if completion==False:
            error='Invalid Cridential,Please try again.'
        else:
            return redirect(url_for('login1'))
    return render_template('login.html',error=error)
@app.route('/login1')
def login1():
    return render_template('/login1.html')
#@app.route('/index')
#def index():
#    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
