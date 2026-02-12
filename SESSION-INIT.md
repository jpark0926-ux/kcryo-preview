# SESSION INITIALIZATION RULE

## On every session start:

### 1. Load ONLY these files:
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `CHRIS-ONTOLOGY.yml`
- `memory/YYYY-MM-DD.md` (today's date, if exists and <500 lines)

### 2. DO NOT auto-load:
- `MEMORY.md` (long-term memory - use on-demand)
- Session history
- Prior messages
- Previous tool outputs
- README files
- Project files

### 3. When user asks about prior context:
- Use `memory_search()` on demand
- Pull only the relevant snippet with `memory_get()`
- Don't load the whole file
- Search first, read second

### 4. Update memory/YYYY-MM-DD.md at end of session with:
- What you worked on
- Decisions made
- Leads generated
- Blockers
- Next steps

## Special Cases

### Heartbeat sessions:
- Load ONLY: `HEARTBEAT.md`
- Skip all other files

### Cron isolated sessions:
- Load per job requirements (already specified in job prompts)
- No automatic workspace loading

### Group chats:
- Same as DM (essential files only)
- Use context-appropriate responses

## Benefits

**Token savings**: ~80% reduction on context overhead
- Before: 74k+ tokens per session start
- After: ~18k tokens (essential + ontology + today's memory)

**Performance**: Faster session initialization, lower costs

**Flexibility**: On-demand loading when actually needed

---

**Last updated**: 2026-02-12
**Status**: Active
