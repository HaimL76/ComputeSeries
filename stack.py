# Source - https://stackoverflow.com/a
# Posted by Matthieu M.
# Retrieved 2025-11-30, License - CC BY-SA 2.5

class Stack:
    def __init__(self):
        self.__storage = []

    def is_empty(self):
        return len(self.__storage) == 0

    def push(self, p):
        self.__storage.append(p)

    def pop(self):
        return self.__storage.pop()

    def __iter__(self):
        for element in self.__storage:
            yield element
