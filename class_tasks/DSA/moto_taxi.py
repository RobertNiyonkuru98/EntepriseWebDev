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