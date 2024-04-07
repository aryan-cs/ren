def get_history():
    history = []
    try:
        with open("history.txt", 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                line1 = lines[i].strip()
                if i + 1 < len(lines):
                    line2 = lines[i + 1].strip()
                    history.append({
                        'role': line1,
                        'content': line2
                    })
            
        return history

    except FileNotFoundError:
        open("history.txt", "w")
        return []

def add_history(history):
    with open('history.txt', 'a') as f:
        for line in history:
            f.write(str(line) + '\n')