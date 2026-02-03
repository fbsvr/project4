output = ""
def main():
    global output
    global code
    handle = open('input.txt')
    code = handle.read()
    handle.close()
    stock_exchange(code)
    handle = open('output.txt','w')
    handle.write(output)
    handle.close()

def stock_exchange(input):
    global output
    global names_and_ids
    input=input.split("\n") #split the input lines
    lines=list()
    for i in range(len(input)-1):
        newline=input[i].split()
        lines.append(newline)

    sell={} #create a dictionary to gather all selling offerss
    buy={} #create a dictionary to gather all buying offers
    all_operations="" #get an empty string to write all transactions happened. 
    names_and_ids={} #create a dictionary to get the id numbers and names

    for t in range(len(lines)): #get the key words from every line
        timestamp=lines[t][0].split("-") #split the date 
        time=""
        for m in range(len(timestamp)): #turn the date into a number, it will not change anything
            time+=timestamp[m]  #because when the number is bigger, the date will be more current

        id_number=int(lines[t][1]) #get the id number, turn into an integer
        name=lines[t][2] #get the name 
        stock_name=lines[t][3] #get the stock name
        order=lines[t][4] #get the type of the order
        stock_number=int(lines[t][5]) #get the quantity of the order
        price_for_stock=float(lines[t][6]) #get the price for the stock
        order_line=[int(time),id_number,name,stock_number,price_for_stock] #get all the info for an order into a list 
        if name not in names_and_ids:
            names_and_ids[name]=id_number
        if order =="Buy": #if the order type is buy, then in a dictionary named buy, append the order to the stock name
            buy[stock_name]=buy.get(stock_name,[])+ [order_line]
        elif order =="Sell": #if the order is sell, then in a dictionary named sell, append the order to the stock name
            sell[stock_name]=sell.get(stock_name,[])+ [order_line]
        
    for key in buy: #for every stock in the buy dictionary
        for d in range(len(buy[key])): #sort the orders according to their priority
            for s in range(0,len(buy[key])-d-1):
                if (buy[key][s][0],-buy[key][s][4],buy[key][s][1])>(buy[key][s+1][0],-buy[key][s+1][4],buy[key][s+1][1]):
                    a=buy[key][s] #change the places of orders for the value of the stock name
                    b=buy[key][s+1]
                    buy[key][s+1]=a
                    buy[key][s]=b
    
    for key in sell: #for every stock in the sell dictionary
        for d in range(len(sell[key])): #sort the orders according to their priority
            for s in range(0,len(sell[key])-d-1):
                if (sell[key][s][0],sell[key][s][4],sell[key][s][1])>(sell[key][s+1][0],sell[key][s+1][4],sell[key][s+1][1]): 
                    #take the negative version of the price because when it comes to sell, the lower price is prioritized
                    a=sell[key][s] #change the places of orders for the value of the stock name
                    b=sell[key][s+1]
                    sell[key][s+1]=a
                    sell[key][s]=b

    for stockname in buy: #for every stock in the buy dictionary
        if stockname in sell: #check if the stockname is also in the sell dictionary
                indexnumberforbuy=0 #index number for the value of the stockname in the buy dictionary
                indexnumberforsell=0 #index number for the value of the stockname in the sell dictionary
                while indexnumberforsell<len(sell[stockname]) and indexnumberforbuy<len(buy[stockname]):         
                    buying_order=buy[stockname][indexnumberforbuy] #get the buying order
                    selling_order=sell[stockname][indexnumberforsell] #get the selling order
                    if buying_order[4]>=selling_order[4] and buying_order[2]!=selling_order[2]:  
                        #if the buying price is equal to or bigger than selling price, and the users are different

                        if buying_order[3]==selling_order[3]: #if the quantities of the stocks in the order are the same
                            #if the quantities of the stock in the orders are the same
                            dateandtime=str(max(buying_order[0],selling_order[0])) #get the transaction date by finding the max value
                            all_operations+= f"{buying_order[2]} bought {selling_order[3]} {stockname} for {selling_order[4]} USD from {selling_order[2]} on {dateandtime} {buying_order[1]}" +"\n"
                            #get the operation above
                            sell[stockname].pop(indexnumberforsell) #delete the order from the sell dictionary 
                            indexnumberforbuy+=1
                            #we delete them cause there is no stock left to sell or buy for both order
                            indexnumberforsell=0 #for the next buying order, start to look from the beginning of the selling offers

                        elif buying_order[3]>selling_order[3]:
                            #if the quantity for the buy order is much than the quantity for the selling order
                            dateandtime=str(max(buying_order[0],selling_order[0]))  #get the transaction date by finding the max value
                            all_operations+= f"{buying_order[2]} bought {selling_order[3]} {stockname} for {selling_order[4]} USD from {selling_order[2]} on {dateandtime} {buying_order[1]}" +"\n"
                            #get the operation above
                            buy[stockname][indexnumberforbuy][3]-=sell[stockname][indexnumberforsell][3] #subtract the amount sold from the buying order
                            sell[stockname].pop(indexnumberforsell) #delete the sell order, cause there is no stock left
                            if indexnumberforsell>=len(sell[stockname]): #if the index is out of range
                            #then, there is no selling offer that is available for the buying offer 
                                indexnumberforbuy+=1
                                indexnumberforsell=0 #start to look for the selling offers from the top for the next buying offer

                        elif buying_order[3]<selling_order[3]:
                            #if the quantity for the sell order is much than the quantity for the buying order
                            dateandtime=str(max(buying_order[0],selling_order[0])) #get the transaction date by finding the max value
                            all_operations+= f"{buying_order[2]} bought {buying_order[3]} {stockname} for {selling_order[4]} USD from {selling_order[2]} on {dateandtime} {buying_order[1]}" +"\n"
                            #get the operation above
                            sell[stockname][indexnumberforsell][3]-=buy[stockname][indexnumberforbuy][3] #subtract the amount bought from the selling order
                            indexnumberforbuy+=1
                            indexnumberforsell=0  #for the next buying order, start to look from the beginning of the selling offers
                            if indexnumberforbuy>=len(buy[stockname]):
                                break
                    else: #if the price for buying is less selling
                        indexnumberforsell+=1 #increase the index, look for other selling options
                        if indexnumberforsell>=len(sell[stockname]): #if the index is out of range
                            #then, there is no selling offer that is available for the buying offer 
                            indexnumberforbuy+=1
                            indexnumberforsell=0 #start to look for the selling offers from the top for the next buying offer


    all_operations=all_operations.split("\n") #get all the operations
    all_operations.pop(-1) #there is an empty thing in all_operations so delete it
    operations=[] #create a new list
    for y in range(len(all_operations)):
        newline=all_operations[y].split() #split every line of the all_operations
        operations.append(newline) #append them to the list

    for i in range(len(operations)-1): #start to sort the operations according to the transaction date and id number
        for s in range(len(operations) - 1 - i):
            date1 = operations[s][10]
            date2 = operations[s + 1][10]
            id1 = operations[s][11]
            id2 = operations[s + 1][11]
            stockname1=operations[s][3]
            stockname2=operations[s+1][3]
            price1=operations[s][4]
            price2=operations[s][4]

            if date1==date2: #sort the transactions, if dates are the same for consecutive transactions
                if stockname1<stockname2: #check the stocknames
                    operations[s],operations[s+1]=operations[s+1],operations[s]
            elif date1>date2: #if a prior transaction in the operations has a later date, change their places
                operations[s],operations[s+1]=operations[s+1],operations[s]

    
    for u in range(len(operations)): #change the operations because in the old version, date is still an integer
        date="on " + operations[u][10][:4]+"-"+operations[u][10][4:6]+"-"+operations[u][10][6:8]+" at "+operations[u][10][8:10]+":"+operations[u][10][10:12]+":"+operations[u][10][12:14]
        for b in range(9): #add every transaction to the output to write to output.txt
            output+= operations[u][b]+" " 
        if u !=len(operations)-1:
            output+=date+  "\n" 
        else:
            output+=date
    output+="\n"
    return output

