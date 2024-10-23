
from os import system

import numbers

def clear_screen():
    """Clears the screen using the system
    """
    system('cls||clear')

def sumvalues(values):
    """Computes the sum of all the values in a list/array

    Args:
        values (list / np.array): the list or array of input values
        
    Exceptions:
        Raises an exception if not all the values are numerical

    Returns:
        int: The total sum
    """
    # Raises exception if list/array contains non-numeric values
    for value in values:
        float(value)

    accumulator = 0
    for value in values:
        accumulator += value
    return accumulator


def maxvalue(values):
    """Computes the maximum of all the values in a list/array

    Args:
        values (list / np.array): the list or array of input values
        
    Exceptions:
        Raises an exception if not all the values are numerical

    Returns:
        int: The maximum value in the list/array
    """
    # Raises exception if list/array contains non-numeric values
    for value in values:
        float(value)
    
    current_max = values[0]
    for value in values:
        if value > current_max:
            current_max = value
    return current_max


def minvalue(values):
    """Computes the minimum of all the values in a list/array

    Args:
        values (list / np.array): the list or array of input values
        
    Exceptions:
        Raises an exception if not all the values are numerical

    Returns:
        int: The mimumum
    """
    # Raises exception if list/array contains non-numeric values
    for value in values:
        float(value)
    
    current_min = values[0]
    for value in values:
        if value < current_min:
            current_min = value
    return current_min


def meannvalue(values):
    """Computes the mean of all the values in a list/array

    Args:
        values (list / np.array): the list or array of input values
        
    Exceptions:
        Raises an exception if not all the values are numerical

    Returns:
        int: The mean of the list/array
    """
    # Raises exception if list/array contains non-numeric values
    for value in values:
        float(value)
    
    return sumvalues(values) / len(values)


def countvalue(values, target):
    """Gives the number of occournces of an value in an list/array

    Args:
        values (list / np.array): the list or array of input values
        
    Exceptions:
        Raises an exception if not all the values are numerical

    Returns:
        int: The count of values matching the target value
    """
    # Raises exception if list/array contains non-numeric values
    for value in values:
        float(value)

    counter = 0
    for value in values:
        if value == target:
            counter += 1
    return counter
