# Cherry-Pick Recovery Plan

## Summary
- **Total commits found**: 72
- **WIP commits to skip**: 2 (`feeb33d`, `4b3597a`)
- **Commits to cherry-pick**: 70
- **Batches**: 7 batches of 10 commits each

## Commits to SKIP (WIP commits user doesn't want):
- `feeb33d` - WIP: Save current changes before upstream merge  
- `4b3597a` - WIP: Save current changes before upstream merge

---

## BATCH 1 (Commits 1-10)
```bash
git cherry-pick 214b678  # Recreate comprehensive Cursor Rules after reset ✓ COMPLETED
git cherry-pick 44dee4e  # Add comprehensive Cursor Rules for Suna project ✓ COMPLETED
git cherry-pick 68652bf  # feat: recreate comprehensive Cursor Rules for Suna AI agent platform ✓ SKIPPED (empty)
git cherry-pick bd5bdde  # chore: update Docker configuration and add .dockerignore files ✓ COMPLETED
git cherry-pick 4be515c  # refactor: move Cursor Rules to proper .cursor/rules directory ✓ COMPLETED
git cherry-pick 1d5e215  # Update docker-compose.yaml configuration ✓ COMPLETED
git cherry-pick 7e42571  # Fix VNC URL update issue in sandbox ensure-active endpoint ✓ COMPLETED
git cherry-pick 970198f  # feat: Replace Kortix branding with Quriosity logo and update all references ✓ COMPLETED
git cherry-pick a87ab39  # feat: Increase logo size from 24px to 32px for better visibility ✓ COMPLETED
git cherry-pick f88bafb  # Replace all user-facing 'Suna' references with 'Q' ✓ COMPLETED
```

## BATCH 2 (Commits 11-20)
```bash
git cherry-pick 5757aa4  # Update .cursor/rules with Q branding and correct Docker compose commands ✓ COMPLETED
git cherry-pick d4923e9  # Update homepage content: Replace 'Kortix Suna' with 'Q' ✓ COMPLETED
git cherry-pick 8c140fd  # Fix use cases section: Change 'See Suna in action' to 'See Q in action' ✓ COMPLETED
git cherry-pick 1ac5807  # Replace static thumbnails with live Quriosity website screenshots ✓ COMPLETED
git cherry-pick 64d0717  # Update legal contact email from legal@kortixai.com to info@quriosity.com.au ✓ COMPLETED
git cherry-pick 0471b80  # Update footer GitHub icon to link to Quriosity website ✓ COMPLETED
git cherry-pick b9c396b  # Update Join Our Team link to point to Quriosity website ✓ COMPLETED
git cherry-pick a36a97d  # Update repository name from kortix-ai/suna to Quriosity/Q ✓ COMPLETED
git cherry-pick 87af5a9  # Add Quriosity Showcase section with 6 agent cards ✓ COMPLETED
git cherry-pick ff62200  # Update footer links to point to Quriosity website ✓ COMPLETED
```

## BATCH 3 (Commits 21-30)
```bash
git cherry-pick a588d8e  # Update .cursor rules to reflect Quriosity branding and new showcase section ✓ COMPLETED
git cherry-pick a4e4372  # Fix build error: Remove HeroVideoSection and reduce showcase padding ✓ COMPLETED
git cherry-pick b94e9c3  # Update .cursor rules: Document HeroVideoSection removal and layout optimizations ✓ COMPLETED
git cherry-pick 021d70f  # Add FlickeringGrid backgrounds to all home sections ✓ COMPLETED
git cherry-pick 73eeffd  # Update Cursor rules: Document FlickeringGrid patterns and divider removal standards ✓ COMPLETED
git cherry-pick f5573fc  # UI improvements: Remove lines, fix branding, improve layouts ✓ COMPLETED
git cherry-pick 2f0bf50  # docs: update and streamline cursor rules ✓ COMPLETED
git cherry-pick 2f42f4a  # feat: Organize fal.ai testing code into dedicated backend/fal_testing directory ✓ COMPLETED
git cherry-pick 28670f4  # fix: Remove non-working fal.ai models from test scripts and frontend selector ✓ COMPLETED
git cherry-pick e953b6c  # fix: Add fal tool support to frontend and system prompt ✓ COMPLETED
```