result=main() #run the code

def total_executed_volume(time): #find the total executed volume
    global output
    time=time.split("-") #split the given time according to the position of "-"
    time_num="" 
    for i in range(len(time)): #bring together all the parts of the given time
        time_num+=time[i]
    time_num=int(time_num) #turn it into an integer
    #turning the date into an integer will help us to find which date is comes before

    all_transactions=output.split("\n") #get the output from the exchange part and split it
    total_volume=0 
    for s in range(len(all_transactions)-1):
        newline=all_transactions[s].split() #get every line in the output
        stocknumber=int(newline[2]) #get the amount of traded stock
        price_for_stock=float(newline[5]) #get the price paid for the stock
        date=newline[10].split("-") #get the YYYY-MM-DD
        hour=newline[12].split(":") #get hh-mm-ss
        date_number="" #start to create your new number
        for t in range(3):
            date_number+=date[t] #bring together the YYYY-MM-DD part
        for y in range(3):
            date_number+=hour[y] #bring together the hh-mm-ss and add at the end of the date_number
        date_number=int(date_number)
        if date_number<=time_num: #check if the date is the same or earlier than the given one
            total_volume+= stocknumber * price_for_stock #get the volume for one line and add up to the total
    int_total=int(total_volume)
    if total_volume-int_total>=0.5: #round the number to the nearest integer value
        total=int_total+1
    else:
        total=int_total
    return total #return the total_volume


