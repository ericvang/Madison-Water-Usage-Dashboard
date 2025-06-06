# Madison Water Usage Dashboard

A web application that visualizes and analyzes water usage data throughout Madison. This dashboard provides insights into residential, commercial, and industrial water consumption patterns.

## Features

- Interactive data visualization with three different dashboard views
- A/B testing for donation page optimization
- Rate-limited API access to water usage data
- Email subscription system
- Responsive web interface

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd madison-water-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to:
```
http://localhost:8080
```

## API Endpoints

- `/` - Homepage
- `/browse.html` - Data table view
- `/browse.json` - JSON API endpoint (rate-limited)
- `/dashboard1.svg` - Total water usage distribution
- `/dashboard2.svg` - Water usage by consumer type
- `/dashboard3.svg` - Residential vs Commercial usage correlation
- `/donate.html` - Donation page
- `/email` - Email subscription endpoint (POST)

## Data Source

The application uses water usage data from Madison, including:
- Total gallons
- Residential gallons
- Commercial gallons
- Industrial gallons

## Contributing

Feel free to submit issues and enhancement requests!
