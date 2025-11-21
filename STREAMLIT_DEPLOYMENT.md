# 🔑 How to Configure Gemini API Key on Streamlit Cloud

## Step-by-Step Guide

### 1. Get Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### 2. Configure in Streamlit Cloud

#### Method 1: Through App Dashboard
1. Go to your deployed app on Streamlit Cloud
2. Click on the **hamburger menu (☰)** in the top-right
3. Select **"Settings"**
4. Click on the **"Secrets"** tab
5. In the text editor, add:
   ```toml
   GEMINI_API_KEY = "paste_your_actual_api_key_here"
   ```
6. Click **"Save"**
7. Your app will automatically restart with the API key

#### Method 2: During Initial Deployment
1. When deploying a new app on Streamlit Cloud
2. In the "Advanced settings" section
3. Look for "Secrets" text area
4. Add the same content as above
5. Click "Deploy"

### 3. Verify It's Working

After adding the secret:
1. Wait for the app to restart (automatic)
2. In the sidebar, you should see: **"✅ Gemini LLM: Available"**
3. Check the "Enable LLM Insights" checkbox
4. Status should change to: **"✅ Gemini LLM: ENABLED"**
5. Run an analysis - insights will now be AI-generated!

### 4. Troubleshooting

**If you see "⚠️ Gemini LLM: DISABLED":**

1. **Check the secret name**: Must be exactly `GEMINI_API_KEY` (case-sensitive)
2. **Check the format**: Use `GEMINI_API_KEY = "your_key"` not `GEMINI_API_KEY: "your_key"`
3. **Verify the key**: Copy it again from Google AI Studio
4. **Wait for restart**: Give it 30-60 seconds after saving
5. **Check app logs**: Look for any error messages in the logs

**If insights still don't work:**
- Make sure you checked the "Enable LLM Insights" checkbox
- Try refreshing the page
- Check that your API key has quota remaining
- Verify the key is valid at [Google AI Studio](https://aistudio.google.com/)

### 5. Security Notes

✅ **Safe**: API keys in Streamlit Secrets are:
- Encrypted at rest
- Not visible in your code
- Not exposed in URLs or logs
- Only accessible to your app

❌ **Never**:
- Commit API keys to GitHub
- Share them publicly
- Include them in code files

### Example Secret Configuration

```toml
# In Streamlit Cloud Secrets editor
GEMINI_API_KEY = "AIzaSyD6oV0PFrSGPuQL0yovxFA87E4vFVykMI4"
```

Replace with your actual key!

---

## Quick Links
- 🔗 [Your GitHub Repo](https://github.com/DeveloperDeva/ADQIA)
- 🚀 [Streamlit Cloud](https://share.streamlit.io)
- 🔑 [Get Gemini API Key](https://makersuite.google.com/app/apikey)
- 📚 [Streamlit Secrets Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
