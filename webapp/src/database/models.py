from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from src import db


class User(db.Model):
    """
    Registered Users
    """
    __tablename__ = 'User'
    username = db.Column(db.Text, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    occupation = db.Column(db.Text)
    affiliation = db.Column(db.Text)
    years_xp = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())

    @validates('username', 'gender', 'education', 'occupation')
    def convert_lower(self, key, value):
        return value.title()


class Note(db.Model):
    """
    Additional notes on artifacts. e.g., "Nice example", "Needs extra caution".
    """
    __tablename__ = 'Note'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    artifact_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text, nullable=False)
    added_by = db.Column(db.Text, nullable=False)
    added_at = db.Column(db.DateTime, default=func.now())


class FlaggedArtifact(db.Model):
    __tablename__ = 'FlaggedArtifact'
    artifact_id = db.Column(db.Integer, primary_key=True)
    added_by = db.Column(db.Text, primary_key=True)
    added_at = db.Column(db.DateTime, default=func.now())


class LockedArtifact(db.Model):
    __tablename__ = 'LockedArtifact'
    username = db.Column(db.Text, primary_key=True)
    artifact_id = db.Column(db.Integer)
    locked_at = db.Column(db.DateTime, default=func.now())


class Artifact(db.Model):
    __tablename__ = 'Artifact'
    id = db.Column(db.Integer, primary_key=True)


class LabelingData(db.Model):
    __tablename__ = 'LabelingData'
    labeling_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artifact_id = db.Column(db.Integer)

    labeling = db.Column(db.Text)
    remark = db.Column(db.Text)

    username = db.Column(db.Text)
    duration_sec = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())

# class ReviewedParagraph(db.Model):
#     __tablename__ = 'ReviewedParagraph'
#     reviewId = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     apiId = db.Column(db.Integer)
#     charStart = db.Column(db.Integer)
#     charEnd = db.Column(db.Integer)
#     text = db.Column(db.Text)
#     username = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=func.now())
#
#     def __init__(self, _api_id, _char_start, _char_end, _text, _username):
#         self.apiId = _api_id
#         self.charStart = _char_start
#         self.charEnd = _char_end
#         self.text = _text
#         self.username = _username

# class ApprovedParagraphDocTypes(db.Model):
#     __tablename__ = 'ApprovedParagraphDocTypes'
#     reviewId = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     apiId = db.Column(db.Integer)
#     charStart = db.Column(db.Integer)
#     charEnd = db.Column(db.Integer)
#     text = db.Column(db.Text)
#     parentLabelingIds = db.Column(db.Text)
#     docType = db.Column(db.Text)
#     rate = db.Column(db.Integer)
#     username = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=func.now())
#     remark = db.Column(db.Text)
#
#     def __init__(self, _api_id, _char_start, _char_end, _text, _parent_labling_ids, _docTypes, _username):
#         self.apiId = _api_id
#         self.charStart = _char_start
#         self.charEnd = _char_end
#         self.text = _text
#         self.parentLabelingIds = _parent_labling_ids
#         self.docType = _docTypes
#         self.rate = None
#         self.username = _username
#         self.remark = ""
#
