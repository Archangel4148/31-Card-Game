#31 Card Game Program
#Written by Joshua Santy, 7/6/2022

#This code assumes that the first person to go directly after being dealt cards knocks.
#You can still use this if you want to knock in the first round even if you aren't the first person to go


'''
TO USE THIS CODE:
1. Go to https://www.programiz.com/python-programming/online-compiler/
2. Clear the existing code that's on the left side (where it says main.py)
3. In its place, copy and paste this entire code WITHOUT ALTERING (ctrl+a, ctrl+c, ctrl+v)
4. Press run
5. On the right side of the screen (under Shell), the program will ask you how many players you want (maximum of 13)
6. Press ENTER
7. It will then ask how many games you want to run (the more the better: 1,000 games is a good estimate; 10,000 will be very precise)
8. Press ENTER
9. The program will give you the results of the average score of the other players, and hence what score it is safe to knock on.
10. The program also gives you the 75th and 25th percentiles that you can base your chances of winning on
11. Thanks!
'''


#What this code understands and and its strategy:
'''
This code assumes that if there is any positive point differential available, 
    the player will take it and not risk drawing from the deck for a possibly higher score

This code will drop the lowest card that doesn't contribute to the score, 
    ignoring what suit the next player may need

This code also understands that three of a kind means a score of 30.5
'''

def write_debug(num, suit):
    with open("old_output.txt", "a") as f:
        f.write(f"{num} {suit}\n")



import random, math

def setup1():
    global e, x, v, o
    scores[x] = total
    e = (3*v)
    v += 1
    x += 1

def setup2():
    global e, x, v, o
    scores[x] = total
    e = (3*v)
    v += 1
    o += 1
    x += 1