def executed_user_volume(user_id,time): #get the total executed volume from a specific user
    global output
    global names_and_ids
    time=time.split("-") #split the given time according to the position of "-"
    time_num="" 
    for i in range(len(time)): #bring together all the parts of the given time
        time_num+=time[i]
    time_num=int(time_num) #turn it into an integer
    #turning the date into an integer will help us to find which date is comes before

    all_transactions=output.split("\n") #get the output from the exchange part and split it
    total_volume=0 
    for s in range(len(all_transactions)-1):
        newline=all_transactions[s].split() #get every line in the output
        stocknumber=int(newline[2]) #get the amount of traded stock
        price_for_stock=float(newline[5]) #get the price paid for the stock
        name1=names_and_ids[newline[0]]
        name2=names_and_ids[newline[8]]
        date=newline[10].split("-") #get the YYYY-MM-DD
        hour=newline[12].split(":") #get hh-mm-ss
        date_number="" #start to create your new number
        for t in range(3):
            date_number+=date[t] #bring together the YYYY-MM-DD part
        for y in range(3):
            date_number+=hour[y] #bring together the hh-mm-ss and add at the end of date_number
        date_number=int(date_number) 
        
        if (name1==user_id or name2==user_id) and date_number<=time_num: #check if the date is the same or earlier than the given one and names match
            total_volume+= stocknumber * price_for_stock #get the volume for one line and add up to the total

    int_total=int(total_volume)
    if total_volume-int_total>=0.5: #round the number to the nearest integer value
        total=int_total+1 #if their sub is equal or more than 0.5, it has to go upwards, else downwards
    else:
        total=int_total
    return total #return the total


