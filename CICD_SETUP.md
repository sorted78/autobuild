# GitHub Actions CI/CD Setup Guide

This guide will help you configure automatic deployment to S3 using GitHub Actions.

## 🚀 What Gets Automated

Every time you push to the `main` branch, GitHub Actions will:
1. ✅ Check out your code
2. ✅ Run `build.py` to generate the HTML
3. ✅ Deploy to S3 automatically
4. ✅ Update your live website

**No manual deployment needed!**

---

## 📋 Setup Instructions

### Step 1: Get Your AWS Credentials

You need to create AWS credentials that GitHub can use. You have two options:

#### Option A: Use Your Existing Credentials (Quick)

If you're already using AWS CLI, your credentials are in `~/.aws/credentials`:

```bash
cat ~/.aws/credentials
```

Look for:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

#### Option B: Create New IAM User (Recommended for Production)

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click "Users" → "Create user"
3. Username: `github-actions-autobuild`
4. Click "Next"
5. Select "Attach policies directly"
6. Search and attach: `AmazonS3FullAccess` (or create a custom policy for just your bucket)
7. Click "Next" → "Create user"
8. Click on the new user
9. Go to "Security credentials" tab
10. Click "Create access key"
11. Choose "Application running outside AWS"
12. Click "Next" → "Create access key"
13. **SAVE THESE CREDENTIALS** (you'll only see them once!)

---

### Step 2: Add Secrets to GitHub

1. Go to your repository: https://github.com/sorted78/autobuild

2. Click **Settings** (top menu)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click **New repository secret**

5. Add the first secret:
   - **Name:** `AWS_ACCESS_KEY_ID`
   - **Value:** Your AWS access key ID (starts with `AKIA...`)
   - Click **Add secret**

6. Click **New repository secret** again

7. Add the second secret:
   - **Name:** `AWS_SECRET_ACCESS_KEY`
   - **Value:** Your AWS secret access key
   - Click **Add secret**

---

### Step 3: Test the Workflow

#### Option A: Make a Small Change

Let's test it by updating the website:

```bash
cd ~/Desktop
git clone https://github.com/sorted78/autobuild.git
cd autobuild

# Edit build.py - change the title or colors
nano build.py  # or use your favorite editor

# Commit and push
git add build.py
git commit -m "Test CI/CD: Update website styling"
git push origin main
```

#### Option B: Manual Trigger

1. Go to https://github.com/sorted78/autobuild/actions
2. Click on "Deploy to S3" workflow
3. Click "Run workflow"
4. Click the green "Run workflow" button

---

### Step 4: Watch It Deploy!

1. Go to https://github.com/sorted78/autobuild/actions

2. You'll see your workflow running with a yellow dot 🟡

3. Click on it to see the live logs

4. When it turns green ✅, your site is deployed!

5. Visit http://autobuild-time-display-static.s3-website-us-east-1.amazonaws.com to see your changes

---

## 🔒 Security Best Practices

### Custom IAM Policy (Most Secure)

Instead of `AmazonS3FullAccess`, create a custom policy that only allows access to your bucket:

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

To apply this:
1. IAM Console → Policies → Create policy
2. Click JSON tab
3. Paste the above policy
4. Name it: `GitHubActionsAutobuildPolicy`
5. Create policy
6. Attach it to your IAM user

---

## 📊 Monitoring Deployments

### View Deployment History
```bash
# List all workflow runs
gh run list --repo sorted78/autobuild

# View details of the last run
gh run view --repo sorted78/autobuild
```

### Check Logs
```bash
# View logs of the last run
gh run view --log --repo sorted78/autobuild
```

Or visit: https://github.com/sorted78/autobuild/actions

---

## 🛠️ Troubleshooting

### Workflow Fails with "403 Forbidden"
- **Cause:** AWS credentials are incorrect or don't have S3 permissions
- **Fix:** Check your GitHub secrets and IAM permissions

### Workflow Fails with "Bucket not found"
- **Cause:** Bucket name mismatch
- **Fix:** Ensure the bucket name in the workflow matches your actual bucket

### Secrets Not Working
- **Cause:** Typo in secret names
- **Fix:** Secret names must be EXACTLY:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`

### Re-add Secrets
If you need to update credentials:
1. Go to Settings → Secrets and variables → Actions
2. Click on the secret name
3. Click "Update secret"
4. Enter new value

---

## 🎯 Workflow Features

### Automatic Triggers
- ✅ Runs on every push to `main`
- ✅ Can be manually triggered from GitHub UI

### What It Does
1. Checks out your code
2. Sets up Python
3. Runs `build.py` to generate HTML
4. Configures AWS credentials
5. Uploads to S3 with proper headers
6. Shows deployment summary

### Deployment Time
- **Typical duration:** 30-60 seconds
- **Cost:** FREE (GitHub Actions has generous free tier)

---

## 🚀 Next Steps

### Add More Environments

Create separate workflows for staging and production:

```yaml
# .github/workflows/deploy-staging.yml
on:
  push:
    branches: [ develop ]
# Deploy to: autobuild-staging bucket
```

```yaml
# .github/workflows/deploy-production.yml
on:
  push:
    branches: [ main ]
# Deploy to: autobuild-time-display-static bucket
```

### Add Tests

Add a testing job before deployment:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 -m py_compile build.py
      
  deploy:
    needs: test  # Only deploy if tests pass
    runs-on: ubuntu-latest
    # ... deployment steps
```

### Notifications

Get notified when deployments complete:

```yaml
- name: Notify on success
  if: success()
  run: |
    # Send Slack notification, email, etc.
```

---

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS Credentials Action](https://github.com/aws-actions/configure-aws-credentials)
- [GitHub CLI](https://cli.github.com/)

---

## ✅ Checklist

- [ ] Created IAM user or identified existing credentials
- [ ] Added `AWS_ACCESS_KEY_ID` to GitHub secrets
- [ ] Added `AWS_SECRET_ACCESS_KEY` to GitHub secrets
- [ ] Tested workflow with a commit or manual trigger
- [ ] Verified deployment at website URL
- [ ] Set up proper IAM permissions (minimal access)

---

**Your CI/CD is now set up!** Every push to `main` will automatically deploy your changes. 🎉
