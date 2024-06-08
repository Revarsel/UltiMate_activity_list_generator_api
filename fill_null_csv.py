# add "null" to the empty places in csv (NOT WORKING)
data = []
with open("table.csv", 'r+') as file:
    temp = file.read()

for i in temp:
    i.strip()
    data.append(i)

# index = 0
# for _ in range(10):
#     data.insert(index, "null")
#     print(data)
#     index += 2

index_arr = []
index = 0
for k in range(len(data)):
    if index >= len(data)-1: # check for end of file
        if data[index] == ';':
            data += "0"
        break

    if data[index] == ';' and data[index+1] == ';':
        index_arr.append(index+1)
        #print(data[index] + "done")
    
    index += 1

index = 0
for i in index_arr:
    data.insert(i + index, "null")
    index += 1

data_str = ""
for k in data:
    data_str += k


with open('table1.csv', 'w+') as file:
    file.write(data_str)
        

