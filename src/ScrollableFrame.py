import tkinter as tk


class ScrollableFrame:
    """
    #### How to use class
    obj = ScrollableFrame(master,height=300 # Total required height of canvas,width=400 # Total width of master)
    objframe = obj.frame
    #### use objframe as the main window to make widget
    """

    def __init__(self, master, width, height, mousescroll=1):
        self.mousescroll = mousescroll
        self.master = master
        self.height = height
        self.width = width
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            self.main_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.adjustScrollregion)

        self.frame = tk.Frame(
            self.canvas, width=self.width, height=self.height)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Enter>", self.entered)
        self.frame.bind("<Leave>", self.left)

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta), "units")

    def entered(self, event):
        if self.mousescroll:
            self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def left(self, event):
        if self.mousescroll:
            self.canvas.unbind_all("<MouseWheel>")

    def adjustScrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
