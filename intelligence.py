
import numpy as np
import skimage

def load_image(map_filename):
    """Loads an image from a file and returns its contents in RGBA form.

    Args:
        map_filename (str): The filename of the input file

    Returns:
        ndarray: returns a 4 dimensional array where the 4 dimensions corrosponds to RGBA colours
        If no image could be loaded, this value is None
    """
    image = None
    try:
        image = skimage.io.imread(map_filename)
    except Exception as err:
        print(f"Failed to load image! Error: {err}")
        return None
    return image

def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Takes an image and returns the number of red pixels in the image

    Args:
        map_filename (str): The filename of the input image.
        upper_threshold (int, optional): The minimum red RGB value to be counted. Defaults to 100.
        lower_threshold (int, optional): The maximum non-red RGB value to be counted. Defaults to 50.

    Returns:
        ndarray: The black and white output image as a 2D array of unsigned bytes
                 If there is an error loading or writing the image files, this function will return None
    """
    image_data = load_image(map_filename)
    x_size, y_size, _ = image_data.shape
    
    # Create new ndarray without alpha layer as jpg does not support the alpha channel
    output_image_data = np.empty((x_size, y_size), np.uint8)
    
    if not type(image_data) is np.ndarray:
        print("Failed to find red pixel count! Image could not be loaded")
        return None
    
    for x in range(x_size):
        for y in range(y_size):
            current_color = image_data[x, y]
            R = current_color[0]
            G = current_color[1]
            B = current_color[2]
            # If pixel is red
            if R > upper_threshold and G < lower_threshold and B < lower_threshold:
                # Set colour to white
                output_image_data[x, y] = 255
            else:
                # Set colour to black
                output_image_data[x, y] = 0
    
    # Write the new image to file
    try:
        skimage.io.imsave("map-red-pixels.jpg", output_image_data)
    except Exception as err:
        print(f"Failed to save red pixels to file! Error: {err}")
        return None
    
    return output_image_data

def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Takes an image and writes a image to data/map-cyan-pixels.jpg containing the cyan pixels in black and white.
       This function also returns an array containing the cyan pixels

    Args:
        map_filename (str): The filename of the input image.
        upper_threshold (int, optional): The minimum non-red RGB value to be counted. Defaults to 100.
        lower_threshold (int, optional): The maximum red RGB value to be counted. Defaults to 50.

    Returns:
        ndarray: The black and white output image as a 2D array of unsigned bytes
                 If there is an error loading or writing the image files, this function will return None
    """
    image_data = load_image(map_filename)
    x_size, y_size, _ = image_data.shape
    
    # Create new ndarray without alpha layer as jpg does not support the alpha channel
    output_image_data = np.empty((x_size, y_size), np.uint8)
    
    if not type(image_data) is np.ndarray:
        print("Failed to find cyan pixel count! Image could not be loaded")
        return None
    
    for x in range(x_size):
        for y in range(y_size):
            current_color = image_data[x, y]
            R = current_color[0]
            G = current_color[1]
            B = current_color[2]
            # If pixel is red
            if R < lower_threshold and G > upper_threshold and B > upper_threshold:
                # Set colour to white
                output_image_data[x, y] = 255
            else:
                # Set colour to black
                output_image_data[x, y] = 0
    
    # Write the new image to file
    try:
        skimage.io.imsave("map-cyan-pixels.jpg", output_image_data)
    except Exception as err:
        print(f"Failed to save cyan pixels to file! Error: {err}")
        return None
    
    return output_image_data

def get_neighbors(input_array: np.ndarray, coords):
    """Returns all neighbors of a item in a 2D array. Rejects values that are not within the array bounds

    Args:
        input_image (np.ndarray): The raw array data which the neighbors will be fetched from
        coords (int, int): The coordinates where the neighbors will be fetched from

    Returns:
        list: A list of tuples representsing coordinates of valid neighbors
    """
    neighbors = []
    x, y = coords
    x_min = y_min = 0
    x_max, y_max = input_array.shape
    # Only return neighbors if they are within the array bounds
    if (x - 1 >= x_min) and (x - 1 < x_max) and (y - 1 >= y_min) and (y - 1 < y_max):
        neighbors.append((x-1, y-1))
    if (x >= x_min) and (x < x_max) and (y - 1 >= y_min) and (y - 1 < y_max):
        neighbors.append((x, y-1))
    if (x + 1 >= x_min) and (x + 1 < x_max) and (y - 1 >= y_min) and (y - 1 < y_max):
        neighbors.append((x+1, y-1))
        
    if (x - 1 >= x_min) and (x - 1 < x_max) and (y >= y_min) and (y < y_max):
        neighbors.append((x-1, y))
    if (x + 1 >= x_min) and (x + 1 < x_max) and (y >= y_min) and (y < y_max):
        neighbors.append((x+1, y))
        
    if (x - 1 >= x_min) and (x - 1 < x_max) and (y + 1 >= y_min) and (y + 1 < y_max):
        neighbors.append((x-1, y+1))
    if (x >= x_min) and (x < x_max) and (y + 1 >= y_min) and (y + 1 < y_max):
        neighbors.append((x, y+1))
    if (x + 1 >= x_min) and (x + 1 < x_max) and (y + 1 >= y_min) and (y + 1 < y_max):
        neighbors.append((x+1, y+1))
    return neighbors

