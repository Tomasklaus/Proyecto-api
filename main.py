from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Configura la conexión a DynamoDB
dynamodb = boto3.resource('dynamodb', 
    region_name='sa-east-1',
     aws_access_key_id='AKIAQ3EGTC2PYB3LSSP7', 
     aws_secret_access_key='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')

# Selecciona la tabla
table = dynamodb.Table('testDB')

# Ruta para obtener un item por User y Order
@app.route('/get_item', methods=['GET'])
def get_item():
    user = request.args.get('user')
    order = request.args.get('order')
    
    try:
        response = table.get_item(Key={'User': user, 'Order': int(order)})
        item = response.get('Item', None)
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
        table.put_item(Item={'User': user, 'Order': int(order), 'Details': details})
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
        table.update_item(
            Key={'User': user, 'Order': int(order)},
            UpdateExpression="set Details=:d",
            ExpressionAttributeValues={':d': details},
            ReturnValues="UPDATED_NEW"
        )
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
        table.delete_item(Key={'User': user, 'Order': int(order)})
        return jsonify({'message': 'Item deleted successfully'})
    except (NoCredentialsError, PartialCredentialsError):
        return jsonify({'message': 'Error with AWS credentials'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)



