#!/bin/bash
# Start Dramatiq workers with resource limits to prevent WSL crashes

# Set resource limits
export DRAMATIQ_PROCESSES=2  # Reduce from 4 to 2
export DRAMATIQ_THREADS=2    # Reduce from 4 to 2

# Set memory limits for Python
export PYTHONMALLOC=malloc
export MALLOC_TRIM_THRESHOLD_=100000

# Activate virtual environment
source venv/bin/activate

# Kill any existing workers
pkill -f "dramatiq run_agent_background"

# Start workers with limited resources
echo "Starting Dramatiq workers with limited resources..."
echo "Processes: $DRAMATIQ_PROCESSES"
echo "Threads: $DRAMATIQ_THREADS"

# Run with nice to lower priority and prevent system overload
nice -n 10 python -m dramatiq \
    --processes $DRAMATIQ_PROCESSES \
    --threads $DRAMATIQ_THREADS \
    --watch . \
    run_agent_background.worker

# Alternative: Use this command if you experience crashes
# nice -n 10 python -m dramatiq \
#     --processes 1 \
#     --threads 1 \
#     --watch . \
#     run_agent_background.worker