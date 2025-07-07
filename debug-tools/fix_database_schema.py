#!/usr/bin/env python3
"""
Fix database schema by adding missing agent_id column to agent_runs table
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def fix_database_schema():
    """Add missing agent_id column to agent_runs table"""
    
    # Get Supabase connection details
    supabase_url = os.getenv('SUPABASE_URL', 'https://xvhreblsabiwgfkykvvn.supabase.co')
    
    # Extract host from URL
    host = supabase_url.replace('https://', '').replace('.supabase.co', '')
    
    # Connection details for direct PostgreSQL connection
    connection_params = {
        'host': f'db.{host}.supabase.co',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
    }
    
    try:
        print("Connecting to Supabase PostgreSQL database...")
        
        # Note: This approach requires the Supabase project to allow direct PostgreSQL connections
        # which may not be available for all plans
        conn = await asyncpg.connect(**connection_params)
        
        print("Connected successfully!")
        
        # Check if agent_id column exists
        check_column_sql = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'agent_runs' AND column_name = 'agent_id';
        """
        
        result = await conn.fetch(check_column_sql)
        
        if result:
            print("✓ agent_id column already exists in agent_runs table")
        else:
            print("Adding agent_id column to agent_runs table...")
            
            # Add the missing column
            alter_table_sql = """
            ALTER TABLE agent_runs 
            ADD COLUMN IF NOT EXISTS agent_id UUID;
            """
            
            await conn.execute(alter_table_sql)
            print("✓ Successfully added agent_id column to agent_runs table")
            
            # Add index for performance
            create_index_sql = """
            CREATE INDEX IF NOT EXISTS idx_agent_runs_agent_id ON agent_runs(agent_id);
            """
            
            await conn.execute(create_index_sql)
            print("✓ Successfully created index on agent_id column")
        
        await conn.close()
        print("Database schema fix completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Direct PostgreSQL connections may not be available for all Supabase plans.")
        print("If this fails, you may need to apply the migration through the Supabase dashboard.")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(fix_database_schema())
    if not success:
        exit(1)