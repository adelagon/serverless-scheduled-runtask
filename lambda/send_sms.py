import boto3
import sys
import os

def handler(event, context):
    try:
        sns = boto3.client(
            "sns",
            region_name="ap-southeast-1",
            aws_access_key_id=os.environ.get("AWS_USER_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("AWS_USER_SECRET_KEY")
        )

        sns.set_sms_attributes(
            attributes={
                "DefaultSMSType": "Transactional",
                "DeliveryStatusSuccessSamplingRate": "100",
                "DefaultSenderID": "AWS"
            }
        )

        response = sns.publish(
            PhoneNumber=os.environ.get("MSISDN"),
            Message=os.environ.get("MESSAGE")
        )
    except Exception as e:
        print ("Error", e)