def total_remaining_volume(time): #get the total remaining volume till a given time
    global code
    time=time.split("-") #split the given time according to the position of "-"
    time_num="" 
    for i in range(len(time)): #bring together all the parts of the given time
        time_num+=time[i]
    time_num=int(time_num) #turn it into an integer

    input=code.split("\n")
    lines=list()
    for i in range(len(input)-1):
        newline=input[i].split()
        lines.append(newline)

    sell={}
    buy={}

    for t in range(len(lines)): #get the key words from every line
        timestamp=lines[t][0].split("-") #split the date 
        time=""
        for m in range(len(timestamp)): #turn the date into a number, it will not change anything
            time+=timestamp[m]  #because when the number is bigger, the date will be more current

        id_number=int(lines[t][1]) #get the id number, turn into an integer
        name=lines[t][2] #get the name 
        stock_name=lines[t][3] #get the stock name
        order=lines[t][4] #get the type of the order
        stock_number=int(lines[t][5]) #get the quantity of the order
        price_for_stock=float(lines[t][6]) #get the price for the stock
        order_line=[int(time),id_number,name,stock_number,price_for_stock] #get all the info for an order into a list 
        if order =="Buy" and int(time)<=time_num: #if the order type is buy, then in a dictionary named buy, append the order to the stock name
            buy[stock_name]=buy.get(stock_name,[])+ [order_line]
        elif order =="Sell" and int(time)<=time_num: #if the order is sell, then in a dictionary named sell, append the order to the stock name
            sell[stock_name]=sell.get(stock_name,[])+ [order_line]
        
    for key in buy: #for every stock in the buy dictionary
        for d in range(len(buy[key])): #sort the orders according to their priority
            for s in range(0,len(buy[key])-d-1):
                if (buy[key][s][0],-buy[key][s][4],buy[key][s][1])>(buy[key][s+1][0],-buy[key][s+1][4],buy[key][s+1][1]):
                    a=buy[key][s] #change the places of orders for the value of the stock name
                    b=buy[key][s+1]
                    buy[key][s+1]=a
                    buy[key][s]=b
    
    for key in sell: #for every stock in the sell dictionary
        for d in range(len(sell[key])): #sort the orders according to their priority
            for s in range(0,len(sell[key])-d-1):
                if (sell[key][s][0],sell[key][s][4],sell[key][s][1])>(sell[key][s+1][0],sell[key][s+1][4],sell[key][s+1][1]): 
                    #take the negative version of the price because when it comes to sell, the lower price is prioritized
                    a=sell[key][s] #change the places of orders for the value of the stock name
                    b=sell[key][s+1]
                    sell[key][s+1]=a
                    sell[key][s]=b

    for stockname in buy: #for every stock in the buy dictionary
        if stockname in sell: #check if the stockname is also in the sell dictionary
                indexnumberforbuy=0 #index number for the value of the stockname in the buy dictionary
                indexnumberforsell=0 #index number for the value of the stockname in the sell dictionary
                while indexnumberforsell<len(sell[stockname]) and indexnumberforbuy<len(buy[stockname]):         
                    buying_order=buy[stockname][indexnumberforbuy] #get the buying order
                    selling_order=sell[stockname][indexnumberforsell] #get the selling order
                    if buying_order[4]>=selling_order[4] and buying_order[2]!=selling_order[2]:  
                        #if the buying price is equal to or bigger than selling price, and the users are different

                        if buying_order[3]==selling_order[3]: #if the quantities of the stocks in the order are the same
                            #if the quantities of the stock in the orders are the same
                            sell[stockname].pop(indexnumberforsell) #delete the order from the sell dictionary 
                            buy[stockname][indexnumberforbuy][3]=0 #make the stock in the buy order 0
                            indexnumberforbuy+=1 #get to the next buying order
                            indexnumberforsell=0 #for the next buying order, start to look from the beginning of the selling offers

                        elif buying_order[3]>selling_order[3]: #if the quantity for the buy order is much than the quantity for the selling order
                            buy[stockname][indexnumberforbuy][3]-=sell[stockname][indexnumberforsell][3] #subtract the amount sold from the buying order
                            sell[stockname].pop(indexnumberforsell) #delete the sell order, cause there is no stock left
                            if indexnumberforsell>=len(sell[stockname]): #if the index is out of range then, there is no selling offer that is available for the buying offer 
                                indexnumberforbuy+=1
                                indexnumberforsell=0 #start to look for the selling offers from the top for the next buying offer

                        elif buying_order[3]<selling_order[3]: #if the quantity for the sell order is much than the quantity for the buying order
                            sell[stockname][indexnumberforsell][3]-=buy[stockname][indexnumberforbuy][3] #subtract the amount bought from the selling order
                            buy[stockname][indexnumberforbuy][3]=0 # make the stock in the buy order 0
                            indexnumberforbuy+=1
                            indexnumberforsell=0  #for the next buying order, start to look from the beginning of the selling offers
                            if indexnumberforbuy>=len(buy[stockname]):
                                break
                    else: #if the price for buying is less selling
                        indexnumberforsell+=1 #increase the index, look for other selling options
                        if indexnumberforsell>=len(sell[stockname]): #if the index is out of range then, there is no selling offer that is available for the buying offer 
                            indexnumberforbuy+=1
                            indexnumberforsell=0 #start to look for the selling offers from the top for the next buying offer

    total_volume=0
    for stock in buy: #get all the remaining buying offers one by one for every different stock
        for i in range(len(buy[stock])):
            stock_number=buy[stock][i][3] #get the stock number
            price=buy[stock][i][4] #get the price
            total_volume+= stock_number*price #multiply them and add to total_volume
    for stock in sell: #get all the remaining selling offers one by one for every different stock
        for i in range(len(sell[stock])):
            stock_number=sell[stock][i][3]#get the stock number
            price=sell[stock][i][4]#get the price
            total_volume+= stock_number*price#multiply them and add to total_volume
    int_total=int(total_volume) #get the integer total volume
    if total_volume-int_total>=0.5: #if their sub is equal or more than 0.5, it should go upwards, otherwise downwards
        total=int_total+1
    else:
        total=int_total
    return total


