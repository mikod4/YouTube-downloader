import customtkinter as ctk

class LogFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, errorColor: str, goodColor: str, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.errorColor = errorColor
        self.goodColor = goodColor
        
        self.logs = []
        
    def add(self, text: str, isError: bool = False) -> None:
        newLog = ctk.CTkLabel(self,
                               width = self.winfo_width() - 20,
                               text = text,text_color = self.errorColor if isError else self.goodColor,
                               anchor='w',
                               justify='left'
                            )

        newLog.pack(side='top', fill='x', pady=2)
        self.logs.append(newLog)
        
        self.update_idletasks()
        self._parent_canvas.yview_moveto(1.0)