from flask import Flask
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL

#libraries: pip3 install flask-mysql

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'passwords'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

@app.route('/create_account', methods=['POST'])
def create_account():
    print(request.json)

    params = {
        'account' : request.json['account'],
        'password' : request.json['password'],
        'platform' : request.json['platform'],
        'note' : request.json['note']
    }
    query = """insert into accounts (account, password, platform, note) 
         values (%(account)s, %(password)s, %(platform)s, %(note)s)"""
    cursor.execute(query, params)
    conn.commit()

    content = {'id': cursor.lastrowid,
               'account': params['account'], 
               'password': params['password'], 
               'platform': params['platform'], 
               'note': params['note']
               }
    return jsonify(content)

@app.route('/accounts', methods=['GET'])
def tasks():
    cursor.execute("SELECT * from accounts")
    #data = cursor.fetchone() # obtiene un registro
    rv = cursor.fetchall()
    data = []
    content = {}
    for result in rv:
        content = {'id': result[0], 
                   'account': result[1], 
                   'password': result[2],
                   'platform': result[3],
                   'note': result[4]
                   }
        data.append(content)
        content = {}
    return jsonify(data)


@app.route('/account/<platform>', methods=['GET'])
def account(platform):
    cursor.execute("SELECT * from accounts where platform='"+platform+"'")
    rv = cursor.fetchall()

    data = []
    content = {}
    for result in rv:
        content = {'id': result[0], 
                   'account': result[1], 
                   'password': result[2],
                   'platform': result[3],
                   'note': result[4]
                   }
        data.append(content)
        content = {}
    return jsonify(data)

@app.route('/delete_account/<id>', methods = ['POST'])
def delete_account(id):
    params = {'id' : id}      
    query = """delete from accounts where id = %(id)s RETURNING id"""    
    cursor.execute(query, params)
    conn.commit()

    account_id = cursor.fetchone()
    if account_id:
        data = {
            'account_id': account_id[0],
            'eliminado' : "True",
        }
    else:
        data = {
            'account_id': id,
            'eliminado' : "False",
        }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)