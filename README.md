# Autobuild

A simple static website that displays the current time and date, built with Python and hosted on AWS S3.

## Overview

This project demonstrates a minimal, cost-effective approach to hosting a dynamic time/date display using:
- **Python** for generating the static HTML file (build process)
- **JavaScript** for live time updates in the browser
- **AWS S3** for cheap, reliable static hosting

## Features

- ⏰ Real-time clock display
- 📅 Current date with timezone
- 📱 Responsive design
- 🎨 Modern gradient UI
- 💰 Ultra-low cost (< $1/month)
- 🚀 Fast global delivery via S3

## Cost Analysis

**Estimated monthly cost: $0.50 - $1.00** for low to moderate traffic

- S3 Storage: ~$0.023 per GB/month (file is < 5KB)
- Data Transfer: First 100 GB/month FREE, then $0.09/GB
- Requests: GET requests $0.0004 per 1,000 requests

For a small static site, you'll likely stay well within free tier limits!

## Project Structure

```
autobuild/
├── build.py          # Python script to generate static HTML
├── deploy.sh         # Bash script for S3 deployment
├── index.html        # Generated static website file
└── README.md         # This file
```

## Quick Start

### Prerequisites

- Python 3.x
- AWS CLI installed and configured
- AWS account with S3 access

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/sorted78/autobuild.git
cd autobuild
```

2. Build the website:
```bash
python3 build.py
```

3. Open `index.html` in your browser to preview

### Deployment to AWS S3

#### Option 1: Using the deployment script (Automated)

1. Edit `deploy.sh` and set your bucket name:
```bash
BUCKET_NAME="your-unique-bucket-name"
REGION="us-east-1"  # Change to your preferred region
```

2. Make the script executable and run it:
```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Build the website
- Create the S3 bucket (if needed)
- Upload files
- Configure static website hosting
- Set public access permissions

#### Option 2: Manual deployment with AWS CLI

1. Build the website:
```bash
python3 build.py
```

2. Create an S3 bucket:
```bash
aws s3 mb s3://your-unique-bucket-name --region us-east-1
```

3. Upload the file:
```bash
aws s3 cp index.html s3://your-unique-bucket-name/
```

4. Enable static website hosting:
```bash
aws s3 website s3://your-unique-bucket-name --index-document index.html
```

5. Make the bucket public (create a policy file):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-unique-bucket-name/*"
    }
  ]
}
```

6. Apply the policy:
```bash
aws s3api put-bucket-policy --bucket your-unique-bucket-name --policy file://policy.json
```

7. Access your site at:
```
http://your-unique-bucket-name.s3-website-us-east-1.amazonaws.com
```

#### Option 3: Using AWS Console

1. Build locally: `python3 build.py`
2. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/)
3. Create a new bucket
4. Upload `index.html`
5. Go to Properties → Static website hosting → Enable
6. Go to Permissions → Bucket Policy → Add the public read policy
7. Access via the provided website endpoint

## Customization

Edit `build.py` to customize:
- Color scheme (gradient colors)
- Font styles
- Time format (12-hour vs 24-hour)
- Layout and spacing

After making changes, rebuild with `python3 build.py`

## Architecture

```
┌─────────────┐
│   Python    │  (Build time)
│  build.py   │────► Generates index.html
└─────────────┘
       │
       ▼
┌─────────────┐
│ index.html  │  (Static file)
│ + CSS       │  Uploaded to S3
│ + JavaScript│
└─────────────┘
       │
       ▼
┌─────────────┐
│   AWS S3    │  (Runtime)
│   Hosting   │  Serves to users
└─────────────┘
       │
       ▼
┌─────────────┐
│   Browser   │  JavaScript updates
│             │  time every second
└─────────────┘
```

## Why This Approach?

1. **Cost-effective**: No servers to run, pay only for storage + bandwidth
2. **Scalable**: S3 handles traffic spikes automatically
3. **Reliable**: 99.99% availability SLA from AWS
4. **Fast**: Content delivered from S3 edge locations
5. **Simple**: No backend infrastructure to maintain

## Adding a Custom Domain

To use a custom domain (e.g., time.yourdomain.com):

1. Register domain in Route 53 or your DNS provider
2. Create bucket with same name as domain
3. Configure Route 53 alias record pointing to S3 endpoint
4. (Optional) Add CloudFront for HTTPS support

## Future Enhancements

- [ ] Add CloudFront CDN for HTTPS and better performance
- [ ] Implement CI/CD with GitHub Actions
- [ ] Add timezone selector
- [ ] Multiple themes/color schemes
- [ ] World clock with multiple timezones

## License

MIT License - feel free to use and modify!

## Contributing

Pull requests welcome! Feel free to:
- Improve the design
- Add features
- Optimize performance
- Enhance documentation
