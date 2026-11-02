
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase


def test_database_tables_can_be_created(tmp_path):
    from app.database import models

    class TestBase(DeclarativeBase):
        pass

    # Use a temporary database so this test does not modify
    # the application's actual database.
    for table in models.Base.metadata.sorted_tables:
        table.to_metadata(TestBase.metadata)

    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}"
    )
    TestBase.metadata.create_all(test_engine)

    table_names = set(inspect(test_engine).get_table_names())

    assert {"incidents", "resources", "system_events"} <= table_names

    test_engine.dispose()
