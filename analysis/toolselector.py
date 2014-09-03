import basic
import eventdetection as event

def toolselector(browser, tool):
    """ Calls the appropriate function depending
    on which tool is selected.
    """
    if tool=='Baseline':
        basic.baseline(browser)
    elif tool=='Average':
        basic.average_traces(browser)
    elif tool=='Measure':
        basic.measure_cursor_stats(browser)
    elif tool=='Event Detection':
        event.event_detect(browser)
