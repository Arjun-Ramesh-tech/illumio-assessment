"""
Author: Arjun Ramesh
Date: 2024-11-13
Time taken to write the code: 48 mins
Description: Program to parse flow log data, match tags based on a lookup table, and output counts of tags and port/protocol combinations.
"""
import csv
from collections import defaultdict

LOG_COLUMN_MAP = {
    "version": 0,
    "account_id": 1,
    "interface_id": 2,
    "src_addr": 3,
    "dst_addr": 4,
    "dstport": 5,
    "srcport": 6,
    "protocol": 7,
    "packets": 8,
    "bytes": 9,
    "start": 10,
    "end": 11,
    "action": 12,
    "log_status": 13
}

def load_protocol_mapping(csv_file: str) -> dict:
    """
    Load the protocol mappings from a CSV file.
    
    Input:
    - csv_file: str, path to the CSV file containing protocol mappings with columns 
      'Decimal' and 'Protocol'.
      
    Output:
    - protocol_map: dict, a dictionary with protocol numbers (as strings) as keys and protocol names as values.
      
    Logic:
    Reads the CSV file and stores each protocol number and name in a dictionary.
    """
    protocol_map = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            protocol_number = row['Decimal'].strip()
            protocol_name = row['Keyword'].strip()
            protocol_map[protocol_number] = protocol_name
    return protocol_map

def load_lookup_table(lookup_file: str) -> dict:
    """
    Load the lookup table from a CSV file.
    
    Input:
    - lookup_file: str, path to the CSV file containing lookup mappings with columns 'dstport', 'protocol', 'tag'.
      
    Output:
    - lookup_dict: dict, a dictionary with (dstport, protocol) as keys and tag as values.
    
    Logic:
    Reads the lookup file row by row, storing each (dstport, protocol) combination as a key in a dictionary (case-insensitive for protocol), and maps it to the corresponding tag.
    """
    lookup_dict = {}
    with open(lookup_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            key = (row['dstport'].strip(), row['protocol'].strip().lower())
            lookup_dict[key] = row['tag'].strip()
    return lookup_dict

def parse_flow_logs(flow_log_file, lookup_dict, protocol_mapping):
    """
    Parse the flow log data and map each entry to a tag using the lookup table.
    
    Input:
    - flow_log_file: str, path to the text file containing flow log entries in version 2 format.
    - lookup_dict: dict, dictionary with (dstport, protocol) as keys and tags as values.
    
    Output:
    - tag_counts: defaultdict(int), a dictionary with tags as keys and the count of each tag as values.
    - port_protocol_counts: defaultdict(int), dictionary with (dstport, protocol) as keys and the 
      count of each combination as values.
    
    Logic:
    Reads each log entry, extracts `dstport` and `protocol`, and checks if it matches any entry in 
    the lookup dictionary. If a tag is found, it increments the count for that tag; otherwise, it 
    increments the count for "Untagged". It also counts each port/protocol combination seen.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    with open(flow_log_file, 'r') as file:
        for line in file:
            columns = line.split()
            if len(columns) != len(LOG_COLUMN_MAP):
                continue 
            dstport = columns[LOG_COLUMN_MAP["dstport"]]
            protocol = protocol_mapping.get(columns[LOG_COLUMN_MAP["protocol"]],"Undefined").lower()
            tag = lookup_dict.get((dstport, protocol), "Untagged")
            tag_counts[tag] += 1
            port_protocol_counts[(dstport, protocol)] += 1
    
    return tag_counts, port_protocol_counts

def write_output(tag_counts: defaultdict, port_protocol_counts: defaultdict, output_file: str) -> None:
    """
    Write the tag counts and port/protocol combination counts to an output file.

    Input:
    - tag_counts: defaultdict(int), tags -> count
    - port_protocol_counts: defaultdict(int), (dstport, protocol) -> count
    - output_file: str, path to the file where the results will be written.

    Output:
    - None (results are written to `output_file`)

    Logic:
    Writes two sections to the output file: "Tag Counts" and "Port/Protocol Combination Counts". 
    The first section lists each tag and its count. The second section lists each port/protocol combination and its count.
    """
    with open(output_file, 'w') as file:
        file.write("Tag Counts:\nTag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        
        file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    """
    Main function to execute the program workflow:

    Steps:
    1. Load the lookup table.
    2. Parse the flow logs and map entries to tags.
    3. Write the results to an output file.

    Input/Output:
    - None

    Logic:
    Defines the file paths, loads data from the lookup table, processes the flow logs, and 
    generates an output file with the required tag and port/protocol combination counts.
    """
    protocol_mapping = load_protocol_mapping('inputfiles/protocol_number_mapping.csv')
    lookup_file = "inputfiles/lookup_table_refer.csv"
    flow_log_file = "inputfiles/flow_log_data.txt"
    output_file = "outputfiles/output_counts.txt"
    
    lookup_dict = load_lookup_table(lookup_file)
    tag_counts, port_protocol_counts = parse_flow_logs(flow_log_file, lookup_dict, protocol_mapping)
    
    write_output(tag_counts, port_protocol_counts, output_file)
    print("Processing complete. Results saved to", output_file)

if __name__ == "__main__":
    main()