# Cassandra Netflix Demo

## Setup

### 1. Start Cassandra
docker compose up -d

Wait 30-60 seconds

### 2. Enter Cassandra
docker exec -it cassandra cqlsh

### 3. Create keyspace and table
CREATE KEYSPACE netflix
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE netflix;

CREATE TABLE user_activity (
    user_id UUID,
    activity_time TIMESTAMP,
    action TEXT,
    movie_name TEXT,
    PRIMARY KEY (user_id, activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC);

### 4. Install Python packages
pip install flask cassandra-driver flask-cors

### 5. Run backend
python app.py

### 6. Open web
Open index.html with Live Server