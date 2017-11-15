#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# This script takes an AMI ID as an argument. This AMI needs to be in the     #
# default configured region. On execution, this script will find matching     #
# AMIs in other regions (same name and same owner) and create a Mapping       #
# section for a CFN template. This is meeant to be used with Quickstart AMIs  #
# and will allow you to quickly create a simple EC2 AMI mapping for every     #
# region in a CloudFormation template.                                        #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import boto3
import json
import sys

# Make sure AMI ID argument is provided
try:
    print("Creating mappings for images similar to " + sys.argv[1])
except(IndexError):
    print("Error: You must provide an AMI ID from the quickstart menu")
    exit(1)

# Here is the mapping as an empty dictionary. This is what we need to return
mapping = {}

# Here we populate regions list so we can iterate through regions
regions = []
session = boto3.client('ec2')
response = session.describe_regions()
for i in response['Regions']:
    regions.append(i['RegionName'])

# Here we will take an AMI-ID as an argument. We will use this to find the
# name of the AMI, which we can use for each region.
ec2 = boto3.client('ec2')
response = ec2.describe_images(
    Filters=[
        {
            'Name': 'image-id',
            'Values': [str(sys.argv[1])],
        }
    ],
),
name = response[0]['Images'][0]['Name']
owner = response[0]['Images'][0]['OwnerId']
print("Searching for AMIs in all regions with the name " + name)

# Here we describe images in every region based on the name we obtained in the
# first describe_images call above.
for i in regions:
    ec2 = boto3.client('ec2', region_name=i)
    try:
        response = ec2.describe_images(
            Filters=[
                {
                    'Name': 'name',
                    'Values': [str(name)],
                },
                {
                    'Name': 'owner-id',
                    'Values': [str(owner)],
                }
            ],
        ),
        ami = response[0]['Images'][0]['ImageId']
        print(ami)
        mapping[i] = {"AMI": ami}

    except(IndexError):
        pass


print("Search Complete - Mappings template snippet generated below:")
print(json.dumps({"Mappings": {"MyCustomMappedAMIs": mapping}}, indent=2))
