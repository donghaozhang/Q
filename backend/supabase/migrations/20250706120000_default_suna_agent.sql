-- Migration: Create Default Suna Agent for New Users
-- Description: Automatically creates a default "Suna" agent for users who don't have one
-- Date: 2025-07-06

-- Create function to generate default agent configuration
CREATE OR REPLACE FUNCTION get_default_suna_agent_config()
RETURNS jsonb
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN jsonb_build_object(
        'sb_files_tool', jsonb_build_object(
            'enabled', true,
            'description', 'File management operations',
            'icon', '📁'
        ),
        'sb_shell_tool', jsonb_build_object(
            'enabled', true,
            'description', 'Execute shell commands in tmux sessions',
            'icon', '💻'
        ),
        'sb_browser_tool', jsonb_build_object(
            'enabled', true,
            'description', 'Browser automation for web interaction',
            'icon', '🌐'
        ),
        'web_search_tool', jsonb_build_object(
            'enabled', true,
            'description', 'Web search using Tavily API',
            'icon', '🔍'
        ),
        'sb_vision_tool', jsonb_build_object(
            'enabled', false,
            'description', 'Image processing capabilities',
            'icon', '👁️'
        ),
        'sb_deploy_tool', jsonb_build_object(
            'enabled', false,
            'description', 'Application deployment capabilities',
            'icon', '🚀'
        ),
        'sb_expose_tool', jsonb_build_object(
            'enabled', false,
            'description', 'Service and port management',
            'icon', '🔌'
        ),
        'data_providers_tool', jsonb_build_object(
            'enabled', false,
            'description', 'External API data access',
            'icon', '🔗'
        )
    );
END;
$$;

-- Get the default Suna system prompt
CREATE OR REPLACE FUNCTION get_default_suna_system_prompt()
RETURNS text
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN 'You are Suna.so, an autonomous AI Agent created by the Kortix team.

# 1. CORE IDENTITY & CAPABILITIES
You are a full-spectrum autonomous agent capable of executing complex tasks across domains including information gathering, content creation, software development, data analysis, and problem-solving. You have access to a Linux environment with internet connectivity, file system operations, terminal commands, web browsing, and programming runtimes.

# 2. EXECUTION ENVIRONMENT

## 2.1 WORKSPACE CONFIGURATION
- WORKSPACE DIRECTORY: You are operating in the "/workspace" directory by default
- All file paths must be relative to this directory (e.g., use "src/main.py" not "/workspace/src/main.py")
- Never use absolute paths or paths starting with "/workspace" - always use relative paths
- All file operations (create, read, write, delete) expect paths relative to "/workspace"

## 2.2 SYSTEM INFORMATION
- BASE ENVIRONMENT: Python 3.11 with Debian Linux (slim)
- CURRENT YEAR: 2025
- INSTALLED TOOLS:
  * PDF Processing: poppler-utils, wkhtmltopdf
  * Document Processing: antiword, unrtf, catdoc
  * Text Processing: grep, gawk, sed
  * File Analysis: file
  * Data Processing: jq, csvkit, xmlstarlet
  * Utilities: wget, curl, git, zip/unzip, tmux, vim, tree, rsync
  * JavaScript: Node.js 20.x, npm
- BROWSER: Chromium with persistent session support
- PERMISSIONS: sudo privileges enabled by default

## 2.3 OPERATIONAL CAPABILITIES
You have the ability to execute operations using both Python and CLI tools:

### 2.3.1 FILE OPERATIONS
- Creating, reading, modifying, and deleting files
- Organizing files into directories/folders
- Converting between file formats
- Searching through file contents
- Batch processing multiple files

### 2.3.2 DATA PROCESSING
- Scraping and extracting data from websites
- Parsing structured data (JSON, CSV, XML)
- Cleaning and transforming datasets
- Analyzing data using Python libraries
- Generating reports and visualizations

### 2.3.3 SYSTEM OPERATIONS
- Running CLI commands and scripts
- Compressing and extracting archives (zip, tar)
- Managing processes and services
- Network operations and API interactions
- Version control with git

### 2.3.4 WEB DEVELOPMENT
- Creating HTML, CSS, JavaScript applications
- Building responsive web interfaces
- Implementing interactive features
- Testing web applications

# 3. COMMUNICATION PROTOCOL
- Be concise but thorough in explanations
- Confirm understanding before proceeding with complex tasks
- Provide progress updates for long-running operations
- Ask clarifying questions when requirements are ambiguous
- Always explain your approach before executing

# 4. TOOL USAGE GUIDELINES
- Use appropriate tools for each task
- Always verify file operations completed successfully
- Test code before considering tasks complete
- Handle errors gracefully and report issues clearly
- Clean up temporary files when done

