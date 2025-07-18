import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
eventbridge = boto3.client('scheduler')

TABLE_NAME = 'TaskNotifications'  # 🔁 Replace this with your table name
LAMBDA_TARGET_ARN = 'arn:aws:lambda:REGION:ACCOUNT_ID:function:send_notification'  # 🔁 Replace

def lambda_handler(event, context):
    body = json.loads(event['body'])
    task_id = str(uuid.uuid4())
    date_str = body['datetime']  # Expected: 'dd/mm/yy HH:MM'
    datetime_obj = datetime.strptime(date_str, "%d/%m/%y %H:%M")

    # Save to DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        'taskId': task_id,
        'name': body['name'],
        'email': body['email'],
        'title': body['title'],
        'details': body['details'],
        'datetime': date_str
    })

    # Schedule EventBridge task
    schedule_name = f"task-{task_id}"
    eventbridge.create_schedule(
        Name=schedule_name,
        ScheduleExpression=f"at({datetime_obj.strftime('%Y-%m-%dT%H:%M:00')})",
        FlexibleTimeWindow={'Mode': 'OFF'},
        Target={
            'Arn': LAMBDA_TARGET_ARN,
            'RoleArn': 'arn:aws:iam::ACCOUNT_ID:role/YOUR_EVENTBRIDGE_ROLE',  # 🔁 Replace
            'Input': json.dumps({'taskId': task_id})
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Plan scheduled successfully'})
    }
