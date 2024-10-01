import csv

# file_data = []

# with open("otherpythonstuff/Only_Activity_Database_Entry_file1.csv", "r") as file: # act to associated
#     data = csv.reader(file, delimiter=',')
#     count = 0
#     for i in data:
#         if count == 0:
#             count += 1
#             continue
#         local = []
#         local.append(i[0])
#         i = i[1:5]
#         for k in i:
#             if k != "None":
#                 local.append(k)
#         file_data.append(local)


# with open("otherpythonstuff/Only_Activity_Database_Entry_file1.csv", "r") as file: # act to standard
#     data = csv.DictReader(file, delimiter=',')
#     for i in data:
#         local = []
#         local.append(i["Act_id"])
#         keys = list(i.keys())
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(0)
#         keys = keys[0:12]
#         for k in keys:
#             if i[k] != "None":
#                 local.append(k)
#         file_data.append(local)

# file_data_question = []
# file_data_options = []
# file_data_activity_question = []

# with open("otherpythonstuff/Only_Activity_Database_Entry_file1.csv", "r") as file: # question and option
#     data = csv.DictReader(file, delimiter=',')
#     question_id = 0
#     question_option_id = 0
#     for i in data:
#         local_question = [question_id]
#         keys = list(i.keys())
#         act_id = i[keys[0]]
#         local_act_to_question = []
#         keys_1 = keys[18:24] # Feedback question 1 [18:24]
#         keys_2 = keys[24:30] # Feedback question 2 [24:30]
#         keys_3 = keys[30:32] # Feedback question 3 [30:32]

#         response = i[keys_1[1]]
#         local_question.append(i[keys_1[0]])
#         local_question.append(response)
#         if i[keys_1[1]] in ["Checkbox"]:
#             local_question.append(True)
#         else:
#             local_question.append(False)
#         local_question.append(None)
#         local_question.append(None)
#         local_question.append(False)

#         local_act_to_question.append(question_id)
#         local_act_to_question.append(question_id)
#         local_act_to_question.append(act_id)
#         file_data_activity_question.append(local_act_to_question.copy())
#         local_act_to_question = []
        
#         file_data_question.append(local_question.copy())

#         for k in range(4):
#             option = i[keys_1[k+2]]
#             local_option = [question_option_id, question_id]
#             if option != "None":
#                 if i[keys_1[1]] in ["Radio Button", "Checkbox"]:
#                     local_option.append(option)
#                     local_option.append("Null")
#                     file_data_options.append(local_option.copy())
#                     local_option = []
#                     question_option_id += 1

#         question_id += 1

#         local_question = [question_id]
#         response1 = i[keys_2[1]]
#         local_question.append(i[keys_2[0]])
#         local_question.append(response1)
#         if i[keys_2[1]] in ["Checkbox"]:
#             local_question.append(True)
#         else:
#             local_question.append(False)
#         local_question.append(None)
#         local_question.append(None)
#         local_question.append(False)

#         local_act_to_question.append(question_id)
#         local_act_to_question.append(question_id)
#         local_act_to_question.append(act_id)
#         file_data_activity_question.append(local_act_to_question.copy())
#         local_act_to_question = []

#         file_data_question.append(local_question.copy())

#         for k in range(4):
#             option = i[keys_2[k+2]]
#             local_option = [question_option_id, question_id]
#             if option != "None":
#                 if i[keys_2[1]] in ["Radio Button", "Checkbox"]:
#                     local_option.append(option)
#                     local_option.append("Null")
#                     file_data_options.append(local_option.copy())
#                     local_option = []
#                     question_option_id += 1
    
#         question_id += 1

#         if i[keys_3[0]] != "None":
#             local_question = [question_id]
#             response1 = i[keys_3[1]]
#             local_question.append(i[keys_3[0]])
#             local_question.append(response1)
#             if i[keys_3[1]] in ["Checkbox"]:
#                 local_question.append(True)
#             else:
#                 local_question.append(False)
#             local_question.append(None)
#             local_question.append(None)
#             local_question.append(False)

