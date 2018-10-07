class Item:
    '''Item - узел двусвязного списка (класс)'''

    def __init__(self, next__item=None, prev__item=None, elem=None):
        self.next__item = next__item
        self.prev__item = prev__item
        self.elem = elem


class DoubleLinkedList:
    '''DoubleLinkedList - двусвязный список (класс)'''

    def __init__(self, head=None, tail=None, length=0):
        self.head = head
        self.tail = tail
        self.length = length

    def push(self, elem):
        '''добавляет элемент в конец списка'''
        if self.tail is None:  # length == 0
            item = Item(None, None, elem)
            self.head = item
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
            if self.tail is not None:
                self.tail.next__item = None
            self.length -= 1

    def unshift(self, elem):
        '''добавляет элемент в начало списка'''
        if self.head is None:
            item = Item(None, None, elem)
            self.head = item
            self.tail = self.head
            self.length = 1
        else:
            item = Item(self.head, None, elem)
            self.head.prev__item = item
            self.head = self.head.prev__item
            self.length += 1

    def shift(self):
        '''убирает элемент из начала списка'''
        if self.head is None:  # length == 0
            print("ERROR (SHIFT): there is nothing to shift!")  # empty list
        else:
            self.head = self.head.next__item
            if self.head is not None:
                self.head.prev__item = None
            self.length -= 1

    def len(self):
        '''возвращает длину списка'''
        return self.length

    def delete(self, elem):
        '''удаляет элемент из списка (первое вхождение с начала)'''
        if self.head is None:  # length == 0
            pass  # return
        elif self.head.elem == elem:
            self.shift()
        else:
            cur = self.head.next__item
            while cur is not None:
                if (cur.elem == elem) and (cur.next__item is not None):
                    temporary_item = cur.prev__item.next__item
                    cur.prev__item.next__item = cur.next__item.prev__item
                    cur.next__item.prev__item = temporary_item
                    self.length -= 1
                    break  # return
                elif (cur.elem == elem) and (cur.next__item is None):
                    cur.prev__item.next__item = None
                    self.tail = cur.prev__item
                    self.length -= 1
                    break  # return
                else:
                    cur = cur.next__item

    def contains(self, elem):
        '''проверяет, входит ли элемент в список'''
        if self.head is None:  # length == 0
            return False
        elif self.head.elem == elem:
            return True
        else:
            cur = self.head.next__item
            while cur is not None:
                if cur.elem == elem:
                    return True
                else:
                    cur = cur.next__item
            return False

    def first(self):
        '''возвращает первый Item в списке'''
        return self.head

    def last(self):
        '''возвращает последний Item в списке'''
        return self.tail

# some extra functions
    def first_elem(self):
        '''возвращает первый Item.elem в списке'''
        return self.head.elem

    def last_elem(self):
        '''возвращает последний Item.elem в списке'''
        return self.tail.elem