You are ready to help with any task that requires autonomous execution in this environment.';
END;
$$;

-- Function to create default Suna agent for an account
CREATE OR REPLACE FUNCTION create_default_suna_agent(account_id_param uuid)
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    new_agent_id uuid;
    new_version_id uuid;
    existing_default_count int;
BEGIN
    -- Check if account already has a default agent
    SELECT COUNT(*)
    INTO existing_default_count
    FROM agents
    WHERE account_id = account_id_param AND is_default = true;
    
    -- Only create if no default agent exists
    IF existing_default_count = 0 THEN
        -- Generate UUIDs
        new_agent_id := gen_random_uuid();
        new_version_id := gen_random_uuid();
        
        -- Create the agent
        INSERT INTO agents (
            agent_id,
            account_id,
            name,
            description,
            system_prompt,
            configured_mcps,
            agentpress_tools,
            is_default,
            avatar,
            avatar_color,
            current_version_id,
            is_public,
            created_at,
            updated_at
        ) VALUES (
            new_agent_id,
            account_id_param,
            'Suna',
            'Your AI assistant for building and automating workflows',
            get_default_suna_system_prompt(),
            '{}',  -- Empty MCP config
            get_default_suna_agent_config(),
            true,  -- is_default
            null,  -- avatar (will use default)
            '#3B82F6',  -- blue color
            new_version_id,
            false,  -- not public
            now(),
            now()
        );
        
        -- Create the initial version
        INSERT INTO agent_versions (
            version_id,
            agent_id,
            version_number,
            version_name,
            system_prompt,
            configured_mcps,
            custom_mcps,
            agentpress_tools,
            is_active,
            created_at,
            updated_at
        ) VALUES (
            new_version_id,
            new_agent_id,
            1,
            'v1',
            get_default_suna_system_prompt(),
            '{}',  -- Empty MCP config
            '{}',  -- Empty custom MCP config
            get_default_suna_agent_config(),
            true,  -- is_active
            now(),
            now()
        );
        
        RETURN new_agent_id;
    END IF;
    
    RETURN null;
END;
$$;

-- Function to ensure user has default agent (called from backend)
CREATE OR REPLACE FUNCTION ensure_default_agent(account_id_param uuid)
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    default_agent_id uuid;
    agent_count int;
BEGIN
    -- Check if user has any agents at all
    SELECT COUNT(*)
    INTO agent_count
    FROM agents
    WHERE account_id = account_id_param;
    
    -- If user has no agents, create default Suna agent
    IF agent_count = 0 THEN
        SELECT create_default_suna_agent(account_id_param) INTO default_agent_id;
        RETURN default_agent_id;
    END IF;
    
    -- Check if user has a default agent
    SELECT agent_id
    INTO default_agent_id
    FROM agents
    WHERE account_id = account_id_param AND is_default = true
    LIMIT 1;
    
    -- If no default agent but has other agents, make the first one default
    IF default_agent_id IS NULL THEN
        SELECT agent_id
        INTO default_agent_id
        FROM agents
        WHERE account_id = account_id_param
        ORDER BY created_at ASC
        LIMIT 1;
        
        -- Update the first agent to be default
        UPDATE agents
        SET is_default = true, updated_at = now()
        WHERE agent_id = default_agent_id;
    END IF;
    
    RETURN default_agent_id;
END;
$$;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_agents_account_default 
ON agents(account_id, is_default) 
WHERE is_default = true;

-- Grant necessary permissions
GRANT EXECUTE ON FUNCTION get_default_suna_agent_config() TO authenticated;
GRANT EXECUTE ON FUNCTION get_default_suna_system_prompt() TO authenticated;
GRANT EXECUTE ON FUNCTION create_default_suna_agent(uuid) TO authenticated;
GRANT EXECUTE ON FUNCTION ensure_default_agent(uuid) TO authenticated;

-- Create default agents for existing users who don't have any
DO $$
DECLARE
    account_record RECORD;
    new_agent_id uuid;
BEGIN
    -- Loop through all accounts that don't have any agents
    FOR account_record IN 
        SELECT DISTINCT a.id as account_id
        FROM basejump.accounts a
        LEFT JOIN agents ag ON ag.account_id = a.id
        WHERE ag.agent_id IS NULL
    LOOP
        -- Create default agent for this account
        SELECT create_default_suna_agent(account_record.account_id) INTO new_agent_id;
        
        IF new_agent_id IS NOT NULL THEN
            RAISE NOTICE 'Created default Suna agent % for account %', new_agent_id, account_record.account_id;
        END IF;
    END LOOP;
END;
$$;