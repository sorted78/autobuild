#!/usr/bin/env python3
"""
Build script for autobuild static website
Generates the static HTML file for deployment
"""

import os
from datetime import datetime

def generate_html():
    """Generate the static HTML file"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Current Time & Date</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 60px 80px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 40px;
            font-weight: 300;
            letter-spacing: 2px;
        }
        
        .time {
            font-size: 5rem;
            font-weight: 700;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            font-variant-numeric: tabular-nums;
        }
        
        .date {
            font-size: 2rem;
            font-weight: 300;
            margin-bottom: 10px;
        }
        
        .timezone {
            font-size: 1rem;
            opacity: 0.8;
            margin-top: 20px;
        }
        
        .footer {
            margin-top: 40px;
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 40px 30px;
            }
            
            h1 {
                font-size: 1.8rem;
            }
            
            .time {
                font-size: 3rem;
            }
            
            .date {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Current Time & Date</h1>
        <div class="time" id="time">00:00:00</div>
        <div class="date" id="date">Loading...</div>
        <div class="timezone" id="timezone"></div>
        <div class="footer">
            Built with Python | Hosted on AWS S3
        </div>
    </div>
    
    <script>
        function updateDateTime() {
            const now = new Date();
            
            // Update time
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            document.getElementById('time').textContent = `${hours}:${minutes}:${seconds}`;
            
            // Update date
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            const dateString = now.toLocaleDateString('en-US', options);
            document.getElementById('date').textContent = dateString;
            
            // Update timezone
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            document.getElementById('timezone').textContent = timezone;
        }
        
        // Update immediately
        updateDateTime();
        
        // Update every second
        setInterval(updateDateTime, 1000);
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated index.html")
    print(f"  Build time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  File size: {len(html_content)} bytes")

if __name__ == '__main__':
    print("Building autobuild static website...")
    generate_html()
    print("\n✓ Build complete!")
    print("  Ready for deployment to S3")
