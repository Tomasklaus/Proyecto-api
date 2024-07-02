from flask import Flask, request, jsonify
from services import DynamoDBService
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Inicializar el servicio de DynamoDB
dynamodb_service = DynamoDBService(
    region_name='tu-region', 
    aws_access_key_id='tu-access-key-id', 
    aws_secret_access_key='tu-secret-access-key', 
    table_name='tu-nombre-de-tabla'
)

# Ruta para obtener un item por User y Order
@app.route('/get_item', methods=['GET'])
def get_item():
    user = request.args.get('user')
    order = request.args.get('order')
    
    try:
        item = dynamodb_service.get_item(user, order)
        if item:
            return jsonify(item)
        else:
            return jsonify({'message': 'Item not found'}), 404
    except (NoCredentialsError, PartialCredentialsError):
        return jsonify({'message': 'Error with AWS credentials'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Ruta para agregar un item
@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    user = data.get('user')
    order = data.get('order')
    details = data.get('details')

    if not user or not order or not details:
        return jsonify({'message': 'Invalid input'}), 400
    
    try:
        dynamodb_service.add_item(user, order, details)
        return jsonify({'message': 'Item added successfully'})
    except (NoCredentialsError, PartialCredentialsError):
        return jsonify({'message': 'Error with AWS credentials'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Ruta para actualizar un item
@app.route('/update_item', methods=['PUT'])
def update_item():
    data = request.json
    user = data.get('user')
    order = data.get('order')
    details = data.get('details')

    if not user or not order or not details:
        return jsonify({'message': 'Invalid input'}), 400

    try:
        dynamodb_service.update_item(user, order, details)
        return jsonify({'message': 'Item updated successfully'})
    except (NoCredentialsError, PartialCredentialsError):
        return jsonify({'message': 'Error with AWS credentials'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Ruta para eliminar un item
@app.route('/delete_item', methods=['DELETE'])
def delete_item():
    user = request.args.get('user')
    order = request.args.get('order')

    try:
        dynamodb_service.delete_item(user, order)
        return jsonify({'message': 'Item deleted successfully'})
    except (NoCredentialsError, PartialCredentialsError):
        return jsonify({'message': 'Error with AWS credentials'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)



