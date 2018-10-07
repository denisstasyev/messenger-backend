import double_linked_list
import unittest


class TestDoubleLinkedList(unittest.TestCase):
    '''DoubleLinkedList - class of unittests'''
    names = ['Bob Belcher',
             'Linda Belcher',
             'Tina Belcher',
             'Gene Belcher',
             'Louise Belcher']

    def test_init(self):
        '''Init test'''
        dll = double_linked_list.DoubleLinkedList()
        self.assertIsNone(dll.head)
        self.assertIsNone(dll.tail)
        self.assertEqual(dll.length, 0)

    def test_push_pop(self):
        '''Push/pop tests'''
        dll = double_linked_list.DoubleLinkedList()
        for name in TestDoubleLinkedList.names:
            dll.push(name)

        self.assertEqual(dll.last_elem(), TestDoubleLinkedList.names[4])
        dll.pop()
        self.assertEqual(dll.last_elem(), TestDoubleLinkedList.names[3])
        dll.pop()
        self.assertEqual(dll.last_elem(), TestDoubleLinkedList.names[2])
        dll.pop()
        self.assertEqual(dll.last_elem(), TestDoubleLinkedList.names[1])
        dll.pop()
        self.assertEqual(dll.last_elem(), TestDoubleLinkedList.names[0])
        dll.pop()
        dll.pop()  # ERROR (POP): there is nothing to pop!

    def test_unshift_shift(self):
        '''Unshift/shift tests'''
        dll = double_linked_list.DoubleLinkedList()
        for name in TestDoubleLinkedList.names:
            dll.unshift(name)

        self.assertEqual(dll.first_elem(), TestDoubleLinkedList.names[4])
        dll.shift()
        self.assertEqual(dll.first_elem(), TestDoubleLinkedList.names[3])
        dll.shift()
        self.assertEqual(dll.first_elem(), TestDoubleLinkedList.names[2])
        dll.shift()
        self.assertEqual(dll.first_elem(), TestDoubleLinkedList.names[1])
        dll.shift()
        self.assertEqual(dll.first_elem(), TestDoubleLinkedList.names[0])
        dll.shift()
        dll.shift()  # ERROR (SHIFT): there is nothing to shift!

    def test_len(self):
        '''Len test'''
        dll = double_linked_list.DoubleLinkedList()

        self.assertEqual(dll.len(), 0)

        for name in TestDoubleLinkedList.names:
            dll.push(name)

        self.assertEqual(dll.len(), 5)

        for name in TestDoubleLinkedList.names:
            dll.push(name)

        self.assertEqual(dll.len(), 10)

        for i in range(10):
            dll.pop()

        self.assertEqual(dll.len(), 0)

        dll.pop()  # ERROR (POP): there is nothing to pop!

        self.assertEqual(dll.len(), 0)

    def test_delete(self):
        '''Delete test'''
        dll = double_linked_list.DoubleLinkedList()
        for name in TestDoubleLinkedList.names:
            dll.push(name)

        dll.delete('Louise Belcher')  # end element

        self.assertEqual(dll.last_elem(), 'Gene Belcher')

        dll.delete('Bob Belcher')  # start element

        self.assertEqual(dll.first_elem(), 'Linda Belcher')

    def test_contains(self):
        '''Contains test'''
        dll = double_linked_list.DoubleLinkedList()
        for name in TestDoubleLinkedList.names:
            dll.push(name)

        self.assertEqual(dll.contains('Louise Belcher'), True)  # end element
        self.assertEqual(dll.contains('Gene Belcher'), True)  # middle element
        self.assertEqual(dll.contains('Bob Belcher'), True)  # start element
        self.assertEqual(dll.contains('Bob'), False)  # wrong element

    def test_first_last(self):
        '''First/last test'''
        dll = double_linked_list.DoubleLinkedList()
        dll.push('Bob Belcher')

        self.assertEqual(dll.first().elem, 'Bob Belcher')
        self.assertEqual(dll.first().prev__item, None)
        self.assertEqual(dll.first().next__item, None)

        self.assertEqual(dll.last().elem, 'Bob Belcher')
        self.assertEqual(dll.last().prev__item, None)
        self.assertEqual(dll.last().next__item, None)

        dll.push('Linda Belcher')

        self.assertEqual(dll.first().elem, 'Bob Belcher')
        self.assertEqual(dll.first().prev__item, None)

        self.assertEqual(dll.last().elem, 'Linda Belcher')
        self.assertEqual(dll.last().next__item, None)


if __name__ == '__main__':
    unittest.main()
