from flask import Flask,render_template,request,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import  sys
from flask_migrate import  Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://postgres:123@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False)
    image=db.Column(db.String(),nullable=False)
    url=db.Column(db.String(),nullable=False)
    def __repr__(self):
     return f'Id: {self.id}, Name: {self.name} Email: {self.email}, Image: {self.image}, Url: {self.url}'
    pass

users = Person.query.order_by('id').all()
@app.route('/user/create', methods=['POST'])
def create_user():
   error=False
   try:
    name= request.get_json()['name']
    email= request.get_json()['email']
    image= request.get_json()['image']
    url= request.get_json()['url']
    newuser=Person(name=name,email=email,image=image,url=url)
    db.session.add(newuser)
    db.session.commit()
   except:
    db.session.rollback()
    error=True
    print(sys.exc_info())
   finally:
    db.session.close()
   if not error:
     return redirect(url_for('User',user_id=16))

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        Person.query.filter_by(id=user_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})
@app.route('/')
def Home():
    return render_template('home.html',title='Hello, Home',users=users)
@app.route('/user/<user_id>')
def User(user_id):
    per = [Person.query.get(user_id)]
    if per :
     return render_template('user.html',users=per)

if __name__ == '__main__':
    app.debug= True
    app.run()
