#!/usr/bin/env python3
"""
CHRIS-ONTOLOGY Query
yml에서 정보를 빠르게 추출하는 쿼리 도구
"""

import yaml
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
ONTOLOGY_FILE = WORKSPACE / "CHRIS-ONTOLOGY.yml"

def load_ontology():
    """온톨로지 로드"""
    with open(ONTOLOGY_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def status_summary(ontology):
    """전체 상태 요약"""
    projects = ontology['active_projects']
    
    print("=" * 50)
    print("📊 Chris Status Summary")
    print("=" * 50)
    print()
    
    # Business
    print("🏢 Business:")
    for company_name, company in ontology['companies'].items():
        for project in company['current_projects']:
            print(f"  {project['status']} {project['name']}: {project.get('progress', '?')}%")
            if 'blocker' in project:
                print(f"     ⚠️  {project['blocker']}")
    print()
    
    # Portfolio highlights
    print("💰 Portfolio:")
    holdings = ontology['portfolio']['holdings']
    for symbol, data in list(holdings.items())[:5]:  # Top 5
        print(f"  {symbol}: {data['shares']} shares")
    print()
    
    # Active projects
    print(f"📋 Active: {projects['count']} projects")
    print(f"⚠️  Blockers: {projects['blockers']['count']}")
    print()
    
    # Priority
    print("🎯 Priority Queue:")
    for i, task in projects['priority_queue'].items():
        print(f"  {i}. {task}")

def blockers_only(ontology):
    """블로커만 표시"""
    print("⚠️  Current Blockers:")
    print()
    
    for company_name, company in ontology['companies'].items():
        for project in company['current_projects']:
            if 'blocker' in project:
                print(f"• {project['name']}")
                print(f"  → {project['blocker']}")
                print()

def portfolio_summary(ontology):
    """포트폴리오 요약"""
    holdings = ontology['portfolio']['holdings']
    watchlist = ontology['portfolio']['watchlist']
    
    print("💰 Investment Portfolio")
    print()
    print("Holdings:")
    for symbol, data in holdings.items():
        print(f"  {symbol}: {data['shares']} shares - {data.get('conviction', 'N/A')}")
    print()
    print("Watchlist:")
    for item in watchlist:
        print(f"  • {item['symbol']}: {item['reason']}")

def main():
    """메인 실행"""
    ontology = load_ontology()
    
    if len(sys.argv) < 2:
        status_summary(ontology)
    else:
        command = sys.argv[1].lower()
        
        if command == 'status':
            status_summary(ontology)
        elif command == 'blockers':
            blockers_only(ontology)
        elif command == 'portfolio':
            portfolio_summary(ontology)
        else:
            print(f"Unknown command: {command}")
            print("Available: status, blockers, portfolio")

if __name__ == '__main__':
    main()
