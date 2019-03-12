from flask_restful import Resource
from flask import request
from models import CategoryModel,IncomeModel,BarcodeModel

# this resource will create,update,read and delete the income resource
# A post request expects json with the following fields

class Income(Resource):
    #     read a specific income
    def get(self, id):
        id, name, amount,date,barcodeId,categoryId = CategoryModel.fetchbyId(id).values()
        return {"id": id, "name": name, "amount": amount,"date":date,"barcodeId":barcodeId,"categoryId":categoryId}, 200

    # update a  specific income
    def put(self, id):
        if request.is_json:
            newName = request.get_json()['name'] if request.get_json()['name'] else None
            newAmount = request.get_json()['amount'] if request.get_json()['budget'] else None
            newDate = request.get_json()['date'] if request.get_json()['date'] else None
            newBarcodeId = request.get_json()['barcodeId'] if request.get_json()['barcodeId'] else None
            newCategoryId = request.get_json()['categoryId'] if request.get_json()['categoryId'] else None
            try:
                updated = IncomeModel.updateby_id(id, newName=newName, newAmount=newAmount,newDate=newDate,newBarcodeId=newBarcodeId,newCategoryId=newCategoryId)
                if updated:
                    return {"Message": "{} updated successfully".format(id)}, 200
                else:
                    return {"Message": "Update not done"}, 500
            except:
                return {"Message": "Something is wrong"}, 500
        else:
            return {"Message": "None Json data sent"}, 400

    # delete a specific income
    def delete(self, id):
        try:
            deleted = IncomeModel.deletebyId(id)
            if deleted:
                return {"Message": "{} deleted successfully".format(id)}, 200
            else:
                return {"Message": "Nothing is deleted"}, 400
        except:
            return {"Message": "Something is wrong in the server"}, 500

class Incomes(Resource):
    # create a record
    def post(self):
        if request.is_json:
            name = request.get_json()['name']
            amount = request.get_json()['amount']
            date = request.get_json()['date']
            barcodeId = request.get_json()['barcodeId']
            categoryId = request.get_json()['categoryId']

            if name == None or name == '' or categoryId == '':
                return {"Message": "Some fields are empty".format(name)}, 400

            if bool(CategoryModel.fetchbyId(categoryId)) != True:
                return {"Message": "Add a valid income Category first"},400

            if bool(BarcodeModel.findby_id(barcodeId)) != True and barcodeId:
                return {"Message": "Add a valid Barcode first"},400

            try:
                income = IncomeModel(name=name, amount=amount,date=date,barcodeId=barcodeId,categoryId=categoryId)
                income.save_record()
                return {"Message": "Income {} Created Successfully".format(name)}, 200
            except:
                return {"Message": "Unable to create Income"}, 500
        else:
            return {"Message": "Only JSON objects accepted"}, 400
        # get a specific category details

    #  read all
    def get(self):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name,
                'amount': x.amount,
                'date':x.date,
                'barcodeId':x.barcodeId,
                'categoryId':x.categoryId
            }
        return {'incomes': list(map(lambda x:to_json(x),IncomeModel.find_all()))},200

    # delete all
    def delete(self):
        try:
            deleted = IncomeModel.delete_all()
            if deleted:
                return {"Message": "{} rows deleted successfully".format(deleted)}, 200
            else:
                return {"Message": "Nothing is deleted"}, 400
        except:
            return {"Message": "Something is wrong in the server"}, 500

class Category(Resource):
    #     read
    def get(self, name):
        record = CategoryModel.fetchby_name(name)
        if record:
            id = record.id
            name = record.name
            budget = record.budget
            return {"id":id,"name":name,"budget":budget}, 200
        return {"Message":"{} Record not Found".format(name)},404

    # update a category
    def put(self, name):
        if request.is_json:
            newName = request.get_json()['name'] if request.get_json()['name'] else None
            newBudget = request.get_json()['budget'] if request.get_json()['budget'] else None
            try:
                updated = CategoryModel.updateby_name(name=name, newName=newName, newBudget=newBudget)
                if updated:
                    return {"Message": "{} updated successfully".format(name)}, 200
                else:
                    return {"Message": "Update not done"}, 500
            except:
                return {"Message": "Something is wrong"}, 500
        else:
            return {"Message": "None Json data sent"}, 400
    # delete
    def delete(self, name):
        try:
            deleted = CategoryModel.deleteby_name(name)
            if deleted:
                return {"Message": "{} deleted successfully".format(name)}, 200
            else:
                return {"Message": "Nothing is deleted"}, 400
        except:
            return {"Message": "Something is wrong in the server"}, 500

