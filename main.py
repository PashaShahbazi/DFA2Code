import re_to_dfa as rd


def read_dict_from_file(file_path):
    my_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            # Remove leading and trailing whitespace characters
            line = line.strip()
            if line:
                # Split the line into key and value
                key, value = line.split(":", 1)
                my_dict[key.strip()] = value.strip()
    return my_dict, list(my_dict.keys())


file_path = input("Enter the file path: ")
try:
    regex_dict, regex_list = read_dict_from_file(file_path)
except:
    print("the file path is not correct!? pleas enter it again")
    exit()
# Define the list of tokens and their respective regex patterns
list__ = [
    "repeat",
    "func",
    "verd",
    "se",
    "alse",
    "al",
    "en",
    "bro",
    "ritorno",
    "ilg",
    "rango",
    "caden",
]
dict_tk = {
    "repeat": "<forwhile>",
    "func": "<def>",
    "verd": "<mkboolian>",
    "se": "<if>",
    "alse": "<elif>",
    "al": "<else>",
    "en": "<in>",
    "bro": "<defcall>",
    "ritorno": "<return>",
    "ilg": "<mknumber>",
    "rango": "<range_num>",
    "caden": "<mkstr>",
}
dict_dtrans = {}

# Process each pattern to create DFA transition tables
for i in regex_list:
    temp = ""
    if "." not in i:
        for j in i:
            temp = temp + j + "."
        temp = temp[:-1]
    else:
        temp = i
    dict_dtrans[i] = rd.make_dfa(rd.make_dtrans_table(temp)[0])

# Generate Python functions for each DFA
with open("generated_dfa_functions.py", "w") as fh:
    for name, a in list(dict_dtrans.items()):
        a = a.split("\n")
        a = [i.split() for i in a]
        aa = []
        for i in a:
            if len(i) >= 1:
                aa.append(i)

        fh.write(f"def {name}(lexim):\n")
        fh.write("    j = 0\n")
        fh.write("    state = 0\n")
        fh.write("    while True:\n")
        fh.write("        ch = lexim[j]\n")
        fh.write("        match state:\n")

        temp = ""
        for t in aa:
            if "T" in t[0]:
                temp = t[0][-1]
        T = temp

        for i in aa:
            if "F" in i[0]:
                fh.write(f"            case {str(int(i[0][-1])-1)}:\n")
            elif "T" in i[0]:
                fh.write(f"            case {str(int(i[0][-1])-1)}:\n")
                fh.write("                return False, None\n")
                continue
            else:
                fh.write(f"            case {str(int(i[0])-1)}:\n")

            for j in range(1, len(i), 2):
                if j == 1:
                    if not "F" in i[j + 1] and not "T" in i[j + 1]:
                        fh.write(f"                if ch == '{i[j]}':\n")
                        fh.write(
                            f"                    state = {str(int(i[j + 1])-1)}\n"
                        )
                        fh.write("                    j += 1\n")
                    else:
                        fh.write(f"                if ch == '{i[j]}':\n")
                        fh.write(
                            f"                    state = {str(int(i[j + 1][-1])-1)}\n"
                        )
                        fh.write("                    j += 1\n")
                elif "T" in i[j + 1]:
                    fh.write(f"                elif ch == '{i[j]}':\n")
                    fh.write(
                        f"                    state = {str(int(i[j + 1][-1])-1)}\n"
                    )
                    fh.write("                    j += 1\n")
                elif "F" in i[j + 1]:
                    fh.write(f"                elif ch == '{i[j]}':\n")
                    fh.write(
                        f"                    state = {str(int(i[j + 1][-1])-1)}\n"
                    )
                    fh.write("                    j += 1\n")
                else:
                    fh.write(f"                elif ch == '{i[j]}':\n")
                    fh.write(f"                    state = {str(int(i[j + 1])-1)}\n")
                    fh.write("                    j += 1\n")
            else:
                if "F" in i[0]:
                    fh.write(f"                elif ch == '\\n':\n")
                    fh.write(f"                    return True, '{regex_dict[name]}'\n")
                    fh.write("                    j += 1\n")
                fh.write("                else:\n")
                fh.write(f"                    state = {T}\n")
