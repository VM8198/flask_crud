from flask import *  
from flask import Flask  
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import *
import os

app = Flask(__name__) #creating the Flask class object 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask'
app.secret_key = "demo_app"  
mysql = MySQL(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "helloFlask"  
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

# @app.route('/get',methods = ['GET','POST'])
# def get():
# 	if request.method == 'GET':
# 		# details = request.form
# 		# fname = details['fname']
# 		# lname = details['lname']
# 		peter = user.query.filter_by(name = 'vivek malvi').all()		
# 		db.session.commit()
# 		return str(peter)

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
				access_token = create_access_token(identity = name)
				refresh_token = create_refresh_token(identity = name)
				return jsonify({'message': 'logged in successfully','access_token': access_token,'refresh_token': refresh_token})	
			else:
				return jsonify({"message": "wrong password"})
				abort(401)
		else:
			return ({"message": "user not found"})	


@app.route('/add', methods = ['POST'])
@jwt_required
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
@jwt_required
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
@jwt_required
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
@jwt_required
def delete(userName):
	if request.method == 'POST	':
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM user WHERE name = %s",[userName])	
		mysql.connection.commit()
		cur.close()		
	return jsonify({"message": "record deleted"})

@app.route('/update/<int:userId>/<string:data>', methods = ['POST'])
@jwt_required
def update(userId,data):
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute("UPDATE user SET name = %s WHERE id = %s",[data,userId])	
		mysql.connection.commit()
		cur.close()
	return jsonify({"message": "record updated"})

@app.route('/getAllUsers',methods = ['GET'])
# @jwt_required
def getAllUsers():
	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user")
		row_headers=[x[0] for x in cur.description]
		print(cur.description)
		users = cur.fetchall();
		mysql.connection.commit()
		cur.close()
		result = []
		for user in users:
			result.append(dict(zip(row_headers,user)))
		return jsonify(result)

@app.route('/upload-file', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return abort(404)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return abort(401)
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return "uploaded"
		
if __name__ =='__main__':  
	app.run(debug = True)






