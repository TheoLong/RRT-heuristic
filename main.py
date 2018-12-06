from rrt import RRT
from rrt import processFiles as pf

# main
def main():
    # read file, perpare for rrt
    # inputFile = 'input_triangle.txt'
    case = 4

    if case == 1:
        pass
        inputFile = 'input_rrt.txt'
        file = pf(inputFile)
        s,g,obs,polyObs = file.pc() 
        polyObs = [polyObs[1]]
        obs = [obs[1]]

    elif case == 2:
        inputFile = 'input_corner.txt'
        file = pf(inputFile)
        s,g,obs,polyObs = file.pc()
        
    elif case == 3:
        inputFile = 'input_triangle.txt'
        file = pf(inputFile)
        s,g,obs,polyObs = file.pc()

    elif case == 4:
        inputFile = 'input_rrt.txt'
        file = pf(inputFile)
        s,g,obs,polyObs = file.pc()  


    # run rrt
    exploreArea = [-15, 15]
    rrt = RRT(s, g, obs, polyObs, exploreArea, improved = True, stepRadius=1)
    rrt.plan()  # grow rtt
    rrt.pathStat() # print path finding statistic
    raw_input('====> press enter to terminate the program')


if __name__ == '__main__':
    main()