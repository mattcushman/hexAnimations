import random
from manim import *

#to run: first make sure Manim is installed
#    conda install -c conda-forge manim
# then run:
#    manim -p -ql main.py CreateHexGrid
# etc

def HexagonalTiling(m,n, scale=1.0):
    points=[]
    for i in np.arange(-m,m+1):
        for j in range(-n,n+1):
            center = np.array([scale*i*np.sqrt(3)/2, scale*j*1 + scale*i*1/2,0])
            points.append(center)
    return points



#  Create a hexagonal grid with 5 rows and 5 hexagons across
#        Then draw the centers of the hexagons and connect adjacent centers with lines
#        Then shift the scene with a skew transformation
class CreateHexGrid(Scene):
    def construct(self):
        hexgrid = HexagonalTiling(5,5)
        hexgridvg=VGroup()
        centersvg=VGroup()
        connectionsvg=VGroup()
        for h in hexgrid:
            hexgridvg.add(Line(h, h+np.array([-np.sqrt(3)/6,   -1/2,0])))
            hexgridvg.add(Line(h, h+np.array([-np.sqrt(3)/6,    1/2,0])))
            hexgridvg.add(Line(h, h+np.array([1*np.sqrt(3)/3,    0,0])))
        for h in hexgrid:
            centersvg.add(Dot(h+np.array([-np.sqrt(3)/3,0,0]), color=RED))
        for h in hexgrid:
            v = h+np.array([-1*np.sqrt(3)/3,    0,0])
            connectionsvg.add(Line(v, v + np.array([   np.sqrt(3)/2,   1/2,0])))
            connectionsvg.add(Line(v, v + np.array([  -np.sqrt(3)/2,   1/2,0])))
            connectionsvg.add(Line(v, v + np.array([0 ,   1    ,0])))
        self.play(GrowFromCenter(hexgridvg))
        self.wait()
        self.add(centersvg)
        self.wait()
        self.add(connectionsvg)
        self.wait()
        self.play(FadeOut(hexgridvg))
        self.wait()
        transformVector = [[1, 0], [-np.sqrt(3)/3, 1]]
        self.play(ApplyMatrix(np.array(transformVector), connectionsvg),
                  ApplyMatrix(np.array(transformVector), centersvg))
        self.wait()

def hexcolor(grid, x, y, d):
    d=d%3
    if x%2==0:
        x=x//2
        if d==0:
            x=x-1
        elif d==2:
            y=y-1
    else:
        x=x//2
        if d==1:
            y=y-1
            x=x+1
        elif d==2:
            y=y-1
    if y<0:
        return 0
    if (x<0 and y<9) or x>8:
        return 1
    if y>8:
        return 0
    return grid[y][x]

def turn_right(x,y,d):
    if x%2==0:
        if d==0:
            return (x-1,y+1,0)
        elif d==1:
            return (x+1,y,1)
        elif d==2:
            return (x-1,y,2)
    else:
        if d==0:
            return (x+1,y,1)
        elif d==1:
            return (x+1,y-1,2)
        elif d==2:
            return (x-1,y,0)

def turn_left(x,y,d):
    if x%2==0:
        if d==1:
            return (x-1,y+1,0)
        elif d==2:
            return (x+1,y,1)
        elif d==0:
            return (x-1,y,2)
    else:
        if d==1:
            return (x+1,y,1)
        elif d==2:
            return (x+1,y-1,2)
        elif d==0:
            return (x-1,y,0)

def point(x,y):
    scale = 0.5
    if x%2==0:
        return np.array([scale*(np.sqrt(3)/2*(x//2) - 2*np.sqrt(3) - np.sqrt(3)/6), scale*(y+ (x//2)/2 - 6 - 1/2), 0])
    else:
        return np.array([scale*(np.sqrt(3)/2*(x//2) - 2*np.sqrt(3)+ np.sqrt(3)/3 - np.sqrt(3)/6), scale*(y+ (x//2)/2 - 6 - 1/2), 0])

class CreateHexColoration(Scene):
    def construct(self):
        hexgrid = HexagonalTiling(4,4, 0.5)
        #fill 9x9 array with random 0 or 1
        hexgridcolor = np.random.randint(2, size=(9,9))
        hexgridvg=VGroup()
        membersvg=[]
        for i,h in enumerate(hexgrid):
            x = i%9
            y = i//9
            if hexgridcolor[x,y]==1:
                c=BLUE
            else:
                c=RED
            hexagon = RegularPolygon(6, color=WHITE).move_to(h).scale(0.5/np.sqrt(3))
            hexgridvg.add(hexagon)
            membersvg.append(hexagon)
        self.play(GrowFromCenter(hexgridvg))
        self.wait()
        for i,h in random.sample(list(enumerate(membersvg)), len(membersvg)):
            x = i%9
            y = i//9
            if hexgridcolor[x,y]==1:
                c=BLUE
            else:
                c=RED
            h.set_fill(c, opacity=1)
            self.wait(0.025)

        self.wait()
        self.add(Line(point(0, 0),  point(-1, 0), color=WHITE))
        self.add(Line(point(18, 0), point(19, 0), color=WHITE))
        self.add(Line(point(-2, 9),  point(-1, 9), color=WHITE))
        self.add(Line(point(17, 9), point(18, 9), color=WHITE))
        self.wait()
        x=-1
        y=0
        d=1
        n=0
        while (x,y)!=(19,0) and (x,y)!=(-2,9) and (x,y)!=(19,9) and n<150:
            n+=1
            mycolor = hexcolor(hexgridcolor, x, y, d)
            rightcolor = hexcolor(hexgridcolor, x,y, d+1)
            print(n, mycolor, rightcolor)
            if mycolor == rightcolor:
                # straight ahead color matches color to the right.  Turn left
                x1,y1,d = turn_left(x,y,d)
                print("left", x,y,d, x1,y1,d)
            else:
                x1, y1,d = turn_right(x,y,d)
                print("right", x,y,d, x1,y1,d)
            self.add(Line(point(x,y), point(x1,y1), color=PURE_RED))
            x=x1
            y=y1
            self.wait(0.2)# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
