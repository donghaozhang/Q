# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Suna (Q) is an open-source generalist AI agent platform built with a modern, scalable architecture. The platform combines a FastAPI backend, Next.js frontend, Docker-based agent execution environment, and Supabase for data persistence.

**Project Branding**: Originally "Kortix Suna", now branded as "Quriosity Q".

## Architecture

### Backend (Python/FastAPI)
- **Entry Point**: `backend/api.py` - Main FastAPI application with comprehensive middleware
- **Agent Framework**: `backend/agentpress/` - Custom framework for agent execution
- **Services**: `backend/services/` - Business logic layer (LLM, Supabase, billing, etc.)
- **Tools**: `backend/agent/tools/` - Agent tool implementations
- **MCP Integration**: `backend/mcp_local/` - Model Context Protocol support

### Frontend (Next.js 14/React)
- **Entry Point**: `frontend/src/app/layout.tsx` - App Router with theme provider
- **Structure**: Route groups `(dashboard)`, `(home)` for organization
- **Components**: Feature-based organization with co-located `_components`, `_hooks`, `_types`
- **UI**: Tailwind CSS with shadcn/ui components

### Agent Execution Environment
- **Sandbox**: Docker containers for secure tool execution
- **Browser Automation**: Playwright integration for web tasks
- **File System**: Secure file operations within containers

### Database & Storage
- **Primary**: Supabase (PostgreSQL) for all data persistence
- **Authentication**: Supabase Auth with JWT tokens
- **Storage**: Supabase Storage for files and media
- **Cache**: Redis for session management and caching

## Development Commands

### Setup & Environment
```bash
# Initial setup (interactive wizard)
python setup.py

# Start services (development)
python start.py

# Using Docker Compose (recommended)
docker compose up -d

# Manual setup infrastructure only
docker compose up redis rabbitmq -d
```

### WSL-Specific Quick Start
```bash
# WSL startup script with Windows Terminal integration
./scripts/run-all.sh

# Fast Docker build with optimizations
./scripts/build-fast.sh --optimized

# Manual start with pre-built images
docker pull ghcr.io/suna-ai/suna-backend:latest
docker compose up -d
```

### Frontend Development
```bash
cd frontend
npm install                    # Install dependencies
npm run dev                   # Development server (localhost:3000)
npm run build                 # Production build
npm run lint                  # ESLint
npm run format                # Prettier formatting
npm run format:check          # Check formatting
```

### Backend Development
```bash
cd backend
uv sync                       # Install Python dependencies
uv run python api.py          # Start main API server (localhost:8000)
uv run python sandbox/api.py  # Start sandbox API server
uv run python mcp_local/api.py # Start MCP server
uv run dramatiq --processes 4 --threads 4 run_agent_background  # Background worker
```

### Docker Commands
```bash
# Use modern syntax (space, not hyphen)
docker compose up -d          # Start all services
docker compose down           # Stop all services
docker compose logs -f        # Follow logs
docker compose ps             # Check service status
docker compose restart backend # Restart specific service
```

### Testing
```bash
cd backend
uv run pytest tests/          # Run backend tests
uv run python tests/check_projects.py  # Project validation

cd frontend
npm test                      # Run frontend tests
```

## Key Architecture Patterns

### Agent System
- **ThreadManager**: Central conversation orchestrator with token compression
- **Tool Registry**: Dynamic tool registration with schema support
- **Agent Runner**: Multi-model LLM integration with tool calling
- **MCP Integration**: External tool server support

### Service Layer
- **Singleton Pattern**: Database connections with proper lifecycle management
- **Async/Await**: Consistent async patterns throughout
- **Structured Logging**: Request tracking with context binding
- **Provider-Agnostic**: LLM abstraction supporting multiple providers

### Frontend Patterns
- **Server/Client Components**: Proper Next.js App Router usage
- **React Query**: Data fetching and state management
- **Feature-Based Organization**: Components grouped by functionality
- **Theme System**: Dark/light mode with Tailwind CSS

### Tool Development
```python
# Tool implementation pattern
from agentpress.tool import Tool
from agentpress.decorators import openapi_schema

@openapi_schema({
    "name": "tool_name",
    "description": "Tool description",
    "parameters": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
})
class CustomTool(Tool):
    async def run(self, param: str) -> dict:
        # Tool implementation
        return {"result": "success"}
```

### Component Development
```typescript
// Frontend component pattern
'use client'  // Only when needed

import { cn } from '@/lib/utils'

interface ComponentProps {
  className?: string
  children?: React.ReactNode
}

export function Component({ className, children }: ComponentProps) {
  return (
    <div className={cn("default-classes", className)}>
      {children}
    </div>
  )
}
```

## Environment Configuration

