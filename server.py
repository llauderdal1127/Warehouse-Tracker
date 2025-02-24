from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/add', methods=['POST'])
def add_item():
    data = request.json
    new_item = Inventory(location=data['location'], item=data['item'], quantity=data['quantity'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item added successfully!"})

@app.route('/get', methods=['GET'])
def get_inventory():
    inventory = Inventory.query.all()
    return jsonify([{"location": i.location, "item": i.item, "quantity": i.quantity} for i in inventory])

if __name__ == '__main__':
    app.run(debug=True)
