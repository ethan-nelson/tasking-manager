from flask_restful import Resource, current_app, request
from server.services.tags_service import TagsService
from distutils.util import strtobool


class OrganisationTagsAPI(Resource):

    def get(self):
        """
        Gets all organisation tags
        ---
        tags:
          - tags
        produces:
          - application/json
        parameters:
          - name: include_empty
            in: query
            type: boolean
            required: false
            description: Set to true if you want tags with no projects
        responses:
            200:
                description: Organisation tags
            500:
                description: Internal Server Error
        """
        try:
            include_empty = strtobool(request.args.get('include_empty')) \
                                if request.args.get('include_empty') else False
            if include_empty is True:
                tags = TagsService.get_all_organisation_tags()
            else:
                tags = TagsService.get_used_organisation_tags()
            return tags.to_primitive(), 200
        except Exception as e:
            error_msg = f'User GET - unhandled error: {str(e)}'
            current_app.logger.critical(error_msg)
            return {"error": error_msg}, 500


class CampaignsTagsAPI(Resource):

    def get(self):
        """
        Gets all campaign tags
        ---
        tags:
          - tags
        produces:
          - application/json
        parameters:
          - name: include_empty
            in: query
            type: boolean
            required: false
            description: Set to true if you want tags with no projects
        responses:
            200:
                description: Campaign tags
            500:
                description: Internal Server Error
        """
        try:
            include_empty = strtobool(request.args.get('include_empty')) \
                                if request.args.get('include_empty') else False
            if include_empty is True:
                tags = TagsService.get_all_campaign_tags()
            else:
                tags = TagsService.get_used_campaign_tags()
            return tags.to_primitive(), 200
        except Exception as e:
            error_msg = f'User GET - unhandled error: {str(e)}'
            current_app.logger.critical(error_msg)
            return {"error": error_msg}, 500
