from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

basedir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/sma"
#app.config['UPLOAD_FOLDER']  = os.path.join(basedir, 'upload')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
#print(os.path.abspath(__file__))  #pick the name of file given in paramter get current directory path APPEND both
#print(os.path.dirname(__file__))  #get the directory path of given file in parameter
#print(os.path.basename(__file__))  #return filename


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.users import User
from models.posts import Post
from models.degrees import Degree

#User.query.filter_by(name=username).first_or_404(description='There is no data with {}'.format(username))
#selectedUser = User.query.first()
#print(selectedUser.posts.all())   # because lazy is dynamic
#print(selectedUser.posts)   # because lazy is True/'select'


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                new_user = User(name=data['name'], grade=data['grade'], address=data['address'], country=data['country'])
                db.session.add(new_user)
                db.session.commit()
                return {"message": f"user {new_user.name} has been created successfully."}
            elif 'file' in request.files:
                f = request.files['file']
                filename = secure_filename(f.filename)
                if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # process File
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as fileUploaded:
                    header = fileUploaded.readline().strip().split(',')
                    for l in fileUploaded:
                        userList = l.strip().split(',')
                        userDict = dict(zip(header, userList))
                        #print(userDict)
                        new_user = User(name=userDict['name'], grade=userDict['grade'], address=userDict['address'],
                                        country=userDict['country'])
                        db.session.add(new_user)
                        db.session.commit()

                return f"{f.filename} Processed"
                #return redirect(url_for('uploaded_file', filename=filename))
            else:
                return {"error": "The request payload is not in JSON format"}
        except Exception as e:
            return {"Error":str(e)}
    elif request.method == 'GET':
        try:
            users = User.query.all()
            results = {}
            if users != None:
                results = [user.serialize() for user in users]
            return {"count": len(results), "users": results}
        except Exception as e:
            return {"error":str(e)}

@app.route('/getUserbyId/<userId>', methods=['GET'])
def getById(userId):
    users = User.query.get_or_404(userId)
    if request.method == 'GET':
        results = {}
        if users != None:
            users = [users]
            results =  [user.serialize() for user in users ]
        return {"message": "success", "Your User is ": results}

@app.route('/deleteuser/<userId>',methods=['GET'])
def deleteUserById(userId):
    user = User.query.get_or_404(userId)
    db.session.delete(user)
    db.session.commit()
    return {"message": f"User {user.name} successfully deleted."}

@app.route('/updateUser/<userId>',methods=['PUT'])
def updateUser(userId):
    user = User.query.get_or_404(userId)
    if request.method == 'PUT':
        newUserDetail = request.get_json()
        user.grade = newUserDetail['grade']
        user.country = newUserDetail['country']
        db.session.add(user)
        db.session.commit()
        return {"message": f"car {user.id} successfully updated"}

@app.route('/addUser', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                new_user = User(name=data['name'], grade=data['grade'], address=data['address'], country=data['country'])
                db.session.add(new_user)
                db.session.commit()
                return {"message": f"post {new_user.id} has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}
        except Exception as e:
            return {"Error":str(e)}
    elif request.method == 'GET':
        try:
             if len(request.args) ==4 and request.args.get('name') != None and request.args.get('grade') != None and request.args.get('address') != None and request.args.get('country') != None :
                 newUser = User(name=request.args['name'], grade=request.args['grade'], address=request.args['address'], country=request.args['country'])
                 db.session.add(newUser)
                 db.session.commit()
                 return {"message": f"post {newUser.id} has been created successfully."}
             else:
                 return {"error": "The request payload is not in JSON format"}
        except Exception as e:
            return {"Error":str(e)}

@app.route('/addDegree/<degreeName>', methods=['GET'])
def add_degrees(degreeName):
    try:
        if degreeName != None:
            new_degree = Degree(degreeName=degreeName)
            db.session.add(new_degree)
            db.session.commit()
            return {"message": f"Degree {new_degree.degreeName} is added successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    except Exception as e:
        return {"Error": str(e)}

@app.route('/addUserDegree', methods=['GET'])
def add_user_degree():
    try:
        if len(request.args) == 2 and request.args.get('degreeId') != None and request.args.get('userId') != None:
            user = User.query.get_or_404(request.args.get('userId'))
            degree = Degree.query.get_or_404(request.args.get('degreeId'))
            user.degrees.append(degree)
            db.session.add(user)
            db.session.commit()
            return {"message": f"user {user.name} {degree.degreeName} is added successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    except Exception as e:
        return {"Error": str(e)}

@app.route('/posts', methods=['POST', 'GET'])
def handle_posts():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                new_post = Post(userId=data['userId'], content=data['content'])
                db.session.add(new_post)
                db.session.commit()

                return {"message": f"post {new_post.id} has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}
        except Exception as e:
            return {"Error":str(e)}
    elif request.method == 'GET':
        try:
            posts = Post.query.all()
            results = [post.serialize() for post in posts]
            return {"count": len(results), "posts": results}
        except Exception as e:
            return {"error":str(e)}


if __name__ == '__main__':
    app.run()