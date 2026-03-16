import uuid
from typing import Sequence

import allure
from allure_commons.types import AttachmentType
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select

from models.config import Envs
from models.user import UserSql


class AuthDb:
    engine: Engine

    def __init__(self, envs: Envs):
        self.engine = create_engine(envs.auth_db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    def get_user(self, username: str) -> Sequence[UserSql]:
        with Session(self.engine) as session:
            statement = select(UserSql).where(UserSql.username == username)
            return session.exec(statement).all()
