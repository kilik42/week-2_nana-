#write a program that cleans up snapshots older than 7 days

import boto3
import schedule
import time
from operator import itemgetter

ec2_client = boto3.client('ec2',  region_name='us-east-2')

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self']
)

# so I want to sort the list by the start time of the snapshot
# and then delete the snapshots that are older than 7 days
sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

# # lambda function is an anonymous function that can take any number of arguments, but can only have one expression
# for snap in snapshots['Snapshots']: 
#     print(snap['StartTime'])
    
# print('-------------------')
# print("Deleting snapshots older than 7 days")
# for snap in sorted_by_date:
#     if snap['StartTime'] < 7:
#         print('Deleting snapshot:', snap['SnapshotId'])
#         ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])

#def clean_up_snapshots():
for snap in sorted_by_date[2:]:
    #delete snapshots that are older than 7 days
    response = ec2_client.delete_snapshot(
        SnapshotId=snap['SnapshotId']
    )
    print('Deleting snapshot:', snap['SnapshotId'])
 