## BATCH 4 (Commits 31-40)
```bash
git cherry-pick e978021  # feat(branding): Update computer panel title from Suna to Q ✓ COMPLETED
git cherry-pick a2d134f  # feat: enhance fal_media_generation tool with improved error handling ✓ COMPLETED
git cherry-pick 901efc7  # feat: enhance fal_media_generation tool with improved error handling ✓ COMPLETED
git cherry-pick 77f948b  # refactor: organize test files into backend/tests directory ✓ COMPLETED
git cherry-pick 6cf82bb  # docs: update cursor rules with feature flag management and troubleshooting ✓ COMPLETED
git cherry-pick 085d009  # Merge remote-tracking branch 'upstream/main' into sync-upstream-changes ✓ SKIPPED (merge commit)
git cherry-pick d839be7  # docs: update cursor rules with infrastructure improvements and troubleshooting guide ✓ COMPLETED
git cherry-pick 1166ae3  # feat: Add Railway deployment configuration ✓ COMPLETED
git cherry-pick 955e3da  # feat: Successfully deploy backend to Railway ✓ COMPLETED
git cherry-pick 8445316  # feat: Successfully deploy Suna backend to Railway with full functionality ✓ COMPLETED
```

## BATCH 5 (Commits 41-50)
```bash
git cherry-pick 47dc169  # chore: Update cursor rules to disable alwaysApply flag
git cherry-pick 31ae5a7  # Fix: Add ESLint ignore config for Railway deployment
git cherry-pick c0bb095  # Fix: Enable TypeScript build error ignoring and update deprecated config
git cherry-pick af5d5e6  # Fix: Add root-level health and feature-flags endpoints for frontend compatibility
git cherry-pick ca6738d  # Fix: Add Railway domains to CORS allowed origins
git cherry-pick 5fbc293  # Fix billing and API endpoints - replace remaining API_URL with getApiUrl() helper
git cherry-pick bf5e5d8  # Add Railway testing workflow and API testing script
git cherry-pick 829176a  # Fix agent API endpoints - replace API_URL with getApiUrl helper in agents utils
git cherry-pick b27a77d  # Add Railway deployment and testing rules
git cherry-pick bfa3251  # Fix API routing issues - update Railway CLI commands to use npx
```

## BATCH 6 (Commits 51-60)
```bash
git cherry-pick 221176d  # Fix remaining API routing issues - replace all API_URL with getApiUrl() helper
git cherry-pick af7202b  # Fix: Centralize getApiUrl function to resolve 404 API routing issues
git cherry-pick 33afc92  # Temp: Disable billing API calls to prevent 404 errors
git cherry-pick 19c1825  # fix: Replace all direct billing API calls with mocks to prevent 404 errors
git cherry-pick dcdf6b1  # fix: Replace ALL billing API functions with mocks
git cherry-pick d4380d4  # Fix WorkspaceFileView TypeScript build error
git cherry-pick d5c3f7b  # feat: add production environment configuration for backend and frontend
git cherry-pick 05c3f7b  # Fix RabbitMQ connection parameters
git cherry-pick d907f36  # Fix RabbitMQ credentials - Use pika.PlainCredentials instead of dict
git cherry-pick ecf6541  # Fix RabbitMQ credentials - Use pika.PlainCredentials instead of dict
```

## BATCH 7 (Commits 61-70)
```bash
git cherry-pick 183dfc4  # Frontend: dynamic backend URL fallback; Backend: allow Railway wildcard CORS
git cherry-pick 1067f50  # chore: standardize formatting in cursor rules
git cherry-pick 3184247  # Update cursor rules with recent deployment and troubleshooting improvements
git cherry-pick 2f551d9  # Merge work-fal branch: Critical bug fixes and deployment improvements
git cherry-pick 34428f7  # fix: share page file load
git cherry-pick 64b1697  # chore: update daytona packages to version 0.21.0a1 and 0.21.0a4
git cherry-pick 61e6d3f  # chore: update daytona packages to version 0.21.0
git cherry-pick 5522622  # feat(setup): enhance ASCII banner with refined Quriosity Q
git cherry-pick 1c74556  # Merge upstream/main: sync latest changes from kortix-ai/suna
git cherry-pick 3710b5f  # docs: update rules for upstream changes and split testing docs
```

---

## Execution Strategy

1. **Prepare**: Ensure we're on `feature/clean-start` branch
2. **Execute batches sequentially**: Run each batch, resolve any conflicts
3. **Test after each batch**: Verify the application still works
4. **Push after every 2-3 batches**: Keep remote updated
5. **Final verification**: Ensure all 70 commits are properly applied

## Conflict Resolution Strategy

- For `.cursor/rules` conflicts: Accept incoming changes (they're documentation updates)
- For code conflicts: Manually resolve, prioritizing functionality
- For config conflicts: Take the newer version unless it breaks something

## Rollback Plan

If any batch fails catastrophically:
```bash
git reset --hard HEAD~[number_of_commits_in_failed_batch]
```

Ready to execute? 🚀 