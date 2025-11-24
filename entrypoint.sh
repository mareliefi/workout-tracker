#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Workout Tracker Backend...${NC}"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file with default values...${NC}"
    SECRET_KEY=$(openssl rand -hex 32)
    cat > .env << EOF
# Flask
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1

# Database (PostgreSQL)
DB_USER=workout_user
DB_PASSWORD=workout_password
DB_HOST=db
DB_PORT=5432
DB_NAME=workout_tracker

# SQLAlchemy
SQLALCHEMY_DATABASE_URI=postgresql://workout_user:workout_password@db:5432/workout_tracker
SQLALCHEMY_TEST_URI=postgresql://workout_user:workout_password@db:5432/workout_tracker_test
SECRET_KEY=${SECRET_KEY}
SQLALCHEMY_TRACK_MODIFICATIONS=False
EOF
    echo -e "${GREEN}✅ .env file created with SECRET_KEY${NC}"
fi

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
max_retries=30
count=0

while ! pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-workout_user}" > /dev/null 2>&1; do
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo -e "${RED}❌ Database connection timeout after ${max_retries} seconds${NC}"
        echo -e "${RED}   Check if database container is running: docker compose ps${NC}"
        exit 1
    fi
    echo -e "${YELLOW}   Attempt $count/$max_retries...${NC}"
    sleep 1
done
echo -e "${GREEN}✅ Database is ready${NC}"

# ---- Run test DB setup if script exists ----
if [ -f ./scripts/create_test_db.py ]; then
    echo -e "${YELLOW}🧪 Running test DB setup script...${NC}"
    python ./scripts/create_test_db.py || echo -e "${YELLOW}⚠️  Test DB setup failed (continuing anyway)${NC}"
    echo -e "${GREEN}✅ Test database setup complete${NC}"
else
    echo -e "${YELLOW}ℹ️  Test DB script not found, skipping.${NC}"
fi

# Run migrations
echo -e "${YELLOW}🔄 Running database migrations...${NC}"
flask db upgrade || {
    echo -e "${RED}❌ Migration failed! Check database connection.${NC}"
    exit 1
}
echo -e "${GREEN}✅ Migrations complete${NC}"

# Check if exercises exist, if not, populate
echo -e "${YELLOW}🏋️  Checking exercise database...${NC}"
EXERCISE_COUNT=$(python -c "
from app import create_app
from app.models import db, Exercise
app = create_app()
with app.app_context():
    try:
        count = Exercise.query.count()
        print(count)
    except Exception as e:
        print('0')
" 2>/dev/null || echo "0")

if [ "$EXERCISE_COUNT" -eq "0" ]; then
    echo -e "${YELLOW}📊 Populating exercise database...${NC}"
    python scripts/adding_exercises.py || {
        echo -e "${RED}❌ Failed to populate exercises${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Exercises loaded${NC}"
else
    echo -e "${GREEN}✅ Exercise database already populated ($EXERCISE_COUNT exercises)${NC}"
fi

echo -e "${GREEN}🎉 Backend ready! Starting Flask server...${NC}"
echo -e "${GREEN}   Access at: http://localhost:5000${NC}"
echo ""

# Start Flask
exec flask run --host=0.0.0.0
