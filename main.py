import tkinter as tk
import folium
from cefpython3 import cefpython as cef
import sys
from threading import Thread

dummy_loc = [41.01513, 28.979530]

# creating a Leaflet map with Folium
h, w = 1920, 1080
def create_map(loc):
    map = folium.Map(location=loc)
    map.save("map.html")

# initialize web page with CEFPython
def web_thread(web_frame):
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(web_frame.winfo_id())
    window_info.SetAsChild(web_frame.winfo_id(), [0, 0, h, w])
    cef.Initialize()
    # globalizing browser object so that the page is reloadable out of method
    global browser
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
    cef.MessageLoop()

def reload_map(new_location):
    lat, long = new_location.strip().split(",")
    create_map([float(lat), float(long)])
    browser.Reload()

create_map(dummy_loc)

# main tkinter GUI
root = tk.Tk()
root.title("Display LeafletJS maps on Tkinter")

# frame to display the map
web_frame = tk.Frame(root, height=h, width=w)
web_frame.pack()

# web page thread
thread = Thread(target=web_thread, args=(web_frame,))
thread.start()

# reloading map example
entry = tk.Entry(root)
entry.place(x=50, y=50)
btn = tk.Button(root, text="Reload to Location", command=lambda:reload_map(entry.get()))
btn.place(x=50,y=70)


root.mainloop()

