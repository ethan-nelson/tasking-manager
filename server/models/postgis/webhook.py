from server import db
from server.models.dtos.webhook_dto import WebhookDTO


class Webhook(db.Model):
    """ Describes a webhook """

    __tablename__ = "webhooks"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    event = db.Column(db.Integer)
    url = db.Column(db.String)
    hashkey = db.Column(db.String)

    # Relationships
    project = db.relationship(Project, foreign_keys=[project_id])
    user_id = db.relationship(User, foreign_keys=[from_user_id])

    @classmethod
    def from_dto(cls, dto: WebhookDTO):
        """ Creates new webhook from DTO """
        webhook = cls()
        webhook.project_id = dto.project_id
        webhook.user_id = dto.user_id
        webhook.event = dto.event
        webhook.url = dto.url
        webhook.hashkey = dto.hashkey

        return webhook

    def as_dto(self) -> WebhookDTO:
        """ Casts webhook as DTO """
        dto = WebhookDTO()
        dto.id = self.id
        dto.project_id = self.project_id
        dto.user_id = self.user_id
        dto.event = self.event
        dto.url = self.url
        dto.hashkey = self.hashkey

        return dto

    def get_webhook_by_id(self, webhook_id: int):
        """ Return the webhook specified """
        Webhook.query.get(webhook_id)

    def get_webhooks(self, project_id: int):
        """ Return webhooks for a project """
        Webhook.query.filter_by(project_id=project_id).all()

    def delete(self):
        """ Delete the webhook in scope from the DB """
        db.session.delete(self)
        db.session.commit()
