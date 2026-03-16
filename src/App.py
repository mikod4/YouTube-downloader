from os import path

import customtkinter as ctk
from src.widgets import LogFrame, ProgressBox
from pathlib import Path
from src.utils import loadJSON, getDownloadsPath
from src.downloader import getVideoOptions, getResolutions, getAudioOptions, download
import threading

configPath = "src/config.json"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.debounce_timer = None
        
        self.loadConfig()
        self.font = ctk.CTkFont(self.config('fontFamily'), self.config('fontSize'))
        
        self.downloadPath = str(Path.home() / "Downloads")
        self.elements = {}
        
        self.initializeGUI()
        self.packElements()
        
        self.after(100, self.liftAndFocus)
    
    
    def liftAndFocus(self):
        self.lift()
        self.focus_force()
    
    def loadConfig(self):
        try:
            self.configData = loadJSON(configPath)
        except Exception as e:
            self.configData = None
            
    def config(self, property):
        return self.configData.get(property, None)
    
            
    def initializeGUI(self):
        self.geometry(f"{self.config('width')}x{self.config('height')}")
        self.minsize(self.config('width'), self.config('height'))
        self.title(self.config('title'))
        
        self.grid_columnconfigure(0, weight=1)
        
        self.link_var = ctk.StringVar()
        
        self.elements['DownloadFrame'] = ctk.CTkFrame(self, fg_color="transparent")
        self.elements["DownloadPath"] = ctk.CTkEntry(self.elements['DownloadFrame'], 
                                             width=self.config('entryWidth'), 
                                             height=self.config('entryHeight'),
                                             placeholder_text=self.config('downloadPathEntryPlaceholder'),
                                             textvariable=ctk.StringVar(value=getDownloadsPath()),
                                             font = self.font
                                            )
        self.elements["DownloadPathButton"] = ctk.CTkButton(self.elements['DownloadFrame'],
                                                        width=self.config('downloadButtonWidth'), 
                                                        height=self.config('downloadButtonHeight'),
                                                        text=self.config('downloadPathButtonText'),
                                                        font = self.font,
                                                        command = lambda: self.elements["DownloadPath"].configure(textVariable=ctk.StringVar(value=ctk.filedialog.askdirectory(initialdir=getDownloadsPath())))
                                                        )
        
        self.elements["Link"] = ctk.CTkEntry(self, 
                                             width=self.config('entryWidth'), 
                                             height=self.config('entryHeight'),
                                             placeholder_text=self.config('linkEntryPlaceholder'),
                                             textvariable=self.link_var,
                                             font = self.font
                                            )
        
        self.videoFrame = ctk.CTkFrame(self, fg_color="transparent", height=self.config('optionMenuHeight') + 10)
        self.elements["Video"] = ctk.CTkCheckBox(self.videoFrame,
                                                 width=self.config('checkBoxWidth'),
                                                 height=self.config('checkBoxHeight'),
                                                 text=self.config('videoCheckBoxText'),
                                                 font = self.font,
                                                 command = lambda: (self.toggleElementVisibility("VideoResolution"), self.selectAudio())
                                                )
        
        self.elements["VideoResolution"] = ctk.CTkOptionMenu(self.videoFrame, 
                                                             width=self.config('optionMenuWidth'),
                                                             height = self.config('optionMenuHeight'),
                                                             values = self.config('OptionMenuValues'),
                                                             font = self.font
                                                            )
        
        self.elements["Audio"] = ctk.CTkCheckBox(self,
                                                 width=self.config('checkBoxWidth'), 
                                                 height=self.config('checkBoxHeight'),
                                                 text=self.config('audioCheckBoxText'),
                                                 font = self.font
                                                )
        
        self.elements["ProgressBar"] = ctk.CTkProgressBar(self,
                                                          width=self.config('progressBarWidth')
                                                        )
        
        self.elements["DownloadButton"] = ctk.CTkButton(self, 
                                                        width=self.config('buttonWidth'), 
                                                        height=self.config('buttonHeight'),
                                                        text=self.config('downloadButtonText'),
                                                        font = self.font,
                                                        state='disabled',
                                                        command = None
                                                        )
        
        self.elements['Log'] = LogFrame.LogFrame(self,
                                        errorColor=self.config('LogFrameErrorColor'),
                                        goodColor=self.config('LogFrameGoodColor'),
                                        width=self.config('LogFrameWidth'), 
                                        height=self.config('LogFrameHeight'),
                                        label_text=self.config('LogFrameTitle'),
                                        label_font=ctk.CTkFont(
                                            family=self.config('fontFamily'), 
                                            size=self.config('LogFrameTitleFontSize')
                                        ),
                                        label_fg_color=self.config('LogFrameTitleBackground')
                                    )

        self.link_var.trace_add("write", self.onLinkChange)
        
    def startDownload(self):
        link = self.elements["Link"].get()
        path = self.elements["DownloadPath"].get()
        is_video = self.elements["Video"].get()
        
        # Disable button so they don't click twice
        self.elements["DownloadButton"].configure(state="disabled")
        self.elements["Log"].add("Starting download...")

        # Start Thread
        thread = threading.Thread(
            target=self.run_safe_download, 
            args=(link, path, is_video), 
            daemon=True
        )
        thread.start()

    def run_safe_download(self, link, path, is_video):
        result = download(link, path, is_video)
        
        self.after(0, lambda: self.finalize_ui(result))

    def finalize_ui(self, message):
        self.elements["Log"].add(message)
        self.elements["DownloadButton"].configure(state="normal")
        self.elements["ProgressBar"].set(0)
    
    def onLinkChange(self, *args):
        if self.debounce_timer:
            self.after_cancel(self.debounce_timer)
        
        url = self.link_var.get().strip()
        
        if "youtu" in url:
            self.elements['DownloadButton'].configure(state='normal')
            
            self.debounce_timer = self.after(500, lambda: self.launch_resolution_thread(url))
        else:
            self.elements['DownloadButton'].configure(state='disabled')

    def launch_resolution_thread(self, url):
        thread = threading.Thread(target=self.setResolutions, args=(url,), daemon=True)
        thread.start()
        
    def setResolutions(self, target_url):
        try:
            resolutions = getResolutions(target_url)
            if self.link_var.get().strip() == target_url:
                self.after(0, lambda: self.updateUIResolutions(resolutions))
                
        except Exception as e:
            self.after(0, lambda: self.elements['Log'].add(f"Link error: {e}", isError=True))
            self.elements['DownloadButton'].configure(state='disabled')

    def updateUIResolutions(self, resolutions):
        if resolutions:
            resolutions = [str(r) for r in resolutions]
            self.elements["VideoResolution"].configure(values=resolutions)
            self.elements["VideoResolution"].set(resolutions[0])
            self.elements['Log'].add("Resolutions loaded successfully.")
    
    def selectAudio(self):
        self.elements["Audio"].select()
    
    def toggleElementVisibility(self, elementName):
        element = self.elements.get(elementName, None)
        if element:
            if element.winfo_viewable():
                self.hide(elementName)
            else:
                self.show(elementName)
                
        self.update_idletasks()
    
    def hide(self, elementName):
        element = self.elements.get(elementName, None)
        if element:
            element.pack_forget()
            
    def show(self, elementName):
        element = self.elements.get(elementName, None)
        if element:
            element.pack()
        
    def packElements(self):
        pady = self.config('pady')
        padx = self.config('padx')
        
        self.elements['DownloadFrame'].grid(row=0, column=0, pady=pady, padx=padx, sticky="ew")
        self.elements["DownloadPath"].pack(side="left", pady=0)
        self.elements["DownloadPathButton"].pack(side="left", padx=(5,0), pady=0)
        self.elements["Link"].grid(row=1, column=0, pady=pady, padx=padx, sticky="ew")
        
        self.videoFrame.grid(row=2, column=0, pady=pady, padx=padx, sticky="we")
        self.elements["Video"].pack(side="left", pady=0)
        self.elements["VideoResolution"].pack(side="left", padx=(5,0), pady=0)
    
        self.elements["Audio"].grid(row=3, column=0, pady=pady, padx=padx, sticky="w")
        
        self.elements["ProgressBar"].grid(row=4, column=0, pady=pady, padx=padx, sticky="ew")
        self.elements["DownloadButton"].grid(row=5, column=0, pady=pady, padx=padx, sticky="ew")
        self.elements["Log"].grid(row=6, column=0, pady=pady, padx=padx, sticky="nsew")
        
        self.hide("VideoResolution")
        