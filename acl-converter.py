import ipaddress
import sys

def read_lines_from_acl() -> list:
    """Function to read the lines from an ACL, strip the ACL name
    and store the result in a list."""
    # Check that both filename and prefix-list name has been supplied
    if len(sys.argv) == 3:
        # Get the filename
        file_name = sys.argv[1]
    else:
        print("Incorrect syntax used. The correct syntax is acl-converter "
             "filename prefix-list-name")
    # Open the file and store results in a list
    with open(file_name, "r") as fh:
        acl_lines = fh.read().splitlines()
    # Remove the access-list name
    del acl_lines[0]
    
    # changed to use list comprehension as example for daniel :)
    return = [line.strip() for line in acl_lines]
    
def get_prefix_list_name() -> str:
    pl_name = sys.argv[2]
    return pl_name

def convert_acl_to_prefix_list(acl_list: list, pl_name: str) -> list:
    """Takes the list from function read_lines_from_acl
    and converts it to prefix-list syntax."""
    # Create a new list to use for the prefix-list
    prefix_list_list = []
    # Prefix-list name to append to each line, except for remarks
    prefix_list_name = f"ip prefix-list {pl_name}"
    # Counter for sequence numbers in the prefix-list, start at 10
    pl_seq = 10
    # Iterate through the acl_list
    for line in acl_list:
        # Check if permit or deny in line
        if "permit" or "deny" in line:
            # Check for any statement
            if "any" in line:
                # Split string into list
                temp_list = line.split()
                # Create string to insert in prefix-list
                temp_string = f"{prefix_list_name} seq {pl_seq} {temp_list[0]} 0.0.0.0/0 le 32"
                # Append to the prefix-list list
                prefix_list_list.append(temp_string)
                # Increase the counter
                pl_seq += 5
            # Check for remarks        
            elif "remark" in line:
                # If remark, simply add the string unmodified to the prefix-list
                prefix_list_list.append(line)
            else:
                # Split the string into three separate strings and put in a temp list
                temp_list = line.split()
                # Create an IP address network object
                temp_network = ipaddress.IPv4Network(f"{temp_list[1]}/{temp_list[2]}")
                # Convert to CIDR notation
                new_network = temp_network.with_prefixlen
                # Create string to insert in prefix-list
                temp_string = f"{prefix_list_name} seq {pl_seq} {temp_list[0]} {new_network} le 32"
                # Append to the prefix-list list
                prefix_list_list.append(temp_string)
                # Increase the counter
                pl_seq += 5
    return prefix_list_list

def save_prefix_list_to_file(pl_name: str, prefix_list: list) -> None:
    """Function to save the lines from the prefix-list list
    to a text file."""
    with open(pl_name, "w") as fh:
        for line in prefix_list:
            fh.write(line +"\n")

acl_lines = read_lines_from_acl()
pl_name = get_prefix_list_name()
prefix_list = convert_acl_to_prefix_list(acl_lines, pl_name)
save_prefix_list_to_file(pl_name, prefix_list)



    
