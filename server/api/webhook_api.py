from flask_restful import Resource, current_app
from server.services.webhooks_service import WebhookService, NotFound, WebhookServiceError

class ProjectWebhooksAPI(Resource):

    @tm.pm_only(True)
    @token_auth.login_required
    def get(self, project_id):
        """
        Gets all webhooks for a project
        ---
        tags:
            - webhook
        produces:
            - application/json
        parameters:

        responses:
            200:
                description: Webhooks retrieved
            400:
                description: Client error - Invalid request
            401:
                description: Unauthorized - Invalid credentials
            404:
                description: Project or webhooks not found
            500: 
                description: Internal Server Error
        """
        try:
            webhooks = WebhookService.get_project_webhooks(project_id)
            return webhooks.to_primitive(), 200
        except WebhookServiceError as e:
            return {"error": str(e)}, 400
        except NotFound:
            return {"Error": "Project/webhooks not found"}, 404
        except Exception as e:
            error_msg = f'Webhook GET - unhandled error: {str(e)}'
            current_app.logger.critical(error_msg)
            return {"error": error_msg}, 500

    @tm.pm_only(True)
    @token_auth.login_required
    def post(self, project_id):
        """
        Add a new webhook to a project
        ---
        tags:
            - webhook
        produces:
            - application/json
        parameters:

        responses:
            200:
                description: Webhook added
            401:
                description: Unauthorized - Invalid credentials
            404:
                description: Project not found
            500: 
                description: Internal Server Error
        """
        # validate configuration here
        try:
            WebhookService.create_project_webhook(project_id, configuration)
            return {"ok": "ok"}, 200
        except NotFound:
            return {"Error": "Project not found"}, 404
        except Exception as e:
            error_msg = f'Webhook GET - unhandled error: {str(e)}'
            current_app.logger.critical(error_msg)
            return {"error": error_msg}, 500

    @tm.pm_only(True)
    @token_auth.login_required
    def delete(self, webhook_id):
        """
        Remove a webhook from a project
        ---
        tags:
            - webhook
        produces:
            - application/json
        parameters:

        responses:
            200:
                description: Webhook removed
            401:
                description: Unauthorized - Invalid credentials
            404:
                description: Webhook not found
            500:
                description: Internal Server Error
        """
        try:
            WebhookService.delete_project_webhook(webhook_id)
            return {'ok': 'ok'}, 200
        except NotFound:
            return {"Error": "Webhook not found"}, 404
        except Exception as e:
            error_msg = f'Webhook GET - unhandled error: {str(e)}'
            current_app.logger.critical(error_msg)
            return {"error": error_msg}, 500
