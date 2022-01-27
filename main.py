import threading
from tkinter import *


window = Tk()
window.title("Dangerous writing")
window.minsize(width=200, height=200)
window.config(padx=5, pady=5)

WRITING_TIME = 300
PAGE_NR = 1
is_checking = False
short_timer = None
long_timer = None
input_text = ""
text_to_save = ""


# Funcs
def five_min_count_down(seconds):
    global text_to_save, long_timer, is_checking
    count = seconds
    count_min = f"0{count // 60}"
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    long_timer_label.config(text=f"Writing time left: {count_min}:{count_sec}")
    if count > 0:
        long_timer = window.after(1000, five_min_count_down, count - 1)
    else:
        stop()


def five_sec_count_down(seconds):
    global short_timer, input_text
    count = seconds
    short_timer_label.config(text=f"Time to erase: 00:0{count}")
    if count > 0:
        short_timer = window.after(1000, five_sec_count_down, count - 1)
    else:
        window.after_cancel(long_timer)
        long_timer_label.config(text="Writing time left: 00:00")
        page_one.delete("1.0", "end-1c")
        input_text = ""


def start():
    global is_checking
    is_checking = True
    if short_timer is not None:
        window.after_cancel(short_timer)
        window.after_cancel(long_timer)
    five_min_count_down(WRITING_TIME)
    five_sec_count_down(5)
    page_one['state'] = 'normal'
    page_one.delete("1.0", "end-1c")
    save_button['state'] = 'disabled'
    page_one.focus_set()
    checking()


def stop():
    global text_to_save, is_checking
    is_checking = False
    window.after_cancel(long_timer)
    window.after_cancel(short_timer)
    page_one['state'] = 'disabled'
    text_to_save = page_one.get("1.0", 'end-1c').strip()
    long_timer_label.config(text="Writing time left: 05:00")
    short_timer_label.config(text="Time to erase: 00:05")
    save_button['state'] = 'normal'


def checking():
    global input_text, is_checking
    if is_checking:
        if input_text != page_one.get("1.0", 'end-1c').strip():
            window.after_cancel(short_timer)
            five_sec_count_down(5)
            if input_text == "" and page_one.get("1.0", 'end-1c').strip() != "" and long_timer is not None:
                window.after_cancel(long_timer)
                five_min_count_down(WRITING_TIME)
        input_text = page_one.get("1.0", 'end-1c').strip()
        if len(input_text) >= 3180:
            stop()
        t = threading.Timer(0.5, checking)
        t.setDaemon(True)
        t.start()


def save_input():
    global PAGE_NR
    with open(f"page_{PAGE_NR}.txt", "w") as file:
        file.write(text_to_save)
    PAGE_NR += 1


# Labels
long_timer_label = Label(text="Writing time: 05:00", font=("Arial", 12, "bold"))
long_timer_label.grid(column=0, row=0, )
long_timer_label.config(padx=5, pady=5)

short_timer_label = Label(text="Time to erase: 00:05", font=("Arial", 12, "bold"), fg='red')
short_timer_label.grid(column=0, row=2)

# Buttons
start_button = Button(text="Start writing", command=start)
start_button.grid(column=0, row=3)

save_button = Button(text="Save text", command=save_input)
save_button.grid(column=0, row=4)
save_button['state'] = 'disabled'

# Text
page_one = Text(width=80, height=40)
page_one.grid(column=0, row=5)
page_one.config(padx=10, pady=5)
page_one['state'] = 'disabled'


window.mainloop()
