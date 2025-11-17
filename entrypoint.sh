#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Workout Tracker Backend...${NC}"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file with default values...${NC}"
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
SECRET_KEY=$(openssl rand -hex 32)
SQLALCHEMY_TRACK_MODIFICATIONS=False
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
fi

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
    sleep 1
done
echo -e "${GREEN}✅ Database is ready${NC}"

# ---- Run test DB setup if script exists ----
if [ -f ./scripts/create_test_db.py ]; then
    echo -e "${YELLOW}🐍 Running test DB setup script...${NC}"
    python ./scripts/create_test_db.py
    echo -e "${GREEN}✅ Test database setup complete${NC}"
else
    echo -e "${YELLOW}⚠️ Test DB script not found, skipping.${NC}"
fi

# Run migrations
echo -e "${YELLOW}🔄 Running database migrations...${NC}"
flask db upgrade
echo -e "${GREEN}✅ Migrations complete${NC}"

# Check if exercises exist, if not, populate
echo -e "${YELLOW}🏋️ Checking exercise database...${NC}"
EXERCISE_COUNT=$(python -c "from app import create_app; from app.models import db, Exercise; app = create_app(); app.app_context().push(); print(Exercise.query.count())")

if [ "$EXERCISE_COUNT" -eq "0" ]; then
    echo -e "${YELLOW}📊 Populating exercise database...${NC}"
    python scripts/adding_exercises.py
    echo -e "${GREEN}✅ Exercises loaded${NC}"
else
    echo -e "${GREEN}✅ Exercise database already populated ($EXERCISE_COUNT exercises)${NC}"
fi

echo -e "${GREEN}🎉 Backend ready! Starting Flask server...${NC}"

# Start Flask
exec flask run --host=0.0.0.0
