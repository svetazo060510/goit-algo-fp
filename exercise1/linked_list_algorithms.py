class Node:
    """
    Вузол однозв'язного списку.
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    """
    Реалізація однозв'язного списку з алгоритмами реверсування та сортування.
    Дотримуються стандарти явних перевірок на None та принципу DRY.
    """
    def __init__(self):
        self.head = None

    def insert_at_end(self, data):
        """
        Додає новий вузол у кінець списку.
        Дотримуються стандарти явних перевірок на None та принципу DRY.
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = new_node

    def print_list(self):
        """Виводить список у зручному для читання форматі."""
        cur = self.head
        nodes = []
        while cur is not None:
            nodes.append(str(cur.data))
            cur = cur.next
        print(" -> ".join(nodes) if nodes else "Список порожній")

    # --- 1. РЕВЕРСУВАННЯ (REVERSAL) ---
    def reverse(self):
        """
        Розвертає список, змінюючи посилання між вузлами.
        Складність: Часова O(n), Просторова O(1).
        """
        prev = None
        cur = self.head
        while cur is not None:
            next_node = cur.next  # Зберігаємо посилання на наступний вузол
            cur.next = prev       # Змінюємо напрямок вказівника
            prev = cur            # Пересуваємо prev на поточний вузол
            cur = next_node       # Переходимо до наступного вузла
        self.head = prev

    # --- 2. СОРТУВАННЯ ВСТАВКАМИ (INSERTION SORT) ---
    def insertion_sort(self):
        """
        Сортує список вставками, переставляючи вузли (in-place).
        Складність: Часова O(n^2), Просторова O(1).
        """
        if self.head is None or self.head.next is None:
            return

        sorted_head = None
        cur = self.head

        while cur is not None:
            next_node = cur.next  # Зберігаємо наступний вузол
            sorted_head = self._sorted_insert(sorted_head, cur)
            cur = next_node
        
        self.head = sorted_head

    def _sorted_insert(self, head_ref, new_node):
        """
        Допоміжна функція для вставки вузла у відсортований список.
        """
        # Випадок 1: Вставка в початок або у порожній список
        if head_ref is None or head_ref.data >= new_node.data:
            new_node.next = head_ref
            return new_node
        
        # Випадок 2: Пошук місця всередині або в кінці
        cur = head_ref
        while cur.next is not None and cur.next.data < new_node.data:
            cur = cur.next
        
        new_node.next = cur.next
        cur.next = new_node
        return head_ref

# --- 3. ЗЛИТТЯ ВІДСОРТОВАНИХ СПИСКІВ (MERGE) ---
def merge_sorted_lists(list1, list2):
    """
    Об'єднує два відсортовані списки в один новий відсортований список.
    Складність: Часова O(n + m), Просторова O(1).
    """
    dummy = Node()
    tail = dummy

    curr1 = list1.head
    curr2 = list2.head

    while curr1 is not None and curr2 is not None:
        if curr1.data <= curr2.data:
            tail.next = curr1
            curr1 = curr1.next
        else:
            tail.next = curr2
            curr2 = curr2.next
        tail = tail.next

    # Приєднуємо залишок списку
    tail.next = curr1 if curr1 is not None else curr2

    merged_ll = LinkedList()
    merged_ll.head = dummy.next
    return merged_ll

# --- ТЕСТУВАННЯ ТА ВАЛІДАЦІЯ ---
if __name__ == "__main__":
    print("--- Тестування Завдання 1: Однозв'язний список (Стандарт 2) ---")
    
    ll = LinkedList()
    for val in [15, 7, 22, 1, 9, 7]:
        ll.insert_at_end(val)
    
    print("\n1. Оригінальний список:")
    ll.print_list()

    ll.reverse()
    print("2. Після реверсування:")
    ll.print_list()

    ll.insertion_sort()
    print("3. Після сортування вставками:")
    ll.print_list()

    l1 = LinkedList()
    for v in [2, 5, 10, 20, 56, 89]: l1.insert_at_end(v)
    l2 = LinkedList()
    for v in [1, 5, 25, 34, 67, 90, 99]: l2.insert_at_end(v)

    print("\n4. Злиття списків:")
    print("Список 1:", end=" ")
    l1.print_list()
    print("Список 2:", end=" ")
    l2.print_list()
    
    merged = merge_sorted_lists(l1, l2)
    print("Результат злиття:", end=" ")
    merged.print_list()