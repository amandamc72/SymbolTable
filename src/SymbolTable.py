'''Amanda McCarty
   COSC 341 Winter 2015
   Python Project Part 1
   This Python project builds a symbol table 
   from an arbitrary LC3 assembler program
   includes a SymbolTable class with functions 
   to insert, retrieve, and pretty print'''
   
class SymbolTable: 
    
    #constructor  
    def __init__(self, table): 
        self.table = {}
          
    #insert label in symbol table
    def insert(self, chunks, locationCounter):
        if chunks.startswith(' ') or chunks.startswith('\t'): #check if valid label
            lable = False
        else:
            lable = True
        if lable == True: #if valid split string and insert
            words = chunks.split()
            self.table[words[0]] = locationCounter           
            
    #retrieve address of desired label
    def retrieve(self):
        k = True
        while(k):
            label = input("Enter label name (case sensitive): ") #prompt for label input
            for key, value in self.table.items(): #search for label
                if label in key:
                    print("The address is " + value + "\n") #display address
                    break
            choice = input("Enter another? y/n ") #continue until user quits
            if choice.lower() in ['n']:
                k = False
        print("Goodbye!")
                
    #print table neatly    
    def prettyPrint(self):
        forOrder = sorted(self.table.items(), key=lambda x: x[1]) #sort by order of inserted
        print("Building list...........\n")
        print("     Symbol: Address")
        print(" -----------------------")
        for i in forOrder:  #iterate and print
            print("     " + i[0] + ":", i[1])
            print(" -----------------------")
#////////End SymbolTable Class///////

#construct dictionary
myTable = SymbolTable({})

#read program
file = input("Enter the file name: ")
with open(file) as codefile:
    code = codefile.read()
            
#Find starting address
for line in code.splitlines(): 
        if '.ORIG' in line: #find .ORIG statement
            words = line.split()
            hexNum = words[1]
            start = hexNum[1:] #store .ORIG address
            break     

# processing the lines
locationCounter = int(start, 16) - 1 #set .ORIG address to location counter
for line in code.splitlines():       
    if line and not line.isspace(): #only check non empty lines
            if line.startswith(';'): #do not increment LC if commented line
                locationCounter = locationCounter
                        
            elif '.BLKW' in line: #increment for.BLKW
                words = line.split() #split string into list
                blkwIncrement = int(words[2]) #set increment
                myTable.insert(line, hex(locationCounter)) #call insert to table
                locationCounter += blkwIncrement
                        
            elif '.STRINGZ' in line: #increment for .STRINGZ
                words = line.split() #split string into list
                stringWords = ' '.join(words[2:]).strip('"').strip("'") #strip '' or "" from words
                stringzIncrement = 0
                for letters in stringWords: #count letters
                    stringzIncrement += 1
                myTable.insert(line, hex(locationCounter)) #call insert to table
                locationCounter += stringzIncrement + 1 #increment by letter count and null terminator
                        
            else:
                myTable.insert(line, hex(locationCounter)) #call insert to table
                locationCounter += 1
        
myTable.prettyPrint() 
 
choice = input("Would you like to retrieve label addresses? y/n ")
if choice.lower() in ['y']:
    myTable.retrieve()      
else:
    print("Goodbye!")