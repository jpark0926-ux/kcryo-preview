#!/usr/bin/env python3
"""
KC Drive Filename Analyzer
Analyzes current file naming patterns and suggests improvements
"""

import os
import re
from datetime import datetime
from collections import Counter

WORKSPACE = "/Users/roturnjarvis/.openclaw/workspace"

def analyze_filenames():
    """Analyze KC Shared Drive filenames"""
    
    # Read quotes tracker output to get current files
    import subprocess
    result = subprocess.run(
        ["python3", f"{WORKSPACE}/scripts/kc-quotes-tracker.py"],
        capture_output=True,
        text=True
    )
    
    output = result.stdout
    
    # Extract filenames
    files = []
    for line in output.split('\n'):
        if '.xlsx' in line or '.pdf' in line or '.docx' in line:
            # Clean up the line
            clean = line.strip().replace('📄', '').replace('견적서', '').replace('발주서', '').strip()
            if clean and len(clean) > 10:
                files.append(clean)
    
    print("=" * 60)
    print("📊 KC DRIVE FILENAME ANALYSIS")
    print("=" * 60)
    print(f"분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"분석 파일 수: {len(files)}")
    print()
    
    # Pattern Analysis
    print("┏" + "━" * 58 + "┓")
    print("┃  🔍 CURRENT PATTERNS                                     ┃")
    print("┣" + "━" * 58 + "┫")
    
    # Check for common patterns
    has_date_pattern = sum(1 for f in files if re.search(r'\d{6}', f))
    has_company_name = sum(1 for f in files if any(kw in f for kw in ['기초과학연구원', '국립암센터', '연세대', '서울대']))
    has_version = sum(1 for f in files if 'rev' in f.lower() or 'Rev' in f)
    has_doc_type = sum(1 for f in files if any(kw in f for kw in ['견적', '발주', '계약', '납품']))
    
    print(f"┃  📅 날짜 패턴 (YYMMDD):        {has_date_pattern}/{len(files)} files      ┃")
    print(f"┃  🏢 고객사명 포함:              {has_company_name}/{len(files)} files      ┃")
    print(f"┃  📝 버전 표시 (Rev):            {has_version}/{len(files)} files      ┃")
    print(f"┃  📄 문서 유형 표시:             {has_doc_type}/{len(files)} files      ┃")
    print("┗" + "━" * 58 + "┛")
    print()
    
    # Sample Files
    print("┏" + "━" * 58 + "┓")
    print("┃  📁 SAMPLE FILES                                         ┃")
    print("┣" + "━" * 58 + "┫")
    for i, f in enumerate(files[:3], 1):
        # Truncate if too long
        display = f[:50] + "..." if len(f) > 50 else f
        print(f"┃  {i}. {display:<52} ┃")
    print("┗" + "━" * 58 + "┛")
    print()
    
    # Issues Found
    print("┏" + "━" * 58 + "┓")
    print("┃  ⚠️  ISSUES FOUND                                        ┃")
    print("┣" + "━" * 58 + "┫")
    
    issues = []
    
    # Check each file for issues
    for f in files:
        if not re.search(r'\d{6}', f):
            issues.append("날짜 패턴 없음 (YYMMDD)")
        if ' ' in f:
            issues.append("공백 포함 (언더스코어 권장)")
        if '(' in f and ')' in f:
            issues.append("괄호 사용 (하이픈 권장)")
    
    # Count unique issues
    issue_counts = Counter(issues)
    
    if issue_counts:
        for issue, count in issue_counts.most_common(5):
            print(f"┃  • {issue}: {count}건{' ' * (35 - len(issue) - len(str(count)))} ┃")
    else:
        print("┃  ✓ 주요 문제 없음                                        ┃")
    
    print("┗" + "━" * 58 + "┛")
    print()
    
    # Naming Convention Proposal
    print("┏" + "━" * 58 + "┓")
    print("┃  💡 PROPOSED NAMING CONVENTION                           ┃")
    print("┣" + "━" * 58 + "┫")
    print("┃                                                          ┃")
    print("┃  형식: [유형]_[상태]_[고객사]_[제품]_[날짜].xlsx         ┃")
    print("┃                                                          ┃")
    print("┃  📄 유형:                                                ┃")
    print("┃     견적 / 발주 / 계약 / 납품 / 세금계산서               ┃")
    print("┃                                                          ┃")
    print("┃  🚦 상태:                                                ┃")
    print("┃     진행중 / 확정 / 완료 / 보류 / 취소                   ┃")
    print("┃                                                          ┃")
    print("┃  📝 예시:                                                ┃")
    print("┃     견적_진행중_기초과학연구원_RD1-260128_250213.xlsx    ┃")
    print("┃     발주_확정_국립암센터_LN2-Tank_250212.xlsx            ┃")
    print("┃     계약_완료_연세대학교_저온장비_250201.xlsx            ┃")
    print("┃                                                          ┃")
    print("┗" + "━" * 58 + "┛")
    print()
    
    # Next Steps
    print("┏" + "━" * 58 + "┓")
    print("┃  🎯 RECOMMENDED NEXT STEPS                               ┃")
    print("┣" + "━" * 58 + "┫")
    print("┃                                                          ┃")
    print("┃  1. 새 파일부터 규칙 적용 (즉시 가능)                    ┃")
    print("┃  2. 기존 파일은 월말 일괄 정리 예약                      ┃")
    print("┃  3. Wayne Manor가 자동 분류 제안 (Drive 모니터링 연동)   ┃")
    print("┃                                                          ┃")
    print("┗" + "━" * 58 + "┛")
    print()

if __name__ == "__main__":
    analyze_filenames()
