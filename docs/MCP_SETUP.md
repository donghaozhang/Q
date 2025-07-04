# MCP Servers Setup Guide

This project is configured with Model Context Protocol (MCP) servers to enhance Claude Code capabilities.

## Configured MCP Servers

### 1. 🗄️ Supabase MCP Server
**Purpose:** Direct database interaction and management  
**Features:**
- Database queries and schema exploration
- Table management and data operations  
- Project configuration access
- Storage and Edge Functions management
- **Read-only mode** for safety

### 2. 🎭 Playwright MCP Server  
**Purpose:** Web automation and testing
**Features:**
- Browser automation
- Web scraping capabilities
- End-to-end testing
- Screenshot and PDF generation
- Mobile device emulation

## Setup Instructions

### Step 1: Configure Supabase Access Token

1. **Get your Supabase Personal Access Token:**
   - Go to [Supabase Dashboard](https://supabase.com/dashboard)
   - Navigate to Settings → Access Tokens
   - Create new token: "Claude MCP Server" 
   - Copy the token (you won't see it again)

2. **Update `.mcp.json`:**
   ```bash
   # Replace YOUR_SUPABASE_PERSONAL_ACCESS_TOKEN_HERE 
   # with your actual token in .mcp.json
   ```

### Step 2: Restart Claude Code
After updating the token, restart Claude Code to load the MCP servers.

### Step 3: Verify Setup
Run `claude mcp list` to see configured servers.

## Security Notes

- ✅ **`.mcp.json` is in `.gitignore`** - your tokens won't be committed
- ✅ **Supabase is read-only** - prevents accidental data modifications  
- ✅ **Template provided** - `.mcp.json.example` for reference

## Usage Examples

### Database Operations (Supabase)
```
"Show me all tables in the database"
"What's the schema for the users table?"
"Query the latest 10 user registrations"
```

### Web Automation (Playwright)  
```
"Take a screenshot of google.com"
"Scrape the headlines from a news website"
"Test the login flow on our frontend"
```

## Project Configuration

Current setup for Q project:
- **Supabase Project:** `xvhreblsabiwgfkykvvn`
- **Mode:** Read-only (safe for exploration)
- **Environment:** Development

## Troubleshooting

### MCP servers not showing up?
- Ensure you've added your actual Supabase access token
- Restart Claude Code after configuration changes
- Check that Node.js is installed (`node --version`)

### Node.js Version 
**Current Node.js version:** v20.19.3 ✅  
**Playwright MCP requires:** Node.js >=20.0.0 ✅

**Node.js v20 installed and configured with nvm!**

**To use Node.js v20 in new terminal sessions:**
```bash
# Node.js v20 is now the default version
# nvm will automatically load in new terminals
```

### Permission issues?
- Verify your Supabase access token has proper permissions
- Check that your Supabase project is accessible

Need help? Check the [Claude Code MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp).