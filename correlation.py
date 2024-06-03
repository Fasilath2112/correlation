# Import the json module to handle JSON data
# Import the sqrt function to compute square roots
import json  
from math import sqrt  
# Open the specified journal file in read mode
 # Parse the JSON data from the file and return it
def load_journal(filename):
    with open(filename, 'r') as file:  
        return json.load(file) 

def compute_phi(journal, event):
   
    # Initialize counts to zero
    n11 = n00 = n10 = n01 = 0  
    for entry in journal:  
        # Check if the event occurred and if the transformation happened
        events, squirrel = event in entry['events'], entry['squirrel']
        n11 += events and squirrel  # Increment n11 if both the event and transformation occurred
        n10 += events and not squirrel  
        n01 += not events and squirrel  
        n00 += not events and not squirrel  

    # Calculate the totals for the event occurring and not occurring
    n1_plus = n11 + n10  
    n0_plus = n01 + n00  
    # Calculate the totals for the transformation occurring and not occurring
    n_plus_1 = n11 + n01  
    n_plus_0 = n10 + n00  

    # Check if any denominator in the correlation formula would be zero
    if n1_plus * n0_plus * n_plus_1 * n_plus_0 == 0:  
        return 0  # Return 0 to avoid division by zero if any of the terms are zero

    # Compute and return the phi coefficient using the formula for correlation
    return (n11 * n00 - n10 * n01) / sqrt(n1_plus * n0_plus * n_plus_1 * n_plus_0)

def compute_correlations(journal):
    #Compute the correlations for all events in the journal
    # Extract a set of all unique events from the journal entries
    events = {event for entry in journal for event in entry['events']}  
    # Compute the phi coefficient for each unique event and return as a dictionary
    return {event: compute_phi(journal, event) for event in events}  

def diagnose(filename):
    #Find the most positively and negatively correlated events with the squirrel transformation
    journal = load_journal(filename)  # Load the journal data from the specified file
    correlations = compute_correlations(journal)  # Compute the correlations for all events
    max_event = max(correlations, key=correlations.get)  # Find the event with the highest positive correlation
    min_event = min(correlations, key=correlations.get)  # Find the event with the highest negative correlation
    return max_event, min_event  # Return the most positively and negatively correlated events

if __name__ == "__main__":
    filename = 'journal.json'  # Specify the journal file path
    # Diagnose the correlations in the journal and get the most correlated events
    most_pos, most_neg = diagnose(filename)  
    # Print the most positively correlated event
    print(f"Most positively correlated event: {most_pos}")  
    # Print the most negatively correlated event
    print(f"Most negatively correlated event: {most_neg}")  
