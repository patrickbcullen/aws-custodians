from custodians.util import age_in_days, flatten_dict
import logging
import dateutil.parser

class ImageCustodian(object):
    def __init__(self, aws):
        self.aws = aws
        self.logger = logging.getLogger(self.__class__.__name__)

    def cleanup(self, dryrun, region, max_days, name_filter=None):
        try:
            self.logger.info("Max retention of unsued images %dd" % max_days)
            in_use_images = self.in_use_images(region)

            for image in self.aws.describe_images(region):
                tag_info = flatten_dict(self.aws.tags_to_dict(image.get('Tags', {})))
                create_time = dateutil.parser.parse(image['CreationDate'])
                days_old = age_in_days(create_time)
                image_id = image['ImageId']
                name = image['Name']

                if name_filter and name and name_filter not in name:
                    self.logger.info("Skipping image because name filter %s is not a substring of %s %s %s" % (name_filter, name, image_id, tag_info))
                    continue

                if days_old >= max_days:
                    self.cleanup_unused_image(dryrun, region, in_use_images, image_id, days_old, name, tag_info)
                else:
                    self.logger.info("Keeping unused image because age of %sd < %sd %s %s %s" % (days_old, max_days, image_id, name, tag_info))
        except Exception as ex:
            self.logger.error("%s: %s" % (self.__class__.__name__, ex))


    def cleanup_unused_image(self, dryrun, region, in_use_images, image_id, days_old, name, tag_info):
        instance_id = in_use_images.get(image_id)
        if instance_id:
            self.logger.info("Skipping image in use by %s (%dd) %s %s %s" % (instance_id, days_old, image_id, name, tag_info))
            return

        if not dryrun:
            self.logger.info("Deleting (%dd) %s %s %s" % (days_old, image_id, name, tag_info))
            self.aws.deregister_image(region, image_id)
        else:
            self.logger.info("Would have deleted (%dd) %s %s %s" % (days_old, image_id, name, tag_info))

    def in_use_images(self, region):
        in_use_images = {}

        for instance in self.aws.describe_instances(region):
            in_use_images[instance['ImageId']] = instance['InstanceId']

        return in_use_images
