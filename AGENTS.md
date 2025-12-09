# AI Agents Guide

This document provides core principles for AI coding assistants.

## Core Principles

### Universal Standards
- **Language**: 
  - Code, comments, and documentation: **English only**
  - Agent communication with user: **Spanish only**
  - GitLab/Linear issues: **Spanish only**
  - Multilingual projects: **Must use i18n** (according to specs)
- **Commits**: Clear, descriptive commit messages using conventional commits
- **Naming**: Descriptive, self-documenting names
- **Comments**: Explain "why" not "what" - code should be self-explanatory
- **Modification First**: Always modify existing files before creating new ones
- **Documentation**: Only generate for major features, not every small change
- **MCP Tools**: Use available MCP tools for every task
- **Verification**: Always verify changes before declaring completion
- **Memory**: Save all important information to Mem0
- **Context7**: Always use Context7 for library documentation
- **Task Tracking**: Track all tasks in GitLab
- **Autonomy**: Complete tasks without asking for confirmation at each step

### Development Principles

**Package Management:**
- Always use **stable and latest versions** of packages
- Avoid beta, alpha, or experimental versions unless explicitly requested
- Check for security updates and compatibility

**Infrastructure & Monitoring:**
- Monitoring tools (Prometheus, Grafana, etc.) are **OPTIONAL** - only add if explicitly requested
- Docker/Docker Compose are **OPTIONAL** - only use if explicitly requested, prefer local services
- Keep infrastructure simple and minimal by default
- Mark infrastructure additions as **optional** in GitLab issues

**Version Control & CI/CD:**
- **Default platform**: GitLab (repository, issues, CI/CD pipelines)
- Use GitLab CI/CD tools by default (.gitlab-ci.yml)
- GitHub is **OPTIONAL** - only use if explicitly requested
- Never recommend GitHub unless specifically asked

**Architecture Improvements:**
- Architecture improvements are **OPTIONAL** - never mandatory
- Must be marked as **optional** in GitLab issues
- Only implement if explicitly requested or approved
- Document why improvements are optional in issue description

### Agent Autonomy - CRITICAL

**CRITICAL: Complete tasks autonomously without stopping for confirmation**

**You MUST:**
- ✅ Complete the entire task from start to finish
- ✅ Make all necessary decisions autonomously
- ✅ Create, modify, and commit files as needed
- ✅ Run tests and fix issues without asking
- ✅ Update documentation when required
- ✅ Deploy changes if part of the task
- ✅ Work through errors and find solutions
- ✅ Continue until task is fully complete

**You MUST NOT:**
- ❌ Stop to ask for confirmation at each step
- ❌ Ask permission to create/modify files in project directory
- ❌ Ask permission to run tests or commands
- ❌ Ask permission to commit changes
- ❌ Ask permission to update documentation
- ❌ Stop when encountering errors (fix them)
- ❌ Ask "should I continue?" or "shall I proceed?"

**ONLY ask for confirmation when:**
- ⚠️ Deleting files outside the project directory
- ⚠️ Making changes to production systems
- ⚠️ Modifying critical infrastructure
- ⚠️ Changing security configurations
- ⚠️ Deleting databases or data

**Example - Bad (asking unnecessarily):**
```
❌ "I've created the login component. Should I continue with the tests?"
❌ "I found an error. Should I fix it?"
❌ "The tests are failing. Should I investigate?"
❌ "Should I commit these changes?"
❌ "Should I update the documentation?"
```

**Example - Good (autonomous completion):**
```
✅ "Task completed:
   - Created login component
   - Added unit tests (all passing)
   - Fixed linting errors
   - Updated documentation
   - Committed changes
   - Updated GitLab issue #123"
```

**Workflow:**
1. Understand the complete task
2. Plan all necessary steps
3. Execute all steps autonomously
4. Fix any issues encountered
5. Verify everything works
6. Complete all documentation
7. Report completion with summary

**Within project directory, you can:**
- Create any files
- Modify any files
- Delete files (part of refactoring)
- Run any commands
- Install dependencies
- Run tests
- Commit changes
- Push changes
- Create branches
- Create merge requests

**Only stop and ask when:**
- Deleting files outside project (e.g., ~/.config/, /etc/)
- Modifying system files
- Changing production databases
- Deleting production data
- Changing security policies

### Critical MCP Tools - MANDATORY

