from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
DB_URL = 'postgresql://postgres:123@127.0.0.1:5432/incomeService'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'very_secret'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

from resources import Income,Incomes,Category,Categories,Barcode,Barcodes



api = Api(app)

api.add_resource(Income,'/income/<int:id>')
api.add_resource(Incomes,'/income')
api.add_resource(Category,'/category/<string:name>')
api.add_resource(Categories,'/category')
api.add_resource(Barcode,'/barcode/<int:id>')
api.add_resource(Barcodes,'/barcode')



# if __name__ == '__main__':
#     app.run()
