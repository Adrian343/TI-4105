from AppKit import NSScreen
import tkinter as tk
from random import shuffle, choice
import ScrollableFrame
from os import path


class App(tk.Frame):
    def _on_mousewheel(self, event):
        self.root.yview_scroll(-1*(event.delta), "units")

    def __init__(self):
        self.window = tk.Tk()
        self.configureWindow()

        self.fetchQuestions()
        self.showingLF = False

        self.spmPrefix = tk.Label(self.root, wraplength=self.ROOTWIDTH-25)
        self.spmPrefix.pack(anchor="w")

        self.spm = tk.Label(self.root, wraplength=self.ROOTWIDTH-25,
                            font=("Times New Roman", 20), justify="left")
        self.spm.pack(anchor="w")
        self.spm.bind("<Configure>", self.obj.adjustScrollregion)

        self.btnfrm = tk.Frame(self.root)
        self.btna = tk.Button(self.btnfrm, text="a", command=lambda: self.answer(
            self.btna), font=("Times New Roman", 20), wraplength=self.ROOTWIDTH-40, justify="left")
        self.btnb = tk.Button(self.btnfrm, text="b", command=lambda: self.answer(
            self.btnb), font=("Times New Roman", 20), wraplength=self.ROOTWIDTH-40, justify="left")
        self.btnc = tk.Button(self.btnfrm, text="c", command=lambda: self.answer(
            self.btnc), font=("Times New Roman", 20), wraplength=self.ROOTWIDTH-40, justify="left")
        self.btnd = tk.Button(self.btnfrm, text="d", command=lambda: self.answer(
            self.btnd), font=("Times New Roman", 20), wraplength=self.ROOTWIDTH-40, justify="left")
        self.btna.grid(row=0, column=0, sticky="W")
        self.btnb.grid(row=1, column=0, sticky="W")
        self.btnc.grid(row=2, column=0, sticky="W")
        self.btnd.grid(row=3, column=0, sticky="W")
        self.btnfrm.pack(anchor="w")
        self.root.bind_all("1", lambda e: self.answer(self.btna))
        self.root.bind_all("2", lambda e: self.answer(self.btnb))
        self.root.bind_all("3", lambda e: self.answer(self.btnc))
        self.root.bind_all("4", lambda e: self.answer(self.btnd))

        self.LF = tk.Label(
            self.root, wraplength=self.ROOTWIDTH-25, justify="left")
        self.LF.pack(anchor="w")

        self.getNextQuestion()

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def configureWindow(self):
        self.SCRWIDTH = NSScreen.mainScreen().frame().size.width
        self.SCRHEIGHT = NSScreen.mainScreen().frame().size.height
        self.ROOTWIDTH = int(self.SCRWIDTH * 0.5)
        self.ROOTHEIGHT = int(self.SCRHEIGHT * 0.8)
        self.ROOTX = int((self.SCRWIDTH - self.ROOTWIDTH) / 5)
        self.ROOTY = int((self.SCRHEIGHT - self.ROOTHEIGHT) / 2)
        self.window.geometry(
            f"{self.ROOTWIDTH}x{self.ROOTHEIGHT}+{self.ROOTX}+{self.ROOTY}")
        self.window.title("Løs TIØ4105 eksamen")
        self.window.maxsize(self.ROOTWIDTH, self.ROOTHEIGHT)
        # Total required height of canvas,width=400 # Total width of master)
        self.obj = ScrollableFrame.ScrollableFrame(
            self.window, height=100, width=self.ROOTWIDTH)
        self.obj.frame.config()

        self.root = self.obj.frame

    def answer(self, button):
        if self.showingLF:
            self.showingLF = False
            self.LF['text'] = ""
            self.LF["image"] = ""
            self.spm['text'] = ""
            self.spm["image"] = ""
            for v in self.btnfrm.children.values():
                v["foreground"] = "WHITE"
            self.getNextQuestion()
        else:
            self.showingLF = True
            """ self.LFimage = tk.PhotoImage(self.LFT)
            self.LF['image'] = self.LFimage """
            if self.LFContent == "":
                self.LF["text"] = ""
                self.LFImage = tk.PhotoImage(file=path.join(path.dirname(
                    __file__), f"resources/pictures/{self.currentQuestion}LF.png"))
                self.LF['image'] = self.LFImage
            else:
                self.LF["image"] = ""
                self.LF["text"] = "" + self.LFContent
            if button["text"] == self.correctAnswer:
                self.scoreChange(self.currentQuestion, 1)
                button["foreground"] = "GREEN"
            else:
                button["foreground"] = "RED"
                [v for v in self.btnfrm.children.values() if v["text"] ==
                 self.correctAnswer][0]["foreground"] = "GREEN"
                self.scoreChange(self.currentQuestion, -1)

    def getNextQuestion(self):
        with open(path.join(path.dirname(__file__), 'scores.txt'), 'r') as file:
            scores = file.readlines()
        lowestScores = [(i, v) for i, v in enumerate(scores)]
        lowestScores.sort(key=lambda x: x[1])
        self.currentQuestion = choice(lowestScores[:35])[0]
        # TODO hva skal determinere hvilke spørsmål som blir valgt
        currQ = self.questions[self.currentQuestion-1]
        if currQ[0] == "":
            self.spm["text"] = ""
            self.spmImage = tk.PhotoImage(file=path.join(path.dirname(
                __file__), f"resources/pictures/{self.currentQuestion}.png"))
            self.spm['image'] = self.spmImage
        else:
            self.spm["image"] = ""
            self.spm["text"] = currQ[0]+""
        self.LFContent = currQ[1]
        self.correctAnswer = currQ[2]
        self.Qs = currQ[2:]
        shuffle(self.Qs)
        self.btna["text"] = self.Qs[0]
        self.btnb["text"] = self.Qs[1]
        self.btnc["text"] = self.Qs[2]
        self.btnd["text"] = self.Qs[3]
        # kreativt eksempel av pythons logikk under:)
        spmPrefix = f"Spørsmål nr. {self.currentQuestion - (60*(self.currentQuestion>60))} eksamen 202{int(self.currentQuestion>60)}\n"
        self.spmPrefix["text"] = spmPrefix

    def scoreChange(self, qNo, change):
        with open(path.join(path.dirname(__file__), 'scores.txt'), 'r') as file:
            self.scores = file.readlines()

        self.scores[qNo-1] = str(int(self.scores[qNo-1].strip())+change)+'\n'

        with open(path.join(path.dirname(__file__), 'scores.txt'), 'w') as file:
            file.writelines(self.scores)

    def fetchQuestions(self):
        self.questions = []
        with open(path.join(path.dirname(__file__), 'resources/Qs.txt'), "r") as file:
            data = [line.replace("\\n", "\n")
                    for line in file.read().splitlines()]

            for i in range(0, len(data), 6):
                self.questions.append(
                    [data[i], data[i+1], data[i+2], data[i+3], data[i+4], data[i+5]])

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
