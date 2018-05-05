import tkinter as tk
import Model
import Plotting
import shutil
from PIL import ImageTk


class MainWindow():



    def __init__(self, master):
        self.master = master

        # 3 High Level Components

        self.topframe = tk.Frame()
        self.topframe.pack(fill = tk.X)
        self.middleFrame = tk.Frame()
        self.middleFrame.pack(fill = tk.X)
        self.bottomFrame = tk.Frame()
        self.bottomFrame.pack(fill=tk.X)



        # Top Frame
        ## Argumentation Framework

        self.argumentationFrame = tk.LabelFrame(self.topframe, text="Argumentation Framework")
        self.argumentationFrame.pack(side=tk.LEFT)

        ### Components

        # Loading graph image
        self.img = ImageTk.PhotoImage(file="./data/graph.jpg")
        self.img.height(), self.img.width()

        # Initializing canvas
        self.argumentationCanvas = tk.Canvas(self.argumentationFrame, scrollregion=(0, 0, self.img.width(), self.img.height()))

        # Setting scrollbars
        self.hbar = tk.Scrollbar(self.argumentationFrame, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.hbar.config(command=self.argumentationCanvas.xview)
        self.vbar = tk.Scrollbar(self.argumentationFrame, orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vbar.config(command=self.argumentationCanvas.yview)

        # Refreshing canvas on scroll
        self.argumentationCanvas.config()
        self.argumentationCanvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # Placing graph on canvas
        self.image_on_canvas = self.argumentationCanvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.argumentationCanvas.pack()

        # Add argument button
        self.add_arg_btn = tk.Button(self.argumentationFrame, text="Add", command = self.add_button_click)
        self.add_arg_btn.pack(side = tk.RIGHT)




        ## Semantics

        # Set all extensions to empty
        self.cfs = []
        self.adm = []
        self.naive = []
        self.grd = []
        self.stb = []
        self.prf = []


        self.prfargs = []
        self.stbargs = []
        self.comargs = []

        self.semanticsFrame = tk.LabelFrame(self.topframe,width=300, text="Semantics")
        self.semanticsFrame.pack(side=tk.RIGHT, fill=tk.BOTH)



        self.topSem = tk.Frame(self.semanticsFrame)
        self.topSem.pack(side=tk.TOP, fill=tk.Y)

        self.botSem = tk.Frame(self.semanticsFrame)
        self.botSem.pack(side=tk.BOTTOM, fill=tk.X)

        ### Components


        self.semanticsContentText = ''
        self.message = tk.Text(self.topSem, width=40, height=13, padx=10,pady=10, state=tk.DISABLED)

        self.message.pack()

        self.skepLabel = tk.Label(self.botSem, text="Show Skep")
        self.skepLabel.pack(side=tk.LEFT)

        self.extension_choice = tk.StringVar(master)
        self.extension_select = tk.OptionMenu(self.botSem, self.extension_choice, ())
        self.extension_select.pack(side=tk.LEFT)
        menu = self.extension_select["menu"]
        menu.delete(0, "end")
        for arg in ["None", "Preferred", "Stable", "Complete"]:
            menu.add_command(label=arg,
                             command=tk._setit(self.extension_choice, arg))
        self.extension_choice.trace('w', self.extension_select_click)

        # Filter visible extensions
        self.filter_button = tk.Button(self.botSem, text="Filter", command=self.filter_button_click)
        self.filter_button.pack(side=tk.RIGHT)
        # Initialise filter to display all semantics
        self.filter_list = [0, 0, 0, 0, 0, 0, 0, 0]



        # Middle Frame
        ## Description
        self.descriptionFrame = tk.LabelFrame(self.middleFrame, text="Description")
        self.descriptionFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE)

        # This should be the default selection in the OptionMenu
        self.arg_choice = tk.StringVar(master)
        self.arg_choice.set(" ")

        # This should be the message in the description
        self.desc_text = ""

        # Description content
        self.description_message = tk.Message(self.descriptionFrame, aspect=500, anchor=tk.NW, text=self.desc_text)
        self.description_message.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE)

        # OptionMenu from which I arguments are selected and their description appears
        self.argument_select = tk.OptionMenu(self.descriptionFrame, self.arg_choice, (), command=self.arg_select_click)
        self.argument_select.pack(side=tk.RIGHT)
        # Call arg_select_click if self.arg_choice choice is changed.
        self.arg_choice.trace('w', self.arg_select_click)
        # BottomFrame
        ### Buttons

        self.evaluate_button = tk.Button(self.bottomFrame, text="Evaluate", command=self.evaluate_button_click)
        self.evaluate_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.bottomFrame, text="Clear", command=self.clear_button_click)
        self.clear_button.pack(side=tk.RIGHT)

    def add_button_click(self):
        self.AddArgWindowMaster = tk.Toplevel(self.master)
        self.AddArgWindow = AddArgWindow(self.AddArgWindowMaster)

    def filter_button_click(self):
        self.FilterWindowMaster = tk.Toplevel(self.master)
        self.FilterWindow = FilterWindow(self.FilterWindowMaster)

    def update_canvas(self):
        self.img = ImageTk.PhotoImage(file="./data/graph.jpg")
        self.img.height(), self.img.width()

        self.argumentationCanvas.itemconfig(self.image_on_canvas, image=self.img)

        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.hbar.config(command=self.argumentationCanvas.xview)

        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vbar.config(command=self.argumentationCanvas.yview)

        self.argumentationCanvas.config(scrollregion=(0, 0, self.img.width(), self.img.height()),
                                        xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.argumentationCanvas.pack()

    def clear_button_click(self):
        # Wipe all model variables
        Model.framework = {}
        Model.descriptions = {}
        Model.arguments = set()
        Model.relations = set()
        Model.cfs = set()
        Model.grod = set()
        Model.prf = set()
        # Wipe the graph plot
        shutil.copy2('./data/blank.png', './data/graph.jpg')
        self.update_canvas()
        # Wipe the semantics text
        self.semanticsContentText=""
        self.message.config(state=tk.NORMAL)
        self.message.delete(1.0, tk.END)
        self.message.config(state=tk.DISABLED)
        # Wipe the descriptions message and options menu
        self.description_message.config(text="")
        menu = self.argument_select["menu"]
        menu.delete(0, "end")

        # Set all extensions to empty
        self.cfs = []
        self.adm = []
        self.naive = []
        self.grd = []
        self.stb = []
        self.prf = []
        self.prfargs = []
        self.stbargs = []
        self.comargs = []

    def evaluate_button_click(self):
        self.cfs = Model.compute_cfs()
        self.adm = Model.compute_admissibility(self.cfs)
        self.naive = Model.compute_naive_extension(self.cfs)
        self.grd = Model.compute_grounded_extension(self.adm)
        self.stb = Model.compute_stable_extension(self.adm)
        self.prf = Model.compute_preferred_extensions(self.adm)

        self.prfargs = []
        self.stbargs = []
        for arg in Model.arguments:
            check = []
            for i in self.prf:
                check.append(arg in i)
            if all(check):
                self.prfargs.append(arg)
            check = []
            for i in self.stb:
                check.append(arg in i)
            if all(check):
                self.stbargs.append(arg)

        self.comargs = []
        for arg in Model.arguments:
            if (arg in self.prfargs) and (arg in self.stbargs):
                self.comargs.append(arg)





        self.cfText = "Conflict Free Subsets: " + self.normalize_semText(self.cfs)
        self.admisText = "Admissible Subsets: " + self.normalize_semText(self.adm)
        self.naiveText = "Naive Extensions: " + self.normalize_semText(self.naive)
        self.stbText = "Stable Extensions: " + self.normalize_semText(self.stb)
        self.grdText = "Grounded Extension: " + self.normalize_semText(self.grd)
        self.prfText = "Preferred Extensions: " + self.normalize_semText(self.prf)
        self.comText = "Complete Extensions: "


        if self.normalize_semText(self.grd) == self.normalize_semText(self.prf):
            self.comText = self.comText + self.normalize_semText(self.grd)
        elif len(self.normalize_semText(self.grd)) == 4:
            self.comText = self.comText + self.normalize_semText(self.prf)
        else:
            self.comText = self.comText + self.normalize_semText(self.grd) + self.normalize_semText(self.prf)

        self.semanticsContentText = ""

        # Apply the filter to the display
        if self.filter_list[0]==0:
            self.semanticsContentText = self.semanticsContentText + self.cfText
        if self.filter_list[1]==0:
            self.semanticsContentText = self.semanticsContentText + self.admisText
        if self.filter_list[2]==0:
            self.semanticsContentText = self.semanticsContentText + self.naiveText
        if self.filter_list[3]==0:
            self.semanticsContentText = self.semanticsContentText + self.stbText
        if self.filter_list[4]==0:
            self.semanticsContentText = self.semanticsContentText + self.grdText
        if self.filter_list[5]==0:
            self.semanticsContentText = self.semanticsContentText + self.prfText
        if self.filter_list[6]==0:
            self.semanticsContentText = self.semanticsContentText + self.comText


        #self.semanticsContentText = self.cfText + self.admisText + self.naiveText + self.stbText + self.grdText + self.prfText + self.comText

        #self.message.config(text=self.semanticsContentText)
        self.message.config(state=tk.NORMAL)
        self.message.delete(1.0, tk.END)
        self.message.insert(tk.END, self.semanticsContentText)
        self.message.config(state=tk.DISABLED)

    def normalize_semText(self, sem):

        return str(sem).replace("{", "").replace("}", "").replace("[", "{").replace("]", "}").replace("',)", "')").replace("'", "").replace("(", "{").replace(")",
        "}")+ "\n" + "\n"


    def arg_select_click(self, *args):

        value = self.arg_choice.get()
        self.desc_text = Model.descriptions[value]
        self.description_message.config(text=self.desc_text)

    def extension_select_click(self, *args):
        if self.extension_choice.get() == "Complete":
            Plotting.ConstructColouredGraph(self.comargs)
            self.update_canvas()
        elif self.extension_choice.get() == "Stable":
            Plotting.ConstructColouredGraph(self.stbargs)
            self.update_canvas()
        elif self.extension_choice.get() == "Preferred":
            Plotting.ConstructColouredGraph(self.prfargs)
            self.update_canvas()
        else:
            Plotting.ConstructGraph()
            self.update_canvas()

class AddArgWindow:

    def __init__(self, master, arg_entry="", attack_entry=""):

        self.master = master
        self.framelabel = tk.Frame(self.master)
        self.framelabel.pack()
        self.frameattacks = tk.Frame(self.master)
        self.frameattacks.pack()
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.arg_label = tk.Label(self.framelabel, text="Label:   ")
        self.arg_label.pack(side=tk.LEFT)
        self.arg_entry = tk.Entry(self.framelabel)
        self.arg_entry.insert(tk.END, arg_entry)
        self.arg_entry.pack(side=tk.LEFT)
        self.attack_label = tk.Label(self.frameattacks, text="Attacks:")
        self.attack_label.pack(side=tk.LEFT)
        self.attack_entry = tk.Entry(self.frameattacks)
        self.arg_entry.insert(tk.END, attack_entry)
        self.attack_entry.pack(side=tk.LEFT)


        self.desc_label = tk.Label(self.frame,text="Description:   ")
        self.desc_label.pack()
        self.desc_text = tk.Text(self.frame, width=30, height=10, borderwidth = 2)
        self.desc_text.pack()

        self.quitButton = tk.Button(self.frame, text='Quit', width=12, command=self.close_windows)
        self.quitButton.pack(side=tk.RIGHT)
        self.addButton = tk.Button(self.frame, text='Save', width=12, command=self.save_button_click)
        self.addButton.pack(side=tk.LEFT)

    def close_windows(self):
        self.master.destroy()

    def save_button_click(self):

        # Update Model
        argument = self.arg_entry.get()
        if argument != '':
            Model.arguments.add(argument)

        attacks = set(self.attack_entry.get().replace(" ","").split(","))
        Model.framework[argument] = attacks

        Model.descriptions[argument] = self.desc_text.get("1.0", tk.END)

        for i in attacks:
            if len(i)>0:
             Model.relations.add((argument,i))
             if i not in Model.arguments:
                 Model.arguments.add(i)

        # Update Graph Image

        Plotting.ConstructGraph()

        # Attempt to fetch description and attempt to add arguments in the OptionMenu of the description
        menu = window.argument_select["menu"]
        menu.delete(0, "end")
        for arg in Model.arguments:
            menu.add_command(label=arg,
                             command=tk._setit(window.arg_choice, arg))


        # Update canvas image
        window.update_canvas()

        #
        self.master.destroy()

# Top View for filtering semantics
class FilterWindow:

    def __init__(self, master):
        self.master = master

        # Dividing space into rows
        self.row1 = tk.Frame(self.master)
        self.row1.pack(fill=tk.X)
        self.row2 = tk.Frame(self.master)
        self.row2.pack(fill=tk.X)
        self.row3 = tk.Frame(self.master)
        self.row3.pack(fill=tk.X)
        self.row4 = tk.Frame(self.master)
        self.row4.pack(fill=tk.X)
        self.row5 = tk.Frame(self.master)
        self.row5.pack(fill=tk.X)
        self.row6 = tk.Frame(self.master)
        self.row6.pack(fill=tk.X)
        self.row7 = tk.Frame(self.master)
        self.row7.pack(fill=tk.X)
        self.row8 = tk.Frame(self.master)
        self.row8.pack(fill=tk.X)

        # Placing labels
        cfLabel = tk.Label(self.row1, text= "Hide conflict free subsets")
        cfLabel.pack(side=tk.LEFT)
        adLabel = tk.Label(self.row2, text="Hide admissible subsets ")
        adLabel.pack(side=tk.LEFT)
        naLabel = tk.Label(self.row3, text="Hide naive extension(s) ")
        naLabel.pack(side=tk.LEFT)
        coLabel = tk.Label(self.row4, text="Hide complete extension(s) ")
        coLabel.pack(side=tk.LEFT)
        grLabel = tk.Label(self.row5, text="Hide grounded extension ")
        grLabel.pack(side=tk.LEFT)
        prfLabel = tk.Label(self.row6, text="Hide preferred extension(s) ")
        prfLabel.pack(side=tk.LEFT)
        stbLabel = tk.Label(self.row7, text="Hide stable extension(s) ")
        stbLabel.pack(side=tk.LEFT)
        lbLabel = tk.Label(self.row8, text="Hide labeling ")



        # Declaring On/Off vars
        self.cfsToggle = tk.IntVar()
        self.cfsToggle.set(window.filter_list[0])
        self.adToggle = tk.IntVar()
        self.adToggle.set(window.filter_list[1])
        self.naToggle = tk.IntVar()
        self.naToggle.set(window.filter_list[2])
        self.coToggle = tk.IntVar()
        self.coToggle.set(window.filter_list[3])
        self.grToggle = tk.IntVar()
        self.grToggle.set(window.filter_list[4])
        self.prfToggle = tk.IntVar()
        self.prfToggle.set(window.filter_list[5])
        self.stbToggle = tk.IntVar()
        self.stbToggle.set(window.filter_list[6])
        self.lbToggle = tk.IntVar()


        # Making check boxes
        self.cf = tk.Checkbutton(self.row1, text="", variable=self.cfsToggle, offvalue="0", onvalue="1", justify=tk.LEFT)
        self.cf.pack(side=tk.RIGHT)
        self.ad = tk.Checkbutton(self.row2, text="", variable=self.adToggle,offvalue="0", onvalue="1", justify=tk.LEFT)
        self.ad.pack(side=tk.RIGHT)
        self.na = tk.Checkbutton(self.row3, text="", variable=self.naToggle, offvalue="0", onvalue="1",justify=tk.LEFT)
        self.na.pack(side=tk.RIGHT)
        self.co = tk.Checkbutton(self.row4, text="", variable=self.coToggle,offvalue="0", onvalue="1", justify=tk.LEFT)
        self.co.pack(side=tk.RIGHT)
        self.gr = tk.Checkbutton(self.row5, text="", variable=self.grToggle, offvalue="0", onvalue="1",justify=tk.LEFT)
        self.gr.pack(side=tk.RIGHT)
        self.prf = tk.Checkbutton(self.row6, text="", variable=self.prfToggle, offvalue="0", onvalue="1",justify=tk.LEFT)
        self.prf.pack(side=tk.RIGHT)
        self.stb = tk.Checkbutton(self.row7, text="", variable=self.stbToggle, offvalue="0", onvalue="1",justify=tk.LEFT)
        self.stb.pack(side=tk.RIGHT)
        self.lb = tk.Checkbutton(self.row8, text="", variable=self.lbToggle,offvalue="0", onvalue="1", justify=tk.LEFT)


        # Buttons to quit or save
        self.quit_btn = tk.Button(master, text='Quit', width=12, command = self.quit_button_click )
        self.quit_btn.pack(side=tk.RIGHT)
        self.filter_btn = tk.Button(master, text='Filter', width=12, command = self.filter_button_click)
        self.filter_btn.pack(side=tk.LEFT)

    def filter_button_click(self):
        filter_list = [self.cfsToggle.get(), self.adToggle.get(), self.naToggle.get(), self.coToggle.get(), self.grToggle.get(), self.prfToggle.get(), self.stbToggle.get(), self.lbToggle.get()]
        window.filter_list = filter_list
        window.evaluate_button_click()
        self.master.destroy()

    def quit_button_click(self):
        self.master.destroy()



if __name__ == "__main__":


    root = tk.Tk()
    root.title("Automated Inference")

    def on_closing():
        shutil.copy2('./data/blank.png', './data/graph.jpg')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    window = MainWindow(root)
    root.mainloop()
