import json
import re
from urllib.request import urlopen


def getCurrAndRates(api_str="https://api.swissborg.io/v1/challenge/rates"):
    """Accepts a string api address link and returns tuple(currencies) and list(order2matrix of rates)"""
    graph = {}
    page = urlopen(api_str)                         #Read the exchange rates into jsrates
    jsrates = json.loads(page.read())


    pattern = re.compile("([A-Z]{3})-([A-Z]{3})")   #create a regex string pattern object to call out currency pairs e.g 'BTC-USD'
    for key in jsrates:                             # iterate over the keys
        matches = pattern.match(key)                # find matching strings(keys) with the pattern ie 'BT-USDC'
        from_rate = matches.group(1)                # strip out the first currency 'BTC' from the matched pair 'BTC-USD'
        to_rate = matches.group(2)                  # strip out the second currency 'USD' from the matched pair 'BTC-USD'
        if from_rate not in graph:                  # if first currency not in dictionary graph = {}
            graph[from_rate] = {}                   # Add it and assigned value of empty dictionary  ie graph = {'BTC': {}}
        graph[from_rate][to_rate] = float(jsrates[key])     #insert the second currency and its conversion rate to the nested dictionary ie {'BTC': {'USD': 14039}}. Rinse and repeat for all keys
    src_sorted_graph = dict((sorted(graph.items())))        #sort the graph dictionary by the graph key. 


    curr = []                                       #array to hold currencies
    [curr.append(x) for x in graph]                 #call out all the graph keys (currencies) and append to list, curr
    sorted_currencies = tuple(sorted(curr))         #sort currency list and convert to tuple eg ('BTC','EUR', 'JPY', 'USD'), this allows corect mapping to th second order matrix of rates


    rates = []                                      #array to hold the currencies as a matrix of order 2 (since conversion happens between two currencies)
    for src_xch_rates in src_sorted_graph.values():             #for each of the currencies/keys in the sorted graph dictionary
        src_rates_sorted = dict(sorted(src_xch_rates.items()))  #sort the items on nexted dictionary eg for BTC. {'BTC': {'BTC': 1,'EUR': 100.7, 'JPY: 136.60,'USD': 14039,}})
        rate_vals = []
        [rate_vals.append(k) for k in src_rates_sorted.values()] #for each BTC conversion rate within the sorted values, add to a list, rate_vals
        rates.append(rate_vals)                                  # insert each list of rates for each currency into another list forming a  matrix. This forms a second order matrix of rates, with diagonals = 1.
          

    return sorted_currencies, rates                 #return the currencies' tuple and rates' list (matrix)

if __name__ == "__main__":
    currencies, rates = getCurrAndRates()
    print(currencies)
    print(rates)