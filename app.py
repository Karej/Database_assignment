from markupsafe import escape
import datetime
from flask import Flask, render_template, request, redirect, url_for
import psycopg2


app = Flask(__name__)




@app.route('/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())


#@app.route('/data/')
def data():
   conn = psycopg2.connect("postgresql://postgres:phucbao12340@localhost:5432/postgres")
   return conn

'''@app.route('/table/')
def chi_nhanh():
    conn = data()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)'''

@app.route('/khach_hang/')
def Kh():
    conn = data()
    cur = conn.cursor()
    cur.execute('SELECT * FROM khach_hang;')
    khach_hang = cur.fetchall()
    #dd_1( khach_hang[0][0])
    cur.close()
    conn.close()
    return render_template('khach_hang.html', khach_hang=khach_hang)

#@app.route('/tim_khach_hang/find')
def Kh_1(username):
    conn = data()
    cur = conn.cursor()
    cur.execute('SELECT * FROM khach_hang WHERE khach_hang.ho_ten = %s;',(username,))
    khach_hang = cur.fetchall()
    cur.close()
    conn.close()
    return khach_hang

@app.route('/don2/<string:ma>')
def dd(ma):
    conn = data()
    cur = conn.cursor()
    cur.execute('SELECT * FROM don_dat_phong WHERE don_dat_phong.ma_khach_hang = %s;',(ma,))
    don_dat = cur.fetchall()  
    cur.close()
    conn.close()
    return render_template('display_don.html', don_dat=don_dat)

#@app.route('/don_dat/', methods=['GET', 'POST'])
#def tim_don():
    #return render_template('display_don.html', don_dat=don_dat)
@app.route('/don/')
def dd_1():
    conn = data()
    cur = conn.cursor()
    #ma = dd
    cur.execute('SELECT * FROM don_dat_phong;')
    don_dat = cur.fetchall()
    #dd_1( khach_hang[0][0])
    cur.close()
    conn.close()
    return render_template('display_don.html', don_dat=don_dat)


@app.route('/tim_khach_hang/', methods=('GET', 'POST'))
def Kh_find():
    #input a username, find and display the user's information
    if request.method == 'POST':
        username = request.form['username']
        khach_hang = Kh_1(username)
        #dd(khach_hang[0][0])
        return render_template('khach_hang.html', khach_hang=khach_hang)
    return render_template('tim_khach_hang.html')

#@app.route('/infor/')
#def infor():
    #show the information of the user
    
    
    
    
    '''if request.method == 'POST':
        conn = data()
        cur = conn.cursor()
        cur.execute('SELECT * FROM khach_hang WHERE username = %s;', (request.form['username'],))
        khach_hang = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('tim_khach_hang.html', khach_hang=khach_hang)
    return render_template('tim_khach_hang.html')'''
    
@app.route('/them_phong/', methods=('GET', 'POST'))
def create_phong():
    if request.method == 'POST':
        ma_loai_phong = int(request.form['id'])
        ten_loai_phong = request.form['ten']
        dien_tich = int(request.form['dien_tich'])
        so_khach = int(request.form['so'])
        mo_ta_khac = request.form['khac']

        conn = data()
        cur = conn.cursor()
        cur.execute('INSERT INTO loai_phong (ma_loai_phong, ten_loai_phong, dien_tich, so_khach, mo_ta_khac)'
                    'VALUES (%s, %s, %s, %s, %s);', 
                    (ma_loai_phong, ten_loai_phong, dien_tich, so_khach, mo_ta_khac))
        conn.commit()
        cur.close()
        conn.close()
        #return redirect(url_for('index'))
    return render_template('create_phong.html')