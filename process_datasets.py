#!/usr/bin/env python3
"""
Script to fetch and process dataset information from CKAN API
and generate Jekyll-compatible JSON data files
"""

import json
import requests
from datetime import datetime
import os

def fetch_datasets():
    """Fetch dataset information from CKAN API"""
    url = "https://ckandev.indiadataportal.com/api/3/action/package_search?q=organization%3Ahigh-value-datasets&rows=999"
    
    print(f"Fetching data from: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Check if we have the expected structure
        if 'result' in data and 'results' in data['result']:
            count = len(data['result']['results'])
            print(f"Successfully fetched {count} packages")
            # Also print the actual count from the API if available
            if 'count' in data['result']:
                print(f"Total available: {data['result']['count']}")
            return data
        else:
            print("Unexpected API response structure:")
            print(json.dumps(data, indent=2)[:500] + "...")  # Print first 500 chars
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return None

def process_datasets(data):
    """Process and flatten dataset resources"""
    processed_datasets = []
    all_sectors = set()
    all_granularities = set()
    
    if not data or 'result' not in data or 'results' not in data['result']:
        print("No data to process")
        return processed_datasets, list(all_sectors), list(all_granularities)
    
    packages = data['result']['results']
    print(f"Processing {len(packages)} packages...")
    
    for package in packages:
        # Get package-level information
        package_name = package.get('title', package.get('name', ''))
        package_source = package.get('source_name', '')
        package_sectors = package.get('sector', [])
        
        # Handle sectors - could be a list or a string
        if isinstance(package_sectors, str):
            package_sectors = [s.strip() for s in package_sectors.split(',') if s.strip()]
        elif not isinstance(package_sectors, list):
            package_sectors = []
        
        # Add sectors to our set
        all_sectors.update(package_sectors)
        
        # Process each resource in the package
        resources = package.get('resources', [])
        if resources:
            print(f"  Package '{package_name}' has {len(resources)} resources")
        
        for resource in resources:
            # Create a flattened dataset entry for each resource
            dataset = {
                'name': resource.get('name', ''),
                'source': package_source,
                'sectors': package_sectors,
                'description': resource.get('description', ''),
                'granularity': resource.get('granularity', ''),
                'frequency': resource.get('frequency', ''),
                'data_retrieval_date': resource.get('data_retreival_date', ''),  # Note: typo in API field name
                'years_covered': resource.get('years_covered', ''),
                'package_name': package_name,
                'package_id': package.get('id', ''),
                'resource_id': resource.get('id', '')
            }
            
            # Add granularity to our set
            if dataset['granularity']:
                all_granularities.add(dataset['granularity'])
            
            # Only add if resource has a name
            if dataset['name']:
                processed_datasets.append(dataset)
            else:
                print(f"    Skipping resource without name in package '{package_name}'")
    
    # Sort alphabetically by name
    processed_datasets.sort(key=lambda x: x['name'].lower() if x['name'] else '')
    
    # Convert sets to sorted lists
    all_sectors = sorted(list(all_sectors))
    all_granularities = sorted(list(all_granularities))
    
    print(f"\nProcessed {len(processed_datasets)} total resources")
    print(f"Found {len(all_sectors)} unique sectors: {all_sectors}")
    print(f"Found {len(all_granularities)} unique granularities: {all_granularities}")
    
    return processed_datasets, all_sectors, all_granularities

def ensure_data_directory():
    """Ensure _data directory exists"""
    if not os.path.exists('_data'):
        os.makedirs('_data')
        print("Created _data directory")

def save_datasets(datasets, filename='_data/datasets.json'):
    """Save processed datasets to JSON file"""
    ensure_data_directory()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(datasets, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(datasets)} datasets to {filename}")

def save_filters(sectors, granularities, filename='_data/filters.json'):
    """Save unique filter values to JSON file"""
    ensure_data_directory()
    
    filters = {
        'sectors': sectors,
        'granularities': granularities
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(filters, f, indent=2, ensure_ascii=False)
    print(f"Saved filter values to {filename}")

def main():
    """Main function"""
    print("=" * 50)
    print("High-Resolution Datasets Processor")
    print("=" * 50)
    
    # Fetch data from API
    data = fetch_datasets()
    
    if not data:
        print("\nFailed to fetch data. Exiting.")
        return
    
    # Process datasets
    datasets, sectors, granularities = process_datasets(data)
    
    if not datasets:
        print("\nNo datasets found after processing.")
        print("API might have returned empty results or unexpected format.")
        return
    
    # Save datasets
    save_datasets(datasets)
    
    # Save filter values
    save_filters(sectors, granularities)
    
    print("\n" + "=" * 50)
    print("Processing complete!")
    print(f"Total datasets: {len(datasets)}")
    print(f"Unique sectors: {len(sectors)}")
    print(f"Unique granularities: {len(granularities)}")
    print("=" * 50)

if __name__ == "__main__":
    main()