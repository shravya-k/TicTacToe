
class tictactoe:
    def __init__(self):
        self.ori=[['x','',''],['x','',''],['o','','x']]
        self.chance=0

    def freecell(self,grid):
        res=[]
        for i in range(3):
            for j in range(3):
                if grid[i][j]=='':
                    res.append([i,j])
        return res
    def maywin(self,grid,player):

        win_pos=[[grid[0][0],grid[0][1],grid[0][2]],
                 [grid[1][0],grid[1][1],grid[1][2]],
                 [grid[2][0],grid[2][1],grid[2][2]],
                 [grid[0][0],grid[1][1],grid[2][2]],
                 [grid[0][2],grid[1][1],grid[2][0]],
                 [grid[0][0],grid[1][0],grid[2][0]],
                 [grid[0][1],grid[1][1],grid[2][1]],
                 [grid[0][2],grid[1][2],grid[2][2]]
                  ]

        if [player,player,player] in win_pos:
            return True
        return False

    def endgame(self,grid):

        for i in range(3):
            for j in range(3):
                if grid[i][j]=='':
                    return False
        return True

    def evaluate(self,grid,player):

        if self.maywin(grid,player):
            if player=='x':
                return 1
            if player=='o':
                return -1

        if self.endgame(grid):
            return 0


    def minimax(self,matrix,depth):

        if depth%2==0:
            player='o'
        else:
            player='x'

        if player=='x':  #human
            basic=[-1,-1,-float('inf')]
        else:
            basic=[-1,-1,float('inf')]

        self.maxdepth= -float('inf')
        if self.maywin(matrix,player) or self.endgame(matrix):
            print('result',depth,self.evaluate(matrix,player))
            return [-1,-1,self.evaluate(matrix,player)]
        freecells = self.freecell(matrix)
        for f in range(len(freecells)):
            [i,j] = freecells[f]
            matrix[i][j]= player
            [a,b,score]=self.minimax(matrix,depth+1)
            self.chance+=1
            basic[0]=i
            basic[1]=j
            if player=='x':
                print(player, score)
                basic[2]=max(basic[2],score)
                if basic[2]!=-float('inf'): #Minimax optimisation: a>=b. Since we already found the least (-1) upcoming scores can be safely ignored as final score is already found!
                    print(basic, player)
                    return basic

            if player=='o':
                print(player,score)
                basic[2] = min(basic[2], score)
                if basic[2]!=float('inf'): #Minimax optimisation: a>=b. Since we already found the Max (1) upcoming scores can be safely ignored as final score is already found!
                    print(basic,player)
                    return basic


            self.maxdepth=max(self.maxdepth,depth)
            matrix[i][j]=''
        return basic





if __name__ == '__main__':
    obj=tictactoe()
    print(obj.minimax(obj.ori,1))
