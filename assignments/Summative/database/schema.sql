-- Schema Export for Taxi Data Project
-- Generated from PostgreSQL

CREATE TABLE taxi_zones (
    "LocationID" integer NOT NULL,
    "Borough" text NULL,
    "Zone" text NULL,
    "service_zone" text NULL
);

CREATE TABLE trips (
    "VendorID" bigint NULL,
    "tpep_pickup_datetime" text NULL,
    "tpep_dropoff_datetime" text NULL,
    "passenger_count" integer NULL,
    "trip_distance" double precision NULL,
    "RatecodeID" integer NULL,
    "store_and_fwd_flag" text NULL,
    "PULocationID" integer NULL,
    "DOLocationID" integer NULL,
    "payment_type" integer NULL,
    "fare_amount" double precision NULL,
    "extra" double precision NULL,
    "mta_tax" double precision NULL,
    "tip_amount" double precision NULL,
    "tolls_amount" double precision NULL,
    "improvement_surcharge" double precision NULL,
    "total_amount" double precision NULL,
    "congestion_surcharge" double precision NULL,
    "pickup_borough" text NULL,
    "pickup_zone" text NULL,
    "dropoff_borough" text NULL,
    "dropoff_zone" text NULL,
    "duration_hours" double precision NULL,
    "avg_speed_kmh" double precision NULL,
    "fare_per_mile" double precision NULL,
    "pickup_hour" integer NULL
);

CREATE TABLE trips_normalized (
    "VendorID" bigint NULL,
    "tpep_pickup_datetime" text NULL,
    "tpep_dropoff_datetime" text NULL,
    "passenger_count" integer NULL,
    "trip_distance" double precision NULL,
    "RatecodeID" integer NULL,
    "store_and_fwd_flag" text NULL,
    "PULocationID" integer NULL,
    "DOLocationID" integer NULL,
    "payment_type" integer NULL,
    "fare_amount" double precision NULL,
    "extra" double precision NULL,
    "mta_tax" double precision NULL,
    "tip_amount" double precision NULL,
    "tolls_amount" double precision NULL,
    "improvement_surcharge" double precision NULL,
    "total_amount" double precision NULL,
    "congestion_surcharge" double precision NULL,
    "duration_hours" double precision NULL,
    "avg_speed_kmh" double precision NULL,
    "fare_per_mile" double precision NULL,
    "pickup_hour" integer NULL
);

-- Indexes & Constraints
ALTER TABLE taxi_zones ADD PRIMARY KEY ("LocationID");
ALTER TABLE trips_normalized ADD FOREIGN KEY ("PULocationID") REFERENCES taxi_zones("LocationID");
ALTER TABLE trips_normalized ADD FOREIGN KEY ("DOLocationID") REFERENCES taxi_zones("LocationID");
CREATE INDEX idx_pickup_borough ON trips (pickup_borough);
CREATE INDEX idx_pickup_hour ON trips (pickup_hour);
CREATE INDEX idx_fare ON trips (fare_amount);
