import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import Tk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.root = self
        self.root.attributes("-fullscreen",True)
        self.width = 1920
        self.height = 1080
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - self.width / 2)
        center_y = int(screen_height/2 - self.height / 2)
        self.root.geometry(f'{self.width}x{self.height}+{center_x}+{center_y}')
        self.root.resizable(0,0)
        self.root.grid_rowconfigure(0, weight=1)  # configure grid system
        self.root.grid_columnconfigure(0, weight=1)

        # Color Palletes
        self.mainBg = "cyan"
        self.mainFont = "black"
        self.timeFont = "white"
        self.btnFont = "white"
        self.bodyBg = "#a7c4f2"

        # Time Range
        self.startTime = '7:00'
        self.endTime = '20:00'
        self.timeList = self.split_time(self.startTime,self.endTime)
        # Key bindings
        self.bind('<Escape>', lambda e: self.exit(e))

        # Subject List
        self.tables = {}

        self.start_menu()
        #self.main()

    def split_time(self, start, end):
        start_time = datetime.strptime(start, '%H:%M')
        end_time = datetime.strptime(end, '%H:%M')
        interval = timedelta(minutes=15)

        time_list = []
        current_time = start_time

        while current_time <= end_time:
            time_list.append(current_time.strftime('%H:%M'))
            current_time += interval

        return time_list

    def start_menu(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0,weight=1)
        self.startFrame = ctk.CTkFrame(master=self.root, fg_color=self.mainBg)
        self.startFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Configure Grid
        self.startFrame.rowconfigure(0,weight=2)
        self.startFrame.rowconfigure(1,weight=1)
        self.startFrame.rowconfigure(2,weight=1)

        self.startFrame.columnconfigure(0,weight=1)
        self.startFrame.columnconfigure(1,weight=1)
        self.startFrame.columnconfigure(2,weight=1)

        self.startBtn = ctk.CTkButton(self.startFrame, text="Start", command=lambda: self.setup_menu(), width=350,height=150,font=("Roboto",45))
        self.settingBtn = ctk.CTkButton(self.startFrame, text="Setting", command=lambda: self.setup_menu(), width=350,height=150,font=("Roboto",45))
        self.startBtn.grid(row=1,column=1)
        self.settingBtn.grid(row=2,column=1)

    def setup_menu(self):
        def submit(prevDay,today):
            times = []

            # Change select btn
            for btn in daysBtn:
                if btn.cget("text") != today:
                    btn.configure(fg_color="#6c6ca3")
                else:
                    btn.configure(fg_color="#383857")
            
            for btn in timeBoxes:
                if btn.get() == "on":
                    times.append(btn.cget("text"))
                    btn.deselect()
            try:
                self.tables[self.subjectEntry.get()][prevDay] = list(set(times))
            except:
                self.tables[self.subjectEntry.get()] = {}
                self.tables[self.subjectEntry.get()][prevDay] = list(set(times))

            loadTimeList(prevDay,today)

        def saveTables(state,day):
            times = []
            for btn in timeBoxes:
                if btn.get() == "on":
                    times.append(btn.cget("text"))
                    btn.deselect()

            try:
                self.tables[self.subjectEntry.get()][day] = list(set(times))
            except:
                self.tables[self.subjectEntry.get()] = {}
                self.tables[self.subjectEntry.get()][day] = list(set(times))

            if state == "next":
                self.subjectEntry.delete(0, ctk.END)
                loadTimeList(day,day)
            else:
                self.confirmation()

        def loadTimeList(prevDay,today):
            x_row = 1
            y_row = 0

            for time in (self.timeList):
                check_var = ctk.StringVar(value="off")
                if x_row > 10:
                    x_row = 1
                    y_row += 1
                else:
                    pass
                self.timeFrame.grid_columnconfigure(y_row,weight=1)
                timeBox = ctk.CTkCheckBox(self.timeFrame, text=time,font=("Roboto",18),variable=check_var, text_color=self.timeFont, onvalue="on", offvalue="off")
                timeBox.grid(row=x_row,column=y_row,pady=30)
                timeBoxes.append(timeBox)
                x_row += 1
            
            for dayBtn in daysBtn:
                todayText = dayBtn.cget("text")
                if todayText == today:
                    dayBtn.configure(fg_color="#383857")
                dayBtn.configure(command= lambda prevDay = today, today = todayText:submit(prevDay,today))

            self.nextBtn = ctk.CTkButton(self.timeFrame,font=("Roboto",25),text_color=self.btnFont,text="Next",command=lambda:saveTables("next",today)).grid(row=11,column=y_row - 1)
            self.confirmBtn = ctk.CTkButton(self.timeFrame,font=("Roboto",25),text_color=self.btnFont,text="Confirm",command=lambda:saveTables("submit",today)).grid(row=11,column=y_row)


        self.startFrame.grid_forget()

        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)

        self.settingFrame = ctk.CTkFrame(master=self.root, fg_color=self.bodyBg,width=self.width,height=300,corner_radius=0)
        self.daysFrame = ctk.CTkFrame(master=self.root,width=self.width,height=80,corner_radius=0)
        self.timeFrame = ctk.CTkFrame(master=self.root, fg_color=self.bodyBg,corner_radius=0)

        # Setup grid
        self.root.grid_rowconfigure(0,weight=0)
        self.root.grid_columnconfigure(0,weight=3)
        self.root.grid_rowconfigure(1,weight=0)
        self.root.grid_rowconfigure(2,weight=10)

        # To store checkboxes
        timeBoxes = []

        # Create days tab
        days = ['Sunday','Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday']
        daysBtn = []
        for count, day in enumerate(days):
            dayBtn = ctk.CTkButton(master=self.daysFrame,font=("Roboto",25),border_width=1,fg_color="#6c6ca3",border_color="black",corner_radius=0,width=(self.width//7)
                                   ,height=80,text_color=self.btnFont,text=day,command=lambda prevDay = day, today = day: loadTimeList(prevDay,today))
            daysBtn.append(dayBtn)
            dayBtn.grid(row=0,column=count,padx=0,pady=0)


        # Grid Frame
        self.settingFrame.grid(row=0, sticky="nsew")
        self.daysFrame.grid(row=1, sticky="ew")
        self.timeFrame.grid(row=2, sticky="nsew")

        self.subjectLabel = ctk.CTkLabel(self.settingFrame,font=("Roboto",25),text_color=self.mainFont,text="Subject Name:").grid(row=0,column=0,padx=30,pady=10)
        self.subjectEntry = ctk.CTkEntry(self.settingFrame,width=600,font=("Roboto",25))
        self.subjectEntry.grid(row=0,column=1, padx=5,pady=30,columnspan=3)

    def confirmation(self):
        for screen in self.root.winfo_children():
            screen.destroy()
        
        self.confirmFrame = ctk.CTkFrame(master=self.root,fg_color=self.mainBg)
        self.confirmFrame.grid(row=0,sticky="nsew")
        for subject in self.tables:
            for day in self.tables[subject]:
                print(subject)
                print(day)
                print(self.tables[subject][day])
        # for subject in self.tables:
        #     for day in subject:
        #         print(self.tables[subject][day])

    
    def main(self):
        for screen in self.root.winfo_children():
            screen.destroy()
        # self.timeFrame.grid_forget()
        # self.settingFrame.grid_forget()
        self.mainFrame = ctk.CTkFrame(master=self.root, fg_color=self.mainBg)
        self.mainFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        days = ['Time/Day','Mon', 'Tue', 'Wed', 'Thu','Fri','Sat','Sun']
        for count, day in enumerate(days):
            dayBox = ctk.CTkLabel(master=self.mainFrame,width=self.width/8,height=150,fg_color="light grey",font=("Roboto",25),text_color="black",text=day)
            dayBox.grid(row=0,column=count,sticky="nsew")
        
        
        # for count,time in enumerate(self.timeList):
        #     timeBox = ctk.CTkLabel(master=self.mainFrame,height=self.height/len(self.timeList),text=time,text_color="black")
        #     timeBox.grid(row=count+1,column=0)

    def exit(self,e):
        self.root.quit()

app = App()
app.mainloop()

