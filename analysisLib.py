import numpy as np

def baseline(browser):
    plotsWidget = browser.ui.plotsWidget
    # get data
    data = getData(browser)
    # get cursors positions
    c1, c2 = getCursors(plotsWidget)
    # make average between cursors and subract for each trace
    dataIndex = browser.ui.plotsWidget.plotDataIndex
    for t in range(len(data)):
        bsl = np.mean(data[t][c1:c2])
        browser.ui.workingTree.data[dataIndex[t]] = data[t]-bsl
        print browser.ui.workingTree.data[dataIndex[t]]
    # refresh plot



# Aux functions
def getCursors(plotsWidget):
    c1 = plotsWidget.cursor1Pos 
    c2 = plotsWidget.cursor2Pos
    if c2<c1:        
        temp = c2
        c2 = c1
        c1 = temp
    return int(c1), int(c2)
    
def getData(browser):
    data = []
    for index in browser.ui.plotsWidget.plotDataIndex:
        data.append(browser.ui.workingTree.data[index])
    data = np.array(data)
    return data
