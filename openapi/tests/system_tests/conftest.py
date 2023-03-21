import pytest
from fastapi import FastAPI

from openapi.modules.system.api.routes import router
from openapi.modules.system.settings import SystemSettings
from openapi.tests.conftest import BaseTest
from openapi.modules.system.api.dependencies import get_system_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from openapi.core.db.db_session import db_session


class BaseSystemTest(BaseTest):
    url_prefix: str = f"http://test{SystemSettings.router_prefix}"


async def override_get_system_session():
    async with db_session() as sess:
        yield sess
        sess.close()

@pytest.fixture
async def test_app(test_app_base_fixt: FastAPI) -> FastAPI:
    test_app_base_fixt.include_router(router)
    # test_app_base_fixt.dependency_overrides[get_system_session] = (
    #     override_get_system_session)
    yield test_app_base_fixt