### Required Environment Variables
- **Supabase**: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
- **LLM Providers**: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`
- **Search/Scraping**: `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`
- **Agent Execution**: `DAYTONA_API_KEY` (for sandboxing)
- **Workflows**: `QSTASH_TOKEN`, `QSTASH_CURRENT_SIGNING_KEY`, `QSTASH_NEXT_SIGNING_KEY`
- **MCP**: `MCP_CREDENTIAL_ENCRYPTION_KEY`

### Optional Integrations
- **RapidAPI**: `RAPID_API_KEY` (for additional data sources)
- **Smithery**: `SMITHERY_API_KEY` (for custom agents)
- **Slack**: `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET` (for integrations)

## Important Implementation Notes

### Agent Execution
- Agents run in isolated Docker containers via Daytona
- Tools are dynamically registered based on agent configuration
- Supports multi-model LLM integration with unified interface
- Implements token compression for long conversations

### Database Patterns
- Row Level Security (RLS) policies for data isolation
- BasejumpDB for team/account management
- Async Supabase client throughout backend
- File uploads handled via base64 conversion

### Frontend Architecture
- Next.js App Router with TypeScript
- Tailwind CSS with dark/light theme support
- React Query for server state management
- Component library based on shadcn/ui

### Security Considerations
- All agent execution happens in sandboxed containers
- JWT-based authentication with Supabase
- Environment variable encryption for sensitive data
- CORS configuration for development and production

### Performance Optimizations
- Redis caching for frequently accessed data
- Streaming LLM responses for real-time interaction
- Connection pooling for database operations
- Lazy loading for large components

## Common Development Tasks

### Adding New Agent Tools
1. Create tool class in `backend/agent/tools/`
2. Implement async `run` method with proper error handling
3. Add schema decoration (`@openapi_schema` or `@xml_schema`)
4. Register tool in agent configuration
5. Add tests in `backend/tests/`

### Creating Frontend Components
1. Create component in appropriate `_components/` directory
2. Follow TypeScript interface patterns
3. Use `cn()` utility for conditional classes
4. Add to component exports if reusable
5. Test responsive behavior

### Database Schema Changes
1. Create migration in `backend/supabase/migrations/`
2. Update TypeScript types if needed
3. Test migration with `supabase db push`
4. Update RLS policies if necessary

### Environment Setup
- Use `python setup.py` for guided configuration
- Environment files are automatically generated
- Supports both Docker and manual setup methods
- Progress is saved and resumable

## Debugging & Troubleshooting

### Backend Issues
- Check logs: `docker compose logs backend -f`
- Verify environment variables in `backend/.env`
- Test database connection via Supabase dashboard
- Validate API endpoints at `http://localhost:8000/docs`

### Frontend Issues
- Check logs: `docker compose logs frontend -f`
- Verify environment variables in `frontend/.env.local`
- Test API connectivity to backend
- Check React Query devtools for data fetching issues

### Agent Execution Issues
- Verify Daytona snapshot creation and configuration
- Check agent logs in database `threads` table
- Validate tool schemas and implementations
- Test individual tools via API endpoints

### Common Errors
- **CORS Issues**: Check `get_cors_origins()` in `backend/api.py`
- **Database Connection**: Verify Supabase credentials and network access
- **Tool Execution**: Check container logs and tool implementations
- **Authentication**: Verify JWT token format and expiration

### WSL-Specific Issues
- **Docker not running**: Start Docker Desktop on Windows first
- **Slow builds**: Use pre-built images with `docker-compose.override.yml`
- **File watching**: Set `WATCHPACK_POLLING=true` for Next.js in WSL
- **Performance**: Store code in WSL filesystem, not Windows mount (`/mnt/c/`)

## Recent Fixes & Solutions

### CORS and Connectivity Issues (Fixed 2025-07-04)
**Problem**: Frontend getting "Failed to fetch" and CORS errors when connecting to backend
**Root Causes**:
1. Multiple backend processes running simultaneously causing port conflicts
2. Missing Python dependencies (sentry-sdk, openai, litellm, etc.)
3. Service startup timing issues

**Solution**:
```bash
# 1. Clean install all dependencies
cd /home/zdhpe/suna/Q/backend
source venv/bin/activate
pip install -r requirements.txt

# 2. Kill any conflicting processes
pkill -f "python api.py"

# 3. Start services cleanly using tmux
tmux new-session -d -s backend-final -c /home/zdhpe/suna/Q/backend 'source venv/bin/activate && python api.py'
tmux new-session -d -s workers-final -c /home/zdhpe/suna/Q/backend 'source venv/bin/activate && python -m dramatiq run_agent_background.worker'
tmux new-session -d -s frontend-complete -c /home/zdhpe/suna/Q/frontend 'npm run dev'

# 4. Verify services
curl http://localhost:8000/api/health  # Should return {"status":"ok"}
curl http://localhost:3000             # Should return HTML page
```

**Key Learnings**:
- Always activate Python virtual environment before starting backend
- Check for port conflicts using `ss -tlnp | grep 8000`
- Use tmux for better service management in development
- Install all requirements.txt dependencies to avoid missing module errors

### Authentication Requirements
**Current Status**: Platform requires user authentication to access agent functionality
- **Agents endpoint**: Returns 401 without valid JWT token
- **Agent execution**: Requires authenticated user for agent creation and runs
- **Frontend access**: Works without auth but agent features need login

**To Use Platform**:
1. Navigate to http://localhost:3000
2. Click "Get started" button
3. Sign up/login with Supabase authentication
4. Access full agent functionality once authenticated

### Service Architecture
**Confirmed Working Setup**:
- **Backend**: FastAPI on port 8000 with Python venv activation
- **Frontend**: Next.js on port 3000 with npm
- **Workers**: Dramatiq background workers for agent execution
- **Database**: Supabase with proper CORS configuration
- **Authentication**: Supabase Auth with JWT tokens

### Development Workflow
1. **Environment Setup**: Use Python venv for backend, npm for frontend
2. **Service Management**: Use tmux sessions for better process control
3. **Dependency Management**: Install all requirements.txt packages before starting
4. **Testing**: Verify health endpoints before proceeding with development
5. **Authentication**: Sign up in browser to access full platform features