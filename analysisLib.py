import numpy as np
from h5TreeWidgetFile import h5Item

def baseline(browser):
    plotsWidget = browser.ui.plotsWidget
    data = getData(browser)
    c1, c2 = getCursors(plotsWidget)
    # make average between cursors and subract for each trace
    dataIndex = browser.ui.plotsWidget.plotDataIndex
    plotsWidget.canvas.ax.clear()
    for t in range(len(data)):
        bsl = np.mean(data[t][c1:c2])
        browser.ui.workingTree.data[dataIndex[t]] = data[t]-bsl
        plotsWidget.canvas.ax.plot(browser.ui.workingTree.data[dataIndex[t]], 'k', linewidth=0.5)
    plotsWidget.canvas.draw()        
    plotsWidget.homeAxis = plotsWidget.canvas.ax.axis() 
    plotsWidget.background = plotsWidget.canvas.copy_from_bbox(plotsWidget.canvas.ax.bbox)
    plotsWidget.createCursor()
    if browser.ui.actionShowCursors.isChecked(): 
        browser.ui.actionShowCursors.setChecked(False)
        #x1,x2,y1,y2 = plotsWidget.canvas.ax.axis()
        #plotsWidget.cursor1.set_data([plotsWidget.cursor1Pos, plotsWidget.cursor1Pos], [y1,y2])         
        #plotsWidget.cursor2.set_data([plotsWidget.cursor2Pos, plotsWidget.cursor2Pos], [y1,y2]) 
        #plotsWidget.cursor1.set_visible(True)
        #plotsWidget.cursor2.set_visible(True)                 
        #plotsWidget.canvas.ax.draw_artist(plotsWidget.cursor1) 
        #plotsWidget.canvas.ax.draw_artist(plotsWidget.cursor2)         
        #plotsWidget.canvas.blit(plotsWidget.canvas.ax.bbox)         

def average(browser):
    plotsWidget = browser.ui.plotsWidget
    data = getData(browser)   
    avgData = np.mean(data,0)
    # Make tree and data entry with result
    item = h5Item(['Avg'])
    browser.ui.workingTree.addTopLevelItem(item)
    item.dataIndex = len(browser.ui.workingTree.data)
    browser.ui.workingTree.data.append(avgData)
    # Plot average 
    plotsWidget.canvas.ax.clear()
    plotsWidget.canvas.ax.plot(avgData, 'r', linewidth=1)
    plotsWidget.canvas.draw()     

def measureStats(browser):
    # Min Max Area
    plotsWidget = browser.ui.plotsWidget
    data = getData(browser)
    c1, c2 = getCursors(plotsWidget)
    dataIndex = browser.ui.plotsWidget.plotDataIndex    
    dataMin, dataMax = [], []
    for t in range(len(data)):
        dataMin.append(np.min(data[t][c1:c2]))
        dataMax.append(np.max(data[t][c1:c2]))
    # Make tree and data entry with results
    item = h5Item(['Min'])
    browser.ui.workingTree.addTopLevelItem(item)
    item.dataIndex = len(browser.ui.workingTree.data)
    browser.ui.workingTree.data.append(np.array(dataMin))
    item = h5Item(['Max'])
    browser.ui.workingTree.addTopLevelItem(item)
    item.dataIndex = len(browser.ui.workingTree.data)
    browser.ui.workingTree.data.append(np.array(dataMax))
        
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