def drawcard1(): #add 3 of a kind
    #if newcard doesn't match suit with any card:
    global upcardsuit, upcardnum, total
    if (deck[-o - 1][1]) != deck[e][1] and (deck[-o - 1][1]) != deck[e+1][1] and (deck[-o - 1][1]) != deck[e+2][1]:
        total = max(deck[e][0], deck[e+1][0], deck[e+2][0], (deck[-o - 1][0]))
        upcardnum = min(deck[e][0], deck[e+1][0], deck[e+2][0], (deck[-o - 1][0]))
        if upcardnum == deck[e][0]:
            upcardsuit = deck[e][1]
            setup2()
        elif upcardnum == deck[e+1][0]:
            upcardsuit = deck[e+1][1]
            setup2()
        elif upcardnum == deck[e+2][0]:
            upcardsuit = deck[e+2][1]
            setup2()
        else:
            upcardsuit = deck[-o - 1][1]
            setup2()

    #if newcard matches suit with card 1:
    elif (deck[-o - 1][1]) == deck[e][1]:
        #if newcard and card 1 combined aren't max or even:
        if ((deck[-o - 1][0]) + deck[e][0]) <= max(deck[e+1][0], deck[e+2][0]):
            total = max(deck[e+1][0], deck[e+2][0])
            upcardnum = min(deck[e+1][0], deck[e+2][0],(deck[-o - 1][0]), deck[e][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            elif upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o-1][1]
                setup2()

        #if newcard and card 1 combined are max:
        else:
            total = (deck[-o - 1][0]) + (deck[e][0])
            upcardnum = min(deck[e+1][0], deck[e+2][0])
            if upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            else:
                upcardsuit = deck[e+2][1]
                setup2()

    #if newcard matches suit with card 2:
    elif (deck[-o - 1][1]) == deck[e+1][1]:
        #if newcard and card 2 combined aren't max or even:
        if ((deck[-o - 1][0]) + deck[e+1][0]) <= max(deck[e][0], deck[e+2][0]):
            total = max(deck[e][0], deck[e+2][0])
            upcardnum = min(deck[e+1][0], deck[e+2][0],(deck[-o - 1][0]), deck[e][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            elif upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o-1][1]
                setup2()
        #if newcard and card 2 combined are max:
        else:
            total = (deck[-o - 1][0]) + (deck[e+1][0])
            upcardnum = min(deck[e][0], deck[e+2][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            else:
                upcardsuit = deck[e+2][1]
                setup2()

    #if newcard matches suit with card 3:
    elif (deck[-o - 1][1]) == deck[e+2][1]:
        #if newcard and card 3 combined aren't max or even:
        if ((deck[-o - 1][0]) + deck[e+2][0]) <= max(deck[e+1][0], deck[e][0]):
            total = max(deck[e+1][0], deck[e][0])
            upcardnum = min(deck[e+1][0], deck[e+2][0],(deck[-o - 1][0]), deck[e][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            elif upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o-1][1]
                setup2()
        #if newcard and card 3 combined are max:
        else:
            total = (deck[-o - 1][0]) + (deck[e+2][0])
            upcardnum = min(deck[e+1][0], deck[e][0])
            if upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            else:
                upcardsuit = deck[e][1]
                setup2()
def drawcard2():
    global upcardsuit, upcardnum, total
    #if newcard shares no suits:
    if deck[-o - 1][1] != deck[e][1] and deck[-o - 1][1] != deck[e+2][1]:
        total = max(deck[-o - 1][0], deck[e][0] + deck[e+1][0], deck[e+2][0])
        if deck[-o - 1][0] ==  min(deck[-o - 1][0], deck[e][0] + deck[e+1][0], deck[e+2][0]):
            upcardnum = deck[-o - 1][0]
            upcardsuit = deck[-o - 1][1]
            setup2()
        elif deck[e+2][0] == min(deck[-o - 1][0], deck[e][0] + deck[e+1][0], deck[e+2][0]):
            upcardnum = deck[e+2][0]
            upcardsuit = deck[e+2][1]
            setup2()
        else:
            if deck[e][0] < deck[e+1][0]:
                upcardnum = deck[e][0]
                upcardsuit = deck[e][1]
                setup2()
            else:
                upcardnum = deck[e+1][0]
                upcardsuit = deck[e+1][1]
                setup2()

    #if newcard shares a suit with the 3rd card:
    elif deck[-o - 1][1] == deck[e+2][1]:
        total = max(deck[-o - 1][0] + deck[e+2][0], deck[e][0] + deck[e+1][0])
        if deck[-o - 1][0] + deck[e+2][0] > deck[e][0] + deck[e+1][0]:
            upcardnum = min(deck[e][0], deck[e+1][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            else:
                upcardsuit = deck[e+1][1]
                setup2()
        elif deck[-o - 1][0] + deck[e+2][0] < deck[e][0] + deck[e+1][0]:
            upcardnum = min(deck[-o - 1][0], deck[e+2][0])
            if upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o - 1][1]
                setup2()
        else:
            upcardnum = min(deck[-o - 1][0], deck[e+2][0], deck[e][0], deck[e+1][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            elif upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o - 1][1]
                setup2()

    #if newcard shares a suit with cards 1 & 2:
    else:
        total = max(deck[-o - 1][0] + deck[e][0] + deck[e+1][0], deck[e+2][0])
        if deck[-o - 1][0] + deck[e][0] + deck[e+1][0] > deck[e+2][0]:
            upcardnum = deck[e+2][0]
            upcardsuit = deck[e+2][1]
            setup2()
        else:
            upcardnum = min(deck[-o - 1][0], deck[e][0], deck[e+1][0])
            if upcardnum == deck[-o - 1][0]:
                upcardsuit = deck[-o - 1][1]
                setup2()
            elif upcardnum == deck[e][0]:
                upcardsuit == deck[e][1]
                setup2()
            else:
                upcardsuit = deck[e+1][1]
                setup2()

def drawcard3():
    global upcardsuit, upcardnum, total
    #if newcard shares no suits:
    if deck[-o - 1][1] != deck[e+1][1] and deck[-o - 1][1] != deck[e+2][1]:
        total = max(deck[-o - 1][0], deck[e][0] + deck[e+2][0], deck[e+1][0])
        if deck[-o - 1][0] ==  min(deck[-o - 1][0], deck[e+2][0] + deck[e][0], deck[e+1][0]):
            upcardnum = deck[-o - 1][0]
            upcardsuit = deck[-o - 1][1]
            setup2()
        elif deck[e+1][0] == min(deck[-o - 1][0], deck[e][0] + deck[e+2][0], deck[e+1][0]):
            upcardnum = deck[e+1][0]
            upcardsuit = deck[e+1][1]
            setup2()
        else:
            if deck[e][0] < deck[e+2][0]:
                upcardnum = deck[e][0]
                upcardsuit = deck[e][1]
                setup2()
            else:
                upcardnum = deck[e+2][0]
                upcardsuit = deck[e+2][1]
                setup2()

    #if newcard shares a suit with the 2nd card:
    elif deck[-o - 1][1] == deck[e+1][1]:
        total = max(deck[-o - 1][0] + deck[e+1][0], deck[e][0] + deck[e+2][0])
        if deck[-o - 1][0] + deck[e+1][0] > deck[e][0] + deck[e+2][0]:
            upcardnum = min(deck[e][0], deck[e+2][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            else:
                upcardsuit = deck[e+2][1]
                setup2()
        elif deck[-o - 1][0] + deck[e+1][0] < deck[e][0] + deck[e+2][0]:
            upcardnum = min(deck[-o - 1][0], deck[e+1][0])
            if upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            else:
                upcardsuit = deck[-o - 1][1]
                setup2()
        else:
            upcardnum = min(deck[-o - 1][0], deck[e+1][0], deck[e][0], deck[e+2][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            elif upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o - 1][1]
                setup2()

    #if newcard shares a suit with cards 1 & 3:
    else:
        total = max(deck[-o - 1][0] + deck[e][0] + deck[e+2][0], deck[e+1][0])
        if deck[-o - 1][0] + deck[e][0] + deck[e+2][0] > deck[e+1][0]:
            upcardnum = deck[e+1][0]
            upcardsuit = deck[e+1][1]
            setup2()
        else:
            upcardnum = min(deck[-o - 1][0], deck[e][0], deck[e+2][0])
            if upcardnum == deck[-o - 1][0]:
                upcardsuit = deck[-o - 1][1]
                setup2()
            elif upcardnum == deck[e][0]:
                upcardsuit == deck[e][1]
                setup2()
            else:
                upcardsuit = deck[e+2][1]
                setup2()

def drawcard4():
    global upcardsuit, upcardnum, total
    #if newcard shares no suits:
    if deck[-o - 1][1] != deck[e][1] and deck[-o - 1][1] != deck[e+2][1]:
        total = max(deck[-o - 1][0], deck[e+1][0] + deck[e+2][0], deck[e][0])
        if deck[-o - 1][0] ==  min(deck[-o - 1][0], deck[e+2][0] + deck[e+1][0], deck[e][0]):
            upcardnum = deck[-o - 1][0]
            upcardsuit = deck[-o - 1][1]
            setup2()
        elif deck[e][0] == min(deck[-o - 1][0], deck[e+1][0] + deck[e+2][0], deck[e][0]):
            upcardnum = deck[e][0]
            upcardsuit = deck[e][1]
            setup2()
        else:
            if deck[e+1][0] < deck[e+2][0]:
                upcardnum = deck[e+1][0]
                upcardsuit = deck[e+1][1]
                setup2()
            else:
                upcardnum = deck[e+2][0]
                upcardsuit = deck[e+2][1]
                setup2()

    #if newcard shares a suit with the 1st card:
    elif deck[-o - 1][1] == deck[e][1]:
        total = max(deck[-o - 1][0] + deck[e][0], deck[e+1][0] + deck[e+2][0])
        if deck[-o - 1][0] + deck[e][0] > deck[e+1][0] + deck[e+2][0]:
            upcardnum = min(deck[e+1][0], deck[e+2][0])
            if upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            else:
                upcardsuit = deck[e+2][1]
                setup2()
        elif deck[-o - 1][0] + deck[e][0] < deck[e+1][0] + deck[e+2][0]:
            upcardnum = min(deck[-o - 1][0], deck[e][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            else:
                upcardsuit = deck[-o - 1][1]
                setup2()
        else:
            upcardnum = min(deck[-o - 1][0], deck[e+1][0], deck[e][0], deck[e+2][0])
            if upcardnum == deck[e][0]:
                upcardsuit = deck[e][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit = deck[e+1][1]
                setup2()
            elif upcardnum == deck[e+2][0]:
                upcardsuit = deck[e+2][1]
                setup2()
            else:
                upcardsuit = deck[-o - 1][1]
                setup2()

    #if newcard shares a suit with cards 2 & 3:
    else:
        total = max(deck[-o - 1][0] + deck[e+1][0] + deck[e+2][0], deck[e][0])
        if deck[-o - 1][0] + deck[e+1][0] + deck[e+2][0] > deck[e][0]:
            upcardnum = deck[e][0]
            upcardsuit = deck[e][1]
            setup2()
        else:
            upcardnum = min(deck[-o - 1][0], deck[e+1][0], deck[e+2][0])
            if upcardnum == deck[-o - 1][0]:
                upcardsuit = deck[-o - 1][1]
                setup2()
            elif upcardnum == deck[e+1][0]:
                upcardsuit == deck[e+1][1]
                setup2()
            else:
                upcardsuit = deck[e+2][1]
                setup2()



num = int(input('Enter number of players: '))
count = 0
iterations = int(input('Enter number of iterations: '))
all_total = 0
total_scores = []
while count < iterations:
    # 1 =  number, 2 = 10, 3 = jack, 4 = queen, 5 = king, 6 = ace
    deck = [(5, 'Club', 1), (10, 'Club', 2), (11, 'Diamond', 6), (10, 'Heart', 2),(6, 'Spade', 1), (3, 'Spade', 1), (10, 'Club', 3), (10, 'Spade', 2), (2, 'Spade', 1),(8, 'Spade', 1), (7, 'Club', 1), (3, 'Heart', 1), (4, 'Spade', 1), (11, 'Club', 6),(5, 'Diamond', 1), (10, 'Heart', 3), (10, 'Diamond', 2), (9, 'Spade', 1), (9, 'Club', 1),(6, 'Heart', 1), (4, 'Heart', 1), (10, 'Diamond', 3), (3, 'Diamond', 1), (6, 'Club', 1),(11, 'Heart', 6), (10, 'Spade', 3), (10, 'Diamond', 4), (10, 'Spade', 4), (5, 'Spade', 1),(7, 'Heart', 1), (6, 'Diamond', 1), (7, 'Diamond', 1), (4, 'Club', 1), (8, 'Heart', 1),(11, 'Spade', 6), (2, 'Club', 1), (3, 'Club', 1), (10, 'Heart', 4), (10, 'Club', 4),(8, 'Club', 1), (2, 'Heart', 1), (9, 'Diamond', 1), (7, 'Spade', 1), (2, 'Diamond', 1),(10, 'Spade', 5), (4, 'Diamond', 1), (10, 'Heart', 5), (9, 'Heart', 1), (8, 'Diamond', 1),(10, 'Club', 5), (5, 'Heart', 1), (10, 'Diamond', 5)]
    random.seed(count)
    deck = random.sample(deck, k=len(deck))
    scores = []

#first draw
    e = 0
    v = 1

    while v <= num:
        total = 0
        #no matching suit:
        if deck[e+1][1] != deck[e+2][1] and deck[e][1] != deck[e+1][1] and deck[e][1] != deck[e+2][1]:
            total = max(deck[e][0], deck[e+1][0], deck[e+2][0])

        #all matching suit:
        elif deck[e+1][1] == deck[e+2][1] and deck[e][1] == deck[e+1][1] and deck[e+1][1] == deck[e+2][1]:
            total = deck[e][0] + deck[e+1][0] + deck[e+2][0]

        #at least 1 matching suit:
        else:
            if deck[e][1] == deck[e+1][1]:
                total = max(deck[e][0] + deck[e+1][0], deck[e+2][0])
            elif deck[e][1] == deck[e+2][1]:
                total = max(deck[e][0] + deck[e+2][0], deck[e+1][0])
            else:
                total = max(deck[e+1][0] + deck[e+2][0], deck[e][0])

        scores.append(total)
        total_scores.append(total)
        #print(scores)
        #print(deck[e][0],deck[e][1],deck[e+1][0],deck[e+1][1], deck[e+2][0],deck[e+2][1])
        e = (3*v)
        v += 1


    #2nd draw, 1st player knocks:

    e = 3
    v = 2
    o = 1
    x = 1
    upcardnum = deck[-o][0]
    upcardsuit = deck[-o][1]
    while v <= (num):
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #all  3 same suit:
        if deck[e+1][1] == deck[e+2][1] and deck[e][1] == deck[e+1][1] and deck[e+1][1] == deck[e+2][1]:

        #if upcard doesn't share the same suit:
            if upcardsuit != deck[e][1]:
                #if upcard is greater than or equal to the sum of all 3 cards:
                if upcardnum >= (deck[e][0] + deck[e+1][0] + deck[e+2][0]):
                    total = upcardnum
                    upcardnum = min(deck[e][0], deck[e+1][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                    elif upcardnum ==  deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                #if upcard is not greater than or equal to the sum of all 3 cards:
                else:
                    #if newcard shares a suit:
                    if deck[-o - 1][1] == deck[e][1]:
                        total = (deck[-o-1][0] + deck[e][0] + deck[e+1][0] + deck[e+2][0]) - min(deck[-o-1][0], deck[e][0], deck[e+1][0], deck[e+2][0])
                        upcardnum = min(deck[-o-1][0], deck[e][0], deck[e+1][0], deck[e+2][0])
                        upcardsuit = deck[e][1]
                        setup2()
                        write_debug(upcardnum, upcardsuit)
                        continue

                    #if newcard doesn't share a suit:
                    else:
                        #if newcard is greater than or equal to the sum of the three cards:
                        if deck[-o - 1][0] >= (deck[e][0] + deck[e+1][0] + deck[e+2][0]):
                            total = deck[-o - 1][0]
                            upcardnum = min(deck[e][0], deck[e+1][0], deck[e+2][0])
                            upcardsuit = deck[e][1]
                            setup2()
                            write_debug(upcardnum, upcardsuit)
                            continue

                        #if newcard is not greater than or equal to the sum of the three cards:
                        else:
                            total = deck[e][0] + deck[e+1][0] + deck[e+2][0]
                            upcardnum = deck[-o - 1][0]
                            upcardsuit = deck[-o - 1][1]
                            setup2()
                            write_debug(upcardnum, upcardsuit)
                            continue

            #if upcard is also same suit:
            elif upcardsuit == deck[e][1]:
                #if upcard is greater than at least 1 of the cards[otherwise newcard]:
                if upcardnum > deck[e][0] or upcardnum > deck[e+1][0] or upcardnum > deck[e+2][0]:
                    total = (total + deck[e][0] + deck[e+1][0] + deck[e+2][0] + upcardnum) - min(deck[e][0], deck[e+1][0], deck[e+2][0])
                    upcardnum = min(deck[e][0], deck[e+1][0], deck[e+2][0])

                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                    elif upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                #if upcard is not greater than any of the cards:
                else:
                    #if newcard shares a suit:
                    if deck[-o - 1][1] == deck[e][1]:
                        total = (deck[-o-1][0] + deck[e][0] + deck[e+1][0] + deck[e+2][0]) - min(deck[-o-1][0], deck[e][0], deck[e+1][0], deck[e+2][0])
                        upcardnum = min(deck[-o-1][0], deck[e][0], deck[e+1][0], deck[e+2][0])
                        upcardsuit = deck[e][1]
                        setup2()
                        write_debug(upcardnum, upcardsuit)
                        continue

                    #if newcard doesn't share a suit:
                    else:
                        #if newcard is greater than or equal to the sum of the three cards:
                        if deck[-o - 1][0] >= (deck[e][0] + deck[e+1][0] + deck[e+2][0]):
                            total = deck[-o - 1][0]
                            upcardnum = min(deck[e][0], deck[e+1][0], deck[e+2][0])
                            upcardsuit = deck[e][1]
                            setup2()
                            write_debug(upcardnum, upcardsuit)
                            continue

                        #if newcard is not greater than or equal to the sum of the three cards:
                        else:
                            total = deck[e][0] + deck[e+1][0] + deck[e+2][0]
                            upcardnum = deck[-o - 1][0]
                            upcardsuit = deck[-o - 1][1]
                            setup2()
                            write_debug(upcardnum, upcardsuit)
                            continue

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #no same suit:
        if deck[e][1] != deck[e+2][1] and deck[e][1] != deck[e+1][1] and deck[e+1][1] != deck[e+2][1]:
            #if cards are three of a kind:
            #if the cards are below 10:
            if deck[e][0] < 10:
                #if all 3 card values are the same:
                if deck[e][0] == deck[e+1][0] and deck[e][0] == deck[e][0] == deck[e+2][0]:
                    total = 30.5
                    upcardnum = deck[-o - 1][0]
                    upcardsuit = deck[-o - 1][1]
                    setup2()
                    write_debug(upcardnum, upcardsuit)
                    continue
            #if the cards are 10 or face cards:
            if deck[e][0] == 10 or deck[e][0] == 11:
                #if all 3 card values are the same:
                if deck[e][2] == deck[e+1][2]  and deck[e][2] == deck[e+2][2]:
                    total = 30.5
                    upcardnum = deck[-o - 1][0]
                    upcardsuit = deck[-o - 1][1]
                    setup2()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard doesn't share a suit:
            if upcardsuit != deck[e][1] and upcardsuit != deck[e+1][1] and upcardsuit != deck[e+2][1]:
                #If upcard is the highest [COULD FLESH OUT MORE: perhaps if upcard is lower than 5 then you choose from the deck, not just the upcard]:
                if upcardnum > deck[e][0] and upcardnum > deck[e+1][0] and upcardnum > deck[e+2][0]:
                    total = upcardnum
                    upcardnum = min(deck[e][0], deck[e+1][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    elif upcardnum == deck[e+1][0]:
                         upcardsuit = deck[e+1][1]
                         setup1()
                         write_debug(upcardnum, upcardsuit)
                         continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #If upcard is the lowest or tied with the highest:
                else:
                    drawcard1()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with card 1:
            elif upcardsuit == deck[e][1]:
                #if upcard and card 1 is greater than either of the other cards:
                if (upcardnum + deck[e][0]) > max(deck[e+1][0], deck[e+2][0]):
                    total = upcardnum + deck[e][0]
                    upcardnum = min(deck[e+1][0], deck[e+2][0])
                    if upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if not:
                else:
                    drawcard1()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with card 2:
            elif upcardsuit == deck[e+1][1]:
                #if upcard and card 2 is greater than either of the other cards:
                if (upcardnum + deck[e+1][0]) > max(deck[e][0], deck[e+2][0]):
                    total = upcardnum + deck[e+1][0]
                    upcardnum = min(deck[e][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if not:
                else:
                    drawcard1()
                    write_debug(upcardnum, upcardsuit)
                    continue
            #if upcard shares a suit with card 3:
            elif upcardsuit == deck[e+2][1]:
                #if upcard and card 3 is greater than or equal to either of the other cards:
                if (upcardnum + deck[e+2][0]) >= max(deck[e][0], deck[e+1][0]):
                    total = upcardnum + deck[e+2][0]
                    upcardnum = min(deck[e+1][0], deck[e][0])
                    if upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if not:
                else:
                    drawcard1()
                    write_debug(upcardnum, upcardsuit)
                    continue

 #--------------------------------------------------------------------------------------------------------------------------------------------------
        #if cards 1 & 2 share suits:
        if deck[e][1] != deck[e+2][1] and deck[e][1] == deck[e+1][1] and deck[e+1][1] != deck[e+2][1]:

            #if upcard shares no suits:
            if upcardsuit != deck[e+2][1] and upcardsuit != deck[e+1][1]:
                #if upcard is max:
                if upcardnum >= deck[e+2][0] and upcardnum >= (deck[e+1][0] + deck[e][0]):
                    total = upcardnum
                    upcardnum == min(deck[e+1][0], deck[e][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    elif upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue

                #if card 3, or cards 1 and 2, are max:
                else:
                    drawcard2()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with the 3rd card:
            elif upcardsuit == deck[e+2][1]:
                #if upcard and 3rd card are greater than cards 1 and 2:
                if (upcardnum + deck[e+2][0]) > (deck[e][0] + deck[e+1][0]):
                    total = upcardnum + deck[e+2][0]
                    upcardnum = min(deck[e][0], deck[e+1][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if cards 1 and 2 are greater than upcard and card 3:
                else:
                    drawcard2()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with cards 1 and 2:
            elif upcardsuit == deck[e+1][1]:
                #if upcard and cards 1 and 2 are greater than or equal to card 3:
                if (upcardnum + deck[e+1][0] + (deck[e][0]) >= deck[e+2][0]):
                    total = upcardnum + deck[e+1][0] + deck[e][0]
                    upcardnum = deck[e+2][0]
                    upcardsuit = deck[e+2][1]
                    setup1()
                    write_debug(upcardnum, upcardsuit)
                    continue
                #if card 3 is greater than upcard, card 1, and card 2:
                else:
                    drawcard2()
                    write_debug(upcardnum, upcardsuit)
                    continue

#--------------------------------------------------------------------------------------------------------------------------
        #if cards 1 & 3 share suits:
        if deck[e][1] == deck[e+2][1] and deck[e][1] != deck[e+1][1] and deck[e+1][1] != deck[e+2][1]:
            #if upcard shares no suits:
            if upcardsuit != deck[e+2][1] and upcardsuit != deck[e+1][1]:
                #if upcard is max:
                if upcardnum >= deck[e+1][0] and upcardnum >= (deck[e+2][0] + deck[e][0]):
                    total = upcardnum
                    upcardnum == min(deck[e+1][0], deck[e][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    elif upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if card 3, or cards 1 and 2, are max:
                else:
                    drawcard3()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with the 2nd card:
            elif upcardsuit == deck[e+1][1]:
                #if upcard and 2nd card are greater than cards 1 and 3:
                if (upcardnum + deck[e+1][0]) > (deck[e][0] + deck[e+2][0]):
                    total = upcardnum + deck[e+1][0]
                    upcardnum = min(deck[e][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if cards 1 and 3 are greater than upcard and card 2:
                else:
                    drawcard3()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with cards 1 and 3:
            elif upcardsuit == deck[e][1]:
                #if upcard and cards 1 and 3 are greater than or equal to card 2:
                if (upcardnum + deck[e+2][0] + (deck[e][0]) >= deck[e+1][0]):
                    total = upcardnum + deck[e+2][0] + deck[e][0]
                    upcardnum = deck[e+1][0]
                    upcardsuit = deck[e+1][1]
                    setup1()
                    write_debug(upcardnum, upcardsuit)
                    continue
                #if card 2 is greater than upcard, card 1, and card 3:
                else:
                    drawcard3()
                    write_debug(upcardnum, upcardsuit)
                    continue

#------------------------------------------------------------------------------------------------------------------------
        #if cards 2 & 3 share suits:
        if deck[e][1] != deck[e+2][1] and deck[e][1] != deck[e+1][1] and deck[e+1][1] == deck[e+2][1]:
            #if upcard shares no suits:
            if upcardsuit != deck[e][1] and upcardsuit != deck[e+1][1]:
                #if upcard is max:
                if upcardnum >= deck[e][0] and upcardnum >= (deck[e+1][0] + deck[e+2][0]):
                    total = upcardnum
                    upcardnum == min(deck[e+1][0], deck[e][0], deck[e+2][0])
                    if upcardnum == deck[e][0]:
                        upcardsuit = deck[e][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    elif upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if card 1, or cards 3 and 2, are max:
                else:
                    drawcard4()
                    write_debug(upcardnum, upcardsuit)
                    continue
            #if upcard shares a suit with the 1st card:
            elif upcardsuit == deck[e][1]:
                #if upcard and 1st card are greater than cards 2 & 3:
                if (upcardnum + deck[e][0]) > (deck[e+2][0] + deck[e+1][0]):
                    total = upcardnum + deck[e][0]
                    upcardnum = min(deck[e+1][0], deck[e+2][0])
                    if upcardnum == deck[e+1][0]:
                        upcardsuit = deck[e+1][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                    else:
                        upcardsuit = deck[e+2][1]
                        setup1()
                        write_debug(upcardnum, upcardsuit)
                        continue
                #if cards 3 and 2 are greater than upcard and card 1:
                else:
                    drawcard4()
                    write_debug(upcardnum, upcardsuit)
                    continue

            #if upcard shares a suit with cards 3 and 2:
            elif upcardsuit == deck[e+1][1]:
                #if upcard and cards 3 and 2 are greater than or equal to card 1:
                if (upcardnum + deck[e+1][0] + (deck[e+2][0]) >= deck[e][0]):
                    total = upcardnum + deck[e+1][0] + deck[e+2][0]
                    upcardnum = deck[e][0]
                    upcardsuit = deck[e][1]
                    setup1()
                    write_debug(upcardnum, upcardsuit)
                    continue
                #if card 1 is greater than upcard, card 3, and card 2:
                else:
                    drawcard4()
                    write_debug(upcardnum, upcardsuit)
                    continue

    #-------------------------------------------------------------------------------------------------------------------------

    _2nd_deal_scores = 0
    average = 0
    r = 1

    while r < num:
        _2nd_deal_scores += scores[r]
        r += 1

    average = float(f'{(_2nd_deal_scores / (num - 1)):.10f}')
    #print(average)
    count += 1
    all_total = float(all_total) + float(average)

all_total = f'{(all_total / iterations):.10f}'
print('')
print(f'Average score of other players after having knocked: {all_total}')
print('')

#Standard deviation:
sum = 0.0
j = 0
h = 0
while j <= iterations:
    sum = float(sum) + (float(total_scores[h]) - float(all_total))**2
    j += 1
    h += 1

std_dev = math.sqrt((sum / iterations))
print(f'Standard Deviation: {std_dev}\n')

#75th and 25th percentile:
#75th percentile = mean + (z * standard deviation), where z is taken from a table (https://www.statology.org/calculate-percentile-from-mean-standard-deviation/)
#Remember, e.g. 75th percentile means that 75% of all the answers are below yours, and 25% are above

percent75 = float(all_total) + (0.67 * std_dev)
percent25 = float(all_total) + (-0.67 * std_dev)
print(f'75th percentile: {percent75}')
print(f'25th percentile: {percent25}')

# MrJoshie333 out o/