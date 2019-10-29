count = 0


class BTreeNode:
    def __init__(self, keys=None, children=None, is_leaf=True, max_num_of_keys=5):
        if children is None:
            children = []
        if keys is None:
            keys = []
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_of_keys < 3:  # max_num_of_keys must always be at least 3
            max_num_of_keys = 3
        if max_num_of_keys % 2 == 0:  # max_num_of_keys must always be odd
            max_num_of_keys += 1
        self.max_num_of_keys = max_num_of_keys

    def is_full(self):
        return len(self.keys) >= self.max_num_of_keys


class BTree:
    def __init__(self, max_num_of_keys=5):
        self.max_num_of_keys = max_num_of_keys
        self.root = BTreeNode(max_num_of_keys=max_num_of_keys)

    def find_child(self, k, node=None):
        if node is None:
            node = self.root
        for i in range(len(node.keys)):
            if k < node.keys[i]:
                return i
        return len(node.keys)

    def insert_internal(self, i, node=None):
        if node is None:
            node = self.root
        if node.is_leaf:
            self.insert_leaf(i, node)
        else:
            k = self.find_child(i, node)
            if node.children[k].is_full():
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def split(self, node=None):
        if node is None:
            node = self.root
        mid = node.max_num_of_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_of_keys=node.max_num_of_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_of_keys=node.max_num_of_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf, max_num_of_keys=node.max_num_of_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf, max_num_of_keys=node.max_num_of_keys)
        return node.keys[mid], left_child, right_child

    def insert_leaf(self, i, node=None):
        if node is None:
            node = self.root
        node.keys.append(i)
        node.keys.sort()

    def insert(self, i, node=None):
        if node is None:
            node = self.root
        if not node.is_full():
            self.insert_internal(i, node)
        else:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def search(self, k, node=None):
        if node is None:
            node = self.root
        if k in node.keys:
            return node
        if node.is_leaf:
            return None
        return self.search(k, node.children[self.find_child(k, node)])


def read_file_btree():
    file = open("test.txt", "r")
    btree = BTree()
    for single_line in file:
        btree.insert(single_line.replace("\n", ""))
    return btree


def print_anagrams_btree(word, english_words, prefix=""):
    if len(word) <= 1:
        if english_words.search(prefix + word, english_words.root):
            print(prefix + word)
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]
            after = word[i + 1:]
            if cur not in before:
                print_anagrams_btree(before + after, english_words, prefix + cur)


def btree_readfile():
    file = open("test.txt", "r")
    tree = BTree()
    for singleLine in file:
        tree.insert(singleLine.replace("\n", ""))
    return tree


def count_anagrams(word, english_words, prefix=""):
    global count
    if len(word) <= 1:
        if english_words.search(prefix + word, english_words.root):
            count = count + 1
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]
            after = word[i + 1:]
            if cur not in before:
                count_anagrams(before + after, english_words, prefix + cur)
    return count


def most_anagrams(english_words):
    file = open("test.txt", "r")
    biggest = 0
    word = ""
    global count
    count = 0
    for singleLine in file:
        a = str(singleLine.replace("\n", ""))
        q = count_anagrams(a, english_words)
        if q > biggest:
            word = a
            biggest = q
        count = 0
    print(word, biggest)
    return 0


def main():
    print("Please enter a word.")
    users_word = input()
    tree = btree_readfile()
    english_words = btree_readfile()
    print("There are", count_anagrams(users_word, english_words), "anagrams for", users_word)
    print("The anagrams for", users_word, "is:")
    print_anagrams_btree(users_word, tree)
    # Most anagrams
    print("Would you like to see the words with the most anagrams?")
    print('Please enter "yes" or "no".')
    users_ans = input()
    if users_ans.lower() == "yes":
        print("One of the words with the most anagram is:")
        most_anagrams(english_words)
    else:
        print("Good bye.")


main()
