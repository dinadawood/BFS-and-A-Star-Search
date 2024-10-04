from collections import deque
import heapq

# Helper Function: Flip pancakes and return new position...index of (0, k)
def flipPancakes(state, k):
    flip = state[:k][::-1]
    flip = [(pancake[0], 'b' if pancake[1] == 'w' else 'w') for pancake in reversed(state[:k])]
    return flip + state[k:]

# Helper Function: Format output with '|'
def flipIndicator(state, flippingIndex):
    stateNindicator = "".join([p[0] + p[1] for p in state])
    return stateNindicator[:flippingIndex * 2] + '|' + stateNindicator[flippingIndex * 2:]


# A* Search Heuristic Function: finding the misplaced pancake with the largest ID
def heuristic(state):
    expected = ['1w', '2w', '3w', '4w']
    for i in range(3, -1, -1):
        if state[i] != expected[i]:
            return i + 1
    return 0

# Breadth-First Search Function: Positions, queuing, and costs
def bfSearch(startingPos):
    queue = deque([(startingPos, [], 0)])
    visitedPos = set()

    while queue:
        state, path, g_func = queue.popleft()

        if state == endingPos:
            return path + [(state, 4, g_func)]
        
        for i in range(2, 5):
            nextState = flipPancakes(state, i)
            if tuple(nextState) not in visitedPos:
                visitedPos.add(tuple(nextState))
                queue.append((nextState, path + [nextState, i, g_func]), g_func + i)


# A* Search Function: Positions, queuing, and costs
def aStarSearch(startingPos):
    queue = [(0 + heuristic(startingPos), 0, startingPos, [])]
    visitedPos = set()

    while queue:
        f_func, g_func, state, path = heapq.heappop(queue)

        if state == endingPos:
            return path + [(state, 4, g_func)], g_func
        
        for i in range(2, 5):
            nextState = flipPancakes(state, i)
            if tuple(nextState) not in visitedPos:
                visitedPos.add(tuple(nextState))
                heapq.heappush(queue, (g_func + i + heuristic(nextState), g_func + i, nextState, path + [nextState, i, g_func]))

    return [], 0


# Main:

def burntPancakes(str):
    pancakes = [(str[i], str[i+1]) for i in range(0, 7, 2)]
    searchAlgorithm = str[-1]

    global endingPos
    endingPos = [('1', 'w'), ('2', 'w'), ('3', 'w'), ('4', 'w')]

    if searchAlgorithm == 'b':
        result = bfSearch(pancakes)
        for output, flippingIndex, g_func in result:
            print(flipIndicator(output, flippingIndex))
    elif searchAlgorithm == 'a':
        result, cost = aStarSearch(pancakes)
        for output, flippingIndex, g_func in result:
            h = heuristic(output)
            print(f"{flipIndicator(output, flippingIndex)} g:{g_func}, h:{h}")
        print(f"{flipIndicator(endingPos, 4)} g:{cost}, h:0")


str = "1w2b3w4b-a"
burntPancakes(str)