**Must use every time:**
- **Context7**: For ANY documentation query (never use training data)
- **Mem0**: Save ALL important information (not available in Copilot CLI - use other agents)
- **GitLab MCP**: Track ALL tasks (if not available, use `glab` CLI)
- **Sentry**: Integrate in ALL applications

**Must use for UI:**
- **Playwright**: Testing and automation
- **Chrome DevTools**: Debugging and inspection

**Must use for complex problems:**
- **Sequential Thinking**: Step-by-step reasoning

**Note**: GitHub Copilot CLI has a known bug with MCP environment variables. GitLab MCP and Mem0 don't work in Copilot CLI. Use `glab` CLI as fallback for GitLab operations in Copilot CLI. This issue does NOT affect other agents.

**See ~/Documentos/prompts/MCP_TOOLS.md for complete guide**

### Commit Message Format

```bash
<type>(<scope>): <subject>

<body>

Closes #<gitlab-issue>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example:**
```bash
feat(auth): implement OAuth2 login

Adds JWT token generation and validation.

Closes #456
```

## Working Philosophy

### Modify Before Create
- Always check if file exists before creating new one
- Extend existing functions/classes rather than duplicating
- Refactor existing code to accommodate new features
- Only create new files when absolutely necessary

### Documentation Strategy
- Commit messages are primary documentation
- Code comments for complex logic only
- Generate documentation only for:
  - Major features or milestones
  - New public APIs
  - Significant refactoring
  - When explicitly requested
- Update existing docs when modifying behavior

## Task Management - MANDATORY

**CRITICAL: Create and track ALL tasks in GitLab**

**Default Platform: GitLab**
- All issues, merge requests, and CI/CD in GitLab
- **Prefer GitLab MCP** for operations (if available)
- **Fallback to `glab` CLI** if GitLab MCP not available
- GitHub is only used if explicitly requested

### Quick Workflow

1. **Create GitLab issue** (technical tracking)
   - Get GitLab ID (e.g., #456)

2. **Work and commit**
   ```bash
   git commit -m "feat: implement feature
   
   Closes #456"
   ```

3. **Close issue**
   - GitLab closes via commit

**See ~/Documentos/prompts/TASK_MANAGEMENT.md for complete workflow**

## UI Development - MANDATORY

**CRITICAL: Always use Playwright and Chrome DevTools for UI work**

### Quick Workflow

1. **Playwright**: Automate and test
   - Write tests for user flows
   - Verify UI behavior
   - Test responsive design
   - Capture screenshots

2. **Chrome DevTools**: Inspect and debug
   - Check console errors
   - Monitor network requests
   - Inspect element styles
   - Profile performance

3. **Verify before completing**
   - All tests pass
   - No console errors
   - Responsive works
   - Accessibility passes

**See ~/Documentos/prompts/UI_TESTING.md for complete guide**

## CI/CD Monitoring - MANDATORY

**CRITICAL: Monitor pipeline status for all changes**

**Default: GitLab CI/CD**
- Use GitLab CI/CD pipelines (.gitlab-ci.yml)
- Monitor GitLab pipeline status
- GitHub Actions only if explicitly requested

### Quick Workflow

1. **After push**: Check pipeline triggered
2. **During pipeline**: Monitor job status
3. **If failure**: Fix immediately
4. **After success**: Update issues with pipeline link
5. **After deployment**: Document in issues

**See ~/Documentos/prompts/CICD.md for complete guide**

## Verification Requirements

Before declaring task complete:

**Code Changes:**
- [ ] Tests pass (unit + integration)
- [ ] Linting passes
- [ ] Code formatted correctly
- [ ] No console errors/warnings

**Documentation:**
- [ ] Context7 used for all library docs
- [ ] Important info saved to Mem0
- [ ] Commit messages descriptive

**Task Tracking:**
- [ ] GitLab issue created and updated
- [ ] Status synchronized

**UI Work (if applicable):**
- [ ] Playwright tests pass
- [ ] Chrome DevTools checks pass
- [ ] Responsive design verified
- [ ] Accessibility verified

**CI/CD:**
- [ ] Pipeline passes
- [ ] All jobs successful
- [ ] Deployment successful (if applicable)
- [ ] Pipeline linked in issues

## Quick Reference

### Before Starting
1. Query Mem0 for project context
2. Check Context7 for library docs
3. Review GitLab issues
4. Verify current patterns

### During Work
1. Use Context7 for API references
2. Use Sequential Thinking for complex logic
3. Use Playwright/Chrome DevTools for UI
4. Save decisions to Mem0

### After Completing
1. Update GitLab issues
2. Save patterns to Mem0
3. Verify pipeline passes
4. Document deployment

### When Stuck
1. Query Mem0 for similar problems
2. Use Roundtable for other perspectives
3. Use Perplexity for research
4. Use Context7 for documentation

## Specialized Guides

For detailed information on specific topics:

### MCP Tools
- **~/Documentos/prompts/MCP_TOOLS.md** - Complete guide to all 14 MCP tools
  - Context7, Mem0, Playwright, Chrome DevTools
  - GitLab, Sentry, SSH, Perplexity
  - Tool combinations and patterns
  - Copilot CLI limitations and workarounds

### Task Management
- **~/Documentos/prompts/TASK_MANAGEMENT.md** - GitLab workflow
  - Dual tracking process
  - Issue creation and linking
  - Status synchronization
  - Commit message format

### UI Testing
- **~/Documentos/prompts/UI_TESTING.md** - Playwright + Chrome DevTools
  - UI testing patterns
  - Debugging techniques
  - Verification checklist
  - Common scenarios

### CI/CD
- **~/Documentos/prompts/CICD.md** - Pipeline monitoring
  - Pipeline tracking
  - Failure handling
  - Deployment procedures
  - Rollback process

### Error Tracking
- **~/Documentos/prompts/SENTRY.MD** - Sentry integration (MANDATORY)
  - SDK installation
  - Configuration
  - Error capture
  - Performance monitoring

### Programming Languages
- **~/Documentos/prompts/TYPESCRIPT.MD** - TypeScript/Node.js/Bun
- **~/Documentos/prompts/PYTHON.MD** - Python development
- **~/Documentos/prompts/GO.MD** - Go development
- **~/Documentos/prompts/RUST.MD** - Rust development

### Frameworks & UI
- **~/Documentos/prompts/REACT.MD** - React development
- **~/Documentos/prompts/REACT_NATIVE.MD** - React Native
- **~/Documentos/prompts/ANGULAR.MD** - Angular development

### Architecture & Patterns
- **~/Documentos/prompts/EDA.MD** - Event-Driven Architecture
- **~/Documentos/prompts/BDS.MD** - Backend Design Systems
- **~/Documentos/prompts/LLM.MD** - LLM integration

### Testing & Quality
- **~/Documentos/prompts/TESTING_ADV.MD** - Advanced testing
- **~/Documentos/prompts/TROUBLESHOOTING.MD** - Debugging strategies

### Project Management
- **~/Documentos/prompts/NEW_TASK.MD** - Starting new tasks
- **~/Documentos/prompts/TECHNICAL_DEBT.MD** - Managing technical debt
- **~/Documentos/prompts/GENERAL.MD** - General guidelines

### Configuration
- **~/Documentos/prompts/AGENTS_CONFIG.md** - Complete agent configuration reference
  - All 21 agents with MCP config paths
  - Configuration formats by agent
  - Quick update commands

## Usage Guidelines

- **Always consult specialized guide** when working in specific domain
- **Follow domain-specific patterns** from specialized guides
- **Use AGENTS.md** as starting point and quick reference
- **Refer to detailed guides** for complete workflows

## GitHub Copilot CLI Specific Notes

**File Location:**
- Copilot CLI reads `AGENTS.md` from **current directory**
- For IDEs (VS Code, etc.), use `.github/copilot-instructions.md`

**Known Limitations:**
- MCP servers requiring environment variables don't work (bug in v1.2.0)
- Affected: mem0, gitlab MCP
- Working: All other 11 MCP servers

**Workarounds:**
- **GitLab**: Prefer GitLab MCP (works in other agents), fallback to `glab` CLI in Copilot CLI
  ```bash
  glab issue list
  glab issue create
  glab mr list
  ```
- **Mem0**: Use other agents (Kiro, Claude Desktop, VS Code)

---

**Last Updated**: 2025-12-07  
**Maintained By**: Alfonso De Gennaro  
**Total Agents**: 21 (17 local + 4 remote)  
**MCP Servers**: 14 functional
