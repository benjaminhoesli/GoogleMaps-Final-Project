import requests
r=[]
def maps(start,destination):                                #https://www.youtube.com/watch?v=yOXQAmYl0Aw&list=PL9PKTtrudOHZTFdodlKzWvJqJBqg77tWF&index=2
    key="Enter your Google API-key"
    url="https://maps.googleapis.com/maps/api/distancematrix/json?"
    r=requests.get(url+"origins="+start+"&destinations="+destination+"&key="+key)
    time=r.json()["rows"][0]["elements"][0]["duration"]["text"]
    return time
def distance(start,destination):                                #https://www.youtube.com/watch?v=yOXQAmYl0Aw&list=PL9PKTtrudOHZTFdodlKzWvJqJBqg77tWF&index=2
    key="Enter your Google API-key"
    url="https://maps.googleapis.com/maps/api/distancematrix/json?"
    r=requests.get(url+"origins="+start+"&destinations="+destination+"&key="+key)
    dist=r.json()["rows"][0]["elements"][0]["distance"]["value"]
    return dist

def dist(route,curr):
  total = 0
  total += int(distance(curr, route[0]))
  if len(route) > 1:
    for i in range(len(route) - 1):
      total += int(distance(route[i], route[i + 1]))
  km = 0
  m =0
  if total > 999:
    km += total // 1000
    m += total % 1000
  else:
    m += total
  return ("Distance=" + str(km) + "." + str(m) + "km")

def home(route,start):
  out=""
  out+=(route[-1]+"-->"+start)+"\n"
  out+=("Duration: "+maps(route[-1],start))
  return out


def destinations(start,desti):
    curr=start
    route=[]
    destinations=desti
  
    total=0
    shortest = 0
    dest1=destinations[0]
    first = maps(curr, destinations[0]).split()
    if "day" in first:
      shortest+=(int(first[0])*24*60)
      shortest+=int(first[2]) * 60
    elif len(first) == 4:                                 #get time of starting point to first destination to compare to others
        shortest += int(first[0]) * 60
        shortest += int(first[2])
    else:
        shortest += int(first[0])

    for el in destinations:                             # get nearest destination from starting point
        data= maps(curr,el).split()
        if "day" in data:
          shortest = (int(first[2]) * 60)+(int(first[0])*24*60)
        elif len(data)==4:
            if (int(data[0])*60 + int(data[2]))<shortest:
                shortest=(int(data[0])*60 + int(data[2]))
                dest1=el
        else:
            if int(data[0])<shortest:
                shortest=int(data[0])
                dest1=el

    route.append(dest1)
    total+=shortest
    destinations.remove(dest1)
    location=dest1
    while destinations!=[]:                             # get nearest point of every destination remaining in destinations list
        quickest=0
        dest=""
        data=maps(location,destinations[0]).split()
        if len(data)==4:
            quickest=(int(data[0])*60 + int(data[2]))
            dest=destinations[0]
        else:
            quickest=int(data[0])
            dest=destinations[0]
        for el in destinations[1:]:
            data=maps(location,el).split()
            if len(data) == 4:
                if (int(data[0]) * 60 + int(data[2])) < quickest:
                    quickest = (int(data[0]) * 60 + int(data[2]))
                    dest = el
            else:
                if int(data[0]) < quickest:
                    quickest = int(data[0])
                    dest = el
        total+=quickest
        route.append(dest)
        destinations.remove(dest)
        location=dest

    out=curr
    for el in route:                        # Create User output for route
        out+="-->"
        out+=el
    out+="'\n' Duration: "
    if total>59:
        out+=str(total//60)+" Hours "
        out+=str(total%60)+" Minutes"
    else:
        out+=str(total)+" Minutes"
    r=route
    return [out,route]
#https://realpython.com/python-gui-tkinter/#getting-user-input-with-entry-widgets
#https://www.youtube.com/watch?v=H3Cjtm6NuaQ
#https://www.python-kurs.eu/tkinter_entry_widgets.php
from tkinter import *

def enter4(r,s):
  out=dist(r,s)
  Label(root,text=out).grid(row=10,column=4)
  return

def enter3(r,s):
  out=home(r,s)
  Label(root,text=out).grid(row=9,column=4)
  return

def enter2(d):
  s=start.get()
  desti=[]
  for el in d:
    if str(el.get())!="":
      desti.append(str(el.get()))
  out=destinations(s,desti) #Getting output from Maps_API.py
  Label(root,text=out[0]).grid(row=7,column=4)
  Label(root,text="Get time to return home? Get Total Distance:").grid(row=8,column=4)
  Button(root, text='Time Home', command=lambda: enter3(out[1],s)).grid(row=8, column=3, sticky=W, pady=4)
  Button(root, text='Total Distance', command=lambda: enter4(out[1],s)).grid(row=8, column=5, sticky=W, pady=4)
  return

def enter1():
  Label(root,text="Please enter all the destinations you would like to reach (up to 6):").grid(row=3,column=4)
  i1 = StringVar(root)
  i2 = StringVar(root)
  i3 = StringVar(root)
  i4 = StringVar(root)
  i5 = StringVar(root)
  i6 = StringVar(root)
  d1=Entry(root,textvariable=i1,width=10)
  d1.grid(row=4,column=3,pady=4,padx=5)
  d2=Entry(root,textvariable=i2,width=10)
  d2.grid(row=4,column=4,pady=4,padx=5)
  d3=Entry(root,textvariable=i3,width=10)
  d3.grid(row=4,column=5,pady=4,padx=5)
  d4=Entry(root,textvariable=i4,width=10)
  d4.grid(row=5,column=3,pady=4,padx=5)
  d5=Entry(root,textvariable=i5,width=10)
  d5.grid(row=5,column=4,pady=4,padx=5)
  d6=Entry(root,textvariable=i6,width=10)
  d6.grid(row=5,column=5,pady=4,padx=5)

  dest=[d1,d2,d3,d4,d5,d6]

  Button(root, text='Enter', command=lambda: enter2(dest)).grid(row=6, column=5, sticky=W, pady=4)
  return

root = Tk()
root.geometry("700x900")
root.title("Google Maps Multiple Locations")
Label(root,text="This is a tool to find the fastest route to reach all your destinations!\n").grid(row=0,column=4)
Label(root,text="Please enter your starting location(City)").grid(row=1,column=4)


user_input = StringVar(root)
start=Entry(root,textvariable=user_input)
start.grid(row=2,column=4)
Button(root, text='Enter', command=lambda: enter1()).grid(row=2, column=5, sticky=W, pady=4)



root.mainloop()
