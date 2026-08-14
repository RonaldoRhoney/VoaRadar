import uuid

from sqlalchemy.orm import Session

from app.models import Profile


class ProfileRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_or_create(self, user_id: uuid.UUID) -> Profile:
        profile = self._session.get(Profile, user_id)
        if profile is not None:
            return profile
        profile = Profile(id=user_id)
        self._session.add(profile)
        self._session.flush()
        return profile
