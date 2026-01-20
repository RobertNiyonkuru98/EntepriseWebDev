-- Passenger, Rider and payment
-- passenger passenger_id, passenger_name, payment_method
-- Rider rider_id, rider_name, bike_plate, availability_status
-- payment payment_id, amount, payment_status, passenger_id, rider_id, payment_method

CREATE TABLE Passengers(
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_name VARCHAR(25) NOT NULL,
);

CREATE TABLE Rider(
    rider_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    rider_name VARCHAR(25) NOT NULL,
    bike_plate VARCHAR(25) NOT NULL,
    availability_status ENUM("available", "not_available") NOT NULL
);

CREATE TABLE Payments(
    payment_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    passenger_id INT NOT NULL,
    rider_id INT NOT NULL,
    payment_method VARCHAR(25) NOT NULL,
    amount INT NOT NULL,
    payment_status ENUM("Paid", "Not_Paid"),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES Rider(rider_id) ON DELETE CASCADE
);