import time
# Linear search

class MotoTaxi:
    def __init__(self):
        self.drivers = []

    def add_driver(self, driver_id, name):
        self.drivers.append({
            "driver_id": driver_id,
            "name": name
        })


    def linear_search_driver(self, driver_id):
        for driver in self.drivers:
            if driver["driver_id"] == driver_id:
                return driver
        return None


# binary_search

class MotoTaxiBin:
    def __init__(self):
        self.drivers = []
        self.driver_index = {}

    def add_driver(self, driver_id, name):
        driver = {
            "driver_id": driver_id,
            "name": name,
        }

        self.drivers.append(driver)
        self.driver_index[driver_id] = driver


    def binary_search(self, driver_id):
        return self.driver_index.get(driver_id)


application = MotoTaxi()
application.add_driver(1, "Ange")
application.add_driver(2, "David")
application.add_driver(3, "Robert")
application.add_driver(4, "Ange-Mu")
application.add_driver(5, "David-Ac")
application.add_driver(6, "Robert-T")
application.add_driver(7, "Ange-M")
application.add_driver(8, "David-A")
application.add_driver(9, "Roberty")
application.add_driver(10, "Angele")
application.add_driver(11, "Davids")
application.add_driver(12, "Roberts")
application.add_driver(13, "Angeline")
application.add_driver(14, "Davidine")
application.add_driver(15, "Robertine")
application.add_driver(16, "Angels")
application.add_driver(17, "Davidho")
application.add_driver(18, "Robertin")
application.add_driver(19, "Angel")
application.add_driver(20, "Davido")
application.add_driver(21, "Robertinho")
application.add_driver(22, "Angelique")
application.add_driver(23, "Davidson")
application.add_driver(24, "Roberto")


# binary_search

app = MotoTaxiBin()
app.add_driver(1, "Ange")
app.add_driver(2, "David")
app.add_driver(3, "Robert")
app.add_driver(4, "Ange-Mu")
app.add_driver(5, "David-Ac")
app.add_driver(6, "Robert-T")
app.add_driver(7, "Ange-M")
app.add_driver(8, "David-A")
app.add_driver(9, "Roberty")
app.add_driver(10, "Angele")
app.add_driver(11, "Davids")
app.add_driver(12, "Roberts")
app.add_driver(13, "Angeline")
app.add_driver(14, "Davidine")
app.add_driver(15, "Robertine")
app.add_driver(16, "Angels")
app.add_driver(17, "Davidho")
app.add_driver(18, "Robertin")
app.add_driver(19, "Angel")
app.add_driver(20, "Davido")
app.add_driver(21, "Robertinho")
app.add_driver(22, "Angelique")
app.add_driver(23, "Davidson")
app.add_driver(24, "Roberto")

start_time = time.time()
result_linear = application.linear_search_driver(24)
end_time = time.time()
print("Linear search result:", result_linear)
print(f"Hash time: {end_time - start_time:.8f}s")

start = time.time()
result_binary = app.binary_search(21)
end = time.time()
print(f"Binary Search Time: {end - start:.8f}s")
