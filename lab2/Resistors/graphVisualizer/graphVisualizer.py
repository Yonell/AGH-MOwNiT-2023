import graphviz

def getEdgeColor(current, maxCurrent):
    red = hex(int(pow(current/maxCurrent, 2/4) * 255))[2:]
    if len(red) == 1:
        red = '0' + red
    green = hex(int((pow((-current+maxCurrent)/maxCurrent, 3/4)) * 255 *1/5))[2:]
    if len(green) == 1:
        green = '0' + green
    return "#" + red + green + "00";


if __name__ == "__main__":
    g = graphviz.Digraph(engine='neato', format='png')
    inFile = open("./resistor_graph_temp.tmp", "r")

    nodesCount = int(inFile.readline())
    edgesCount = int(inFile.readline())

    edgesBeforeInit = []

    for i in range(0,edgesCount):
        first, second, resistance, current = inFile.readline().split()
        first = int(first)
        second = int(second)
        resistance = float(resistance)
        current = float(current)
        edgesBeforeInit.append([first, second, resistance, current])



    edges = []

    sem1, sem2, semVolt, semI = inFile.readline().split();
    sem1 = int(sem1)
    sem2 = int(sem2)
    semVolt = float(semVolt)
    semI = float(semI)
    

    for i in range(0,nodesCount):
        if i == sem1:
            g.node("n" + str(i), "node" + str(i), fillcolor = '#0000ff', style = 'filled')
        elif i == sem2:
            g.node("n" + str(i), "node" + str(i), fillcolor = '#ff0000', style = 'filled')
        else:
            g.node("n" + str(i), "node" + str(i), fillcolor = '#aaaaaa', style = 'filled')

    maxCurrent = max(map(lambda x : x[3], edgesBeforeInit))
    #maxCurrent = semI

    for i in edgesBeforeInit:
        edges.append(g.edge("n"+str(i[0]), 
                            "n"+str(i[1]), 
                            constraint='false', 
                            color=getEdgeColor(i[3], maxCurrent), 
                            label = ("R = " + str(i[2]) + " Ohm\nI = " + str(i[3]) + "A"), 
                            font = "times bold sans-serif",
                            fontsize = "17",
                            fontcolor='white',
                            labelfloat = "true",
                            penwidth = "5"
                            ))
        
    g.attr(bgcolor='darkblue', label=("OPORNIKI I NATEZENIA\nSEM\nU = " + str(semVolt) + "V\nI = " + str(semI) + "A"), fontcolor='white', fontsize = "30", scale = "5")
    #edges.append(g.edge("n"+str(sem1), "n"+str(sem2), constraint='false', color=getEdgeColor(semI, maxCurrent), label = ("SEM\n" + "V = " + str(semVolt) + " V\nI = " + str(semI) + "A"), fontsize = "15"))
    g.view()

    inFile.close()