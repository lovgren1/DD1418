qty = [0,0,0,0,0,0,0,0]

with open('classified_data.txt','r') as f:
    for line in f:
        linelist = line.split()

        for cursor in range(len(linelist)):

            file_item = linelist[cursor]
            if file_item[0] == "N" and file_item[1] == "-":
                file_item_list = file_item.split("-")
                
                label = int(file_item_list[len(file_item_list)-1])
                qty[label-1] += 1


print("ANTAL DATAPUNKTER KLASSIFICERADE:\n")
j = 1
sum = 0
for i in range(len(qty)):
    if i != 8:

        sum += qty[i]    

for i in qty:
    print("av ",j, " finns det ",i," st ")

    j += 1
print("\nSUMMA: ",sum,"\n")