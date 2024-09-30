import boto3
import schedule
import time
from operator import itemgetter

ec2_client = boto3.client('ec2',  region_name='us-east-2')
ec2_resource = boto3.resource('ec2', region_name='us-east-2')

instance_id =  'i-08ca2131f8c812c7f'

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

instance_volume = volumes['Volumes'][0]
print(instance_volume['VolumeId'])

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)
latest_snapshots = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

print(snapshots['Snapshots'])
print('Latest snapshot:', latest_snapshots['StartTime'])

#lets attach the snapshot

ec2_resource.create_volume(

    AvailabilityZone="us-east-2c",
    SnapshotId=latest_snapshots['SnapshotId'],
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'dev'
                }
            ]
        }
    ]
)
