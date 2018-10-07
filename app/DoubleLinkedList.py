class DoubleLinkedList:

    class Item:
        def __init__(self, next__item=None, prev__item=None, elem=None):
            '''конструктор Item'''
            self.next__item = next__item
            self.prev__item = prev__item
            self.elem = elem

    def __init__(self, head=None, tail=None, length=0):
        '''конструктор DoubleLinkedList'''
        self.head = head
        self.tail = tail
        self.length = length

    def push(self, elem):
        '''добавляет элемент в конец списка'''
        if self.tail is None:  # length == 0
            self.head = Item(None, None, elem)
            self.tail = self.head
            self.length = 1
        else:
            item = Item(None, self.tail, elem)
            self.tail.next__item = item
            self.tail = item
            self.length += 1

    def pop(self):
        '''убирает элемент из конца списка'''
        if self.tail is None:  # length == 0
            print("ERROR (POP): there is nothing to pop!")  # empty list
        else:
            self.tail = self.tail.prev__item
            self.tail.next__item = None
            self.length -= 1

    def unshift(self, elem):
        '''добавляет элемент в начало списка'''
        if self.head is None:
            self.head = Item(None, None, elem)
            self.tail = self.head
            self.length = 1
        else:
            self.head.prev__item = Item(self.head, None, elem)
            self.head = self.head.prev__item
            self.length += 1

    def shift(self):
        '''убирает элемент из начала списка'''
        if self.head is None:  # length == 0
            print("ERROR (SHIFT): there is nothing to shift!")  # empty list
        else:
            self.head = self.head.next__item
            self.head.prev__item = None
            self.length -= 1

    def len(self):
        '''возвращает длину списка'''
        return self.length

    def delete(self, elem):
        '''удаляет элемент из списка (первое вхождение с начала)'''
        if self.head is None:  # length == 0
            return
        elif self.head.elem == elem:
            self.shift()
        else:
            cursor_item = self.head.next__item
            while cursor_item is not None:
                if (cursor_item.elem == elem) and (cursor_item.next__item is not None):
                    temporary_item = cursor_item.prev__item.next__item
                    cursor_item.prev__item.next__item = cursor_item.next__item.prev__item
                    cursor_item.next__item.prev__item = temporary_item
                    self.length -= 1
                    return
                elif (cursor_item.elem == elem) and (cursor_item.next__item is None):
                    cursor_item.prev__item.next__item = None
                    self.tail = cursor_item.prev__item
                    self.length -= 1
                    return
                else:
                    cursor_item = cursor_item.next__item

    def contains(self, elem):
        '''проверяет, входит ли элемент в список'''
        if self.head is None:  # length == 0
            return False
        elif self.head.elem == elem:
            return True
        else:
            cursor_item = self.head.next__item
            while cursor_item is not None:
                if cursor_item.elem == elem:
                    return True
                else:
                    cursor_item = cursor_item.next__item
            return False

    def first(self):
        '''возвращает первый Item в списке'''
        return self.head

    def last(self):
        '''возвращает последний Item в списке'''
        return self.tail
