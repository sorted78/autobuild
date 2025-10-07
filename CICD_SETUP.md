# GitHub Actions CI/CD Setup Guide

This guide will help you configure automatic deployment to S3 using GitHub Actions.

## Overview

Once configured, every push to the `main` branch will automatically:
1. Build the website using Python
2. Deploy to S3
3. Make your changes live in seconds!

## Prerequisites

- AWS account with S3 access
- GitHub repository access
- AWS Access Key ID and Secret Access Key

---

## Step 1: Create AWS IAM User for GitHub Actions

### Option A: Use Existing Credentials (Quick Start)

If you're already using AWS CLI, you can use your existing credentials. Skip to Step 2.

### Option B: Create Dedicated IAM User (Recommended for Production)

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → **Create user**
3. User name: `github-actions-autobuild`
4. Click **Next**
5. Select **Attach policies directly**
6. Search and select: `AmazonS3FullAccess` (or create custom policy below)
7. Click **Next** → **Create user**
8. Click on the user name
9. Go to **Security credentials** tab
10. Click **Create access key**
11. Select **Application running outside AWS**
12. Click **Next** → **Create access key**
13. **IMPORTANT:** Copy both:
    - Access key ID
    - Secret access key
    - ⚠️ You won't be able to see the secret again!

### Custom IAM Policy (More Secure)

For better security, create a custom policy that only allows access to your specific bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::autobuild-time-display-static",
        "arn:aws:s3:::autobuild-time-display-static/*"
      ]
    }
  ]
}
```

---

## Step 2: Add Secrets to GitHub Repository

### Via GitHub Web Interface

1. Go to your repository: https://github.com/sorted78/autobuild
2. Click **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add the first secret:
   - Name: `AWS_ACCESS_KEY_ID`
   - Secret: *paste your AWS Access Key ID*
   - Click **Add secret**
6. Click **New repository secret** again
7. Add the second secret:
   - Name: `AWS_SECRET_ACCESS_KEY`
   - Secret: *paste your AWS Secret Access Key*
   - Click **Add secret**

### Via GitHub CLI (Alternative)

If you have GitHub CLI installed:

```bash
# Set AWS Access Key ID
gh secret set AWS_ACCESS_KEY_ID --repo sorted78/autobuild
# Paste your access key when prompted

# Set AWS Secret Access Key
gh secret set AWS_SECRET_ACCESS_KEY --repo sorted78/autobuild
# Paste your secret key when prompted
```

---

## Step 3: Test the CI/CD Pipeline

### Automatic Test (Recommended)

Just push any change to the `main` branch:

```bash
cd ~/Desktop/autobuild

# Make a small change
echo "# CI/CD Test" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

### Manual Trigger

1. Go to https://github.com/sorted78/autobuild/actions
2. Click on **Deploy to S3** workflow
3. Click **Run workflow** → **Run workflow**
4. Watch it deploy!

---

## Step 4: Monitor Deployment

### View Workflow Runs

1. Go to https://github.com/sorted78/autobuild/actions
2. You'll see all workflow runs
3. Click on any run to see detailed logs
4. Green ✓ = Success, Red ✗ = Failed

### Check Deployment Status

Each workflow run shows:
- Build output
- Deployment progress
- Final website URL
- Commit information

---

## Workflow Details

### Deploy Workflow (`.github/workflows/deploy.yml`)

**Triggers:**
- Push to `main` branch
- Manual trigger from GitHub UI

**Steps:**
1. Checkout code
2. Set up Python 3.11
3. Run `build.py` to generate `index.html`
4. Configure AWS credentials from secrets
5. Upload to S3 with proper content-type
6. Display success message

**Duration:** ~30-60 seconds

### Test Workflow (`.github/workflows/test-build.yml`)

**Triggers:**
- Pull requests to `main`

**Purpose:**
- Validates build process
- Checks HTML generation
- Verifies file structure
- Prevents broken deployments

---

## Troubleshooting

### Build Failed

**Error: "AWS credentials not found"**
- Check that secrets are properly set in GitHub
- Verify secret names: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- Ensure no extra spaces in secret values

**Error: "Access Denied"**
- Verify IAM user has S3 permissions
- Check bucket name in workflow file
- Ensure IAM policy includes `s3:PutObject` permission

**Error: "NoSuchBucket"**
- Confirm bucket exists: `autobuild-time-display-static`
- Check region in workflow (us-east-1)
- Verify bucket name spelling

### Build Succeeds but Site Not Updated

