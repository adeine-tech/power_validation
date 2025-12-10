import pandas as pd
import os
from datetime import datetime
import logging

import pandas as pd
import json
import csv

class Radio:
    def __init__(self, radio_id, num_carriers, allowed_carriers, power_limit, tolerance, diversity, band_power_limits, bandwidth_limit, power_usage):
        self.radio_id = radio_id
        self.num_carriers = num_carriers
        self.allowed_carriers = allowed_carriers
        self.power_limit = power_limit
        self.tolerance = tolerance
        self.diversity = diversity
        self.band_power_limits = band_power_limits
        self.bandwidth_limit = bandwidth_limit
        self.power_usage = power_usage

    def calculate_power_state(self):
        if self.num_carriers > self.allowed_carriers:
            raise ValueError("Number of carriers exceeds allowed limit")

        aggregate_power_usage = sum(self.power_usage.values())
        if aggregate_power_usage > self.power_limit + self.tolerance:
            power_state = "Overpowered"
        elif aggregate_power_usage < self.power_limit - self.tolerance:
            power_state = "Underpowered"
        else:
            power_state = "Powered Correctly"

        for band, power in self.power_usage.items():
            if power > self.band_power_limits.get(band, 0):
                raise ValueError(f"Power usage exceeds band-specific power limit for band {band}")

        return {
            "radio_id": self.radio_id,
            "power_state": power_state,
            "aggregate_power_usage": aggregate_power_usage
        }

def calculate_radio_power_limitation(radios):
    results = []
    logs = []
    for radio in radios:
        try:
            result = Radio(**radio).calculate_power_state()
            results.append(result)
            logs.append({
                "input_attributes": radio,
                "calculated_power_usage": result["aggregate_power_usage"],
                "power_state": result["power_state"]
            })
        except ValueError as e:
            print(f"Error processing radio {radio['radio_id']}: {str(e)}")
    return results, logs

def save_results(results, logs):
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['radio_id', 'power_state', 'aggregate_power_usage'])
        writer.writeheader()
        writer.writerows(results)

    with open('logs.json', 'w') as jsonfile:
        json.dump(logs, jsonfile, indent=4)


