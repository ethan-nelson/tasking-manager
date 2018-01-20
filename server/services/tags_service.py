from server import db
from server.models.dtos.tags_dto import TagsDTO
from server.models.postgis.project import Project
from server.models.postgis.tags import Tags


class TagsService:

    @staticmethod
    def get_all_organisation_tags():
        """ Get all org tags"""
        return Tags.get_all_organisations()

    @staticmethod
    def get_all_campaign_tags():
        """ Get all org tags"""
        return Tags.get_all_campaigns()

    @staticmethod
    def get_used_organisation_tags():
        """ Get org tags in DB that are assigned to a project """
        result = db.session.query(Tags.organisations) \
                     .filter(Tags.organisations.isnot(None))
        result = result.union(db.session.query(Project.organisation_tag))

        dto = TagsDTO()
        dto.tags = [r for r, in result]
        return dto

    @staticmethod
    def get_used_campaign_tags():
        """ Get campaign tags in DB that are assigned to a project """
        result = db.session.query(Tags.campaigns) \
                     .filter(Tags.campaigns.isnot(None))
        result = result.union(db.session.query(Project.campaign_tag))

        dto = TagsDTO()
        dto.tags = [r for r, in result]
        return dto        
