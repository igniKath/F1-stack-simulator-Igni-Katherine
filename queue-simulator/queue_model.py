
class Queue:
    def __init__(self):
        self.items = []
        self.removed = []

    # Add an item to the rear of the queue
    def enqueue(self, value):
        self.items.append(value)

    # Remove an item from the front of the queue
    def dequeue(self):
        if self.is_empty():
            return None

        removed_item = self.items.pop(0)
        self.removed.insert(0, removed_item)
        return removed_item

    # View the front item without removing it
    def peek(self):
        if self.is_empty():
            return None

        return self.items[0]

    # Clear the queue and removed items
    def clear(self):
        self.items.clear()
        self.removed.clear()

    # Check if the queue is empty
    def is_empty(self):
        return len(self.items) == 0

    # Get the number of items
    def size(self):
        return len(self.items)
