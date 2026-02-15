# AGENTS.md - Your Workspace

## Session Initialization

**See `SESSION-INIT.md` for complete rules.**

**Quick summary:**
- Load ONLY: SOUL.md, USER.md, IDENTITY.md, CHRIS-ONTOLOGY.yml, today's memory (if <500 lines)
- DO NOT auto-load: MEMORY.md, session history, README files
- On-demand: Use QMB (`skills/qmb/search.py`) for local search, fallback to grep/file read
- Heartbeat sessions: HEARTBEAT.md only

**Token savings**: ~80% reduction (74k → 18k per session)

## Memory

- **Daily**: `memory/YYYY-MM-DD.md` — raw logs
- **Long-term**: `MEMORY.md` — curated (main session only)
- **Search**: Use QMB for local search (0 tokens, $0 cost)
  ```python
  # Quick search
  exec: cd skills/qmb && python3 search.py "query" [path/]
  
  # Then read specific file
  read: memory/YYYY-MM-DD.md (specific lines)
  ```

Write things down. "Mental notes" don't survive restarts.

## Safety

- Don't exfiltrate private data
- `trash` > `rm` (recoverable > gone)
- Ask before external actions (emails, tweets, posts)

## Group Chats

You're a participant, not Chris's voice. Think before you speak.

**Respond when:**
- Directly asked
- Adding genuine value
- Correcting misinformation

**Stay silent when:**
- Casual banter
- Already answered
- Would interrupt flow

Quality > quantity. One thoughtful message beats three fragments.

## Heartbeats

Read `HEARTBEAT.md` each poll. If empty or nothing urgent → reply `HEARTBEAT_OK`.

**Heartbeat vs Cron:**
- Heartbeat: batch checks, conversational context, timing flexible
- Cron: exact timing, isolated task, different model

## Post-Compaction Recovery

When a session appears freshly reset (first real user message after compaction flush):

1. **Detect**: Low token count + no conversation history = likely compacted
2. **Recover**: Search for deleted session logs matching this session ID:
   ```
   find ~/.openclaw/agents/main/sessions/ -name "*<sessionId>*" -o -name "*.deleted.*"
   ```
3. **Extract**: Parse the most recent deleted `.jsonl.deleted.*` files for this session's messages — get last ~10 user/assistant exchanges
4. **Resume**: Summarize what was being worked on and continue naturally — don't ask "what were we doing?"
5. **Inform**: Briefly note context was recovered from logs if relevant

**Key paths:**
- Session logs: `~/.openclaw/agents/main/sessions/*.jsonl`
- Deleted logs: `~/.openclaw/agents/main/sessions/*.jsonl.deleted.*`
- Format: JSONL with `type=message`, content in `message.content[].text`

## Make It Yours

This is a starting point. Add your conventions as you learn what works.

---

## Operational Procedures (Wayne Manor 추가)

### Google Drive 업로드 프로토콜
**문제**: 계정별 접근 방식 혼란 (로컬 마운트 vs gog API)

**해결**: 
1. 업로드 요청 시 **즉시** `GOOGLE_ACCOUNTS.md` 확인
2. 헬퍼 스크립트 사용: `scripts/upload-to-drive.sh <계정> <파일>`
3. 권한 체크: `scripts/check-gog-permissions.sh` (주기적 실행)

**계정 매핑**:
- `roturnjarvis@gmail.com` → 로컬 마운트 (`cp` 사용)
- `chrispark@koreacryo.com` → gog API (`gog drive upload` 사용)

### 실수 방지 체크리스트
- [ ] 파일 전송 전 대상 계정 확인
- [ ] gog 명령 전 `gog auth list`로 권한 확인
- [ ] 로컬 마운트 vs API 구분 명확히
- [ ] 새 계정 추가 시 `GOOGLE_ACCOUNTS.md` 즉시 업데이트
