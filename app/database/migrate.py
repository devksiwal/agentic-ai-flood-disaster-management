
from sqlalchemy import inspect, text

from app.database.connection import engine


def migrate_database() -> None:
    inspector = inspect(engine)

    if "resources" not in inspector.get_table_names():
        from app.database import initialize_database
        initialize_database()
        inspector = inspect(engine)

    columns = {
        column["name"]
        for column in inspector.get_columns("resources")
    }

    with engine.begin() as connection:
        if "capabilities" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE resources "
                    "ADD COLUMN capabilities TEXT "
                    "NOT NULL DEFAULT 'general_rescue'"
                )
            )


if __name__ == "__main__":
    migrate_database()
    print("Database migration completed.")