# Define radio attributes
radio_attributes_list = pd.DataFrame([
{'Radio_Type': 'rf4486', 'Technology': 'LTE', 'Bandwidth': 5, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4486', 'Technology': 'LTE', 'Bandwidth': 10, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'LTE', 'Bandwidth': 15, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'LTE', 'Bandwidth': 20, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'NR', 'Bandwidth': 5, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4486', 'Technology': 'NR', 'Bandwidth': 10, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'NR', 'Bandwidth': 15, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'NR', 'Bandwidth': 20, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'NR', 'Bandwidth': 25, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4486', 'Technology': 'NR', 'Bandwidth': 30, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4494', 'Technology': 'LTE', 'Bandwidth': 5, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4494', 'Technology': 'LTE', 'Bandwidth': 10, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4494', 'Technology': 'LTE', 'Bandwidth': 15, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4494', 'Technology': 'LTE', 'Bandwidth': 20, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4494', 'Technology': 'NR', 'Bandwidth': 5, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4494', 'Technology': 'NR', 'Bandwidth': 10, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4494', 'Technology': 'NR', 'Bandwidth': 15, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4494', 'Technology': 'NR', 'Bandwidth': 20, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4435', 'Technology': 'LTE', 'Bandwidth': 5, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4435', 'Technology': 'LTE', 'Bandwidth': 10, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4435', 'Technology': 'LTE', 'Bandwidth': 15, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4435', 'Technology': 'LTE', 'Bandwidth': 20, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4435', 'Technology': 'NR', 'Bandwidth': 5, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4435', 'Technology': 'NR', 'Bandwidth': 10, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4435', 'Technology': 'NR', 'Bandwidth': 15, 'Max_Bandwidth': 35, 'Max_Num_Carriers': 4, 'Tx': '4T', 'Output_Power_in_W': 80.0, 'Output Power_in_dBm': 49, 'Total_Power': 320},
{'Radio_Type': 'rf4461', 'Technology': 'LTE', 'Bandwidth': 5, 'Max_Bandwidth': 25, 'Max_Num_Carriers': 3, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4461', 'Technology': 'LTE', 'Bandwidth': 10, 'Max_Bandwidth': 25, 'Max_Num_Carriers': 3, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4461', 'Technology': 'NR', 'Bandwidth': 5, 'Max_Bandwidth': 25, 'Max_Num_Carriers': 3, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'rf4461', 'Technology': 'NR', 'Bandwidth': 10, 'Max_Bandwidth': 25, 'Max_Num_Carriers': 3, 'Tx': '4T', 'Output_Power_in_W': 40.0, 'Output Power_in_dBm': 46, 'Total_Power': 160},
{'Radio_Type': 'mt6402', 'Technology': 'LTE', 'Bandwidth': 5, 'Max_Bandwidth': 100, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
{'Radio_Type': 'mt6402', 'Technology': 'LTE', 'Bandwidth': 10, 'Max_Bandwidth': 100, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
{'Radio_Type': 'mt6402', 'Technology': 'LTE', 'Bandwidth': 15, 'Max_Bandwidth': 100, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
{'Radio_Type': 'mt6402', 'Technology': 'LTE', 'Bandwidth': 20, 'Max_Bandwidth': 100, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
{'Radio_Type': 'mt6402', 'Technology': 'NR', 'Bandwidth': 10, 'Max_Bandwidth': 80, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
{'Radio_Type': 'mt6402', 'Technology': 'NR', 'Bandwidth': 20, 'Max_Bandwidth': 80, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
{'Radio_Type': 'mt6402', 'Technology': 'NR', 'Bandwidth': 40, 'Max_Bandwidth': 80, 'Max_Num_Carriers': 3, 'Tx': '64T', 'Output_Power_in_W': 0.03, 'Output Power_in_dBm': 15, 'Total_Power': 20},
]}

results, logs = calculate_radio_power_limitation(radios)
save_results(results, logs)



# Define the directory and file path
dir_path = '/data/usm_data/usm_ciq'
excel_files = [f for f in os.listdir(dir_path) if f.endswith('.xlsx') or f.endswith('.xls')]
if len(excel_files) != 1:
    raise ValueError("Expected exactly one Excel file in the directory")
file_name = excel_files[0]
full_path = os.path.join(dir_path, file_name)

# Read the Excel file
excel_file = pd.ExcelFile(full_path)

# Parse the sheets
lte_sheet = excel_file.parse("LTE_RAN_CIQ")
nr_sheet = excel_file.parse("NR_RAN_CIQ")


# Process LTE_RAN_CIQ sheet
lte_sheet['enb_id'] = lte_sheet['ENB_ID']
lte_sheet['gnb_id'] = lte_sheet['COLO_NODE_ID'].str.split('_', expand=True).iloc[:, 1].fillna('')
# Create Radio_Port column
required_columns = ['GCB_CARD_ID', 'PRIMARY_CPRI_PORT_ID', 'UNIT_ID']
lte_carrier_attrib = ['BANDWIDTH','OUTPUT_POWER','TX','RRH_CODE']


mask_lte = lte_sheet[required_columns].notna().all(axis=1)

lte_sheet.loc[mask_lte, 'Radio_Port'] = (
    lte_sheet.loc[mask_lte, 'UNIT_ID'].astype(int).astype(str) +
    '_' +
    lte_sheet.loc[mask_lte, 'GCB_CARD_ID'].astype(int).astype(str) +
    '_' +
    lte_sheet.loc[mask_lte, 'PRIMARY_CPRI_PORT_ID'].astype(int).astype(str)
)
lte_sheet.loc[~mask_lte, 'Radio_Port'] = ''

# Process NR_RAN_CIQ sheet
nr_carrier_attrib = ['BANDWIDTH','OUTPUT_POWER_DBM','TX','RRH_TYPE']
mask_nr = nr_sheet[required_columns].notna().all(axis=1)
nr_sheet.loc[mask_nr, 'Radio_Port'] = (
    nr_sheet.loc[mask_nr, 'UNIT_ID'].astype(int).astype(str) +
    '_' +
    nr_sheet.loc[mask_nr, 'GCB_CARD_ID'].astype(int).astype(str) +
    '_' +
    nr_sheet.loc[mask_nr, 'PRIMARY_CPRI_PORT_ID'].astype(int).astype(str)
)
nr_sheet.loc[~mask_nr, 'Radio_Port'] = ''

lte_sheet['gnb_id'] = lte_sheet['gnb_id'].astype(str).str.strip()
nr_sheet['NR_ID'] = nr_sheet['NR_ID'].astype(str).str.strip()
lte_sheet['Radio_Port'] = lte_sheet['Radio_Port'].astype(str).str.strip()
nr_sheet['Radio_Port'] = nr_sheet['Radio_Port'].astype(str).str.strip()


# Create gnb_available column
lte_sheet['gnb_available'] = ''
for index, row in lte_sheet.iterrows():
    gnb_id = row['gnb_id']
    radio_port = row['Radio_Port']
    #if not pd.isna(gnb_id) and not pd.isna(radio_port):
    if radio_port != '' and not pd.isna(gnb_id):    
        if ((nr_sheet['NR_ID'] == gnb_id) & (nr_sheet['Radio_Port'] == radio_port)).any():
            lte_sheet.loc[index, 'gnb_available'] = 'Yes'


# Iterate over LTE_RAN_CIQ
for enb_id, group in lte_sheet.groupby('enb_id'):
    for index, row in group.iterrows():
        radio_port = row['Radio_Port']
        if row['gnb_available'] == 'Yes':
            # Fetch corresponding row(s) from NR_RAN_CIQ
            nr_rows = nr_sheet[(nr_sheet['Radio_Port'] == radio_port) & (nr_sheet['NR_ID'] == row['gnb_id'])]
            lte_rows = group[group['Radio_Port'] == radio_port]
            lte_attributes = lte_rows[lte_carrier_attrib].to_dict('records')
            nr_attributes = nr_rows[nr_carrier_attrib].to_dict('records')
            radio = Radio(enb_id, radio_port, lte_attributes, nr_attributes)
        else:
            lte_rows = group[group['Radio_Port'] == radio_port]
            lte_attributes = lte_rows[lte_carrier_attrib].to_dict('records')
            radio = Radio(enb_id, radio_port, lte_attributes)
        for result in radio.calculate_power():
            # Do something with the result
            print(result)


# Save the updated LTE_RAN_CIQ sheet
timestamp = datetime.now().strftime('%m_%d_%H_%M')
new_file_name = f"{file_name.split('.')[0]}_{timestamp}.xlsx"
save_path = os.path.join('/home/ljackson/rnd/Power_Check', new_file_name)
lte_sheet.to_excel(save_path, index=False)




class RadioPowerCalculator:
    def __init__(self, radio_attributes):
        self.radio_attributes = radio_attributes
        self.logger = logging.getLogger(__name__)

    def calculate_power(self):
        # Validate input data
        self.validate_input()

        # Calculate aggregate power usage per band and technology
        power_usage = self.calculate_power_usage()

        # Determine power state
        power_state = self.determine_power_state(power_usage)

        # Generate output
        output = self.generate_output(power_state, power_usage)

        return output

    def validate_input(self):
        # Check number of carriers
        if self.radio_attributes['num_carriers'] > self.radio_attributes['allowed_carriers']:
            self.logger.error("Number of carriers exceeds allowed limit")
            raise ValueError("Number of carriers exceeds allowed limit")

        # Check power limit for each band
        diversity = self.radio_attributes.get('diversity', '4T')  # default to 4T
        band_power_limits = self.radio_attributes[f'band_power_limits_at_{diversity}']
        for band, power_limit in band_power_limits.items():
            if self.radio_attributes['power_usage'][band] * self.radio_attributes['num_carriers'] > power_limit:
                self.logger.error(f"Power limit exceeded for band {band} at {diversity}")
                raise ValueError(f"Power limit exceeded for band {band} at {diversity}")

    def calculate_power_usage(self):
        # Calculate aggregate power usage per band and technology
        power_usage = {}
        for band, usage in self.radio_attributes['power_usage'].items():
            power_usage[band] = usage * self.radio_attributes['num_carriers']
        return power_usage

    def determine_power_state(self, power_usage):
        # Determine power state based on tolerance
        tolerance = self.radio_attributes['tolerance']
        power_limit = self.radio_attributes['power_limit']
        total_power_usage = sum(power_usage.values())

        if total_power_usage > power_limit + tolerance:
            return "Overpowered"
        elif total_power_usage < power_limit - tolerance:
            return "Underpowered"
        else:
            return "Powered Correctly"

    def generate_output(self, power_state, power_usage):
        # Generate log file output
        log_output = {
            'radio_attributes': self.radio_attributes,
            'power_usage': power_usage,
            'power_state': power_state
        }

        # Generate line output
        line_output = {
            'radio_id': self.radio_attributes['radio_id'],
            'power_state': power_state,
            'aggregate_power_usage': sum(power_usage.values())
        }

        return log_output, line_output

# Process radios
log_outputs = []
line_outputs = []
for radio_attributes in radio_attributes_list:
    calculator = RadioPowerCalculator(radio_attributes)
    try:
        log_output, line_output = calculator.calculate_power()
        log_outputs.append(log_output)
        line_outputs.append(line_output)
    except ValueError as e:
        print(f"Error processing {radio_attributes['radio_id']}: {e}")

# Save to CSV
df = pd.DataFrame(line_outputs)
df.to_csv('output.csv', index=False)

# Save log outputs to JSON
#with open('log_output.json', 'w') as f:
#    json.dump(log_outputs, f, indent=4)
