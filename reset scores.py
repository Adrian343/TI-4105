with open("scores.txt", "w") as file:
    string = ""
    for i in range(100):
        string += "0"
        if i < 99:
            string += "\n"
    file.write(string)
