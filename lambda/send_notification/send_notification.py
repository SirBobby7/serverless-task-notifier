import boto3
import json

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = 'TaskNotifications'  # 🔁 Replace
TOPIC_ARN = 'arn:aws:sns:REGION:ACCOUNT_ID:NotificationTopic'  # 🔁 Replace

def lambda_handler(event, context):
    task_id = event['taskId']

    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={'taskId': task_id})

    if 'Item' in response:
        task = response['Item']
        message = f"Hi {task['name']},\n\nYour scheduled task is here!\n\nTitle: {task['title']}\nDetails: {task['details']}\nTime: {task['datetime']}"
        
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Task Alert Notification",
            Message=message
        )
        return {'statusCode': 200, 'body': 'Notification sent'}
    else:
        return {'statusCode': 404, 'body': 'Task not found'}
