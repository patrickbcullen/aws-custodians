from custodians.util import age_in_days, flatten_dict
import logging
import dateutil.parser

class ImageCustodian(object):
    def __init__(self, aws):
        self.aws = aws
        self.logger = logging.getLogger(self.__class__.__name__)

    def cleanup(self, dryrun, region, max_days):
        try:
            self.logger.info("Max retention of unsued images %dd" % max_days)
            in_use_images = self.in_use_images(region)

            for image in self.aws.describe_images(region):
                tags = self.aws.tags_to_dict(image.get('Tags', {}))
                create_time = dateutil.parser.parse(image['CreationDate'])
                days_old = age_in_days(create_time)
                image_id = image['ImageId']
                name = image['Name']

                if days_old >= max_days:
                    instance_id = in_use_images.get(image_id)
                    if instance_id:
                        self.logger.info("Skipping image in use by %s (%dd) %s %s %s" % (instance_id, days_old, image_id, name, flatten_dict(tags)))
                        continue

                    if not dryrun:
                        self.logger.info("Deleting (%dd) %s %s %s" % (days_old, image_id, name, flatten_dict(tags)))
                        self.aws.deregister_image(region, image_id)
                    else:
                        self.logger.info("Would have deleted (%dd) %s %s %s" % (days_old, image_id, name, flatten_dict(tags)))
        except Exception as ex:
            self.logger.error("%s: %s" % (self.__class__.__name__, ex))


    def in_use_images(self, region):
        in_use_images = {}

        for instance in self.aws.describe_instances(region):
            in_use_images[instance['ImageId']] = instance['InstanceId']

        return in_use_images
