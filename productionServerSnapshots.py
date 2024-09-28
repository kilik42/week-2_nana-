import boto3
import schedule
import time

# Create an EC2 client
ec2_client = boto3.client('ec2',  region_name='us-east-2')

# Get all volumes
volumes = ec2_client.describe_volumes()
#this will create a snapshot of all volumes
print(volumes['Volumes'])
# this will create a snapshot of each volume

def create_volume_snapshots():
    #this will create a snapshot of volumes with tag name prod
    volumes = ec2_client.describe_volumes(
        Filters=[
             {
                'Name': 'tag:Name', 
                'Values': ['prod']
             } 

            ] 
    )
    
    for volume in volumes['Volumes']:
        new_snapshot =ec2_client.create_snapshot(
            VolumeId=volume['VolumeId'], Description='This is a snapshot')
        print('Snapshot created for volume:', new_snapshot['VolumeId'])

# Get all snapshots
# snapshots = ec2_client.describe_snapshots()
# print(snapshots['Snapshots'])

# lets create a scheduler to 
schedule.every().day.do(create_volume_snapshots)
while True:
    schedule.run_pending() 
   
