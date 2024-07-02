import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class DynamoDBService:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, table_name):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name, 
                                       aws_access_key_id=aws_access_key_id, 
                                       aws_secret_access_key=aws_secret_access_key)
        self.table = self.dynamodb.Table(table_name)
    
    def get_item(self, user, order):
        try:
            response = self.table.get_item(Key={'User': user, 'Order': int(order)})
            return response.get('Item', None)
        except (NoCredentialsError, PartialCredentialsError):
            raise
        except Exception as e:
            raise
    
    def add_item(self, user, order, details):
        try:
            self.table.put_item(Item={'User': user, 'Order': int(order), 'Details': details})
        except (NoCredentialsError, PartialCredentialsError):
            raise
        except Exception as e:
            raise
    
    def update_item(self, user, order, details):
        try:
            self.table.update_item(
                Key={'User': user, 'Order': int(order)},
                UpdateExpression="set Details=:d",
                ExpressionAttributeValues={':d': details},
                ReturnValues="UPDATED_NEW"
            )
        except (NoCredentialsError, PartialCredentialsError):
            raise
        except Exception as e:
            raise
    
    def delete_item(self, user, order):
        try:
            self.table.delete_item(Key={'User': user, 'Order': int(order)})
        except (NoCredentialsError, PartialCredentialsError):
            raise
        except Exception as e:
            raise
