from app import db

# income category model
class CategoryModel(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    budget = db.Column(db.Float, nullable=True)

    # create
    def save_record(self):
        db.session.add(self)
        db.session.commit()

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
            return True
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
    __tablename__ = 'barcode'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(500),unique=True,nullable=False)
    productName = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=True)

    # create
    def save_record(self):
        db.session.add(self)
        db.session.commit()

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
            return True
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
    __tablename__ = 'income'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    amount = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime)
    barcodeId = db.Column(db.Integer,db.ForeignKey('barcode.id'))
    barcode = db.relationship(BarcodeModel)
    categoryId = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(CategoryModel)

    # create
    def save_record(self):
        db.session.add(self)
        db.session.commit()

    # read
    @classmethod
    def findby_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # update
    @classmethod
    def updateby_id(cls, id, newName=None, newAmount=None, newDate=None, newCategoryId=None, newBarcodeId=None):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.name = newName if newName else record.name
            record.amount = newAmount if newAmount else record.amount
            record.date = newDate if newDate else record.date
            record.categoryId = newCategoryId if newCategoryId else record.categoryId
            record.barcodeId = newBarcodeId if newBarcodeId else record.barcodeId
            db.session.commit()
            return True
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
