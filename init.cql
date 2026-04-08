CREATE KEYSPACE IF NOT EXISTS netflix
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE netflix;

CREATE TABLE IF NOT EXISTS user_activity (
    user_id UUID,
    activity_time TIMESTAMP,
    action TEXT,
    movie_name TEXT,
    PRIMARY KEY (user_id, activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC);