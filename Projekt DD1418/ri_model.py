import os
import numpy as np
import random
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import confusion_matrix



class ClassifyNumerics(object):


    def __init__(self,dimension = 1000, non_zero=50,non_zero_values=list([-1,1]),left_window_size=3,right_window_size=3):
        self.__vocab = set()
        self.__dim = dimension
        self.__non_zero = non_zero
        self.__non_zero_values = non_zero_values
        self.__lws = left_window_size
        self.__rws = right_window_size
        self.__cv = None
        self.__rv = None
        self.__cv_vocab = []
        self.__class_converter = {1:"Ålder",2:"Avstånd",3:"Datum/Årtal",4:"Tid",6:"Pengar",7:"Övrigt"}

    ## @brief En funktion som rensar data på "punctuations"
    ##
    ##        Rensar alla punctuations och separerar ord med mellanslag    
    ##        Om ex. bindestreck eller mellanslag kommer mitt i ett numeriskt uttryck så skapas en dict av det numeriska uttrycket 

    def clean_line(self,line):

        new_line = ''
        i = 0
        while i < (len(line)):
            cursor = line[i]
            if i+1 < len(line):
                nextword = line[i+1]
            else:
                nextword = None
            tempstr = ''
            if cursor.isnumeric():

                while cursor.isnumeric() or nextword.isnumeric():
                    if self.ascii_ok(cursor):
                        tempstr += cursor
 
                    i += 1
                    cursor = nextword
                    if i+1 < len(line):
                        nextword = line[i+1]
                    else:
                        nextword = "a"
                new_line += tempstr
            elif cursor == '[':
                while cursor.isnumeric() or cursor == '[' or cursor == ']':
                    i += 1
                    cursor = nextword
                    if i+1 < len(line):
                        nextword = line[i+1]
                    else:
                        nextword = "a"
            else:
                if cursor.isalpha():
                    new_line += cursor
                else:
                    new_line += ' '
                i +=1        
            
        new_line_list = new_line.split()

        for i in range(len(new_line_list)):
            word = new_line_list[i]
            tempdict = {}
            for j in word:
                if j.isnumeric():
                    tempdict["Value"] = word
                    tempdict["Label"] = "Numerical"
                    new_line_list[i] = tempdict
                break

        return new_line_list
                    
    def clean_input(self,line):
        new_line = ''
        i = 0
        while i < (len(line)):
            cursor = line[i]
            if i+1 < len(line):
                nextword = line[i+1]
            else:
                nextword = "a"
            tempstr = ''
            if cursor.isnumeric():

                while cursor.isnumeric() or nextword.isnumeric():
                    if self.ascii_ok(cursor):
                        tempstr += cursor
 
                    i += 1
                    cursor = nextword
                    if i+1 < len(line):
                        nextword = line[i+1]
                    else:
                        nextword = "a"
                new_line += tempstr
            elif cursor == '[':
                while cursor.isnumeric() or cursor == '[' or cursor == ']':
                    i += 1
                    cursor = nextword
                    if i+1 < len(line):
                        nextword = line[i+1]
                    else:
                        nextword = "a"
            else:
                if cursor.isalpha():
                    new_line += cursor
                else:
                    new_line += ' '
                i +=1        
            
        new_line_list = new_line.split()

        return new_line_list

    def ascii_ok(self,char):
        ascii_list = [48,49,50,51,52,53,54,55,56,57,46,45,58,44,47,8211]
        for i in ascii_list:
            if ord(char) == i:
                return True

        return False

    def classify_datapoints(self):
        with open('classified_data.txt','a') as f:
            for templine in tuple(self.text_gen()):
                i = 0
                for tempword in templine:
                    if type(tempword) != dict:
                        string = tempword + ' '
                        f.write(string)
                    else:
                        if i == 0:
                            print("LINE ÄR: \n",templine)
                            print("\n1-ålder, 2-avstånd, 3-datum, 4-tid, 5-antal, 6-pengar, 7-övrigt, 8-skip")

                        newclass = input("Skriv in en siffra motsvarande den klass som siffran har:\n")
                        tempword["Label"] = newclass
                        i += 1
                        string = "N-" + tempword["Value"] + "-" + tempword["Label"] + ' '
                        f.write(string)
                f.write("\n")
        
        return

    # vi vill läsa in texterna från filen med klassade numeriska uttryck och skapa ett set av alla ord
    def build_vocab(self):
        with open("classified_data.txt",'r') as file:
            
            for templine in file:
                templine_list = templine.split()
                for tempword in templine_list:
                    
                    if tempword[0] == "N" and tempword[1] == '-':
                        self.__vocab.add("<number>")

                    # om typen är dictionary så skiter vi i den
                    # annars lägg till ordet i set
                    else:
                        self.__vocab.add(tempword)

        self.write_vocabulary()


    def write_vocabulary(self):
        with open('vocab.txt', 'w') as f:
            for w in self.__vocab:
                f.write('{}\n'.format(w))


    def text_gen(self):
        fname = "data/Elon_Musk.txt"
                        
        with open(fname, encoding='utf8', errors='ignore') as f:
            for line in f:
                yield self.clean_line(line)

    def create_word_vectors(self):
        # initialize random vector 
        self.__rv = {}

        # skapa lista av alla index [0, 1, 2, ..., self.__dim - 1]
        # för att slumpa senare
        sample_list = []
        for i in range(self.__dim):
            sample_list.append(i)

        # random vector för varje ord i vocabulary
        for word in list(self.__vocab):
            #initierar random vector för varje ord, storlek: self.dim
            self.__rv[word] = np.zeros(self.__dim)
            
            # slumpar platser där -1 eller 1 ska sättas in
            random_indexes = random.sample(sample_list, self.__non_zero)

            # nu slumpas -1 eller 1 för varje plats
            for index in random_indexes:
                self.__rv[word][index] = random.choice(self.__non_zero_values)


        with open('classified_data.txt','r') as f:
            # loopa igenom var rad för sig, från texterna som träningen ska ske på:
            for line in f:
                linelist = line.split()
                
                # loopa igenom varje ord i varje line
                for cursor in range(len(linelist)):
                    
                    # cursor är indexet för varje element och file_item är det faktiska ordet
                    file_item = linelist[cursor]
                    
                    # om vi hittar ett numeriskt uttryck så ska vi skapa en kontextvektor för den och märk den med dess label
                    if file_item[0] == "N" and file_item[1] == "-":
                        
                        # hämta label för siffran
                        file_item_list = file_item.split("-")
                        
                        #Om N-###-8 så ska vi inte klassificera
                        if file_item[2] != 8:
                            label = int(file_item_list[len(file_item_list)-1])
                            
                            # skapar lista med grannarnas index
                            nbrs_index = []
                            # vi vill hämta alla index som är "ett steg bak till lws steg bak" från cursor.
                            # MEN vi måste ta hänsyn till att det inte alltid finns ord "lws steg bakåt"

                            for i in range(1, self.__lws+1):
                                if cursor-i >= 0:
                                    nbrs_index.append(cursor-i)
                            for i in range(1, self.__rws+1):
                                if cursor+i < len(linelist):
                                    nbrs_index.append(cursor+i)
                            
                            # skapar temporär variabel där context vectorn byggs upp
                            diff_vector = np.zeros(self.__dim)
                            for nbr_index in nbrs_index:
                                if linelist[nbr_index][0] == "N" and linelist[nbr_index][1] == "-":
                                    diff_vector += self.__rv["<number>"]
                                else: 
                                    diff_vector += self.__rv[str(linelist[nbr_index])]
                            
                            # lägg till context värdet i context vektorn för ordet
                            item = {"CV":diff_vector, "Label":label}
                            self.__cv_vocab.append(item)
    
        
    def find_class(self,sentence,k=15):
        
        # städa sentence 
        sentence_list = self.clean_input(sentence)

        # initiera 
        X = []
        label_of_cvs = []

        for dict in self.__cv_vocab:
            X.append(dict["CV"])
            label_of_cvs.append(dict["Label"])

        nbrs = NearestNeighbors(metric='cosine')
        # laddar in X
        nbrs.fit(X)
        
        
        return_list = []
        for cursor in range(len(sentence_list)):
            
            item = sentence_list[cursor]
            if item[0].isnumeric():

                nbrs_index = []

                for i in range(1, self.__lws+1):
                    if cursor-i >= 0:
                        nbrs_index.append(cursor-i)
                for i in range(1, self.__rws+1):
                    if cursor+i < len(sentence_list):
                        nbrs_index.append(cursor+i)

                temp_cv = np.zeros(self.__dim)


                for nbr in nbrs_index:
                    

                    if sentence_list[nbr][0].isnumeric():
                        temp_cv += self.__rv["<number>"]

                    elif sentence_list[nbr] not in self.__vocab: 
                        None
                    
                    elif sentence_list[nbr] in self.__vocab:
                        temp_cv += self.__rv[sentence_list[nbr]]

                neighbours_info = nbrs.kneighbors([temp_cv], k)
                
                neighbours_index = neighbours_info[1][0]
                temp_counter = [0,0,0,0,0,0,0,0]

                
                
                for i in neighbours_index:
                    idx = label_of_cvs[i]
                    temp_counter[idx-1] += 1
                
                
                max_value = max(temp_counter)
     

                most_probable_class = self.__class_converter[temp_counter.index(max_value)+1]
                return_list.append(most_probable_class)
                
        print(return_list)
          

if __name__ == "__main__":
    
    cn = ClassifyNumerics()
    
    # om vi redan har klassifierat datapunkter vill vi inte göra det igen
    #cn.classify_datapoints()
        
    
    cn.build_vocab()
    print("------------------VOKABULÄR ÄR BYGGT------------------\n\n\n")
    
    # när vi klassifierat datapunkter och byggt vokabulär vill vi skapa ordvektorerna
    cn.create_word_vectors()
            
    

    sentence = input("\nSkriv in en mening där du vill klassificera ett uttryck: (exit för att avsluta)\n")
    while sentence != "exit":
        cn.find_class(sentence)
        sentence = input("\nVill du testa en mening till? (exit för att avsluta)\n")

