# 🤖 Regex-to-DFA Code Generator

This project automates the process of converting **regular expressions** into **Deterministic Finite Automata (DFA)** and then **generates executable Python functions** for each DFA automatically.

It was originally built to simplify a repetitive task in a **compiler design project**, where each regex pattern had to be manually converted into a DFA and coded by hand.  
Here, that entire process has been turned into a **fully automated pipeline**, written purely in Python.

---
## 🎯 Project Goal

The main idea behind this project is to show how **theoretical concepts in automata theory** can be translated into **practical, executable programs** — and to automate a tedious part of the compiler design workflow.

Instead of writing each DFA manually, the program:

1. Reads regex patterns from a file (e.g. `regex.txt`)
    
2. Converts each regex to a DFA using syntax tree and followpos computation
    
3. Generates ready-to-use Python functions for each DFA
    

---
## ⚙️ How It Works

### 🧩 Input

A simple text file (`regex.txt`) containing token names and their corresponding regex patterns:
```text
repeat : <forwhile>
func   : <def>
verd   : <mkboolean>

```

### 🔄 Process

1. The script (`main.py`) reads regexes from the file
    
2. For each regex:
    
    - It builds a **syntax tree**
        
    - Computes **firstpos**, **lastpos**, and **followpos**
        
    - Generates the **DFA transition table**
        
3. It writes the resulting DFA logic as a Python function in `generated_dfa_functions.py`
    

Each generated function can then be used to validate tokens against its corresponding DFA.

---

## 📂 Project Structure

```pgsql
.
├── main.py                  # Entry point: reads regex.txt, generates DFA functions
├── re_to_dfa.py             # Core logic for regex → DFA conversion
├── regex.txt                # Input file: regex patterns and token names
├── generated_dfa_functions.py  # Auto-generated output
└── README.md

```
---
## 🚀 Usage

### 1️⃣ Prepare your regex file

Example (`regex.txt`):
```text
repeat : <forwhile>
func   : <def>
verd   : <mkboolean>
```

### 2️⃣ Run the main script

```bash
python main.py
```

You’ll be prompted to enter the path to your regex.txt file:

```bash
Enter the file path: regex.txt
```

### 3️⃣ Output
A new file named generated_dfa_functions.py will be created, containing Python functions like:
```python
def repeat(lexim):
    j = 0
    state = 0
    while True:
        ch = lexim[j]
        match state:
            case 0:
                if ch == 'r':
                    state = 1
                    j += 1
                elif ch == 'e':
                    state = 2
                    j += 1
                elif ch == 'p':
                    state = 2
            ...

```

---
## 🧠 Implementation Details

- Uses **syntax tree construction** and **followpos-based DFA generation**
- Builds **transition tables** directly from computed positions
- Converts the table into human-readable DFA format
- Uses **pure Python** and **pandas** (for formatting transition tables)

Key functions:
- `build_syntax_tree()` → builds regex syntax tree
- `make_dtrans_table()` → constructs DFA transitions
- `make_dfa()` → formats and outputs DFA representation
- `main.py` → orchestrates regex reading and code generation
---


## 🧰 Tech Stack

- **Language:** Python 3
- **Libraries:** pandas
- **Paradigm:** Algorithmic / Automata Theory
- **Output:** Pure Python code (no external dependencies)

---
## 🔗 Related Work

This project was created for my Compiler Design course to automate regex-based lexical analysis. You can find the related project [here](https://github.com/PashaShahbazi/pasha_lexer).