class Categories(Resource):
    # create a record
    def post(self):
        if request.is_json:
            try:
                name = request.get_json()['name']
                budget = int(request.get_json()['budget'])
                if name == None or name == '':
                    return {"Message": "Name field cannot be {}".format(name)}, 400
            except:
                return {"Message": "Your Json Body is not right"}, 400


            if CategoryModel.fetchby_name(name=name):
                return {"Message": "Category {} Already Exists".format(name)}, 409

            try:
                category = CategoryModel(name=name, budget=budget)
                category.save_record()
                return {"Message": "Category {} Created Successfully".format(name)}, 200
            except:
                return {"Message": "Unable to create Category"}, 500
        else:
            return {"Message": "Only JSON objects accepted"}, 400
        # get a specific category details

    #     read all
    def get(self):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name,
                'budget': x.budget
            }
        return {"categories": list(map(lambda x:to_json(x),CategoryModel.find_all()))},200

    # delete all
    def delete(self):
        try:
            deleted = CategoryModel.delete_all()
            if deleted:
                return {"Message": "{} rows deleted successfully".format(deleted)}, 200
            else:
                return {"Message": "Nothing is deleted"}, 400
        except:
            return {"Message": "Something is wrong in the server"}, 500

class Barcode(Resource):
    #     read by id
    def get(self, id):
        id, code, productName, amount = BarcodeModel.findby_id(id).values()
        return {"id": id, "code": code, "productName": productName, "amount": amount}, 200

    # update a barcode by id
    def put(self, id):
        if request.is_json:
            newCode = request.get_json()['code'] if request.get_json()['code'] else None
            newProductName = request.get_json()['productName'] if request.get_json()['productName'] else None
            newAmount = request.get_json()['amount'] if request.get_json()['amount'] else None
            try:
                updated = BarcodeModel.updatebyId(id=id, newCode=newCode, newProductName=newProductName, newAmount=newAmount)
                if updated:
                    return {"Message": "{} updated successfully".format(id)}, 200
                else:
                    return {"Message": "Update not done"}, 500
            except:
                return {"Message": "Something is wrong"}, 500
        else:
            return {"Message": "None Json data sent"}, 400

    # delete by id
    def delete(self, id):
        try:
            deleted = BarcodeModel.deletebyId(id)
            if deleted:
                return {"Message": "{} deleted successfully".format(id)}, 200
            else:
                return {"Message": "Nothing is deleted"}, 400
        except:
            return {"Message": "Something is wrong on the server"}, 500

class Barcodes(Resource):
    # create a record
    def post(self):
        if request.is_json:
            code = request.get_json()['code']
            productName = request.get_json()['productName']
            amount = request.get_json()['amount']

            if code == None or code == '' or productName == '':
                return {"Message": "Some fields are empty"}, 400

            if BarcodeModel.findby_code(code):
                return {"Message":"{} already exsits".format(code)}
            try:
                barcode = BarcodeModel(code=code, productName=productName, amount=amount)
                barcode.save_record()
                return {"Message": "Barcode {} Register Successfully".format(code)}, 200
            except:
                return {"Message": "Unable to create Income"}, 500
        else:
            return {"Message": "Only JSON objects accepted"}, 400
        # get a specific category details

    # read all
    def get(self):
        def to_json(x):
            return {
                'id': x.id,
                'code': x.code,
                'productName': x.productName,
                'amount': x.amount
            }
        return {list(map(lambda x:to_json(x),BarcodeModel.find_all()))},200

    # delete all
    def delete(self):
        try:
            deleted = BarcodeModel.delete_all()
            if deleted:
                return {"Message": "{} rows deleted successfully".format(deleted)}, 200
            else:
                return {"Message": "Nothing is deleted"}, 400
        except:
            return {"Message": "Something is wrong in the server"}, 500


