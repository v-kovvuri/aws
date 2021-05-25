import boto3
import logging
import os
import sys
from botocore.config import Config
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

ec2_resource = boto3.resource('ec2', region_name='us-east-1')
s3 = boto3.resource('s3')
ssm_client = boto3.client('ssm', region_name='us-east-1')

ami_parameter = ssm_client.get_parameter(Name='/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id')
ami_id = ami_parameter['Parameter']['Value']
logging.info("Imageid:" + ami_id)


for i in range(1,11):
    print(i)
instance_name = 'myinstance' + str(i)
print("instance_name:"+instance_name)
bucket_name = 'mys3bucket' + str(i)
print("bucket_name:"+bucket_name)
#Creating EC2 Resource with t3 micro
try:
    response = ec2_resource.create_instances(
        ImageId=ami_id,
        InstanceType='t3.micro',
        MaxCount=1,
        MinCount=1,
        KeyName='test',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                        },
                    ]
                },
            ]
        )
except Exception as e:
    logging.error(e)
id = response[0].instance_id
#id refers to instanceid
print(id)
f = open(id+".txt", "w")
f.write(id)
f.close()

try:
    s3.meta.client.upload_file(id+".txt", "test123krish", bucket_name+"/"+id+".txt")
except Exception as e:
    logging.error(e)
