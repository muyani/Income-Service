import datetime
from main import db



# income category model
class CategoryModel(db.Model):
    __tablename__ = 'income_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    budget = db.Column(db.Float, nullable=True)
    incomes = db.relationship('IncomeModel',backref = 'category')

    # create
    def save_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # read
    @classmethod
    def fetchby_name(cls, name):
        return cls.query.filter_by(name=name).first()
    # read
    @classmethod
    def fetchbyId(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # update
    @classmethod
    def updateby_name(cls, name, newName=None, newBudget=None):
        record = cls.query.filter_by(name=name).first()
        if record:
            print(newName)
            record.name = newName if newName else record.name
            print(record.name)
            record.budget = newBudget if newBudget else record.budget
            print(record.budget)
            db.session.commit()
            return cls.query.filter_by(name=newName).first()
        else:
            return False

    # delete

    @classmethod
    def delete_all(cls):
        try:
            deleted = db.session.query(cls).delete()
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def deleteby_name(cls, name):
        record = cls.query.filter_by(name=name)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False

# barcode model
class BarcodeModel(db.Model):
    __tablename__ = 'barcodes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(500),unique=True,nullable=False)
    productName = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=True)

    # create
    def save_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # read
    @classmethod
    def findby_code(cls, code):
        return cls.query.filter_by(code=code).first()

    # read
    @classmethod
    def findby_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # update
    @classmethod
    def updatebyId(cls, id, newCode=None, newProductName=None, newAmount=None):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.code = newCode if newCode else record.code
            record.amount = newAmount if newAmount else record.amount
            record.productName = newProductName if newProductName else record.productName
            db.session.commit()
            return cls.query.filter_by(id=id).first()
        else:
            return False

    # delete
    @classmethod
    def delete_all(cls):
        try:
            deleted = db.session.query(cls).delete()
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def deletebyId(cls, id):
        record = cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False

#  income model
class IncomeModel(db.Model):
    __tablename__ = 'incomes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    amount = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime,default = datetime.datetime.utcnow)
    usernumber = db.Column(db.Integer, nullable=False, unique=False)
    barcodeId = db.Column(db.Integer,db.ForeignKey('barcodes.id'),nullable=True)
    barcode = db.relationship(BarcodeModel)
    categoryId = db.Column(db.Integer, db.ForeignKey('income_categories.id'))


    # create
    def save_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # read
    @classmethod
    def findby_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls,uid):
        return cls.query.filter_by(usernumber = uid).all()
    # update
    @classmethod
    def updateby_id(cls, id, newName=None, newAmount=None, newCategoryId=None, newBarcodeId=None):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.name = newName if newName else record.name
            record.amount = newAmount if newAmount else record.amount
            record.categoryId = newCategoryId if newCategoryId else record.categoryId
            record.barcodeId = newBarcodeId if newBarcodeId else record.barcodeId
            db.session.commit()
            return cls.query.filter_by(id=id).first()
        else:
            return False

    # delete
    @classmethod
    def delete_all(cls):
        try:
            deleted = db.session.query(cls).delete()
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def deletebyId(cls, id):
        record = cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False