def count_connected_components(mark: np.ndarray):
    """Groups connected components into a dictionary where the key is the connected component id and the
       value is the connected component size

    Args:
        mark (np.ndarray): the raw connected component data

    Returns:
        dict: the connected components grouped by id
    """
    # Empty dictionary
    connected_components = {}
    
    # Groups each connected component id into a dictionary key
    for row in mark:
        for value in row:
            if value != 0:
                if not value in connected_components.keys():
                    connected_components[value] = 1
                else:
                    connected_components[value] += 1
                           
    return connected_components

def write_connected_components_to_file(file_name, connected_components: dict):
    """Writes a dictionary containing connected component data to a file where each newline corrosponds
       to a connected component

    Args:
        file_name (str): The filename of the output text file
        connected_components (dict): the raw connected component data (Key = id, value = component size)
    """
    try:
        file = open(file_name, "w")
        for key in connected_components.keys():
            file.write(f"Connected Component {key}, number of pixles = {connected_components[key]}\n")
        file.write(f"Total number of connected components = {len(connected_components.values())}")
        file.close()
    except Exception as err:
        print(f"Failed to write connected components to file! Error: {err}")

def detect_connected_components(input_image: np.ndarray):
    """Takes an image and returns a 2D array where each value is a unique identifier for a connected component

    Args:
        input_image (np.ndarray): A 2D array which contains the strictly black and white colour data

    Returns:
        np.ndarray: A 2D array where each item corrosponds to a unique id for a connected component
    """
    
    # IMPROVMENTS AND MODIFICATIONS MADE TO ALGORITHM:
    #   Algorithm now has a counter, 'component_count,' that increments by one each time it encounters a
    #   new connected component. This counter value is used as a unique ID for each connected component.
    #   MARK[x, y] is set to the counter value, instead of 1
    
    PAVEMENT_COLOUR = 255
    NOT_VISITED = 0
    component_count = NOT_VISITED + 1
    
    x_size, y_size = input_image.shape
    # Make MAKE initally empty
    mark = np.zeros((x_size, y_size), type(int))
    # Queue is initially empty
    # Queue is sized to hold the entire MARK array, so it never runs out of memory
    queue = np.empty((x_size * y_size), dtype=type((int, int)))
    queue_ptr = 0
    
    for x in np.arange(x_size):
        for y in np.arange(y_size):
            if input_image[x, y] == PAVEMENT_COLOUR and mark[x, y] == NOT_VISITED:       
                mark[x, y] = component_count
                # Add p(x, y) to queue
                queue[queue_ptr] = (x, y)
                queue_ptr += 1
                # While queue not empty
                while queue_ptr > 0:
                    # Pop first item off queue
                    queue_ptr -= 1
                    x0, y0 = queue[queue_ptr]
                    neighbors = get_neighbors(input_image, (x0, y0))
                    for neighbor in neighbors:
                        if input_image[neighbor] == PAVEMENT_COLOUR and mark[neighbor] == NOT_VISITED:
                            mark[neighbor] = component_count
                            # Add n(s, t) to queue
                            queue[queue_ptr] = neighbor
                            queue_ptr += 1
                component_count += 1
                
    connected_components = count_connected_components(mark)
    # Sort connected connected_components by key, as they lose their order when counted with the 
    # 'count_connected_components' function
    connected_components = bullshit_sort_keys(connected_components)
    write_connected_components_to_file("cc-output-2a.txt", connected_components)
    
    return mark
    
def bullshit_sort_values(dictionary: dict):
    """Sorts a dictionary in descending order using bubblesort

    Args:
        dictionary (dict): The dictionary that will be sorted

    Returns:
        dict: The sorted dictionary
    """
    # Sorts with highest to lowest
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    for i in range(len(keys)):
        for j in range(len(values) - i - 1):
            if values[j] < values[j+1]:
                # Swap both values
                values[j], values[j+1] = values[j+1], values[j]
                # Swap both keys
                keys[j], keys[j+1] = keys[j+1], keys[j]
    
    dictionary = dict(zip(keys, values))
    return dictionary

def bullshit_sort_keys(dictionary: dict):
    """Sorts a dictionary in ascending order using bubblesort

    Args:
        dictionary (dict): The dictionary that will be sorted

    Returns:
        dict: The sorted dictionary
    """
    # Sorts with highest to lowest
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    for i in range(len(keys)):
        for j in range(len(values) - i - 1):
            if keys[j] > keys[j+1]:
                # Swap both values
                values[j], values[j+1] = values[j+1], values[j]
                # Swap both keys
                keys[j], keys[j+1] = keys[j+1], keys[j]
    
    dictionary = dict(zip(keys, values))
    return dictionary

def detect_connected_components_sorted(mark: np.ndarray):
    """Writes the connected components to "cc-output-2b.txt" in decending order and 
       Writes the largest 2 connected components to "cc-top-2.jpg" in white

    Args:
        mark (ndarray): A representation of the connected components' pixels, where
        mark's values represent the id of the connected component
    """
    # Sort connected components
    components = count_connected_components(mark)
    sorted_components = bullshit_sort_values(components)
    
    write_connected_components_to_file("cc-output-2b.txt", sorted_components)

    # Get top 2 largest components' keys
    largest_component_keys = list(sorted_components.keys())[:2]
    x_size, y_size = mark.shape
    output_image_data = np.empty((x_size, y_size), np.uint8)
    # Write white pixles for the 2 largest connected components and black otherwise
    for x in np.arange(x_size):
        for y in np.arange(y_size):
            if mark[x, y] in largest_component_keys:
                output_image_data[x, y] = 255
            else:
                output_image_data[x, y] = 0
                
    # Write the new image to file
    try:
        skimage.io.imsave("cc-top-2.jpg", output_image_data)
    except Exception as err:
        print(f"Failed to save largest connected components to file! Error: {err}")