1. Check browser cache (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)
2. Verify file was uploaded:
   ```bash
   aws s3 ls s3://autobuild-time-display-static/
   ```
3. Check S3 object metadata
4. Clear cache-control if needed

### Viewing Workflow Logs

1. Go to Actions tab
2. Click on failed workflow
3. Click on the failed job
4. Expand steps to see detailed error messages

---

## Customizing the Workflow

### Change Deployment Branch

Edit `.github/workflows/deploy.yml`:

```yaml
on:
  push:
    branches:
      - main        # Change to your branch
      - production  # Add more branches
```

### Add Notifications

Add Slack notification on deployment:

```yaml
- name: Notify Slack
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Autobuild deployed successfully!"
      }
```

### Deploy to Multiple Environments

Create separate workflows for staging/production:

```yaml
# .github/workflows/deploy-staging.yml
on:
  push:
    branches:
      - develop

# Deploy to staging bucket
aws s3 cp index.html s3://autobuild-staging/
```

### Add CloudFront Cache Invalidation

If you add CloudFront later:

```yaml
- name: Invalidate CloudFront
  run: |
    aws cloudfront create-invalidation \
      --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
      --paths "/*"
```

---

## Security Best Practices

### 1. Use Least Privilege IAM Permissions

✅ **Good:** Custom policy for specific bucket
❌ **Bad:** `AdministratorAccess` or `AmazonS3FullAccess` for all buckets

### 2. Rotate Access Keys Regularly

Set a reminder to rotate keys every 90 days:

```bash
# Delete old access key
aws iam delete-access-key --access-key-id OLD_KEY_ID --user-name github-actions-autobuild

# Create new access key
aws iam create-access-key --user-name github-actions-autobuild

# Update GitHub secrets
```

### 3. Use GitHub Environments (Pro/Enterprise)

For additional protection:

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: http://autobuild-time-display-static.s3-website-us-east-1.amazonaws.com
    runs-on: ubuntu-latest
```

### 4. Enable Branch Protection

1. Go to Settings → Branches
2. Add rule for `main`
3. Require pull request reviews
4. Require status checks to pass

---

## Monitoring and Costs

### GitHub Actions Usage

- Public repos: **Unlimited free minutes** ✨
- Private repos: 2,000 minutes/month (free tier)
- Each deployment: ~1 minute
- **Your usage: FREE** (public repo)

### AWS Costs

- S3 PUT requests: $0.005 per 1,000 requests
- 30 deployments/month = $0.00015
- **Basically free!**

### Total CI/CD Cost

**$0.00/month** for public repo with moderate deployments! 🎉

---

## Advanced Features

### 1. Automated Testing

Add HTML validation:

```yaml
- name: Validate HTML
  run: |
    npm install -g html-validator-cli
    html-validator index.html
```

### 2. Lighthouse Performance Testing

```yaml
- name: Run Lighthouse
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: |
      http://autobuild-time-display-static.s3-website-us-east-1.amazonaws.com
```

### 3. Scheduled Deployments

Rebuild daily at midnight:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
```

### 4. Deployment Rollback

Keep previous versions:

```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket autobuild-time-display-static \
  --versioning-configuration Status=Enabled

# Rollback to previous version
aws s3api list-object-versions \
  --bucket autobuild-time-display-static \
  --prefix index.html
```

---

## Success Checklist

- [ ] AWS IAM user created with S3 permissions
- [ ] AWS credentials added as GitHub secrets
- [ ] Pushed a commit to test deployment
- [ ] Workflow ran successfully (green checkmark)
- [ ] Website updated with changes
- [ ] Verified deployment URL works

---

## Next Steps

1. **Make your first automated deployment!**
   ```bash
   # Edit build.py to change colors or text
   git add build.py
   git commit -m "Update website colors"
   git push origin main
   # Watch it deploy automatically!
   ```

2. **Set up branch protection** (optional)
   - Require PR reviews before merging
   - Require tests to pass

3. **Add more features**
   - Timezone selector
   - Dark/light mode toggle
   - Weather widget

4. **Enhance CI/CD**
   - Add CloudFront invalidation
   - Implement blue-green deployments
   - Add Slack notifications

---

## Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **AWS S3 CLI Reference:** https://docs.aws.amazon.com/cli/latest/reference/s3/
- **IAM Best Practices:** https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- **Workflow Syntax:** https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

---

## Support

If you encounter issues:
1. Check workflow logs in GitHub Actions tab
2. Verify AWS credentials and permissions
3. Review this guide's troubleshooting section
4. Check AWS CloudTrail for API errors

Happy automated deploying! 🚀
