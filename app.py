from markupsafe import escape
import datetime
from flask import Flask, render_template, request, redirect, url_for
import psycopg2


app = Flask(__name__)




@app.route('/')
def hello():
    return render_template('index.html')

def data():
   conn = psycopg2.connect("postgresql://smanager:phucbao12340@localhost:5432/postgres")
   return conn

@app.route('/khach_hang/')
def Kh():
    conn = data()
    cur = conn.cursor()
    cur.execute('SELECT * FROM khach_hang;')
    khach_hang = cur.fetchall()
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
        return render_template('khach_hang.html', khach_hang=khach_hang)
    return render_template('tim_khach_hang.html')

#call function thong ke luot khach
@app.route('/thong_ke/',methods=('GET','POST'))
def thong_ke():
    if request.method == 'POST':
        chi_nhanh = request.form['chi_nhanh']
        year = int(request.form['year'])
        conn = data()
        cur = conn.cursor()
        cur.execute('SELECT thongkeluotkhach(%s,%s);',(chi_nhanh,year,))
        thong_ke = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('hien_thi_thong_ke.html', thong_ke=thong_ke, chi_nhanh=chi_nhanh, year=year)
    return render_template('thong_ke.html')
    
    
@app.route('/them_phong/', methods=('GET', 'POST'))
def create_phong():
    if request.method == 'POST':
        ten_loai_phong = request.form['ten']
        dien_tich = float(request.form['dien_tich'])
        so_khach = int(request.form['so'])
        kt_giuong = request.form['kt_giuong']
        sl_giuong = int(request.form['sl_giuong'])
        mo_ta_khac = request.form['mo_ta']
        id_vat_tu = request.form['id_vat_tu']
        sl_vattu = int(request.form['sl_vattu'])

        conn = data()
        cur = conn.cursor()
        cur.execute('SELECT MAX(ma_loai_phong) FROM loai_phong;')
        max_ma = cur.fetchall()
        ma_max = int(max_ma[0][0]) +1
        cur.execute('INSERT INTO loai_phong (ma_loai_phong,ten_loai_phong, dien_tich, so_khach, mo_ta_khac)'
                    'VALUES ( %s ,%s, %s, %s, %s);', 
                    ( ma_max,ten_loai_phong, dien_tich, so_khach, mo_ta_khac))
        cur.execute('SELECT MAX(ma_loai_phong) FROM loai_phong;')
        max_ma = cur.fetchall()
        cur.execute('INSERT INTO thong_tin_giuong(ma_loai_phong, kich_thuoc, so_luong)'
                    'VALUES (%s, %s, %s);',
                    (ma_max, kt_giuong, sl_giuong))
        cur.execute('INSERT INTO loai_vat_tu_trong_phong(ma_loai_vat_tu, ma_loai_phong, so_luong)'
                    'VALUES (%s, %s, %s);',
                    ( id_vat_tu,ma_max, sl_vattu))
        conn.commit()
        cur.close()
        conn.close()
    return render_template('create_phong.html')

@app.route('/about_us/')
def about_us():
    return render_template('about_us.html')
