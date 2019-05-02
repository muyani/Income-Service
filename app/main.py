import datetime
from flask import Flask,make_response,jsonify
from flask_restplus import Api,Resource,fields,reqparse,marshal
from flask_sqlalchemy import SQLAlchemy
DB_URL = 'postgresql://postgres:123@127.0.0.1:5432/incomeService'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'very_secret'
db = SQLAlchemy(app)
import models

api = Api(app)

ns = api.namespace('api/v1',description='Bizweb Income Microservice')


incomeParser = reqparse.RequestParser()
incomeParser.add_argument('name', type=str, help='Name of Income',required= True)
incomeParser.add_argument('amount', type=str, help='Amount of Income',required=True)
incomeParser.add_argument('barcodeId', type=int, help='Barcode Id',required= False)
incomeParser.add_argument('categoryId', type=int, help='Category Id',required= True)


incomeUpdateParser = reqparse.RequestParser()
incomeUpdateParser.add_argument('name', type=str, help='New name',required= False)
incomeUpdateParser.add_argument('amount', type=str, help='New Amount',required= False)
incomeUpdateParser.add_argument('barcodeId', type=int, help='Change Barcode Id',required= False)
incomeUpdateParser.add_argument('categoryId', type=int, help='Change Category Id',required= False)


catUpdateParser = reqparse.RequestParser()
catUpdateParser.add_argument('name', type=str, help='New name',required= False)
catUpdateParser.add_argument('budget', type=str, help='New Category Budget',required= False)


catParser = reqparse.RequestParser()
catParser.add_argument('name', type=str, help='Name of Category',required= True)
catParser.add_argument('budget', type=str, help='Category Budget',required= False)


barUpdateParser = reqparse.RequestParser()
barUpdateParser.add_argument('code', type=str, help='New Bar Code',required= False)
barUpdateParser.add_argument('productName', type=str, help='New Product Name',required= False)
barUpdateParser.add_argument('amount', type=str, help='New Amount attached to Barcode',required= False)


barParser = reqparse.RequestParser()
barParser.add_argument('code', type=str, help=' Bar Code',required= True)
barParser.add_argument('productName', type=str, help='Product Name',required= True)
barParser.add_argument('amount', type=str, help=' Amount attached to Barcode',required= True)

incomeStructure = api.model('Income', {
    'id': fields.Integer,
    'name': fields.String,
    'amount': fields.String,
    'date': fields.DateTime,
    'usernumber': fields.String,
    'barcodeId': fields.Integer,
    'categoryId': fields.Integer
})

categoryStructure = api.model('Category', {
    'id': fields.Integer,
    'name': fields.String,
    'budget': fields.Float
})

barcodeStructure = api.model('Barcode', {
    'id': fields.Integer,
    'code': fields.String,
    'productName': fields.String,
    'amount': fields.Float
})


@app.errorhandler(400)
def badRequest(e):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def notFound(e):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@app.errorhandler(405)
def notAllowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@app.errorhandler(500)
def internalServer(e):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

@app.before_first_request
def create_tables():
    db.create_all()

@ns.route('/')
class Homepage(Resource):
    def get(self):
        return {"message":"This is a private api"},200
    def post(self):
        return {"message":"This is a private api"},200

@ns.route('/incomes/<int:uid>/<int:id>')
class Income(Resource):
    def get(self, uid,id):
        record = models.IncomeModel.findby_id(id)
        if record and record.usernumber == uid :
            return marshal(record,incomeStructure),200
        return {'message':'not found'},404
    # update a  specific income
    @ns.expect(incomeUpdateParser)
    def put(self,uid, id):
        body = incomeUpdateParser.parse_args()
        newName = body['name'] if body['name'] else None
        newAmount = body['amount'] if body['amount'] else None
        newBarcodeId = body['barcodeId'] if body['barcodeId'] else None
        newCategoryId = body['categoryId'] if body['categoryId'] else None
        try:
            income = models.IncomeModel.findby_id(id)
            if income.usernumber == uid:
                record = models.IncomeModel.updateby_id(id, newName=newName, newAmount=newAmount,newBarcodeId=newBarcodeId,newCategoryId=newCategoryId)
                if record:
                    return marshal(record,incomeStructure), 200
                else:
                    return {"message": "Record not found"}, 404
            else:
                return {"message": "Record not found"}, 404

        except:
            return {"message": "Something is wrong"}, 500

    # delete a specific income
    def delete(self,uid, id):
        income = models.IncomeModel.findby_id(id)
        if income.usernumber != uid:
            return {"message": "Record not found"}, 404
        try:
            deleted = models.IncomeModel.deletebyId(id)
            if deleted:
                return {"message": "{} deleted successfully".format(id)}, 200
            else:
                return {"message": "Nothing is deleted"}, 400
        except:
            return {"message": "Something is wrong in the server"}, 500

