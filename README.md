# Autobuild

A simple static website that displays the current time and date, built with Python and hosted on AWS S3 with **automated CI/CD deployment**.

## Overview

This project demonstrates a minimal, cost-effective approach to hosting a dynamic time/date display using:
- **Python** for generating the static HTML file (build process)
- **JavaScript** for live time updates in the browser
- **AWS S3** for cheap, reliable static hosting
- **GitHub Actions** for automated CI/CD deployment

## Features

- ⏰ Real-time clock display
- 📅 Current date with timezone
- 📱 Responsive design
- 🎨 Modern gradient UI
- 💰 Ultra-low cost (< $1/month)
- 🚀 Fast global delivery via S3
- 🤖 **Automated deployment on every push to main**

## Cost Analysis

**Estimated monthly cost: $0.50 - $1.00** for low to moderate traffic

- S3 Storage: ~$0.023 per GB/month (file is < 5KB)
- Data Transfer: First 100 GB/month FREE, then $0.09/GB
- Requests: GET requests $0.0004 per 1,000 requests
- **GitHub Actions: FREE for public repositories**

For a small static site, you'll likely stay well within free tier limits!

## Project Structure

```
autobuild/
├── .github/
│   └── workflows/
│       ├── deploy.yml       # Automated deployment workflow
│       └── test-build.yml   # PR testing workflow
├── build.py                 # Python script to generate static HTML
├── deploy.sh                # Bash script for manual S3 deployment
├── index.html               # Generated static website file
├── CICD_SETUP.md           # Complete CI/CD setup guide
└── README.md                # This file
```

## Quick Start

### Prerequisites

- Python 3.x
- AWS CLI installed and configured
- AWS account with S3 access
- GitHub account (for CI/CD)

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

## Deployment Options

### 🚀 Option 1: Automated CI/CD with GitHub Actions (Recommended)

**Set up once, deploy automatically forever!**

1. **Add AWS credentials to GitHub secrets:**
   - Go to your repository Settings → Secrets and variables → Actions
   - Add `AWS_ACCESS_KEY_ID` secret
   - Add `AWS_SECRET_ACCESS_KEY` secret

2. **That's it!** Now every push to `main` automatically deploys to S3.

📖 **[Complete CI/CD Setup Guide →](CICD_SETUP.md)**

**Benefits:**
- ✅ Deploy in ~30 seconds
- ✅ No manual steps needed
- ✅ Automated testing on PRs
- ✅ Deployment history and logs
- ✅ Can trigger manually from GitHub UI
- ✅ Completely free for public repos

### Option 2: Using the deployment script (Manual)

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

### Option 3: Manual deployment with AWS CLI

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
aws s3 cp index.html s3://your-unique-bucket-name/ --content-type text/html
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

## CI/CD Workflow

Once CI/CD is set up, your deployment workflow is:

```bash
# 1. Make changes locally
vim build.py  # Edit colors, layout, etc.

# 2. Commit and push
git add .
git commit -m "Update website design"
git push origin main

# 3. GitHub Actions automatically:
#    - Runs build.py
#    - Tests the build
#    - Deploys to S3
#    - Shows deployment status

# 4. Your site is live in ~30 seconds! 🎉
```

**Monitor deployments:** https://github.com/sorted78/autobuild/actions

## Customization

Edit `build.py` to customize:
- Color scheme (gradient colors)
- Font styles
- Time format (12-hour vs 24-hour)
- Layout and spacing

After making changes:
- **With CI/CD:** Just `git push` and it deploys automatically
- **Without CI/CD:** Run `python3 build.py` and upload manually

## Architecture

```
┌─────────────┐
│  Developer  │
│   Changes   │
└──────┬──────┘
       │ git push
       ▼
┌─────────────┐
│   GitHub    │  Stores code
│ Repository  │  Triggers workflows
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GitHub    │  (Automated)
│   Actions   │  - Runs build.py
│   CI/CD     │  - Tests build
└──────┬──────┘  - Deploys to S3
       │
       ▼
┌─────────────┐
│   AWS S3    │  (Runtime)
│   Hosting   │  Serves to users
└──────┬──────┘
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
6. **Automated**: CI/CD handles all deployments
7. **Free CI/CD**: GitHub Actions is free for public repositories

## Adding a Custom Domain

To use a custom domain (e.g., time.yourdomain.com):

1. Register domain in Route 53 or your DNS provider
2. Create bucket with same name as domain
3. Configure Route 53 alias record pointing to S3 endpoint
4. (Optional) Add CloudFront for HTTPS support

## CI/CD Features

### Automated Deployment Workflow
- **Triggers:** Push to main, manual trigger
- **Steps:** Build → Test → Deploy
- **Duration:** ~30-60 seconds
- **Status:** Visible in GitHub Actions tab

### Pull Request Testing
- **Triggers:** Pull requests to main
- **Purpose:** Validate builds before merging
- **Checks:** Build success, file generation, content validation

### Monitoring
- View deployment logs in GitHub Actions
- Get notifications on deployment failures
- Track deployment history
- See exact commit that was deployed

📖 **[Complete CI/CD Setup Guide →](CICD_SETUP.md)**

## Troubleshooting

### CI/CD Not Working?
1. Check GitHub Actions tab for error logs
2. Verify AWS credentials are set as secrets
3. Ensure IAM user has S3 permissions
4. See [CICD_SETUP.md](CICD_SETUP.md) troubleshooting section

### Manual Deployment Issues?
1. Verify AWS CLI is configured: `aws s3 ls`
2. Check bucket exists: `aws s3 ls s3://your-bucket-name/`
3. Verify bucket policy for public access
4. Hard refresh browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)

## Future Enhancements

- [x] Add CloudFront CDN for HTTPS and better performance
- [x] Implement CI/CD with GitHub Actions ✅
- [ ] Add timezone selector
- [ ] Multiple themes/color schemes
- [ ] World clock with multiple timezones
- [ ] CloudFront cache invalidation in CI/CD
- [ ] Deployment notifications (Slack, Discord)
- [ ] Blue-green deployments

## License

MIT License - feel free to use and modify!

## Contributing

Pull requests welcome! Feel free to:
- Improve the design
- Add features
- Optimize performance
- Enhance documentation
- Improve CI/CD workflows

### Contribution Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `python3 build.py`
5. Create a pull request
6. CI/CD will automatically test your build
7. After merge, changes deploy automatically!

## Resources

- **Live Site:** http://autobuild-time-display-static.s3-website-us-east-1.amazonaws.com
- **GitHub Actions:** https://github.com/sorted78/autobuild/actions
- **CI/CD Setup Guide:** [CICD_SETUP.md](CICD_SETUP.md)
- **AWS S3 Static Hosting:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html
- **GitHub Actions Docs:** https://docs.github.com/en/actions

---

Made with ❤️ using Python, S3, and GitHub Actions
