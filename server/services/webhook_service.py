from flask import current_app

from server.models.dtos.webhook_dto import WebhookDTO
from server.models.postgis.utils import NotFound
from server.models.postgis.webhooks import Webhook
from server.models.statuses import Event
from server.services.project_service import ProjectService

from barker import Webhook as WebhookObj


class WebhookServiceException(Exception):
    """ Custom Exception to notify callers an error occurred when in the Webhook Service """

    def __init__(self, message):
        if current_app:
            current_app.logger.error(message)


class WebhookService:
    @staticmethod
    def create_project_webhook(self, project_id, config):
        """ Create a webhook for a project """
        project = ProjectService.get_project_by_id(project_id)
        if project is None:
            raise NotFound
        # validate config

        # make webhook
        webhook = Webhook().from_dto(config)
        

        return webhook

    @staticmethod
    def get_project_webhooks(self, project_id):
        """ Return all webhooks for a project """
        project = ProjectService.get_project_by_id(project_id)
        if project is None:
            raise NotFound

        webhooks = get_webhooks(project_id)

        return webhooks

    @staticmethod
    def delete_project_webhook(self, webhook_id):
        """ Delete a webhook """
        webhook = get_webhook_by_id(webhook_id)
        if webhook is None:
            raise NotFound

        webhook.delete()

    def construct_webhook_data(self, webhook):
        return {"projectId": webhook['project_id'],
                "event": webhook['event']}

    @staticmethod
    def send_webhook(self, webhook):
        data = construct_webhook_data()
        WebhookSender = WebhookObj(url=webhook['url'],
                                   data=data,
                                   key=webhook[hashkey'])
        WebhookSender.send()
        return WebhookSender.response.response_code
