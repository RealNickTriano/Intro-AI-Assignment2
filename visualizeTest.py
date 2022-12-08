from tkinter import *

SIDE_LENGTH = 30
PADDING_X = 20
PADDING_Y = 20

def create_circle(x, y, r, canvas): # center x,y, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    c = canvas.create_oval(x0, y0, x1, y1, fill='#000', tags='1')
    
def create_square(my_canvas, color, number):
    for i in range(100):
        for k in range(50):
            center = ((k * (SIDE_LENGTH)) + PADDING_X, (i * (SIDE_LENGTH)) + PADDING_Y)
            print(center)
            x1 = center[0] - (SIDE_LENGTH / 2)
            y1 = center[1] - (SIDE_LENGTH / 2)
            x2 = center[0] + (SIDE_LENGTH / 2)
            y2 = center[1] + (SIDE_LENGTH / 2)
            my_canvas.create_rectangle(x1, y1, x2, y2, outline = "black", fill=color, width = 2)
    return

def main():
    root = Tk()
    root.title('Codemy.com -  Canvas')
    root.geometry("1920x1080")
    root.wm_attributes("-transparentcolor", 'grey')

    my_canvas = Canvas(root, width=1920, height=1080, bg="white")
    my_canvas.pack(pady=20)
    
    moveFlag = False
           
    def _on_mousewheel(event):
        if event.delta < 0:
            my_canvas.yview_scroll(1, "units")
        else:
            my_canvas.yview_scroll(-1, "units")

    root.bind("<MouseWheel>", _on_mousewheel)

    create_square(my_canvas, 'white', 0.002)

    root.mainloop()
    
    return

if __name__ == "__main__":
    main()