# High-Value Datasets Portal

A Jekyll-based website for showcasing high-value datasets curated by the Bharti Institute of Public Policy at ISB.

## Setup Instructions

### Prerequisites
- Ruby (version 2.5.0 or higher)
- RubyGems
- Git
- Python 3.x (for data processing)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/bippisb/data-hub.git
cd data-hub

Install Jekyll and dependencies:

bashgem install bundler
bundle install

Process dataset information:

bashpip install requests
python process_datasets.py

Serve the site locally:

bashbundle exec jekyll serve

View the site at: http://localhost:4000/data-hub

Updating Dataset Information

Run the data processing script:

bashpython process_datasets.py

This will:

Fetch latest data from the CKAN API
Process and flatten the resources
Generate _data/datasets.json
Generate _data/filters.json with unique filter values


Commit and push changes:

bashgit add _data/*.json
git commit -m "Update dataset information"
git push origin main
Deployment to GitHub Pages

Ensure all changes are committed
Push to the main branch:

bashgit push origin main

GitHub Pages will automatically build and deploy the site

Maintenance

Maintainer: Data Team, Bharti Institute of Public Policy
Update Frequency: Monthly or as new datasets are added
Support: For technical issues, please contact the maintainer

License
This project is maintained by the Bharti Institute of Public Policy, ISB.