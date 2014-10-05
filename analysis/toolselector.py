import basic
import eventdetection as event

# Get browser instance
global browser

def set_browser(b):
    # Called by mainWindow.py to set global browser
    global browser
    browser = b

def toolselector(browser, tool):
    """ Calls the appropriate function depending
    on which tool is selected.
    """
    if tool=='Baseline':
        basic.baseline(browser)
    elif tool=='Smooth':
        basic.smooth_traces(browser)
    elif tool=='Average':
        basic.average_traces(browser)
    elif tool=='Measure':
        basic.measure_cursor_stats(browser)
    elif tool=='Event Detection':
        event.event_detect(browser)
    elif tool=='Custom':
        basic.custom_func(browser)
        
        
class ToolSelector():
    """ Class for selecting the appropriate function
    when the Analysis action is called.
    """
    
    def __init__(self):
        self.tools = []
    
    def add_tool(self, toolName, toolFunc):
        self.tools.append([toolName, toolFunc])
        
    def tool_select(self, browser, selectedTool):
        for tool in self.tools:
            if selectedTool==tool[0]: tool[1](browser)

                  
