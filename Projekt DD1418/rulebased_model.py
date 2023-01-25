from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import random




"""
om : eller timmar, sekunder, minuter, dagar,månader kommer efter, tid
om SLUT = kr/mkr/kronor/miljarder, pengar
om / eller - eller 4 siffror och börjar på 17/18/19/20, datum
om 20XX/19XX/18XX om siffra förekommer med e efter, datum
om "talet" kommer efter siffran, datum
om år kommer efter, ålder
om km, kilometer, meter, m, cm , mm kommer efter, avstånd
om t.ex. procent,stycken,kg osv kommer efter, övrigt
"""

def check_if_date(word):
    if word in ["januari","februari","mars","april","maj","juni","juli","augusti","september","oktober","november","december","talet"]:
        return True

    return False

def check_if_distance(word):
    if word in ["km","kilometer","meter","m","cm","centimeter","mm","millimeter"]:
        return True
    
    return False

def check_if_money(word):
    if word in ["kr","kronor","mkr","dollar","miljarder","miljoner","euro"]:
        return True
        
    return False

def check_if_age(word):
    if word in ["år"]:
        return True

    return False

def check_if_time(word):
    if word in ["timmar", "h", "sekunder", "s", "minuter", "dagar", "månader"]:
        return True
    return False

def check_char_in_expr(express):
    char_yesno = [0,0,0]
    # 1 is "/"
    # 2 is ":"
    # 3 is "-"
    for i in express:
        if i == '/':
            char_yesno[0] += 1
        
        if i == ":":
            char_yesno[1] += 1
        
        if i == "-":
            char_yesno[2] += 1
        
    return char_yesno 
    

def find_class(sentence):
    correct_class_label = []
    guess_class_label = []
    
    i = 0
    sentence_list = sentence.split()
    for item in sentence_list:
        item_scoreboard = [0,0,0,0,0,0,0]
        # vi tar ut de numeriska uttrycken
        if item[0] == "N" and item[1] == "-":
            char = item[2:len(item)-2]
            correct_class_label.append(int(item[len(item)-1]))
            char_score = check_char_in_expr(char)
            print(char_score)
            # datum, "24/12-2023"
            if char_score[0] == 1 and char_score[2] == 1:
                item_scoreboard[2] += 1
            
            # datum, till exempel 2023-12-24
            if char_score[2] == 2:
                item_scoreboard[2] += 1

            # tid, till exempel 13:37 eller 2:01:34 
            if char_score[1] > 0 and char_score[0]+char_score[2] == 0:
                item_scoreboard[3] += 1
                
            # datum, t.ex. 2021 eller 1849    
            if len(char) == 4:
                if char[0:1] in [20,19,18,17,16,15,14,13]:
                    item_scoreboard[2] += 1


            if i+1 < len(sentence_list):
                next_word = sentence_list[i+1]
                if check_if_time(next_word):
                    item_scoreboard[3] += 1
                        
                if check_if_date(next_word):
                    item_scoreboard[2] += 1

                if check_if_age(next_word):
                    item_scoreboard[0] += 1

                if check_if_money(next_word):
                    item_scoreboard[5] += 1
                    
                if check_if_distance(next_word):
                    item_scoreboard[1] += 1
                
            if all(i == 0 for i in item_scoreboard):
                item_scoreboard[len(item_scoreboard)-1] = 1

            j = max(item_scoreboard)
            best_guesses = []
            print(item_scoreboard)
            for k in range(len(item_scoreboard)):
                if item_scoreboard[k] == j:
                    best_guesses.append(k)

            best_class_list = random.sample(best_guesses,1)
            best_class = int(best_class_list[0])+1
            guess_class_label.append(best_class)    
                    
        i += 1

    return guess_class_label,correct_class_label
       

if __name__ == "__main__":
    no_of_testlines = 100
    
    # slumpa index, måste ha längden på filen
    with open('classified_data.txt','r') as f:
        i = 0
        file_indexes = []
        for line in f:
            file_indexes.append(i)
            i += 1
    
    # denna kan köras om "no_of_testlines" stycken slumpade lines i datasetet ska plockas ut som testdata
    #test_indexes = random.sample(file_indexes,no_of_testlines)
    
    # här kan man manuellt skriva in de testdata som körts på evaluate_ri_model.py
    test_indexes = [329, 590, 84, 256, 331, 320, 401, 284, 664, 653, 130, 421, 90, 163, 161, 438, 24, 541, 143, 474, 517, 64, 183, 307, 457, 579, 293, 160, 264, 623, 522, 54, 666, 573, 574, 218, 78, 205, 316, 107, 212, 25, 694, 5, 156, 547, 607, 216, 0, 189, 592, 641, 62, 101, 188, 544, 244, 373, 598, 297, 596, 420, 650, 231, 81, 36, 672, 477, 39, 495, 374, 122, 279, 458, 406, 104, 391, 22, 196, 121, 652, 501, 132, 296, 252, 492, 30, 59, 494, 417, 7, 540, 582, 565, 332, 261, 656, 408, 245, 58]

    correct_class_label = []
    guess_class_label = []
    i = 0
    with open('classified_data.txt','r') as f:
        for line in f:
        
            # om det matchar de indexen vi vill testa
            if i in test_indexes:
                guess, correct = find_class(line)
                for index in range(len(guess)):
                    
                    guess_class_label.append(guess[index])
                    correct_class_label.append(correct[index])
            
            i += 1

    print(confusion_matrix(correct_class_label,guess_class_label))
    print("\n")
    print(classification_report(correct_class_label,guess_class_label))