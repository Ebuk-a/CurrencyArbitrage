from math import log, prod
from readAPI import getCurrAndRates



currencies, rates = getCurrAndRates()
"""
#Example of outputs from the getCurrAndRates function

currencies = ('BTC', 'EUR', 'JPY', 'USD')

rates = [
    [1.0, 101.16588, 14039.60311, 137.15075],
    [0.00969, 1.0, 113.35804, 1.10639],
    [8.24e-05, 0.00772, 1.0, 0.00992],
    [0.00816, 0.76448, 100.69101, 1.0]
]
"""


def negative_logarithm_convertor(graph):
    ''' log of each rate in graph and negate it'''
    result = [[-log(edge) for edge in row] for row in graph]           #Get the -ln of each rate in the rates matrix/ graph
    return result


def arbitrage(currency_tuple, rates_matrix):
    ''' Using Bellman-Ford's Algorthm (for -ve cycle) to Calculate arbitrage situations and prints out the details of this calculations'''

    trans_graph = negative_logarithm_convertor(rates_matrix)

    # Pick any source vertex -- we can run Bellman-Ford from any vertex and get the right result

    source = 0                                          
    n = len(trans_graph)                                #Length of matrix, in this particular case = 4
    min_dist = [float('inf')] * n                       #List of values = infinity. Initially assume each currency as at infinity from the source. From there find the least path
    pre = [-1] * n                                      #list of values -1. Used to track the predecessor curr that resulted in least path for each curr
    min_dist[source] = source                           # distance from a source to itself = 0



    # 'Relax edges |V-1| times'
    # A simple shortest path from src to any other vertex can have at-most |V| - 1 edges 
    # (eg BTC -> EUR, EUR -> JPY , JPY -> USD. A total of 3 edges for 4 currencies)
    for _ in range(n-1):
        for source_curr in range(n):                       #For each row in matrix (ie one particular currency conversion rates) e.g  for BTC, it is  [1.0, 101.16588, 14039.60311, 137.15075]
            for dest_curr in range(n):                     #For each destinaton curr conversion rate in the list of pairs
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:           
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr


    # The above step guarantees shortest distances if graph doesn't contain negative weight cycle.
    # If we can still relax edges, and get a shorter path, then we have a negative cycle.
    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                # negative cycle exists, and use the predecessor chain to print the cycle
                print_cycle = [dest_curr, source_curr]
                # Start from the source and go backwards until you see the source vertex again or any vertex that already exists in print_cycle array
                while pre[source_curr] not in  print_cycle:         # If predecessor of the source is not in the print_cycle list
                    print_cycle.append(pre[source_curr])            # Add predecessor of the source to the print_cycle list. There is a relationship between each
                    source_curr = pre[source_curr]                  # predecessor becomes the new source, retracing backward until the next predecessor is within the list, forming a complete cycle
                print_cycle.append(pre[source_curr])                # Add that last predecessor (the new source_curr, that closes the loop) to the end of the list. output eg  [0,2,0]
                if len(print_cycle) % 2 ==0:                        # Corrects a leakage in the process
                    print_cycle.pop(0)
                print_cycle_reversed = print_cycle[::-1]            #print_cycle list shows adjacent curr's predecessor from dest_curr -> src_curr -> src_curr_pred..., we need to reverse this to start with the currency we have.
                multiplier = []
                exchange_paths =[]            
                for indx in range(len(print_cycle_reversed)-1):              # For each currency in the list
                    exchange_paths.append([print_cycle_reversed[indx],print_cycle_reversed[indx+1]])               
                    multiplier.append(rates[print_cycle_reversed[indx]][print_cycle_reversed[indx+1]])        #call out each pair exchange rate from the rates table using the indices from the print_cycle_reversed path; and append to the multiplier list
                joined = " * ".join(str(i) for i in multiplier)                             # mimic visual multiplication ie a * b * c *...
                print("Arbitrage Opportunity: Starting with 1 " + currency_tuple[print_cycle[0]] )
                print(" --> ".join([currency_tuple[p] for p in print_cycle_reversed]))     
                print( joined + " = " + str(prod(multiplier)) + " " + currencies[print_cycle_reversed[0]] + "\n")


if __name__ == "__main__":
    arbitrage(currencies, rates)
   
