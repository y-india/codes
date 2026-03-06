# ####################################################
# NUMBER GAME 
# ####################################################

import random
import pandas as pd 
import os
import csv
import datetime 


####### ONLY TODAY DATE ###########
from datetime import date 

today = date.today()
# print(today)

########Time ###########
# print(current_time)

current_time = datetime.datetime.now().time()

# # in pm or am 
# current_time = 

# current_time = "7 Baj Ge"


# datetime.time.hour
GAME_DATA = r"C:\Users\User\OneDrive\Desktop\time pass code\game_data.csv"






number = random.randint(0,100)


# print(number)

game_data = pd.DataFrame(pd.read_csv(r"C:\Users\User\OneDrive\Desktop\time pass code\game_data.csv"))
# print(game_data)



name = input("Enter Your Name : ")
try_ = 0

while True :
    user = int(input("Enter Your Number in Range 1 to 100 " \
    ": ")) 
    try_ += 1

    if user > number :
        print("Smaller")


    elif user < number :
        print("Greater")


    elif user == number :
        print("Correct !")
        print(f"You Won in {try_} trys")

        df_new = pd.DataFrame( [
    { "Game_Date" : today , "Time" : current_time  , "Trys" : try_ , "Name" : name }
])


        df_new.to_csv(GAME_DATA , mode = "a" , header=False , index = False )
        break

    
        
    else :
        print("BAD")
    


# df_new = pd.DataFrame( [

#     { "Game_Date" : 3 , "Time" : 5  , "Trys" : 3 , "Name" : 3 }
# ])


# df_new.to_csv(GAME_DATA , mode = "a" , header=False , index = False )

        




