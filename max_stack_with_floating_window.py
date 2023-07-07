from collections import deque

n = int(input())
stack_l = deque([])
stack_r = deque([])
items = deque(list(map(int, input().split())))
length = int(input()) - 1
while items:
    item = items.popleft()
    if length > 0:
        stack_l.append(item)
        length -= 1
    else:
        stack_r.append(item)
        curr_max = item
        while stack_l:
            new_item = stack_l.pop()
            if new_item > curr_max:
                curr_max = new_item
            stack_r.append(new_item)
        stack_r.pop()
        print(curr_max, end = ' ')
        while stack_r:
            stack_l.append(stack_r.pop())
