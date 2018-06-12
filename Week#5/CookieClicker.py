"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 16.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("[total_cookies:"+str(self._total_cookies)+
                ", current_cookies:"+str(self._current_cookies)+
                ", current_time:"+str(self._current_time)+
                ", cps:"+str(self._cps)+"]")
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            time_need = 0.0
        else:
            time_need = math.ceil((cookies-self._current_cookies)/self._cps)
        
        return time_need
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        
        if time <= 0.0 :
            return
        else:
            self._current_time += time
            self._current_cookies += time*self._cps
            self._total_cookies += time*self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies < cost:
            return
        else:
            self._history.append((self._current_time,item_name,cost,self._total_cookies))
            self._current_cookies -= cost
            self._cps += additional_cps
   
  
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    # Replace with your code
    new_binfo = build_info.clone()
    new_clickstate = ClickerState()
    
    while new_clickstate.get_time() < duration:
        #print new_clickstate.get_time()
        stg_item = strategy(new_clickstate.get_cookies(),
                            new_clickstate.get_cps(),
                            new_clickstate.get_history(),
                            duration - new_clickstate.get_time(),
                            new_binfo)
        
        while stg_item != None:
            
            cost = new_binfo.get_cost(stg_item)
            time_stg_item = new_clickstate.time_until(cost)
            
            if new_clickstate.get_time()+time_stg_item > duration:
            
                new_clickstate.wait(duration-new_clickstate.get_time())
                return new_clickstate
            
            new_clickstate.wait(time_stg_item)
            
            new_clickstate.buy_item(stg_item, cost, new_binfo.get_cps(stg_item))
            
            new_binfo.update_item(stg_item)
            
            stg_item = strategy(new_clickstate.get_cookies(),
                            new_clickstate.get_cps(),
                            new_clickstate.get_history(),
                            duration - new_clickstate.get_time(),
                            new_binfo)
            
            
        new_clickstate.wait(duration-new_clickstate.get_time())
        
    return new_clickstate


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies. Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    if (cookies+cps*time_left) < build_info.get_cost("Cursor"):
        return None
    else:
        return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cheapest_item_cost = float("inf")
    cheapest_item = None
    
    items = build_info.build_items()
    
    for item in items:
        if build_info.get_cost(item) < cheapest_item_cost:
            cheapest_item_cost = build_info.get_cost(item)
            cheapest_item = item
    
    if (cookies+cps*time_left) < cheapest_item_cost:
        cheapest_item = None
    
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    
    expe_item = None
    
    price_item = []
    
    items = build_info.build_items()
    
    
    
    for item in items:
        price_item.append((build_info.get_cost(item),item))
        
    price_item.sort(reverse=True)
    
    for item_cost in price_item:
        if (cookies+cps*time_left) >= item_cost[0]:
            expe_item = item_cost[1]
            return expe_item
        else:
            expe_item = None
    
    return expe_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    best_item = None
    
    price_cps_ratio = []
    
    items = build_info.build_items()
    
    for item in items:
        price_cps_ratio.append((build_info.get_cost(item)/build_info.get_cps(item),item))
    
    price_cps_ratio.sort()
    
    for val in price_cps_ratio:
        item = val[1]
        if (cookies+cps*time_left) >= build_info.get_cost(item):
            best_item = item
            return best_item
        else:
            best_item = None
    
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
#run()

#print strategy_expensive(500000.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
#simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, strategy_cursor_broken)
    

