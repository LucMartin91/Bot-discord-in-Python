class Node:
    def __init__(self, data):
        self.data = data
        self.next_node = None
        self.prev_node = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev_node = self.tail
            self.tail.next_node = new_node
            self.tail = new_node
        self.size += 1

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get_last_n_messages(self, n):
        messages = []
        current_node = self.tail
        while current_node is not None and n > 0:
            messages.append(current_node.data)
            current_node = current_node.prev_node
            n -= 1
        return messages[::-1]