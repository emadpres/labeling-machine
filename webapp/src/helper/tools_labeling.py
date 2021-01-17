import random

from sqlalchemy import func, distinct

from src import db
from src.database.models import LabelingData, Artifact, FlaggedArtifact
from src.helper.consts import N_API_NEEDS_LABELING
from src.helper.tools_common import who_is_signed_in, get_locked_artifacts, get_false_positive_artifacts


def get_labeling_status(username):  # OLD: get_user_labeling_status
    if username is None:
        return None

    labeling_status = {'username': username,
                       'total_n_api': get_n_labeled_artifact_per_user().get(username, 0),
                       'total_n_sentence': 0,
                       'total_n_reviewed': 0  # get_n_reviewed_api_per_user().get(username, 0)
                       }
    return labeling_status


def get_overall_labeling_progress():
    labeling_status = {'source_id': 0,
                       'source_name': "Artifact Set 1",
                       'n_artifacts_labeled': get_n_artifacts_labeled_by_n_or_more(2),
                       'n_artifacts_to_be_labeled': N_API_NEEDS_LABELING,
                       'n_artifacts_reviewed': 0
                       }
    return labeling_status


def get_n_labeled_artifact_per_user():
    """
    Return a dictionary of {username: n_labeled_artifact, ...}
    """
    result = db.session.query(LabelingData.username, func.count(distinct(LabelingData.artifact_id))).group_by(LabelingData.username).all()
    ret = {}
    for row in result:
        ret[row[0]] = row[1]
    return ret


def get_n_artifacts_labeled_by_n_or_more(num):
    artifacts_labeled_num_times = db.session.query(LabelingData.artifact_id).group_by(LabelingData.artifact_id).having(
        func.count(distinct(LabelingData.username)) >= num)
    artifacts_flagged_2_times = FlaggedArtifact.query.with_entities(
        FlaggedArtifact.artifact_id).group_by(FlaggedArtifact.artifact_id).having(func.count() > 1)
    result = artifacts_labeled_num_times.except_(artifacts_flagged_2_times).with_entities(func.count(LabelingData.artifact_id)).scalar()
    return result


def choose_next_random_api():
    candidate_artifact_ids = {row[0] for row in db.session.query(Artifact.id).all()}

    # ############### 1. Remove Already Labeled By Me
    labeled_artifact_ids = {row[0] for row in
                            db.session.query(distinct(LabelingData.artifact_id)).filter(LabelingData.username == who_is_signed_in()).all()}
    candidate_artifact_ids -= labeled_artifact_ids

    # ############### 2. Remove APIs Locked by two at the moment
    locked_artifacts = get_locked_artifacts()
    locked_artifacts_by_2 = set(k for k, v in locked_artifacts.items() if v >= 2)
    candidate_artifact_ids -= locked_artifacts_by_2

    # ############### 3. Remove FP (got 2 FP in general OR marked as FP by me)
    fp_artifact_ids = get_false_positive_artifacts()
    candidate_artifact_ids -= fp_artifact_ids

    if len(candidate_artifact_ids) == 0:
        return -1

    # ############### 4. Starting from the javadoc-class with least labeled APIs, select a random API

    n_tagger_per_artifact = {row[0]: row[1] for row in
                             db.session.query(LabelingData.artifact_id, func.count(distinct(LabelingData.username))) \
                                 .group_by(LabelingData.artifact_id).all()}
    candidate_groups = [[], []]  # index 0,1: artifacts labeled by 0/1 tagger
    for artifact_id in candidate_artifact_ids:
        if artifact_id not in n_tagger_per_artifact.keys():
            candidate_groups[0].append(artifact_id)  # never tagged
        elif n_tagger_per_artifact[artifact_id] == 1:
            candidate_groups[1].append(artifact_id)  # tagged by one tagger

    if len(candidate_groups[1]) > 0:
        return random.choice(candidate_groups[1])
    elif len(candidate_groups[0]) > 0:
        return random.choice(candidate_groups[0])
    else:
        return -2
