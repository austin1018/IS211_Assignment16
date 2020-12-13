import re
import sqlite3 as lite
from flask import Flask,render_template,request, redirect
app = Flask(__name__)
from datetime import datetime



error_message=''
add_message=''
username=''
edit_message=''

@app.route('/')
def main():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    global error_message
    global username
    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']
        if (username != 'jack' and username != 'john') or password != 'password':
            error_message = 'Username or password is incorrect, please try again.'
            return render_template('login.html', error_message=error_message)
        else:
            error_message =''
            return redirect('/dashboard')
    else:
        error_message=''
        return render_template('login.html', error_message=error_message)

@app.route('/add', methods = ['POST'])
def add_post():
    global add_message
    global username
    title=request.form["title"]
    content=request.form["content"]
    if title=="" or content=="":
        add_message="Please input title and content"
    else:
        add_message = ""
        con = lite.connect("blog.db")
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO posts(title,published_date,author,content) VALUES('"+title+"','"+datetime.today().strftime('%Y-%m-%d')+"','"+username+"','"+content+"')")
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    con = lite.connect("blog.db")
    global add_message
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM posts where author='"+username+"' order by post_id desc")
        posts = cur.fetchall()
    return render_template('dashboard.html', posts=posts,add_message=add_message)

@app.route('/post/<n>')
def edit_post(n):
    con = lite.connect("blog.db")
    global edit_message
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM posts WHERE post_id="+n)
        posts = cur.fetchall()
    return render_template('edit_post.html', posts=posts, edit_message=edit_message)

@app.route('/edit', methods = ['POST'])
def save_post():
    global edit_message
    global username
    post_id=request.form["post_id"]
    title = request.form["title"]
    content = request.form["content"]
    if title == "" or content == "":
        edit_message = "Please input title and content"
    else:
        edit_message = ""
        con = lite.connect("blog.db")
        with con:
            cur = con.cursor()
            cur.execute(
                "update posts set title='" + title + "',published_date='" + datetime.today().strftime(
                    '%Y-%m-%d') + "',content='" + content + "' where post_id="+post_id)
    return redirect('/dashboard')

@app.route('/delete/<n>')
def delete_post(n):
    con = lite.connect("blog.db")
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM posts WHERE post_id="+n)
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)