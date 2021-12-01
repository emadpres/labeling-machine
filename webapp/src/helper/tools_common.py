from datetime import datetime

from flask import session
from sqlalchemy import func, distinct

from src import db
from src.database.models import User, LockedArtifact, FlaggedArtifact


def sign_in(username):
    session['username'] = username


def sign_out():
    session.pop('username', None)


def is_signed_in():
    if 'username' not in session:
        return False
    else:
        session_username = session['username']
        db_user = User.query.filter_by(username=session_username).first()
        if db_user is None:
            sign_out()
            return False
        else:
            return True


def who_is_signed_in():
    if 'username' in session:
        return session['username']
    else:
        return None


def get_all_users():
    sql = """SELECT username FROM User"""
    result = db.engine.execute(sql)
    users = [user[0] for user in result]
    return users


def unlock_artifacts_by(username):
    if not username:
        return
    myLock = LockedArtifact.query.filter_by(username=username).first()
    if myLock is not None:
        db.session.delete(myLock)
        db.session.commit()


def lock_artifact_by(username, artifact_id):
    if not username:
        return
    unlock_artifacts_by(username)
    db.session.add(LockedArtifact(username=username, artifact_id=artifact_id))
    db.session.commit()


def get_locked_artifacts():
    update_api_locks()
    result = db.session.query(LockedArtifact.artifact_id, func.count(LockedArtifact.username)).group_by(LockedArtifact.artifact_id).all()
    all_locks = {row[0]: row[1] for row in result}
    return all_locks


def update_api_locks():
    all_locks = LockedArtifact.query.all()
    now_datetime = datetime.utcnow()
    for aLock in all_locks:
        if (now_datetime - aLock.locked_at).total_seconds() / 60 >= 15:  # 15min
            # print("Unlocking Artifact: {} ->  {}:{}".format(aLock.username, aLock.sourceId, aLock.artifact_post_id))
            db.session.delete(aLock)
    db.session.commit()


def get_false_positive_artifacts():
    """
    Return artifacts marked as false positive by me, or marked as false positive by at least 2 people
    """
    q_artifacts_marked_fp_by_me = db.session.query(distinct(FlaggedArtifact.artifact_id)).filter(
        FlaggedArtifact.added_by == who_is_signed_in())
    q_artifacts_marked_fp_by_2 = db.session.query(distinct(FlaggedArtifact.artifact_id)).group_by(FlaggedArtifact.artifact_id).having(
        func.count() > 1)
    result = {row[0] for row in q_artifacts_marked_fp_by_me.union(q_artifacts_marked_fp_by_2).all()}
    return result
