import tkinter as tk
from fordFulkerson import FordFulkersonAlgorithm
from tkinter import ttk
import pydot, os

def on_enter(event):
    event.widget['bg']="gray"
    event.widget['fg']="black"

def on_leave(event):
    event.widget['bg']="black"
    event.widget['fg']="white"

class ImageViewer:
    def __init__(self, root, images, maxFlows):
        self.root = root
        self.images = images
        self.current_index = 0
        self.maxFlows=maxFlows

        self.root.wm_iconphoto(False, tk.PhotoImage(file='icon.png'))
        self.root.title('Ford-Fulkerson')
        self.root.geometry("1000x650")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings={'TCombobox':
                                        {'configure':
                                            {'selectforeground': 'white',   # black font color for selection
                                            'selectbackground': 'black',   # gray background for selection
                                            'fieldbackground': 'black',    # dark gray for the combobox field
                                            'background': 'gray',        # black background
                                            'foreground': 'red',        # white font color
                                            }
                                        }
                                        }
                                )
        combostyle.theme_use('combostyle') 

        self.heading = tk.Label(self.root, text="FORD FULKERSON ALGORITHM", font=("Century Gothic",32), bg="black", fg="white")
        
        self.heading2Text=tk.StringVar()
        self.heading2Text.set('Current Flow: ' + str(maxFlows[0]))
        self.heading2Label=tk.Label(self.root,  textvariable=self.heading2Text, font=("Century Gothic", 16), bg="black", fg="white")
            
        self.next_button = tk.Button(self.root, text="Next", command=self.show_next_image)    
        self.next_button = tk.Button(self.root, text="Next", font=("Century Gothic", 12), command=self.show_next_image, bg="black", fg="white", borderwidth=2, width=15)
        
        self.heading.place(relx=0.5, y=50, anchor='center')
        self.heading2Label.place(relx=0.5, y=110, anchor="center")
        self.next_button.place(relx=0.5, y=150, anchor='center')
        
        self.next_button.bind("<Enter>", on_enter)
        self.next_button.bind("<Leave>", on_leave)
        
        self.image_label = tk.Label(self.root)
        self.image_label.pack(expand=True)
        
        self.show_image()

    def show_image(self):
        image_path = self.images[self.current_index]
        self.tk_image = tk.PhotoImage(file=image_path)
        self.image_label.config(image=self.tk_image)

    def show_next_image(self):
        self.current_index = (self.current_index + 1)
        self.show_image()
        self.heading2Text.set("Current Flow: " + str(self.maxFlows[self.current_index]))
        if self.current_index>=len(self.images)-1:
            self.heading2Text.set("Maximum Flow: " + str(self.maxFlows[self.current_index-1]))
            self.next_button.destroy()    

if __name__ == "__main__":
    graph = {
        'A': [False,['B',10,0],['C',10,0]],
        'B': [False,['D',4,0],['E',8,0]],
        'C': [False,['F',9,5]],
        'D': [False,['F',10,0]],
        'E': [False,['D', 6,0],['F',10,0]],
        'F': [False]
    }
    src = 'A'
    dest = 'F'
    image_files = []
    
    obj = FordFulkersonAlgorithm(src, dest, graph)
    maxFlows= obj.maximumFlow()
    print('Maximum Flows: ', maxFlows)
    j = 0
    for i in obj.augPathsGraph:
        if not os.path.exists('Graphs'):
            os.makedirs("Graphs")
        imagePath='Graphs/'+ str(j)+'.png'
        image_files.append(imagePath)
        i.write_png(imagePath)
        j+=1

    root = tk.Tk()

    viewer = ImageViewer(root, image_files, maxFlows)

    root.mainloop()
