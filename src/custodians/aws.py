import socket
import boto3
import botocore
from os import environ
import logging
import hashlib

class AWS(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.kwargs = {}


    def tags_to_dict(self, aws_tags):
        return {x['Key']: x['Value'] for x in aws_tags}


    def _get_client(self, service, region):
        return boto3.client(service, region_name=region)


    def describe_images(self, region):
        ec2 = self._get_client('ec2', region)
        sts = self._get_client('sts', region)
        account = sts.get_caller_identity().get('Account')
        self.logger.debug('Using account_id %s' % account)
        filters = [
            {'Name': 'state', 'Values': ['available', 'failed']},
            {'Name': 'owner-id', 'Values': [account]},
            {'Name': 'is-public', 'Values': ['false']},
        ]

        return ec2.describe_images(Filters=filters).get('Images', [])


    def describe_instances(self, region):
        ec2 = self._get_client('ec2', region)

        instances = []
        kwargs = {}
        while True:
            resp = ec2.describe_instances(MaxResults=100, **kwargs)

            for reservation in resp.get('Reservations', []):
                instances.extend(reservation.get('Instances', []))

            if resp.get('NextToken'):
                kwargs['NextToken'] = resp.get('NextToken')
            else:
                break

        return instances


    def deregister_image(self, region, image_id):
        ec2 = self._get_client('ec2', region)
        try:
            ec2.deregister_image(ImageId=image_id)
        except botocore.exceptions.ClientError as exception:
            if exception.response["Error"]["Code"] not in ['InvalidAMIID.Unavailable']:
                raise exception
