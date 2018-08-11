from flask import Flask, render_template, request , url_for , redirect
import sqlite3 as sql
import random
DATABASE_PATH ="C:\\Users\\Hp\\sqlite\\emp_mgt.db"
app = Flask(__name__)
def query_run(statement, flag=False):
    out =[]
    try:
        con= sql.connect(DATABASE_PATH)
        cursor=con.cursor()
        cursor.execute(statement)
        if flag:
            con.commit()
        out=cursor.fetchall()
        con.close()
    except Exception as err:
        print("Database not found", err)
    return out


@app.route("/")
def emp_read():
    read_query ="SELECT * FROM emp_detail;"
    emp_list=query_run(read_query)
    return render_template("index.html",employee = emp_list)

@app.route("/create", methods = ['POST'])
def emp_write():
    if request.method == 'POST':
        query_mod = "SELECT MAX(emp_id) FROM emp_detail;"
        out = query_run(query_mod)
        if out:
            emp_id = query_run(query_mod)[0][0] +1
        else:
            emp_id = random.randint(1000,100000)
        write_query ="INSERT INTO emp_detail(ID,Name,Address,Contact) values"
        write = "".join([write_query, "(",str(emp_id), ",'",request.form['Name'], "','",request.form['Address'], "',",str(request.form['Contact']), ");"])
        print(write)
        query_run(write,True)
        return redirect(url_for("emp_read"))

@app.route("/home")
def test():
    return "<html><body><h1>welcome Home</h1></body></html>"

@app.route("/delete/<emp_id>", methods =["POST"])
def emp_remove(emp_id,):
    if request.method =="POST":
        delete = "DELETE FROM emp_detail WHERE ID="
        delete_query = "".join([delete, str(emp_id), ";"])
        query_run(delete_query, True)
    return redirect(url_for("emp_read"))

@app.route("/update/<emp_id>", methods =["POST"])
def emp_update(emp_id):
    if request.method =="POST":
        update_query ="UPDATE emp_detail SET "
        update = "".join([update_query, "Name='", request.form["Name"],"',Address='", request.form['Address'], "',Contact=", str(request.form['Contact']), " WHERE id=", str(emp_id), ";"])
        print(update)
        query_run(update, True)
    return redirect(url_for("emp_read"))

if __name__ == "__main__":
    app.run(debug =True, port=8000)
