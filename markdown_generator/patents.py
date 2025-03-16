#!/usr/bin/env python3

import csv
from datetime import datetime
import os

def read_patents(tsv_file='patents.tsv'):
    """Read patents data from TSV file."""
    patents = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            patents.append(row)
    return patents

def format_date(date_str):
    """Convert date string to YYYY-MM-DD format."""
    try:
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return date_str

def generate_markdown(patent):
    """Generate markdown content for a patent."""
    formatted_date = format_date(patent['date'])
    filename = f"{formatted_date}-{patent['title'].lower().replace(' ', '-')[:30]}.md"
    
    content = f"""---
title: "{patent['title']}"
collection: publications
permalink: /patent/{formatted_date}-{patent['title'].lower().replace(' ', '-')[:30]}
excerpt: '{patent['description']}'
date: {formatted_date}
venue: 'US Patent'
paperurl: '{patent['link']}'
citation: 'Patent No. {patent['number']}'
category: 'patents'
---
{patent['description']}

[View patent here]({patent['link']})
"""
    return filename, content

def main():
    """Main function to process patents and generate markdown files."""
    patents = read_patents()
    
    # Create _publications directory if it doesn't exist
    os.makedirs('../_publications', exist_ok=True)
    
    for patent in patents:
        filename, content = generate_markdown(patent)
        filepath = os.path.join('../_publications', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {filepath}")

if __name__ == '__main__':
    main() 