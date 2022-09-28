import numpy as np

from typing import List, Dict, Set

# Main function
def main():
    
    #initialize general variables here
    support: int = 100
    total_lines: int = 31101
    max_column: int = 38
    
    #open file
    with open("browsing-data.txt", "r") as file:
        
        #read all the data from file
        lines: List[str] = file.readlines()
        
    #store all items and their counts here
    items: Dict[str, int] = dict()
    
    #generate the empty matrix
    baskets = np.empty((total_lines, max_column), dtype = "U8")
    
    #populate the baskets matrix and count the occurences of all items
    for i in range(len(lines)):
        words = lines[i].split()
        for j in range(len(words)):
            baskets[i, j] = words[j] #add an entry into baskets
            
            if items.get(words[j]) != None: #add item to dict
                items[words[j]] += 1
            else:
                items[words[j]] = 1

    #get all the items that are frequent and store them in a set
    frequent: Set[str] = set()
    for (item, count) in items.items():
        if count >= support:
            frequent.add(item)
            
    #DEBUGGING
    print(f"{len(frequent)} frequent items")
            
    #store all doubles and their counts here
    doubles: Dict[(str, str), int] = dict()
    
    #store all triples and their counts here
    triples: Dict[(str, str, str), int] = dict()
    
    #filter out all the frequent items and add them to new_baskets
    new_baskets = np.empty((total_lines, max_column), dtype = "U8")
    for i in range(total_lines): #for every line
        cur: int = 0 #current position in the line
        
        #copy frequent items into new_baskets
        for j in range(max_column): #for every word
            
            if baskets[i, j] == "": #if we've run out of items in this list
                break
            
            word: str = baskets[i, j]
            if word in frequent:
                new_baskets[i, cur] = word #if word is frequent, add it to the new basket
                cur += 1 #current word was frequent, so increment our position by 1
                
        #get the doubles of frequents on this line
        if cur > 1:
            for j in range(cur): #for every frequent item in this line
                for k in range(j + 1, cur): #create a skewed triangle with the other frequent items in this line
                    
                    #generate a double
                    this_double_list = [new_baskets[i, j], new_baskets[i, k]] #choose items for a double
                    this_double_list.sort() #sort the items (so that order does not matter)
                    this_double = tuple(this_double_list) #generate a tuple
                    
                    #add item to doubles
                    if doubles.get(this_double) != None:
                        doubles[this_double] += 1
                    else:
                        doubles[this_double] = 1
        
        #get the triples of frequents on this line    
        if cur > 2:
            for j in range(cur): #for every frequent item in this line
                for k in range(j + 1, cur): #create a skewed triangle with the other frequent items in this line
                    for l in range(k + 1, cur):
                        
                        #generate a triple
                        this_triple_list = [new_baskets[i, j], new_baskets[i, k], new_baskets[i, l]] #choose items for a triple
                        this_triple_list.sort() #sort the items (so that order does not matter)
                        this_triple = tuple(this_triple_list) #generate a tuple
                        
                        #add item to triples
                        if triples.get(this_triple) != None:
                            triples[this_triple] += 1
                        else:
                            triples[this_triple] = 1
    
    #get all the frequent doubles and triples
    frequent_doubles: Set[(str, str)] = set()
    frequent_triples: Set[(str, str, str)] = set()
    for (double, count) in doubles.items():
        if count >= support:
            frequent_doubles.add(double)
    for (triple, count) in triples.items():
        if count >= support:
            frequent_triples.add(triple)
    
    #DEBUGGING
    print(f"{len(frequent_doubles)} frequent doubles")
    print(f"{len(frequent_triples)} frequent triples")
    
    #get all associations for doubles
    double_associations: List[((str, str), int)] = [] #the association from tuple[0] to tuple[1] as a confidence score
    for double in frequent_doubles: #iterate through all frequent doubles
        this_tuple0 = ((double[0], double[1]), doubles[double] / items[double[0]]) #calculate the fraction of {X,Y} to X
        this_tuple1 = ((double[1], double[0]), doubles[double] / items[double[1]]) #calculate the fraction of {X,Y} to Y
        double_associations.append(this_tuple0)
        double_associations.append(this_tuple1)
        
    #get all associations for triples
    triple_associations: List[(((str, str), str), float)] = [] #the association from tuple[0] to tuple[1] as a confidence score
    for triple in frequent_triples: #iterate through all frequent triples
        this_tuple0 = (((triple[0], triple[1]), triple[2]), triples[triple] / doubles[(triple[0], triple[1])]) #calculate fraction of {X,Y,Z} to {X,Y}
        this_tuple1 = (((triple[0], triple[2]), triple[1]), triples[triple] / doubles[(triple[0], triple[2])]) #calculate fraction of {X,Y,Z} to {X,Z}
        this_tuple2 = (((triple[1], triple[2]), triple[0]), triples[triple] / doubles[(triple[1], triple[2])]) #calculate fraction of {X,Y,Z} to {Y,Z}
        triple_associations.append(this_tuple0)
        triple_associations.append(this_tuple1)
        triple_associations.append(this_tuple2)
        
    #sort by confidence and by alphabetical order
    double_associations = sorted(sorted(double_associations, key = lambda x: x[0][0]), key = lambda x: x[1], reverse = True)
    triple_associations = sorted(sorted(triple_associations, key = lambda x: x[0][0][0]), key = lambda x: x[1], reverse = True)
    
    #this is where we'll store the output
    output_str = ""

    #get top 5 doubles
    output_str += "OUTPUT A"
    for i in range(5):
        this_double = double_associations[i]
        output_str += "\n" + this_double[0][0] + " " + this_double[0][1] + " " + str(this_double[1])
    
    #get top 5 triples
    output_str += "\nOUTPUT B"
    for i in range(5):
        this_triple = triple_associations[i]
        output_str += "\n" + this_triple[0][0][0] + " " + this_triple[0][0][1] + " " + this_triple[0][1] + " " + str(this_triple[1])
        
    #save file
    with open("output.txt", "w") as file:
        file.write(output_str)
    
    
                    
            

        
        
    
    
if __name__ == "__main__":
    main()