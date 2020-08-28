import subprocess
from datetime import datetime

INPUT_FILE = "nodes.txt"
FILE_NOT_PINGABLE = 'non_pingable_{}'
FILE_PINGABLE = 'pingable_{}'


def write_to_file(node_list, filename):

    with open(filename, 'w') as filehandler:
        for node in node_list:
            filehandler.write(node)
            filehandler.write('\n')

def write_to_screen(node_list, title='RESULTS'):
    print('PINGABLE NODES:')
    print('=' * 16)
    
    for node in node_list:
        print(node)

    print()

def is_pingable(host, timeout=50):
    #  If the result is 0, the node is pingable
    #  All other values were not pingable
    try:
        result = subprocess.call(
            ["ping", "-c", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout
        )

        if result == 0:
            result = True
        else:
            result = False
        
    except:
        result = False
    
    return result
    


if __name__ == "__main__":

    # build list of nodes
    with open(INPUT_FILE) as filehandler:
        nodes = filehandler.read().split('\n')
    
    # List for results
    pingable_nodes = []
    non_pingable_nodes = []

    # Pinging nodes and assigning to list
    for node in nodes:
        if is_pingable(node):
            pingable_nodes.append(node)
        else:
            non_pingable_nodes.append(node)
    
    # Writing to screen
    write_to_screen(pingable_nodes, 'PINGABLE NODES:')
    write_to_screen(non_pingable_nodes, 'NON-PINGABLE NODES:')
    
    # Write results to file, using a timestamp to keep unique filename between
    # connsecutive script execution
    timestamp = datetime.now().isoformat()
    write_to_file(pingable_nodes, FILE_PINGABLE.format(timestamp))
    write_to_file(non_pingable_nodes, FILE_NOT_PINGABLE.format(timestamp))