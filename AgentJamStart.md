# 🚀 Metorial MCP Hackathon Template

A ready-to-deploy website template for integrating WhatsApp via Metorial's Model Context Protocol (MCP). Perfect for hackathons - customize in minutes!

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Setup Instructions](#setup-instructions)
- [Hackathon Customization Guide](#hackathon-customization-guide)
- [File Structure](#file-structure)
- [API Integration](#api-integration)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Start

### Prerequisites
- A Metorial account with WhatsApp MCP deployment
- A code editor (VS Code, Cursor, etc.)
- A web browser
- Your Metorial API key

### 5-Minute Setup

1. **Clone/Download the template files to your local machine**

2. **Update your credentials in `config.js`:**
   ```javascript
   METORIAL_API_KEY: 'metorial_sk_YOUR_ACTUAL_KEY',
   DEPLOYMENT_ID: 'svd_0mhc9f3hjdYjgYZXP6M2SN',  // Your deployment ID
   ```

3. **Open `index.html` in your browser**

4. **Test the demo** - Send a WhatsApp message!

That's it! Now customize for your use case.

---

## 🔧 Setup Instructions

### Step 1: Get Your Metorial Credentials

1. Go to [app.metorial.com](https://app.metorial.com)
2. Navigate to **API** in the sidebar
3. Click **"Create API Key"**
4. Copy your secret key (starts with `metorial_sk_`)
5. Go to **Connect > Deployments**
6. Copy your WhatsApp deployment ID (starts with `svd_`)

### Step 2: Configure the Template

Open `config.js` and update:

```javascript
const CONFIG = {
    METORIAL_API_KEY: 'metorial_sk_abc123...',  // Paste your key here
    DEPLOYMENT_ID: 'svd_0mhc9f3hjdYjgYZXP6M2SN',  // Paste your deployment ID
    API_BASE_URL: 'https://api.metorial.com/v1',
    
    SETTINGS: {
        timeout: 30000,
        maxRetries: 3,
        debug: true
    }
};
```

### Step 3: Test Locally

1. Open `index.html` in a web browser
2. Scroll to the "Try It Out" section
3. Enter a phone number (with country code): `+1234567890`
4. Enter a message: `Hello from my template!`
5. Click "Send Message"

**Note:** Remember to add your phone number to Meta's approved recipient list first!

---

## 🎨 Hackathon Customization Guide

### Quick Customization (5 minutes)

At the hackathon, you only need to change a few things to adapt this template to your use case:

#### 1. Update the Hero Section

**File:** `index.html` (lines 20-28)

```html
<section class="hero">
    <div class="container">
        <!-- CHANGE THESE TWO LINES -->
        <h1 class="hero-title">Your Use Case Title</h1>
        <p class="hero-subtitle">Your subtitle explaining the use case</p>
        <button class="cta-button" onclick="scrollToDemo()">Try It Now</button>
    </div>
</section>
```

**Examples:**
- Customer Support: `"AI Customer Support Bot"` / `"Get instant answers 24/7"`
- Marketing: `"Smart Marketing Campaigns"` / `"Reach customers with targeted WhatsApp messages"`
- Orders: `"Order Notification System"` / `"Real-time updates for your customers"`

#### 2. Update Features (Optional)

**File:** `index.html` (lines 32-58)

Change the feature cards:

```html
<div class="feature-card">
    <div class="feature-icon">💬</div>  <!-- Change emoji -->
    <h3>Your Feature Name</h3>          <!-- Change title -->
    <p>Your feature description</p>      <!-- Change description -->
</div>
```

#### 3. Customize Colors (Optional)

**File:** `styles.css` (lines 1-15)

```css
:root {
    --primary-color: #6366f1;      /* Main brand color */
    --secondary-color: #10b981;    /* Accent color */
    --accent-color: #f59e0b;       /* Highlight color */
}
```

**Popular color schemes:**
- **Tech Blue:** `#3b82f6`
- **Success Green:** `#10b981`
- **Vibrant Purple:** `#8b5cf6`
- **Energetic Orange:** `#f97316`

#### 4. JavaScript Customization (Advanced)

Use the built-in customization API:

```javascript
// Add this to a <script> tag at the bottom of index.html
window.addEventListener('DOMContentLoaded', () => {
    MetorialApp.customize({
        heroTitle: 'AI Customer Support',
        heroSubtitle: 'Automate your customer service',
        features: [
            { icon: '🎧', name: '24/7 Support', description: 'Always available' },
            { icon: '⚡', name: 'Instant', description: 'Real-time responses' },
            { icon: '📊', name: 'Analytics', description: 'Track performance' },
            { icon: '🔒', name: 'Secure', description: 'End-to-end encrypted' }
        ]
    });
});
```

---

## 📁 File Structure

```
metorial-template/
├── index.html          # Main HTML file
├── styles.css          # Styling (customize colors here)
├── app.js              # Application logic
├── config.js           # API configuration (UPDATE YOUR KEYS HERE)
└── README.md           # This file
```

### What Each File Does

| File | Purpose | Customize? |
|------|---------|------------|
| `index.html` | Page structure and content | ✅ Yes - Update text, features |
| `styles.css` | Visual styling | ✅ Yes - Change colors, spacing |
| `app.js` | WhatsApp API integration | ⚠️ Only if needed |
| `config.js` | API credentials | ✅ Required - Add your keys |

---

## 🔌 API Integration

### How It Works

```
Your Website (Frontend)
    ↓
    Metorial API
    ↓
    Your WhatsApp MCP Server
    ↓
    Meta WhatsApp Cloud API
    ↓
    Recipient's WhatsApp
```

### Available Functions

The template includes these ready-to-use functions:

#### Send Message
```javascript
const client = new MetorialClient(CONFIG);
await client.sendMessage('+1234567890', 'Hello!');
```

#### Send Template (for approved templates)
```javascript
await client.sendTemplate(
    '+1234567890',
    'hello_world',
    { language: 'en' }
);
```

### Adding New Features

To add custom functionality, extend the `MetorialClient` class in `app.js`:

```javascript
async customFunction(phoneNumber, data) {
    const endpoint = `${this.baseUrl}/deployments/${this.deploymentId}/invoke`;
    
    return this.makeRequest(endpoint, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tool: 'your_tool_name',
            parameters: data
        })
    });
}
```

---

## 💡 Common Use Cases

### Use Case 1: Customer Support Bot

**Quick Changes:**
```javascript
// Hero Section
heroTitle: "AI Customer Support"
heroSubtitle: "Get instant answers to your questions 24/7"

// Features
features: [
    { icon: '🎧', name: '24/7 Availability', description: 'Always there for customers' },
    { icon: '⚡', name: 'Instant Replies', description: 'Real-time automated responses' },
    { icon: '📊', name: 'Track Issues', description: 'Monitor support tickets' },
    { icon: '🤖', name: 'AI-Powered', description: 'Smart contextual answers' }
]
```

**Form Customization:**
- Change "Message" label to "Your Question"
- Add dropdown for issue categories
- Add file upload for screenshots

### Use Case 2: Marketing Campaign Manager

**Quick Changes:**
```javascript
// Hero Section
heroTitle: "WhatsApp Marketing Campaigns"
heroSubtitle: "Reach thousands of customers instantly"

// Features
features: [
    { icon: '📢', name: 'Broadcast', description: 'Send to multiple contacts' },
    { icon: '📈', name: 'Analytics', description: 'Track campaign performance' },
    { icon: '🎯', name: 'Targeting', description: 'Reach the right audience' },
    { icon: '⏰', name: 'Scheduling', description: 'Schedule messages ahead' }
]
```

**Form Customization:**
- Add "Campaign Name" input
- Add "Recipient List" textarea
- Add "Schedule Date/Time" picker

### Use Case 3: Order Notifications

**Quick Changes:**
```javascript
// Hero Section
heroTitle: "Smart Order Notifications"
heroSubtitle: "Keep customers updated in real-time"

// Features
features: [
    { icon: '📦', name: 'Order Updates', description: 'Real-time tracking' },
    { icon: '✅', name: 'Confirmations', description: 'Instant order confirmations' },
    { icon: '🚚', name: 'Delivery', description: 'Track delivery status' },
    { icon: '💳', name: 'Payments', description: 'Payment notifications' }
]
```

**Form Customization:**
- Change "Phone Number" label to "Customer Phone"
- Add "Order Number" input
- Add "Status" dropdown (Processing, Shipped, Delivered)

### Use Case 4: Appointment Reminders

**Quick Changes:**
```javascript
// Hero Section
heroTitle: "Appointment Reminder System"
heroSubtitle: "Never miss an appointment again"

// Features
features: [
    { icon: '📅', name: 'Smart Reminders', description: 'Automated appointment alerts' },
    { icon: '🔔', name: 'Multi-Channel', description: 'SMS + WhatsApp + Email' },
    { icon: '✏️', name: 'Easy Rescheduling', description: 'Let clients reschedule' },
    { icon: '📊', name: 'Show Tracking', description: 'Reduce no-shows' }
]
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Please configure your API credentials"

**Problem:** API key not set correctly

**Solution:**
- Open `config.js`
- Replace `'metorial_sk_YOUR_SECRET_KEY_HERE'` with your actual key
- Make sure there are no extra spaces
- Save the file and refresh your browser

#### 2. "Recipient phone number not in allowed list"

**Problem:** Phone number not verified in Meta

**Solution:**
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Select your app
3. Go to **WhatsApp > API Setup**
4. Click **"Manage phone number list"**
5. Add and verify the recipient number

#### 3. "Invalid phone number format"

**Problem:** Phone number missing country code

**Solution:**
- Use international format: `+1234567890`
- Include the `+` sign
- Include country code (e.g., `+1` for US/Canada)
- No spaces or dashes

#### 4. Message sends but doesn't arrive

**Problem:** Using test number with unverified recipient

**Solution:**
- Verify the recipient number in Meta (see #2 above)
- Or add your own business phone number to Meta

#### 5. CORS Error in Browser Console

**Problem:** Making API requests from local file

**Solution:**
- Use a local server instead of opening HTML directly
- Install Live Server in VS Code
- Or use Python: `python -m http.server 8000`
- Then open `http://localhost:8000`

#### 6. "Access token expired"

**Problem:** Temporary access token from Meta expired

**Solution:**
- Generate a permanent system user token
- Update it in your Metorial deployment settings
- See Meta's documentation on system users

---

## 🎯 Deployment Options

### Option 1: GitHub Pages (Free & Easy)

1. Create a GitHub repository
2. Upload all template files
3. Go to repository Settings > Pages
4. Select "main" branch
5. Your site is live at `https://yourusername.github.io/repo-name`

**⚠️ Security Note:** Don't commit your API key! Use environment variables or a backend proxy.

### Option 2: Netlify (Free & Fast)

1. Go to [netlify.com](https://netlify.com)
2. Drag and drop your template folder
3. Site is live instantly!

### Option 3: Vercel (Free & Optimized)

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your template folder
3. Follow the prompts

### Security Best Practice: Backend Proxy

For production, don't expose your API key in frontend code:

```javascript
// Instead of calling Metorial directly:
// await client.sendMessage(...)

// Call your own backend:
await fetch('/api/send-whatsapp', {
    method: 'POST',
    body: JSON.stringify({ phone, message })
});
```

Then create a simple backend (Node.js, Python, etc.) that:
1. Receives requests from your frontend
2. Calls Metorial API with your secret key
3. Returns the response

---

## 📚 Additional Resources

### Metorial Documentation
- API Reference: [docs.metorial.com](https://docs.metorial.com)
- Dashboard: [app.metorial.com](https://app.metorial.com)

### WhatsApp Cloud API
- Getting Started: [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)
- Message Templates: Create in WhatsApp Manager

### Model Context Protocol (MCP)
- Specification: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- GitHub: [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)

---

## 🎉 Hackathon Tips

### Time-Saving Strategies

1. **Don't start from scratch** - Use this template!
2. **Focus on the use case** - Spend time on the story, not the code
3. **Use browser developer tools** - Test API calls directly
4. **Keep it simple** - One core feature done well beats many half-done
5. **Demo early** - Make sure it works before adding features

### What Judges Look For

- ✅ Clear problem statement
- ✅ Working demo (even if simple)
- ✅ Good UX/UI
- ✅ Practical use case
- ✅ Scalability potential

### 30-Minute Customization Plan

| Time | Task |
|------|------|
| 0-5 min | Update config.js with credentials |
| 5-10 min | Change hero title & subtitle |
| 10-15 min | Update feature cards |
| 15-20 min | Test the demo |
| 20-25 min | Customize colors (optional) |
| 25-30 min | Add your branding |

---

## 🤝 Need Help?

### During the Hackathon

- Check the console (F12) for error messages
- Read the error message carefully - it usually tells you what's wrong
- Ask mentors for help with Metorial-specific issues
- Check Meta's WhatsApp documentation for API errors

### After the Hackathon

- Email: support@metorial.com
- Documentation: docs.metorial.com
- Community: Join the Metorial Discord

---

## 📄 License

This template is provided as-is for hackathon use. Feel free to modify and use for your projects!

---

## 🚀 Quick Reference Commands

```bash
# Open in VS Code
code .

# Start local server (Python)
python -m http.server 8000

# Start local server (Node.js)
npx serve

# Open in browser
open index.html  # Mac
start index.html  # Windows
xdg-open index.html  # Linux
```

---

**Good luck at the hackathon! 🎉**

Remember: The best projects tell a story and solve a real problem. This template handles the technical stuff - you focus on the creative part!
