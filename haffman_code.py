import sys


class Letter:
    def __init__(self, letter=None, count=None, code=None, left=None, right=None):
        self.letter = letter
        self.count = count
        self.code = code
        self.left = left
        self.right = right


word = str(input())
new_set = set(word)
len_old = len(new_set)
if len(word) == 1:
    print(f'1 1')
    print(f'{word}: 0')
    print(f'0')
    sys.exit()
elif len(new_set) == 1:
    print(f'{len(new_set)} {len(word)}')
    print(f'{word[0]}: 0')
    print('0'*len(word))
    sys.exit()
letters = []
for letter in new_set:
    count = 0
    for item in word:
        if letter == item:
            count += 1
    letters.append(Letter(letter, count))

while True:
    if len(letters) == 1:
        break
    if len(letters) == 2:
        item_1 = letters[0]
        item_2 = letters[1]
        new_item = Letter(None, item_1.count + item_2.count, None, left=item_1, right=item_2)
        break
    letters.sort(key=lambda x: x.count)
    item_1 = letters[0]
    item_2 = letters[1]
    new_item = Letter(None, item_1.count + item_2.count, None, left=item_1, right=item_2)
    letters.remove(item_1)
    letters.remove(item_2)
    letters.append(new_item)
item = new_item
item_temp = item
stack = []
while True:
    if item.right:
        stack.append(item.right)
        if item.code:
            item.right.code = item.code + '0'
        elif item.code:
            item.right.code += '0'
        else:
            item.right.code = '0'
    if item.left:
        if item.code:
            item.left.code = item.code + '1'
        elif item.code:
            item.left.code += '1'
        else:
            item.left.code = '1'
        item = item.left
    elif stack:
        item = stack[len(stack) - 1]
        stack.remove(item)
    else:
        break
item = item_temp
encoded_letters = []
while True:
    if item.letter:
        encoded_letters.append(item)
    if item.right:
        stack.append(item.right)
    if item.left:
        item = item.left
    elif stack:
        item = stack[len(stack) - 1]
        stack.remove(item)
    else:
        break
encoded_letters.sort(key = lambda x:x.letter)
for unit in encoded_letters:
    word = word.replace(unit.letter, unit.code)
len_new = len(word)
print(len_old, len_new)
for unit in encoded_letters:
    print(f'{unit.letter}: {unit.code}')
print(word)
