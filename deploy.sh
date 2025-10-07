#!/bin/bash

# Deployment script for autobuild to AWS S3
# This script uploads the static website to S3 and configures it for public access

set -e

# Configuration
BUCKET_NAME="autobuild-static-site"  # Change this to your bucket name
REGION="us-east-1"  # Change to your preferred region

echo "====================================="
echo "  Autobuild S3 Deployment Script"
echo "====================================="
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ Error: AWS CLI is not installed"
    echo "   Install it from: https://aws.amazon.com/cli/"
    exit 1
fi

echo "Step 1: Building the website..."
python3 build.py
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not generated"
    exit 1
fi
echo ""

echo "Step 2: Checking if S3 bucket exists..."
if aws s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
    echo "   Bucket doesn't exist. Creating bucket: $BUCKET_NAME"
    aws s3 mb "s3://$BUCKET_NAME" --region "$REGION"
    echo "   ✓ Bucket created"
else
    echo "   ✓ Bucket exists"
fi
echo ""

echo "Step 3: Uploading files to S3..."
aws s3 cp index.html "s3://$BUCKET_NAME/index.html" \
    --content-type "text/html" \
    --cache-control "max-age=300"
echo "   ✓ Files uploaded"
echo ""

echo "Step 4: Configuring bucket for static website hosting..."
aws s3 website "s3://$BUCKET_NAME" \
    --index-document index.html \
    --error-document index.html
echo "   ✓ Website hosting configured"
echo ""

echo "Step 5: Setting public access policy..."
cat > /tmp/bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
    }
  ]
}
EOF

aws s3api put-bucket-policy \
    --bucket "$BUCKET_NAME" \
    --policy file:///tmp/bucket-policy.json

echo "   ✓ Public access configured"
rm /tmp/bucket-policy.json
echo ""

echo "====================================="
echo "  ✓ Deployment Complete!"
echo "====================================="
echo ""
echo "Your website is available at:"
echo "http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo ""
echo "Cost estimate: ~$0.50/month for low traffic"
echo "  - S3 storage: ~$0.023/GB/month"
echo "  - Data transfer: First 100GB/month free"
echo ""
