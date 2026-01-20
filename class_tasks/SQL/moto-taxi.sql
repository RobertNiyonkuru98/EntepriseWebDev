-- Active: 1768379690394@@127.0.0.1@3306@class-mysql
CREATE TABLE Riders (
    rider_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    bike_plate VARCHAR(20),
    rating DECIMAL(2,1)

);

CREATE TABLE Trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT,
    start_location VARCHAR(100) NOT NULL,
    end_location VARCHAR(100) NOT NULL,
    fare INT NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (rider_id) REFERENCES Riders(rider_id)
);


INSERT INTO Riders (name, phone, bike_plate, rating)
VALUES ("Jean Claude", "0788999222", "RAE 234 K", 4.6);

INSERT INTO Trips (rider_id, start_location, end_location, fare, status)
VALUES (1, "Kimironko", "Remera", 2500, "completed");

INSERT INTO Trips (rider_id, start_location, end_location, fare, status)
VALUES (1, "Nyabugogo", "Kacyiru", 3000, "completed");

SELECT start_location, fare
FROM Trips;

SELECT start_location, fare
FROM Trips
WHERE trip_id = 1;


UPDATE riders
SET phone = "0788000111"
WHERE rider_id = 1;

DELETE FROM trips
WHERE trip_id = 2;