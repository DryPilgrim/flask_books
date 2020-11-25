from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key='dry'

#1.数据库配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:duanyu@127.0.0.1:3306/flask_books"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

#2.定义作者类和书本类
class Author(db.Model):
    query = None
    __tablename__ = 'authors'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16), unique=True)
    books=db.relationship('Book',backref='author')
    def __repr__(self):
        return 'Author:%s'%self.name

class Book(db.Model):
    __tablename__='books'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(16),unique=True)
    author_id=db.Column(db.Integer,db.ForeignKey('authors.id'))
    def __repr__(self):
        return 'Book:%s %s'%(self.name,self.author_id)

#5.使用WTF显示表单
#自定义表单类
class AuthorForm(FlaskForm):
    author=StringField('作者',validators=[DataRequired()])
    book=StringField('书名',validators=[DataRequired()])
    submit=SubmitField('提交')


@app.route('/',methods=['GET','POST'])
def hello_world():
    #4.使用模板显示这些信息
    #查询所有数据，将数据传给模板
    authors=Author.query.filter_by(name='zs').first()#,authors=authors

    flask_form=AuthorForm()
    return render_template('books.html',authors=authors,form=flask_form)

#3.添加数据
db.drop_all()
db.create_all()
#生成数据
au1 = Author(name='zs')
au2 = Author( name='ls')
au3 = Author(name='ww')#把数据提交给用户会话*
db.session.add_all( [au1, au2, au3])#提交会话
db.session.commit()

bk1 = Book(name='zxc1',author_id=au1.id)
bk2 = Book(name="zxc2",author_id=au1.id)
bk3 = Book(name="zxc3",author_id=au2.id)
bk4 = Book(name="zxc4",author_id=au3.id)
bk5 = Book(name="zxc5",author_id=au3.id)
#把数据提交给用户会话
db.session.add_all( [bk1,bk2,bk3,bk4,bk5])
#提交会话
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
