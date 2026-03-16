import customtkinter as ctk

class ProgressBox(ctk.CTkFrame):
    def __inti__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent')
        
        barWidth = kwargs.pop('width', 300)
        barHeight = kwargs.pop('height', 28)
        labelFont = kwargs.pop('font', None)
        startingText = kwargs.pop('text', "")

        self.bar = ctk.CTkProgressBar(
            self,
            width = barWidth,
            height = barHeight,
            **kwargs
        )
        
        self.bar.pack(fill='x', expand=True)
        self.bar.set(0)
        
        self.label = ctk.CTkLabel(
            self,
            text = startingText,
            text_color="white",
            font = labelFont,
            fg_color='transparent'
        )
        
        self.label.place(relx=0.5, rely=0.5, anchor='center')
    
    def updateText(self, text: str) -> None:
        self.label.configure(text=text)
        
        
    def updateProgress(self, value: float, total: float) -> None:
        if total > 0:
            progress = value / total
            self.bar.set(progress)
            self.updateText(f"{int(progress * 100)}%")
        else:
            self.bar.set(0)
            self.updateText("0%")