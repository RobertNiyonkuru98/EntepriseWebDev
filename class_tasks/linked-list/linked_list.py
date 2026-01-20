class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None


    def add_node(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next

        return False

    def delete_node(self, data):
        current = self.head

        if current and current.data == data:
            self.head = current.next
            return True

        prev = None
        while current:
            if current.data == data:
                prev.next = current.next
                return True

            prev = current
            current = current.next

        return False