class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    while l1 or l2 or carry:
        total_sum = carry
        if l1:
            total_sum += l1.val
            l1 = l1.next
        if l2:
            total_sum += l2.val
            l2 = l2.next
        carry = total_sum // 10
        current.next = ListNode(total_sum % 10)
        current = current.next
    return dummy.next


# Create linked lists
# l1 = ListNode(2, ListNode(4, ListNode(3)))
# l2 = ListNode(5, ListNode(6, ListNode(4)))

# Compute the sum
# result = addTwoNumbers(l1, l2)

# Display the result
# while result:
#     print(result.val, end=' -> ' if result.next else '')
#     result = result.next
