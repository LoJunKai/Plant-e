# DW-Plant-e

## Naming convention

main.py - contains the main code

Upload all your other code into this repo. Filename should represent the functions in that file (eg. firebase functions would be in a file named firebase.py)

main.py would then import all the functions as from firebase import *

Stuff that you don't want it to be run when you import the module (testing code etc.), please place it into this
```
if __name__ == '__main__':
    # Code here won't be run when you import the file.
```

All the variables used in the function should be initialised in the function or passed as parameters

Bad examples:
```
# Eg. 1
# plant is a variable that is used in other functions too
# This confuses the reader on what variables does the function uses
plant = 0 

def get_moisture_level():
    # Get the moisture sensor data for the plant
    return moisture(plant) # Plant is used in the function

# Eg. 2

# a is instantiated outside of function
# But a is used only inside the function and nowhere else
a = 0

def get_list_of_a():
    b = []
    while a<10:
        b.append(a)
        a += 1
    return b
    
...
# a is not referenced anymore and is only used in the function
```  

Preferred way:
```
# Eg. 1
plant = 0

# Any variables used in the function is passed into the function as parameters, and not just used sliently
def get_moisture_level(plant): 
    # Get the moisture sensor data for the plant
    return moisture(plant) # Plant is used in the function
   
Eg. 2
# Since a is not used anywhere else, it shall be instantiated inside the function
def get_list_of_a():
    a = 0
    b = []
    while a<10:
        b.append(a)
        a += 1
    return b
    
Eg. 3
def populate_list(a, b)
    for i in range(b):
        a.append(i)
    
    return a

a = [9,4,2,5]
populated_list = populate_list(a, 3)
print(populated_list) #[9,4,2,5, 0, 1, 2]
```

Function names should be representative of what the function does
```
# It is good to add get in front if you are retrieving data
# Set when you setting data
def get_moisture_level(plant):
    # Get the moisture sensor data
    
# Rather than:
def moisture(plant):
    # Get the moisture sensor data
    
# Or not even representative of what it does:
def water_plant():
    # Get the moisture sensor data
```



## Whitespaces and Documentation

Do leave spaces before and after = and ==
```
a = b

while a == b:
    a += b
```
Math calculations and operations, leave a space only when needed to divide the expression
```
a = 12*34**2 / 45*343
```

Leave a line before and after a code block.
Outer most functions are separated with 2 line breaks.
```
def foo():
    a = 0
    b = 0
    c = 0
    
    if a == b: # Leave a line before the code block
        print(a)
        print(b) # Leave a line after the code block
        
    a = b+c
    b = a+c
    return a,b # Code on the same indentation level do need to leave a line, unles you want to separate the code (transiting to a different purpose, etc.)
    

def bar(): # 2 line spaces to separate functions with on indentation level 0
    # Next function

```
