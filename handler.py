import json
import boto3
import os
import time
import random


def invalidate(event, context):
    print(event)
    Items = ["/" + record['s3']['object']['key']
             for record in event['Records']]
    client = boto3.client("cloudfront")
    response = client.create_invalidation(
        DistributionId=os.getenv("CLOUDFRONT_DISTRIBUTION_ID"),
        InvalidationBatch={
            'Paths': {
                'Quantity': len(Items),
                'Items': Items,
            },

            # borrowed from aws-cli/awscli/customizations/cloudfront.py
            'CallerReference': '%s-%s-%s' % ('cli', int(time.time()), random.randint(1, 1000000))
        }
    )
    print(response)
    response = {
        "statusCode": 200,
        "body": json.dumps({
            'event': event,
            'response': str(response)
        })
    }
    return response
