import pandas as pd


class Node:
    def __init__(self, value=None, positions=None):
        self.value = value
        self.children = []
        self.positions = positions if positions else set()


def build_syntax_tree(regex):
    postfix = infix_to_postfix(regex)
    stack = []
    position_counter = 1

    for char in postfix:
        if char.isalnum() or char in {"&", "_", "#", "@"}:
            stack.append(Node(value=char, positions={position_counter}))
            position_counter += 1
        elif char == ".":
            right = stack.pop()
            left = stack.pop()
            stack.append(
                Node(value=".", positions=left.positions.union(right.positions))
            )
            stack[-1].children = [left, right]
        elif char == "|":
            right = stack.pop()
            left = stack.pop()
            stack.append(
                Node(value="|", positions=left.positions.union(right.positions))
            )
            stack[-1].children = [left, right]
        elif char == "*":
            child = stack.pop()
            stack.append(Node(value="*", positions=child.positions))
            stack[-1].children = [child]

    return stack[0]


def infix_to_postfix(infix):
    postfix = []
    stack = []

    precedence = {"*": 3, ".": 2, "|": 1}

    for char in infix:
        if char.isalnum() or char in {"&", "_", "#", "@"}:
            postfix.append(char)
        elif char == "(":
            stack.append(char)
        elif char == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                postfix.append(stack.pop())
            stack.append(char)

    while stack:
        postfix.append(stack.pop())

    return "".join(postfix)


def nullable(node):
    if node.value.isalnum() or node.value in {"&", "_", "#", "@"}:
        return False
    elif node.value == "|":
        return nullable(node.children[0]) or nullable(node.children[1])
    elif node.value == ".":
        return nullable(node.children[0]) and nullable(node.children[1])
    elif node.value == "*":
        return True


def firstpos(node):
    if node.value.isalnum() or node.value in {"&", "_", "#", "@"}:
        return node.positions if not nullable(node) else set()
    elif node.value == "|":
        return firstpos(node.children[0]).union(firstpos(node.children[1]))
    elif node.value == ".":
        return (
            firstpos(node.children[0])
            if not nullable(node.children[0])
            else firstpos(node.children[0]).union(firstpos(node.children[1]))
        )
    elif node.value == "*":
        return firstpos(node.children[0])


def lastpos(node):
    if node.value.isalnum() or node.value in {"&", "_", "#", "@"}:
        return node.positions if not nullable(node) else set()
    elif node.value == "|":
        return lastpos(node.children[0]).union(lastpos(node.children[1]))
    elif node.value == ".":
        return (
            lastpos(node.children[1])
            if not nullable(node.children[1])
            else lastpos(node.children[0]).union(lastpos(node.children[1]))
        )
    elif node.value == "*":
        return lastpos(node.children[0])


def followpos(node, followpos_table):
    if node.value == ".":
        for pos in lastpos(node.children[0]):
            followpos_table[pos] = followpos_table.get(pos, set()).union(
                firstpos(node.children[1])
            )
    elif node.value == "*":
        for pos in lastpos(node.children[0]):
            followpos_table[pos] = followpos_table.get(pos, set()).union(firstpos(node))


def compute_followpos_table(syntax_tree):
    followpos_table = {}
    compute_followpos_table_recursive(syntax_tree, followpos_table)
    return followpos_table


def compute_followpos_table_recursive(node, followpos_table):
    if node:
        if node.value == ".":
            compute_followpos_table_recursive(node.children[0], followpos_table)
            compute_followpos_table_recursive(node.children[1], followpos_table)
        elif node.value == "*":
            compute_followpos_table_recursive(node.children[0], followpos_table)
        followpos(node, followpos_table)


def make_dtrans_table(regex):
    regex = regex + ".#"
    syntax_tree = build_syntax_tree(regex)
    followpos_table = compute_followpos_table(syntax_tree)
    dtrans_table = {}
    regex_pos = ""
    for i in regex:
        if i.isalnum() or i in {"&", "_", "#", "@"}:
            regex_pos += i

    dtrans_table = {tuple(firstpos(syntax_tree)): {i: () for i in regex_pos[:-1]}}
    iter_c = 0
    # making the dtrans table from firstpos and followpos
    while True:
        try:
            flag = len(list(dtrans_table.items()))
            first_pos = set(list(dtrans_table.items())[iter_c][0])
            if first_pos == set():
                iter_c += 1
                first_pos = set(list(dtrans_table.items())[iter_c][0])
            top = {i: () for i in regex_pos[:-1]}
            for i, j in list(top.items()):

                andis = []
                for z, z2 in enumerate(list(regex_pos[:-1])):
                    if z2 == i:
                        andis.append(z + 1)
                tmp = first_pos.intersection(set(andis))
                temp = []
                for pos in tmp:
                    temp = temp + list(followpos_table.get(pos, ()))

                top[i] = tuple(temp)
                dtrans_table[tuple(first_pos)][i] = tuple(temp)
                flage = dtrans_table.get(tuple(temp), False)
                if not flage:
                    dtrans_table[tuple(temp)] = {i: () for i in regex_pos[:-1]}
            iter_c += 1
        except IndexError:
            break
    temp = {}
    dtrans_table2 = {}
    num_c = 1
    # making the dtrans talbe read able
    for key, value in dtrans_table.items():
        if key == ():
            temp[key] = f"T{num_c}"
            dtrans_table2[f"T{num_c}"] = value
        elif len(regex_pos) in key:
            temp[key] = f"F{num_c}"
            dtrans_table2[f"F{num_c}"] = value
        else:
            temp[key] = f"{num_c}"
            dtrans_table2[f"{num_c}"] = value
        num_c += 1
    for key, value in dtrans_table2.items():
        for key2, value2 in value.items():
            dtrans_table2[key][key2] = temp[value2]
    df_dtrans = pd.DataFrame(
        dict([(str(k), pd.Series(v)) for k, v in dtrans_table2.items()])
    )
    # df_dtrans.T.to_csv('dtrans_table.csv')
    return dtrans_table2, df_dtrans.T


def make_dfa(dtrans_table):
    dfa_ = ""
    # make the dtrans table to a format that is like to a dfa graph
    # that format is state symbol1 next_state1 symbol2 next_state1 .......
    for num_c, key in dtrans_table.items():
        dfa_ = dfa_ + f"{num_c} "
        for key2, value2 in key.items():
            dfa_ = dfa_ + f"{key2} {value2} "
        dfa_ = dfa_ + "\n"
    # with open('dfa_made.txt', 'w') as fh:
    #     fh.write(dfa_)
    return dfa_


if __name__ == "__main__":
    regex = input("Enter your dfa example: (a|b)*.c*.(b|a)--> ")  # "(a|b).c.c*.c.#"
    syntax_tree = build_syntax_tree(regex)
    followpos_table = compute_followpos_table(syntax_tree)
    print("Firstpos:")
    print(firstpos(syntax_tree))
    print()
    print("\nLastpos:")
    print(lastpos(syntax_tree))
    print()
    print("\nFollowpos Table:")
    for pos, followpos_set in followpos_table.items():
        print(f"Pos {pos}: {followpos_set}")
    print()
    dtrans_t, df_dtrans = make_dtrans_table(regex)
    print(df_dtrans)
    print()
    dfa_ = make_dfa(dtrans_t)
    print(dfa_)
