from flask import request

from app import app

items = []


@app.route('/')
def hello():
    return 'Hello, Flask!'


@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200


@app.route('/items', methods=['GET'])
def get_items():
    return {'items': items}


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id < len(items):
        return {'item': items[item_id]}
    return {'error': 'Item not found'}, 404


@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json(silent=True) or {}
    if not isinstance(item, dict):
        return {'error': 'JSON object required'}, 400
    items.append(item)
    return {'message': 'Item added successfully'}, 201
