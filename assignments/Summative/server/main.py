# from scipy.stats._discrete_distns import randint_gen
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app) # Allows frontend to talk to backend

def get_db_connection():
    # conn = sqlite3.connect("../ETL/assets/urban_mobility.db")
    # conn.row_factory = sqlite3.Row # Allows us to access columns by name
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route('/api/trips', methods=['GET'])
def get_trips():
    # Capture options to filter from the requiest\
    borough = request.args.get('borough')
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM trips"
    params = []

    if borough:
        query += " WHERE pickup_borough = %s"
        params.append(borough)

    query += " LIMIT %s OFFSET %s"
    params.append(limit)
    params.append(offset)

    cur.execute(query, params)
    trips = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in trips])

@app.route('/api/top_fares', methods=['GET'])
def get_top_fare():
    # means to apply custom logic to a real problem

    borough = request.args.get('borough', 'Manhattan')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # fetfching data WITHOUT sql sorting to demonstrate the manual logic
    cur.execute("SELECT pickup_borough, dropoff_borough, fare_amount FROM trips WHERE pickup_borough = %s LIMIT 50", (borough,))
    raw_trips = cur.fetchall()
    conn.close()

    # Convert to list of dicts
    trip_data = [dict(row) for row in raw_trips]

    # Apply the manual algorithm
    sorted_trips = manual_sort_by_fare(trip_data)

    # Return the top 50
    return jsonify(sorted_trips[:50])
# PLACEHOLDER FOR VUX

def manual_sort_by_fare(trip_list):
    # Manual sort of list of dict by fare_amount in desc order.
    # COMPLEXITY: O(n^2)
    n = len(trip_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if trip_list[j]['fare_amount'] < trip_list[j + 1]['fare_amount']:
                # Swap of the elements
                trip_list[j], trip_list[j + 1] = trip_list[j + 1], trip_list[j]
    return trip_list




if __name__ == "__main__":
    app.run(debug=True, port=5001)