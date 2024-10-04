# Helper function: Flip pancakes with an index (0, k)
def flipPancakes(pancakes, k):
    flip = pancakes[:k][::-1]
    
    #Flip the burnt pancakes to white and white to burnt
    flip = [(x[0], 'w' if x[1] == 'b' else 'b') for x in flip]
    
    # Return the pancakes new position
    return flip + pancakes[k:], k
    

# A* Search Heuristic Function: finding the misplaced pancake with the largest ID
def aStarHeuristic(pancakes):
    for i in range(len(pancakes) -1, -1, -1):
        if pancakes[i] != (i + 1, 'w'):
            return i + 1
    return 0
    

# A* Search Function: Positions, queuing, and costs
def aStarSearch(pancakes):
    startingPos = tuple(pancakes)
    endingPos = ((1, 'w'), (2, 'w'), (3, 'w'), (4, 'w'))
    
    queue = [(startingPos, [], 0, aStarHeuristic(startingPos), None)]
    visitedPos = set()
    
    while queue:
        queue.sort(key=lambda x: x[2] + x[3])
        currentPos, path, g_actualCost, h_actualCost, flippingPos = queue.pop(0)
        
        if currentPos == endingPos:
            return path, g_actualCost, h_actualCost
            
        visitedPos.add(currentPos)
        for i in range(2, len(currentPos) + 1):
            nextState, flippingPos = flipPancakes(list(currentPos), i)
            nextState = tuple(nextState)
            if nextState not in visitedPos:
                g_func = g_actualCost + i
                h_func = aStarHeuristic(nextState)
                queue.append((nextState, path + [(nextState, flippingPos)], g_func, h_func, flippingPos))
    return None


# Breadth-First Search Function: Positions, queuing, and costs
def bfSearch(pancakes):
    startingPos = tuple(pancakes)
    endingPos = ((1, 'w'), (2, 'w'), (3, 'w'), (4, 'w'))
    
    #List for queue:
    queue = [(startingPos, [], 0)]
    visitedPos = set()
    
    #remove from the front position
    while queue:
        currentPos, path, totalCost = queue.pop(0)
    
        if currentPos == endingPos:
            return path
            
        visitedPos.add(currentPos)
        for i in range(2, len(currentPos) + 1):
            nextState, flippingPos = flipPancakes(list(currentPos), i)
            nextState = tuple(nextState)
            if nextState not in visitedPos:
                queue.append((nextState, path + [(nextState, flippingPos)], totalCost + i))
    return None    



# Main:

def burntPancakes():
    userInput =  input("Enter order and algorithm (-a | -b): ")
    pancakes, searchAlgorithm = userInput[:-2], userInput[-1]
    
    pancakes = [(int(p[0]), p[1]) for p in zip(pancakes[::2], pancakes[1::2])]
    print(pancakes)
    
    if searchAlgorithm == 'a':
        result, g_finalCost, h_finalCost = aStarSearch(pancakes)
        print("\nA*: ")

        if result:
            g_currentCost = 0
            #g function position will increase each time it goes through loop
            for i, (state, flippingPos) in enumerate(result):
                g_currentCost = g_currentCost + flippingPos
                h_currentCost = aStarHeuristic(state)
                stateReturns = "".join(f"{p[0]}{p[1]}" for p in state[:flippingPos]) + '|' + "".join(f"{p[0]}{p[1]}" for p in state[flippingPos:])
                print(f"{stateReturns} g:{g_currentCost}, h:{h_currentCost}")
        else:
            print("None")
    elif searchAlgorithm == 'b':
        result = bfSearch(pancakes)
        print("\nBFS: ")
        if result:
            for state, flippingPos in result:
                stateReturns = "".join(f"{p[0]}{p[1]}" for p in state[:flippingPos]) + '|' + "".join(f"{p[0]}{p[1]}" for p in state[flippingPos:])
                print(f"{stateReturns}")
        else:
            print("None")
    else:
        print("Algorithm Not Available")
        
burntPancakes()