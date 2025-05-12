import os
import sys
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command


# Add root directory to path so app can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

# Load environment variables
load_dotenv()

# Use test DB for migrations
os.environ["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")

# Create the app
app = create_app()

# Run migrations against test DB
with app.app_context():
    print("Using DB:", os.getenv("SQLALCHEMY_DATABASE_URI"))

    # Manually configure Alembic
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")  # ✅ Add this
    alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("SQLALCHEMY_DATABASE_URI"))

    command.upgrade(alembic_cfg, "head")
    print("✅ Migrations applied to test DB.")
















