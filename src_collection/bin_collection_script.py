#!/usr/bin/env python3.11

import json
import subprocess
from datetime import datetime, timedelta

# southwark council config
COUNCIL_NAME = "SouthwarkCouncil"
COUNCIL_URL = "https://services.southwark.gov.uk/bins/lookup/200003412963"
UPRN = "200003412963"

def get_optional_params():
    params = {
        'uprn': UPRN
    }
    return params

def fetch_bin_data(council_name, url, params):
    """
    Fetch bin collection data using the UKBinCollectionData library via command line.
    
    Args:
        council_name: Name of the council module
        url: Council URL (if required)
        params: Dictionary of optional parameters (postcode, number, uprn)
    
    Returns:
        dict: Bin collection data
    """
    print("\n" + "="*60)
    print("FETCHING BIN COLLECTION DATA...")
    print("="*60)
    
    try:
        # usage of python module script
        cmd = ["python3.11", "-m", "uk_bin_collection.uk_bin_collection.collect_data", council_name]
        
        if url:
            cmd.append(url)
        
        if 'uprn' in params:
            cmd.extend(["-u", str(params['uprn'])])
        if 'postcode' in params:
            cmd.extend(["-p", params['postcode']])
        if 'number' in params:
            cmd.extend(["-n", str(params['number'])])
        
        print(f"\nFetching data for: {council_name}")
        if params:
            print(f"Parameters: {params}\n")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            return json.loads(result.stdout)
        else:
            print("No data returned from the collection.")
            return None
        
    except subprocess.CalledProcessError as e:
        print(f"\nError: Command failed")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"\nError: Invalid JSON response")
        return None
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return None

def display_bin_schedule(data):
    """Display the bin collection schedule in a readable format with monthly projections."""
    if not data or 'bins' not in data:
        print("\nNo bin collection data found.")
        return
    
    print("\n" + "="*60)
    print("BIN COLLECTION SCHEDULE - NEXT COLLECTION")
    print("="*60)
    
    bins = data['bins']
    today = datetime.now()
    
    for bin_info in bins:
        bin_type = bin_info.get('type', 'Unknown')
        collection_date_str = bin_info.get('collectionDate', 'Unknown')
        
        print(f"\nBin Type: {bin_type}")
        print(f"Next Collection: {collection_date_str}")
        
        try:
            collection_date = datetime.strptime(collection_date_str, "%d/%m/%Y")
            days_until = (collection_date - today).days
            
            if days_until == 0:
                print(f"TODAY")
            elif days_until == 1:
                print(f"Tomorrow ({days_until} day)")
            elif days_until < 7:
                print(f"In {days_until} days ({collection_date.strftime('%A')})")
            else:
                print(f"In {days_until} days")
            
        except ValueError:
            print(f"   (Unable to parse date)")
        
        print("-" * 40)
    
    # Display projected monthly schedule
    print("\n" + "="*60)
    print("PROJECTED MONTHLY SCHEDULE")
    print("(Assuming weekly collections)")
    print("="*60)
    
    for bin_info in bins:
        bin_type = bin_info.get('type', 'Unknown')
        collection_date_str = bin_info.get('collectionDate', 'Unknown')
        
        try:
            first_date = datetime.strptime(collection_date_str, "%d/%m/%Y")
            print(f"\n{bin_type}:")
            
            # Project next 4 weeks
            current_date = first_date
            week = 1
            while week <= 4:
                if current_date >= today:
                    days_diff = (current_date - today).days
                    if days_diff == 0:
                        status = "TODAY"
                    elif days_diff == 1:
                        status = "Tomorrow"
                    else:
                        status = f"In {days_diff} days"
                    print(f"   Week {week}: {current_date.strftime('%a %d/%m/%Y')} - {status}")
                    week += 1
                current_date += timedelta(days=7)
            
        except ValueError:
            print(f"\n{bin_type}: (Unable to project schedule)")
    
    print("\n" + "="*60)
    print("Note: This projection assumes weekly collections.")
    print("Actual dates may vary due to bank holidays or council changes.")
    print("="*60)

def main():

    council_name = COUNCIL_NAME
    url = COUNCIL_URL
    params = get_optional_params()
    
    data = fetch_bin_data(council_name, url, params)
    if data:
        display_bin_schedule(data)
    else:
        print("\nFailed to fetch bin collection data.")
        print("\nPlease check:")
        print("1. Council name is correct (check the wiki for supported councils)")
        print("2. URL and parameters are correct for your council")
        print("3. You have an internet connection")

if __name__ == '__main__':
    main()
