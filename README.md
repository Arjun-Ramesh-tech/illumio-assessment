# Flow Log Parser

### Author: Arjun Ramesh
#### Date: 2024-11-13
#### Time taken to write the code: 48 mins

## Description
This program parses flow log data to map each entry to a tag based on a provided lookup table. Additionally, it uses a protocol number mapping to convert protocol numbers to protocol names. The program generates an output file containing:
1. Counts of each tag found in the logs.
2. Counts of each port/protocol combination.

The program is structured to be adaptable for future changes in flow log format, lookup tables, and protocol mappings.

---

## How It Works
1. **Protocol Mapping**: Reads a CSV file (`protocol_number_mapping.csv`) containing mappings of protocol numbers to protocol names.
2. **Lookup Table**: Reads a CSV file (`lookup_table_refer.csv`) with mappings of `dstport` and `protocol` to tags.
3. **Flow Logs Parsing**: Reads and parses a flow log file (`flow_log_data.txt`).
4. **Output**: Writes the counts of tags and port/protocol combinations to `output_counts.txt`.

---

## File Structure
- `protocol_number_mapping.csv`: Contains protocol numbers and corresponding protocol names.
- `lookup_table_refer.csv`: Contains mappings of destination ports and protocol names to tags.
- `flow_log_data.txt`: Flow log data in version 2 format.
- `output_counts.txt`: Generated output file containing counts of tags and port/protocol combinations.

---

## Assumptions
- **Log Format**: Each line must have exactly 14 columns, as defined in the `LOG_COLUMN_MAP` dictionary.
- **Protocol Mappings**: The protocol number mapping is provided in a CSV file (`protocol_number_mapping.csv`) with columns `Decimal` (for protocol number) and `Keyword` (for protocol name).
- **Case Sensitivity**: Protocols in the lookup table are case-insensitive. They are converted to lowercase to match protocol names consistently.
- **Malformed Lines**: If a line in the flow log file does not have exactly 14 fields, it is skipped.
- **File Encoding**: All input files are assumed to be in standard ASCII/UTF-8 encoding.
- **Output Structure**: The output file is structured with two sections: Tag Counts and Port/Protocol Combination Counts. The sections are clearly labeled for readability.

---

## Usage Instructions

### Prerequisites
- Python 3.x
- Required modules: `csv`, `collections` (standard libraries, no additional installation needed)

### Running the Program
1. Ensure the following input files are in the same directory as the script:
   - `protocol_number_mapping.csv`: Mapping of protocol numbers to names.
   - `lookup_table_refer.csv`: Lookup table with destination port, protocol, and tag mappings.
   - `flow_log_data.txt`: The flow log file to be processed.
   
2. Run the script:
   ```bash
   python main.py
