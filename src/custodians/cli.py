import click
from custodians.image import ImageCustodian
from custodians.aws import AWS
import os
import logging

# Get AWS region from the environment if available
AWS_REGION = os.getenv('AWS_REGION')

# Setup logging defaults
logging.basicConfig(format="[%(levelname)s] %(message)s")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("datadog").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

@click.group()
def cli():
    pass


@cli.command()
@click.option('--region', default=AWS_REGION, help='AWS region.')
@click.option('--dryrun/--no-dryrun', default=False, help='Dry run what action would be taken instead of actually taking them.')
@click.option('--max-days', default=30, help='Keep unused images for this many days.')
def image(dryrun, region, max_days):
    aws = AWS()
    custodian = ImageCustodian(aws)
    custodian.cleanup(dryrun, region, max_days)


if __name__ == '__main__':
    cli()