@ns.route('/incomes/<int:uid>')
class Incomes(Resource):
    @ns.expect(incomeParser)
    def post(self,uid):
        body = incomeParser.parse_args()
        name = body['name']
        amount = body['amount']
        barcodeId = body['barcodeId']
        categoryId = body['categoryId']
        if bool(models.CategoryModel.fetchbyId(categoryId)) != True:
            return {"message": "Add a valid income Category first"},400
        if bool(models.BarcodeModel.findby_id(barcodeId)) != True and barcodeId:
            return {"message": "Add a valid Barcode first"},400
        income = models.IncomeModel(name=name, amount=amount,usernumber = uid,barcodeId=barcodeId,categoryId=categoryId)
        record = income.save_record()
        return marshal(record,incomeStructure), 200

    #  read all
    def get(self,uid):
        records = models.IncomeModel.find_all(uid)
        return marshal(records,incomeStructure),200

    # # delete all
    # def delete(self):
    #     try:
    #         deleted = models.IncomeModel.delete_all()
    #         if deleted:
    #             return {"message": "All rows deleted successfully"}, 200
    #         else:
    #             return {"message": "Nothing is deleted"}, 400
    #     except:
    #         return {"message": "Something is wrong in the server"}, 500

@ns.route('/categories/<string:cat_name>')
class Category(Resource):
    def get(self, cat_name):
        record = models.CategoryModel.fetchby_name(cat_name)
        if record:
            return marshal(record,categoryStructure),200
        return {"message":"{} Record not Found".format(cat_name)},404
    # update a category
    @ns.expect(catUpdateParser)
    def put(self, cat_name):
        body = catUpdateParser.parse_args()
        newName =body['name'] if body['name'] else None
        newBudget = body['budget'] if body['budget'] else None
        try:
            record = models.CategoryModel.updateby_name(name=cat_name, newName=newName, newBudget=newBudget)
            if record:
                return marshal(record,categoryStructure), 200
            else:
                return {"message": "Record not found"}, 404
        except:
            return {"message": "Something is wrong"}, 500
    # delete
    def delete(self, cat_name):
        try:
            deleted = models.CategoryModel.deleteby_name(cat_name)
            if deleted:
                return {"message": "{} deleted successfully".format(cat_name)}, 200
            else:
                return {"message": "Nothing is deleted"}, 404
        except:
            return {"message": "Cannot delete {} because it is a parent of some incomes".format(cat_name)}, 409





@ns.route('/categories')
class Categories(Resource):
    @ns.expect(catParser)
    def post(self):
        body = catParser.parse_args()
        name = body['name']
        budget = float(body['budget']) if body['budget'] else None
        if models.CategoryModel.fetchby_name(name=name):
            return {"message": "Category {} Already Exists".format(name)}, 409
        try:
            category = models.CategoryModel(name=name, budget=budget)
            record = category.save_record()
            return marshal(record,categoryStructure), 200
        except:
            return {"message": "Unable to create Category"}, 500

    def get(self):
        records = models.CategoryModel.find_all()
        return marshal(records,categoryStructure),200

    # delete all
    def delete(self):
        try:
            deleted = models.CategoryModel.delete_all()
            if deleted:
                return {"message": "All rows deleted successfully"}, 200
            else:
                return {"message": "Nothing is deleted"}, 404
        except:
            return {"message": "Something is wrong in the server"}, 500

@ns.route('/barcodes/<int:bid>')
class Barcode(Resource):
    def get(self, bid):
        record = models.BarcodeModel.findby_id(bid)
        if record:
            return marshal(record,barcodeStructure)
        return {"message":" Record {} not Found".format(bid)},404

    @ns.expect(barUpdateParser)
    def put(self, bid):
        body = barUpdateParser.parse_args()
        newCode = body['code'] if body['code'] else None
        newProductName = body['productName'] if body['productName'] else None
        newAmount = body['amount'] if body['amount'] else None
        try:
            record = models.BarcodeModel.updatebyId(id=bid, newCode=newCode, newProductName=newProductName, newAmount=newAmount)
            if record:
                return marshal(record,barcodeStructure), 200
            else:
                return {"message": "Record not found"}, 404
        except:
            return {"message": "Code already exists(cannot have duplicates)"}, 409

    # delete by id
    def delete(self, bid):
        try:
            deleted = models.BarcodeModel.deletebyId(bid)
            if deleted:
                return {"message": "{} deleted successfully".format(bid)}, 200
            else:
                return {"message": "Nothing is deleted"}, 400
        except:
            return {"message": "Something is wrong on the server"}, 500

@ns.route('/barcodes')
class Barcodes(Resource):
    @ns.expect(barParser)
    def post(self):
        body = barParser.parse_args()
        code = body['code']
        productName = body['productName']
        amount = body['amount']
        if models.BarcodeModel.findby_code(code):
            return {"message":"{} already exists".format(code)}
        try:
            barcode = models.BarcodeModel(code=code, productName=productName, amount=amount)
            record = barcode.save_record()
            return marshal(record,barcodeStructure), 200
        except:
            return {"message": "Unable to create Income"}, 500

    # read all
    def get(self):
        records = models.BarcodeModel.find_all()
        return marshal(records,barcodeStructure),200

    # delete all
    def delete(self):
        try:
            deleted = models.BarcodeModel.delete_all()
            if deleted:
                return {"message": "All rows deleted successfully"}, 200
            else:
                return {"message": "Nothing is deleted"}, 404
        except:
            return {"message": "Something is wrong in the server"}, 500