def remaining_user_volume(user_id, time): #get the remaining volume till a given time of a given user
    global code
    time=time.split("-") #split the given time according to the position of "-"
    time_num="" 
    for i in range(len(time)): #bring together all the parts of the given time
        time_num+=time[i]
    time_num=int(time_num) #turn it into an integer

    input=code.split("\n") #split the code line by line
    lines=list()
    for i in range(len(input)-1):
        newline=input[i].split()
        lines.append(newline)

    sell={}
    buy={}

    for t in range(len(lines)): #get the key words from every line
        timestamp=lines[t][0].split("-") #split the date 
        time=""
        for m in range(len(timestamp)): #turn the date into a number, it will not change anything
            time+=timestamp[m]  #because when the number is bigger, the date will be more current

        id_number=int(lines[t][1]) #get the id number, turn into an integer
        name=lines[t][2] #get the name 
        stock_name=lines[t][3] #get the stock name
        order=lines[t][4] #get the type of the order
        stock_number=int(lines[t][5]) #get the quantity of the order
        price_for_stock=float(lines[t][6]) #get the price for the stock
        order_line=[int(time),id_number,name,stock_number,price_for_stock] #get all the info for an order into a list 
        if order =="Buy" and int(time)<=(time_num): #if the order type is buy, then in a dictionary named buy, append the order to the stock name
            buy[stock_name]=buy.get(stock_name,[])+ [order_line]
        elif order =="Sell" and int(time)<=(time_num): #if the order is sell, then in a dictionary named sell, append the order to the stock name
            sell[stock_name]=sell.get(stock_name,[])+ [order_line]
        
    for key in buy: #for every stock in the buy dictionary
        for d in range(len(buy[key])): #sort the orders according to their priority
            for s in range(0,len(buy[key])-d-1):
                if (buy[key][s][0],-buy[key][s][4],buy[key][s][1])>(buy[key][s+1][0],-buy[key][s+1][4],buy[key][s+1][1]):
                    #taking negative version of the price will help us to get the biggest one first
                    a=buy[key][s] #change the places of orders for the value of the stock name
                    b=buy[key][s+1]
                    buy[key][s+1]=a
                    buy[key][s]=b
    
    for key in sell: #for every stock in the sell dictionary
        for d in range(len(sell[key])): #sort the orders according to their priority
            for s in range(0,len(sell[key])-d-1):
                if (sell[key][s][0],sell[key][s][4],sell[key][s][1])>(sell[key][s+1][0],sell[key][s+1][4],sell[key][s+1][1]): 
                    a=sell[key][s] #change the places of orders for the value of the stock name
                    b=sell[key][s+1]
                    sell[key][s+1]=a
                    sell[key][s]=b

    for stockname in buy: #for every stock in the buy dictionary
        if stockname in sell: #check if the stockname is also in the sell dictionary
                indexnumberforbuy=0 #index number for the value of the stockname in the buy dictionary
                indexnumberforsell=0 #index number for the value of the stockname in the sell dictionary
                while indexnumberforsell<len(sell[stockname]) and indexnumberforbuy<len(buy[stockname]):         
                    buying_order=buy[stockname][indexnumberforbuy] #get the buying order
                    selling_order=sell[stockname][indexnumberforsell] #get the selling order
                    if buying_order[4]>=selling_order[4] and buying_order[2]!=selling_order[2]:  
                        #if the buying price is equal to or bigger than selling price, and the users are different

                        if buying_order[3]==selling_order[3]: #if the quantities of the stocks in the order are the same
                            #if the quantities of the stock in the orders are the same
                            sell[stockname].pop(indexnumberforsell) #delete the order from the sell dictionary 
                            buy[stockname][indexnumberforbuy][3]=0 #make the stock number in the buy order 0
                            indexnumberforbuy+=1  
                            indexnumberforsell=0 #for the next buying order, start to look from the beginning of the selling offers

                        elif buying_order[3]>selling_order[3]:
                            #if the quantity for the buy order is much than the quantity for the selling order
                            buy[stockname][indexnumberforbuy][3]-=sell[stockname][indexnumberforsell][3] #subtract the amount sold from the buying order
                            sell[stockname].pop(indexnumberforsell) #delete the sell order, cause there is no stock left
                            if indexnumberforsell>=len(sell[stockname]): #if the index is out of range then, there is no selling offer that is available for the buying offer 
                                indexnumberforbuy+=1
                                indexnumberforsell=0 #start to look for the selling offers from the top for the next buying offer

                        elif buying_order[3]<selling_order[3]:
                            #if the quantity for the sell order is much than the quantity for the buying order
                            sell[stockname][indexnumberforsell][3]-=buy[stockname][indexnumberforbuy][3] #subtract the amount bought from the selling order
                            buy[stockname][indexnumberforbuy][3]=0#make the stock number in the buy order 0
                            indexnumberforbuy+=1
                            indexnumberforsell=0  #for the next buying order, start to look from the beginning of the selling offers
                            if indexnumberforbuy>=len(buy[stockname]):
                                break
                    else: #if the price for buying is less selling
                        indexnumberforsell+=1 #increase the index, look for other selling options
                        if indexnumberforsell>=len(sell[stockname]): #if the index is out of range then, there is no selling offer that is available for the buying offer 
                            indexnumberforbuy+=1
                            indexnumberforsell=0 #start to look for the selling offers from the top for the next buying offer

    total_volume=0
    for stock in buy:
        for i in range(len(buy[stock])): #get every remaining buy order for every stock 
            if buy[stock][i][1]== user_id: #if the user ids match
                stock_number=buy[stock][i][3] #get the stock number
                price=buy[stock][i][4] #get the price 
                total_volume+= stock_number*price #multiply them and add to total_volume

    for stock in sell:
        for i in range(len(sell[stock])): #get every remaining sell order for every stock 
            if sell[stock][i][1]==user_id: #if the user ids match
                stock_number=sell[stock][i][3]#get the stock number
                price=sell[stock][i][4]#get the price 
                total_volume+= stock_number*price #multiply them and add to total_volume
    int_total=int(total_volume) #get the integer version of total volume
    if total_volume-int_total>=0.5:  #if their sub is equal or more than 0.5
        total=int_total+1 #get the upper value
    else:
        total=int_total #else, get the lower value
    return total
