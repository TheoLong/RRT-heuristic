from rrt import RRT
from rrt import processFiles as pf

# main
def main():
    # append and switch case to the map you want to run rrt

    case = 10

    # box
    if case == 1:
        inputFile = 'maps/box.txt'

    # corner
    elif case == 2:
        inputFile = 'maps/corner.txt'
       
    # triangle 
    elif case == 3:
        inputFile = 'maps/triangle.txt'

    # maze
    elif case == 4:
        inputFile = 'maps/maze.txt'

    # drillfield
    elif case == 5:
        inputFile = 'maps/drillfield.txt'

    # military_base
    elif case == 6:
        inputFile = 'maps/military_base.txt'

    # prison
    elif case == 7:
        inputFile = 'maps/prison.txt'

    # ruins
    elif case == 8:
        inputFile = 'maps/ruins.txt'

    # school
    elif case == 9:
        inputFile = 'maps/school.txt'

    # shooting_range
    elif case == 10:
        inputFile = 'maps/shooting_range.txt'

    else:
        exit('Error: no such map')


    # process input maps
    file = pf(inputFile)
    s,g,obs,polyObs = file.pc() 

    # run rrt
    exploreArea = [0, 15]
    rrt = RRT(s, g, obs, polyObs, exploreArea, improved = False, stepRadius=0.9)
    rrt.plan()  # grow rtt
    rrt.pathStat() # print path finding statistic
    raw_input('====> press enter to terminate the program')


if __name__ == '__main__':
    main()