#             local_act_to_question.append(question_id)
#             local_act_to_question.append(question_id)
#             local_act_to_question.append(act_id)
#             file_data_activity_question.append(local_act_to_question.copy())
#             local_act_to_question = []

#             file_data_question.append(local_question.copy())

#             question_id += 1

# file_data_question_option_id = []
# with open("otherpythonstuff/act_to_feedback_question_duplicate_removed.csv", "r") as file: # activity question
#     data = csv.DictReader(file)
#     question_option_id = 0
#     for i in data:
#         keys = list(i.keys())
#         question_id = i[keys[0]]
#         local = [question_option_id, question_id]
#         keys_1 = keys[3:]
#         if i[keys[2]] != "Text Box": 
#             for k in keys_1:
#                 if i[k] not in ["None", None]:
#                     local.append(i[k])
#                     file_data_question_option_id.append(local.copy())
#                     question_option_id += 1
#                     local = [question_option_id, question_id]

file_data_act_question_sequence_map = []
with open("otherpythonstuff/Only_Activity_Database_Entry_file(Batch_1_Activity_question).csv", "r") as file: # Act_id, question 1-3 given as col headers convert to act_id_question_id_sequence no.
    data = csv.DictReader(file)
    for i in data:
        keys = list(i.keys())
        local = []
        seq_no = 1
        for k in keys[1:]:
            if i[k] == "None":
                continue
            local.append(i[keys[0]])
            local.append(i[k])
            local.append(seq_no)
            file_data_act_question_sequence_map.append(local.copy())
            seq_no += 1
            local=[]


# print(file_data_question[0])
# print(file_data_options[0])
# print(file_data_options[1])

# string = ""
# for i in file_data: # associated and std (one by one)
#     act_id = i[0]
#     # string += str(i[0])
#     for k in i[1:]:
#         string = string + act_id + "," + str(k) + "\n"

# print(string)

# string1 = ""
# for i in file_data_question: # question
#     # act_id = i[0]
#     string1 += str(i[0])
#     for k in i[1:]:
#         string1 = string1 + "," + str(k)
#     string1 += "\n"

# string2 = ""
# for i in file_data_options: # option
#     # act_id = i[0]
#     string2 += str(i[0])
#     for k in i[1:]:
#         string2 = string2 + "," + str(k)
#     string2 += "\n"

# string3 = ""
# for i in file_data_activity_question: # question
#     # act_id = i[0]
#     string3 += str(i[0])
#     for k in i[1:]:
#         string3 = string3 + "," + str(k)
#     string3 += "\n"

# string4 = ""
# for i in file_data_question_option_id: # option_id
#     # act_id = i[0]
#     string4 += str(i[0])
#     for k in i[1:]:
#         string4 = string4 + "," + str(k)
#     string4 += "\n"

string5 = ""
for i in file_data_act_question_sequence_map: # act_question_sequence_map
    # act_id = i[0]
    string5 += str(i[0])
    for k in i[1:]:
        string5 = string5 + "," + str(k)
    string5 += "\n"

# print(string5)
# print(string2)
# with open("otherpythonstuff/act_to_feedback_question.csv", "w") as file1: # question
#     file1.write(string1)

# with open("otherpythonstuff/act_to_feedback_option.csv", "w") as file2: # option
#     file2.write(string2)

# with open("otherpythonstuff/act_to_question.csv", "w") as file5: # question_option
#     file5.write(string3)

# with open("otherpythonstuff/act_to_question_option.csv", "w") as file6: # question_option duplicate removed
#     file6.write(string4)

# with open("otherpythonstuff/act_to_associated.csv", "w") as file3: # associated
#     file3.write(string)

# with open("otherpythonstuff/act_to_std.csv", "w") as file4: # std
#     file4.write(string)

with open("otherpythonstuff/act_question_sequence_map.csv", "w") as file7: # act_question_sequence_map
    file7.write(string5)