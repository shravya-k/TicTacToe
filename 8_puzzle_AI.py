from copy import deepcopy
import collections
import time
import resource
class game:
    def __init__(self):
        #Start star of the board
        self.start = [[6,1,8],[4,0,2],[7,3,5]]
        #Desired final state
        self.final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        # To find the deviation in the position of the numbers on the borad at a given situation. Gives the g(x) to find the heuristic.
        self.expected = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

# Obtain the direction which was taken.
    def finddirection(self,d):
        if d == 0:
            direction = "UP"
        elif d == 1:
            direction = "Down"
        elif d == 2:
            direction = "Left"
        elif d == 3:
            direction = "Right"
        return direction

    def misplacedtiles(self, cur):
        misp = 0
        for i in range(3):
            for j in range(3):

                if cur[i][j] != 0:
                    [a, b] = self.expected[cur[i][j]]

                    if a != i or b != j:
                        misp += 1

        return misp

    def initialise(self, cur, matrix):
        for i in range(0, 3):
            for j in range(0, 3):
                cur[i][j] = matrix[i][j]

    def findzero(self, matrix):
        for a in range(0, 3):
            for b in range(0, 3):
                if matrix[a][b] == 0:
                    i = a
                    j = b
        return [i, j]

# Heap sort applied on the nodes in the queue to find the node with the best cost.(low f(x), where f(x)=g(x)+h(x))
    def Heapify(self, q, i):
        l = (len(q) // 2) - 1
        if i <= l:
            small = i
            if (2 * i) + 1 < len(q) and q[small][0] > q[(2 * i) + 1][0]:
                small = (2 * i) + 1
            if (2 * i) + 2 < len(q) and q[small][0] > q[(2 * i) + 2][0]:
                small = (2 * i) + 2
            if small != i:
                t = q[i]
                q[i] = q[small]
                q[small] = t
                self.Heapify(q, small)
        return



    def A(self, cur):
        q = []
        q.append((0,cur, 0))
        t = tuple(map(tuple, cur))
        dic = collections.defaultdict(int)
        d1 = [1, -1, 0, 0]
        d2 = [0, 0, 1, -1]
        predecessor=collections.defaultdict(list)
        predecessor[t]=(0,'None')
        while q:
            (f,matrix, cost) = q[0]
            parent = tuple(map(tuple, matrix))
            q[0]=q[-1]
            q.pop()
            self.Heapify(q,0)
            if parent in dic:
                continue
            if matrix == self.final:
                print('Reached via A* algorithm! the cost of the pasth is:', cost)
                (prev,direction)=predecessor[parent]
                res=[]
                while prev:
                    res.append(direction)
                    (prev, direction)=predecessor[prev]
                print('The path of the search is:',res[::-1])
                return
            dic[parent] = f
            k = []
            [i, j] = self.findzero(matrix)
            for d in range(0, 4):
                if (i + d1[d]) < 0 or (j + d2[d]) < 0 or (i + d1[d]) >= 3 or (j + d2[d]) >= 3:
                    continue
                cur = deepcopy(matrix)
                cur[i][j] = matrix[i + d1[d]][j + d2[d]]
                cur[i + d1[d]][j + d2[d]] = 0
                t = tuple(map(tuple, cur))
                f = (self.misplacedtiles(cur)) + (cost + 1) # Heauristic f(x) for A*: g(x) (Cost from the current node to the final state) + h(x) (Cost from the start to the current node)
                if t in dic:
                    continue
                q.append((f,cur, cost + 1))
                direction = self.finddirection(d)
                predecessor[t]=(parent,direction)
            l = (len(q) // 2) - 1
            for lef in range(l, -1, -1):
                self.Heapify(q, lef)

    def BFS(self,cur):
        start=cur
        predecessor = collections.defaultdict(list)
        predkey = 1
        id = 0
        visited=set()
        q=[]
        qq=[]
        exp=0

        if cur not in visited:
            visited.add(cur)
        d1=[1,-1,0,0] #change for dfs
        d2=[0,0,1,-1]
        predecessor[1].append((-1, -1))
        q.append((cur,0,cur,-1))
        res=[]
        while q:
            exp += 1
            curpop,curcost,parent,key=q.pop(0) #changes for dfs
            if curpop==tuple(map(tuple,self.final)):
                direction,parent,parentkey=predecessor[key].pop()
                while parent!=start:
                    res.append(direction)
                    direction,parent, parentkey = predecessor[parentkey].pop()
                res.append(direction)
                print("Reached! via BFS algorithm",curcost)
                print("The path taken to reach:",res[::-1])
                print('The total nodes expanded:',exp)
                return
            for fini in range(3):
                for finj in range(3):
                    if curpop[fini][finj]==0:
                        i=fini
                        j=finj
                        break


            for d in range(0,4):

                copycurpop = list(map(list, deepcopy(curpop)))
                if i+d1[d]<0 or j+d2[d]<0 or i+d1[d]>=3 or j+d2[d]>=3:
                    continue
                copycurpop[i][j]=copycurpop[i+d1[d]][j+d2[d]]
                copycurpop[i + d1[d]][j + d2[d]]=0
                copycurpop = tuple(map(tuple,copycurpop))
                if (copycurpop in visited):
                    continue

                predkey+=1
                direction=self.finddirection(d)
                predecessor[predkey].append((direction,curpop,key))
                q.append((copycurpop,curcost+1,curpop,predkey))
                visited.add(copycurpop)


    def DFS(self,cur):
        start=cur
        predecessor = collections.defaultdict(list)
        predkey = 1
        id = 0
        visited=set()
        q=[]
        qq=[]
        exp=0

        if cur not in visited:
            visited.add(cur)
        d1=[0,0,1,-1] #changes for bfs
        d2=[1,-1,0,0]
        predecessor[1].append((-1, -1))
        q.append((cur,0,cur,-1))
        res=[]
        while q:
            exp += 1
            curpop,curcost,parent,key=q.pop() #changes for bfs
            if curpop==tuple(map(tuple,self.final)):

                direction,parent,parentkey=predecessor[key].pop()
                while parent!=start: #once the final state reaches, backtrack till the root node to record all the nodes which come on way. print the reversed array to display the path.
                    res.append(direction)
                    direction,parent, parentkey = predecessor[parentkey].pop()
                res.append(direction)
                print("Reached! via the DFS algorithm with a cost of:",curcost)
                print("The path taken to reach:",res[-1])
                print("The total nodes expanded",exp)
                return
            for fini in range(3):
                for finj in range(3):
                    if curpop[fini][finj]==0:
                        i=fini
                        j=finj
                        break
            for d in range(0,4):
                copycurpop = list(map(list, deepcopy(curpop)))
                if i+d1[d]<0 or j+d2[d]<0 or i+d1[d]>=3 or j+d2[d]>=3:
                    continue
                copycurpop[i][j]=copycurpop[i+d1[d]][j+d2[d]]
                copycurpop[i + d1[d]][j + d2[d]]=0
                copycurpop = tuple(map(tuple,copycurpop))
                if (copycurpop in visited):
                    continue
                predkey+=1
                if d==0:
                    direction="UP"
                elif d==1:
                    direction="Down"
                elif d==2:
                    direction="Left"
                elif d==3:
                    direction ="Right"

                predecessor[predkey].append((direction,curpop,key))
                q.append((copycurpop,curcost+1,curpop,predkey))
                visited.add(copycurpop)



def main():
    obj=game()
    val = input("Enter your value: ")

    start = time.time()
    if val=='A':
        obj.A(obj.start)
    if val=='B':
        obj.BFS(tuple(map(tuple,obj.start)))
    if val=='D':
        obj.DFS(tuple(map(tuple, obj.start)))
    end = time.time()
    print('Running time:',float(end-start),'seconds')
    max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024
    print('RAM Usage:', max_ram_usage)

if __name__ == '__main__':
    main()
'''
Sample outputs:

DFS:
Enter your value: D
Reached! via the DFS algorithm with a cost of: 46142
The total nodes expanded 51016
"The path taken to reach:" ['Right' .........'Right', 'Down', 'Left', 'Left', 'UP', 'UP', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'UP', 'UP', 'Right', 'Down', 'Right', 'Down']
The total nodes expanded 51016
Running time: 8.185726165771484 seconds
RAM Usage: 65.5

A:

Enter your value: AReached via A* algorithm! the cost of the pasth is: 20
The path of the search is: ['UP', 'Left', 'Down', 'Down', 'Right', 'UP', 'Left', 'UP', 'Right', 'Down', 'Right', 'Down', 'Left', 'Left', 'UP', 'UP', 'Right', 'Right', 'Down', 'Down']
Running time: 4.8219828605651855 seconds
RAM Usage: 12.3984375


BFS:

Reached! via BFS algorithm 20
The path taken to reach: ['UP', 'Left', 'Down', 'Down', 'Right', 'UP', 'Left', 'UP', 'Right', 'Down', 'Right', 'Down', 'Left', 'Left', 'UP', 'UP', 'Right', 'Right', 'Down', 'Down']
The total nodes expanded: 45168
Running time: 7.6360838413238525 seconds
RAM Usage: 49.84375


'''