from flask import Flask, request, jsonify
from flask_cors import CORS
from cassandra.cluster import Cluster
import uuid

from datetime import datetime
import pytz


app = Flask(__name__)

# Bảng phân loại phim
movie_categories = {
    "Avengers": "action",
    "Batman": "action",
    "Spiderman": "action",
    "Chernobyl": "history",
    "Oppenheimer": "history",
    "Conan": "detective",
    "Sherlock Holmes": "detective",
    "Interstellar": "scifi",
    "Inception": "scifi",
    "Titanic": "romance",
    "La La Land": "romance"
}

# Danh sách phim theo thể loại
category_movies = {}
for m, c in movie_categories.items():
    category_movies.setdefault(c, []).append(m)
CORS(app)

# connect Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('netflix')

USER_ID = uuid.UUID("01079585-4ab2-47db-bacd-f0897ad94bb0")

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    action = data['action']
    movie = data['movie']

    session.execute("""
        INSERT INTO user_activity (user_id, activity_time, action, movie_name)
        VALUES (%s, toTimestamp(now()), %s, %s)
    """, (USER_ID, action, movie))

    return jsonify({"status": "ok"})


# API gợi ý phim cùng thể loại
@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    movie = data['movie']
    cat = movie_categories.get(movie)
    if not cat:
        return jsonify([])
    # Gợi ý các phim cùng thể loại, trừ phim hiện tại
    suggestions = [m for m in category_movies[cat] if m != movie]
    return jsonify(suggestions)


@app.route('/history', methods=['GET'])
def history():
    rows = session.execute("""
        SELECT action, movie_name, activity_time
        FROM user_activity
        WHERE user_id = %s
        LIMIT 10
    """, (USER_ID,))

    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    result = []
    for r in rows:
        # Chuyển sang múi giờ Việt Nam nếu có timezone info, nếu không thì assume UTC
        t = r.activity_time
        if t.tzinfo is None:
            t = pytz.utc.localize(t)
        t_vn = t.astimezone(vn_tz)
        result.append({
            "action": r.action,
            "movie": r.movie_name,
            "time": t_vn.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(result)

app.run(port=5000)

