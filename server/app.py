#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    if request.method == 'POST':
        baked_goods = BakedGood(
            id=request.form.get('id'),
            name=request.form.get('name'),
            bakery_id=request.form.get('bakery_id'),
            created_at=request.form.get('created_at'),
            updated_at=request.form.get('updated_at'),
        )
        db.session.add(baked_goods)
        db.session.commit()
        baked_goods_dict = baked_goods.to_dict()
        response = make_response(jsonify(baked_goods_dict), 201)  # 201 Created status code for POST
        return response
    
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakeries_name(id):
    if request.method == 'PATCH':
        bakery = Bakery.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            bakery_dict=bakery.to_dict()

            response=make_response(jsonify(bakery_dict), 200)
            return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    if request.method=="DELETE":
        db.session.delete(baked_good)
        db.session.commit()
        response_body={"deleted":True,
                        "message":"Baked good deleted successfully", 
                        }
        response=make_response(jsonify(response_body), 200)
        return response
    else:
        response=make_response("Baked good not found", 404)  
        return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)