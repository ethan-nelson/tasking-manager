from schematics import Model
from schematics.exceptions import ValidationError
from schematics.types import IntType, LongType, StringType

from server.models.postgis.statuses import WebhookEvent


def is_known_event(value):
    """ Validates that supplied webhook event is known value """
    try:
        Event[value.upper()]
    except KeyError:
        raise ValidationError(f'Unknown Event type: {value}')


class WebhookDTO(Model):
    """ Describes JSON model used for a Webhook """
    id = IntType(serialized_name='webhookId')
    project_id = IntType(serialized_name='projectId') 
    user_id = LongType(serialized_name='creatorId')
    event = StringType(serialized_name='event')
    url = StringType(serialized_name='urlEndpoint')
    hashkey = StringType(serialized_name='hashKey')
