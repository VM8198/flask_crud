from flask import *  
from flask import Flask  
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__) #creating the Flask class object 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask'
app.secret_key = "demo_app"  
mysql = MySQL(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "helloFlask"  


class user(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	password = db.Column(db.String(100))


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'


@app.route('/')
def home():
	return render_template('signup.html')

# @app.route('/signup',methods = ['GET','POST'])
# def signup():
# 	if request.method == 'POST':
# 		details = request.form
# 		fname = details['fname']
# 		lname = details['lname']
# 		return render_template('login.html')

# @app.route('/login',methods = ['GET','POST'])
# def validate():
# 	if request.method == 'GET':
		# details = request.form
		# fname = details['fname']
		# lname = details['lname']
		# entry = user(firstName = fname, lastName = lname)
		# getUser = user.query.filter_by(firstName = 'asdas').first()
		# db.session.add(get)
		# db.session.commit()
		# cur = mysql.connection.cursor()
		# cur.execute("INSERT INTO user(firstName, lastName) VALUES (%s, %s)", (fname, lname))
		# cur.execute("SELECT * FROM user WHERE firstName = 'vivek'")
		# row_headers = [ x[0] for x in cur.description]
		# getUser = cur.fetchall()
		# json_data = []
		# for result in getUser:
		# 	json_data.append(dict(zip(row_headers,result)))
		# mysql.connection.commit()
		# cur.close()
		# return getUser
		# return json.dumps(json_data)
	# 	return render_template('registered.html',email = getUser)
	# return "hahahah"		
# @app.route('/logout',methods = ['GET','POST'])
# def logout():
# 	session.pop('email',None)
# 	return render_template('login.html')

# @app.route('/add', methods = ['GET','POST'])
# def addDetails():
# 	if request.method == 'POST':
# 		details = request.form
# 		name = details['name']
# 		cur = mysql.connection.cursor()
# 		cur.execute("INSERT INTO user(firstName) VALUES	%s",name)
# 		mysql.connection.commit()
# 		cur.close()
# 		flash("Record Added")
# 	return render_template('login.html')

# @app.route('/delete', methods = ['GET','POST'])
# def deleteDetails():
# 	cur = mysql.connection.cursor()
# 	cur.execute("DELETE FROM user WHERE firstName = 'gfgfgh'")
# 	mysql.connection.commit()
# 	cur.close()
# 	return "Record Deleted"

@app.route('/signup', methods = ['POST'])
def signup():
	if request.method == 'POST':
		details = request.form
		name = details['name']
		password = details['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user WHERE name = %s",[name])
		foundUser = cur.fetchall()
		if foundUser:
			return jsonify({"message": "user already exist"})
		else:
			pw_hash = bcrypt.generate_password_hash(password)
			cur.execute("INSERT INTO user(name, password) VALUES (%s,%s)",[name,pw_hash])	
			mysql.connection.commit()
			cur.close()
			return jsonify({'message': 'successfully registered'})

@app.route('/login', methods = ['POST'])
def login():
	if request.method == 'POST':
		details = request.form
		name = details['name']
		password = details['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user WHERE name = %s",[name])
		foundUser = cur.fetchone()
		if foundUser:
			pw_hash = bcrypt.check_password_hash(foundUser[2],password)
			if pw_hash:
				return jsonify({'message': 'logged in successfully'})	
			else:
				return jsonify({"message": "wrong password"})
				abort(401)
		else:
			return ({"message": "user not found"})	


@app.route('/add', methods = ['POST'])
def add():
	if request.method == 'POST':
		details = request.form
		name = details['name']
		password = details['password']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO user(name, password) VALUES (%s,%s)",[name,password])
		mysql.connection.commit()
		cur.close()		
	return jsonify({"message": "record added"})

@app.route('/getUserByName/<string:name>', methods = ['GET'])
def getUserByName(name):
	if request.method == 'GET':
		details = request.form
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user WHERE name = %s",[name])
		foundUser = cur.fetchall()
		mysql.connection.commit()
		cur.close()
	return jsonify({"user": foundUser})

@app.route('/getUserById/<int:uid>', methods = ['GET'])
def getUserById(uid):
	if request.method == 'GET':
		details = request.form
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user WHERE id = %s",[uid])
		foundUser = cur.fetchall()
		mysql.connection.commit()
		cur.close()
	return jsonify({"user": foundUser})


@app.route('/delete/<string:userName>', methods = ["POST"])
def delete(userName):
	if request.method == 'POST	':
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM user WHERE name = %s",[userName])	
		mysql.connection.commit()
		cur.close()		
	return jsonify({"message": "record deleted"})

@app.route('/update/<int:userId>/<string:data>', methods = ['POST'])
def update(userId,data):
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute("UPDATE user SET name = %s WHERE id = %s",[data,userId])	
		mysql.connection.commit()
		cur.close()
	return jsonify({"message": "record updated"})

if __name__ =='__main__':  
    app.run(debug = True)






