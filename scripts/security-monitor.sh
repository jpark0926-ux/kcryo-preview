#!/bin/bash
# 보안 모니터링 시스템 - 의심스러운 활동 감지

TELEGRAM_BOT_TOKEN='8551723387:AAGbR3Sqg8SFFGw_16iIqQd1WjdkCTVcjAw'
TELEGRAM_CHAT_ID='6948605509'
LOG_FILE="/Users/roturnjarvis/.openclaw/workspace/logs/security-monitor.log"
ALERT_FILE="/Users/roturnjarvis/.openclaw/workspace/logs/security-alerts.json"

# 로그 함수
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 텔레그램 알림
send_alert() {
    local message="$1"
    local priority="$2"  # high, medium, low
    
    local emoji="⚠️"
    [ "$priority" = "high" ] && emoji="🚨"
    [ "$priority" = "medium" ] && emoji="⚡"
    
    local full_message="${emoji} <b>보안 알림</b>%0A%0A${message}%0A%0A<i>$(date '+%H:%M')</i>"
    
    curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${full_message}" \
        -d "parse_mode=HTML" \
        -d "disable_web_page_preview=true" > /dev/null 2>&1
    
    # 로그에도 기록
    log "ALERT [$priority]: $message"
    
    # 알림 파일에 저장
    echo "{\"time\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"priority\":\"$priority\",\"message\":\"$message\"}" >> "$ALERT_FILE"
}

# 1. 의심스러운 포트 체크 (0.0.0.0 바인딩)
check_suspicious_ports() {
    log "포트 스캔 중..."
    
    # macOS용 포트 확인 (netstat)
    local suspicious=""
    if command -v netstat &> /dev/null; then
        suspicious=$(netstat -anv | grep LISTEN | grep -v "127.0.0.1" | grep -v "::1" | head -20)
    elif command -v lsof &> /dev/null; then
        suspicious=$(lsof -i -P | grep LISTEN | grep -v "127.0.0.1" | grep -v "\[::1\]" | head -20)
    fi
    
    # OpenClaw gateway (8080)는 제외
    if [ -n "$suspicious" ]; then
        # 8080은 OpenClaw 정상 포트
        local filtered=$(echo "$suspicious" | grep -v ":8080")
        
        if [ -n "$filtered" ]; then
            local count=$(echo "$filtered" | wc -l)
            local details=$(echo "$filtered" | head -5 | tr '\n' '%0A')
            
            send_alert "<b>외부 노출 포트 감지!</b>%0A%0A총 ${count}개 의심 포트:%0A%0A${details}%0A%0A<b>즉시 확인 필요</b>" "high"
            return 1
        fi
    fi
    
    return 0
}

# 2. 의심스러운 프로세스 체크
check_suspicious_processes() {
    log "프로세스 스캔 중..."
    
    # 위험한 프로세스 패턴
    local suspicious=$(ps aux | grep -E "(python.*http\.server|nc -l|ncat -l|netcat|socat.*TCP-LISTEN)" | grep -v grep | head -10)
    
    if [ -n "$suspicious" ]; then
        local count=$(echo "$suspicious" | wc -l)
        local details=$(echo "$suspicious" | head -3 | awk '{print "• " $11 " " $12 " (PID:" $2 ")"}' | tr '\n' '%0A')
        
        send_alert "<b>의심스러운 프로세스 감지!</b>%0A%0A${count}개 의심 프로세스:%0A%0A${details}%0A%0A<b>의도하지 않은 서버라면 즉시 종료하세요</b>%0A%0A<code>kill [PID]</code>" "high"
        return 1
    fi
    
    return 0
}

# 3. 파일 권한 체크 (world-writable)
check_file_permissions() {
    log "파일 권한 체크 중..."
    
    # workspace 내 world-writable 파일
    local bad_perms=$(find /Users/roturnjarvis/.openclaw/workspace -type f -perm +002 2>/dev/null | head -10)
    
    if [ -n "$bad_perms" ]; then
        local count=$(echo "$bad_perms" | wc -l)
        send_alert "<b>취약한 파일 권한 감지</b>%0A%0A${count}개 파일이 other에 쓰기 권한 있음%0A%0A<code>chmod o-w [파일]</code>로 수정 권장" "medium"
        return 1
    fi
    
    return 0
}

# 4. .env / 토큰 파일 노출 체크
check_exposed_secrets() {
    log "토큰 노출 체크 중..."
    
    # 코드 내 API 키 패턴 검색
    local exposed=$(grep -r "sk-[a-zA-Z0-9]\{20,\}" /Users/roturnjarvis/.openclaw/workspace/scripts --include="*.py" --include="*.sh" 2>/dev/null | grep -v "os.getenv\|getenv" | head -5)
    
    if [ -n "$exposed" ]; then
        local count=$(echo "$exposed" | wc -l)
        send_alert "<b>API 키 하드코딩 감지!</b>%0A%0A${count}개 파일에 API 키가 하드코딩됨%0A%0A환경변수(os.getenv)로 이동 권장" "high"
        return 1
    fi
    
    return 0
}

# 5. 로그인 기록 체크 (의심스러운 IP)
check_login_history() {
    log "로그인 기록 체크 중..."
    
    # 오늘 날짜만 체크
    local today=$(date +'%a %b %e')
    
    # SSH 로그인만 체크 (pts 터미널), console(직접 로그인) 제외
    # IP 패턴: 숫자.숫자.숫자.숫자 또는 100.x.x.x (Tailscale)
    local ssh_logins=$(last 2>/dev/null | grep "$today" | grep "pts" | grep -v "100\." | head -5)
    
    # IP 주소 패턴 검증 (숫자.숫자.숫자.숫자 형태인지)
    if [ -n "$ssh_logins" ]; then
        # 실제 IP 주소인지 확인 (Mon/Tue 등 요일 이름 제외)
        local real_ip=$(echo "$ssh_logins" | grep -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | head -3)
        
        if [ -n "$real_ip" ]; then
            local details=$(echo "$real_ip" | awk '{print "• " $1 " from " $3 " at " $4" "$5}' | tr '\n' '%0A')
            send_alert "<b>외부 SSH 로그인 감지</b>%0A%0A${details}%0A%0A<b>확인 필요</b>" "high"
            return 1
        fi
    fi
    
    return 0
}

# 메인 실행
main() {
    log "보안 스캔 시작"
    
    local issues=0
    
    check_suspicious_ports || ((issues++))
    check_suspicious_processes || ((issues++))
    check_file_permissions || ((issues++))
    check_exposed_secrets || ((issues++))
    check_login_history || ((issues++))
    
    if [ $issues -eq 0 ]; then
        log "✅ 보안 스캔 완료 - 이상 없음"
        # 매일 한 번은 정상 보고 (00:00에)
        if [ "$(date +%H)" = "00" ] && [ "$(date +%M)" -lt "10" ]; then
            send_alert "<b>✅ 일일 보안 체크 완료</b>%0A%0A모든 항목 정상%0A• 외부 포트: 없음%0A• 의심 프로세스: 없음%0A• 파일 권한: 양호%0A• 토큰 노출: 없음" "low"
        fi
    else
        log "⚠️  보안 스캔 완료 - ${issues}개 문제 발견"
    fi
    
    log "보안 스캔 종료"
}

# 실행
main "$@"
