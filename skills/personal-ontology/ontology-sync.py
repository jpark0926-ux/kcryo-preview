#!/usr/bin/env python3
"""
CHRIS-ONTOLOGY Auto-Sync
자동으로 README 파일들을 파싱해서 CHRIS-ONTOLOGY.yml 업데이트
"""

import yaml
import re
from datetime import datetime
from pathlib import Path

# Paths
WORKSPACE = Path(__file__).parent.parent
ONTOLOGY_FILE = WORKSPACE / "CHRIS-ONTOLOGY.yml"

def parse_readme_status(readme_path):
    """README에서 프로젝트 상태 추출"""
    if not readme_path.exists():
        return None
    
    content = readme_path.read_text(encoding='utf-8')
    
    # Extract status indicators
    status_map = {
        '🟢': 'active',
        '🟡': 'waiting',
        '🔴': 'blocked',
        '✅': 'completed',
        '⏳': 'in-progress'
    }
    
    # Find first status emoji
    for emoji, status in status_map.items():
        if emoji in content:
            return status
    
    return 'unknown'

def parse_roturn_readme():
    """로턴 블로그 README 파싱"""
    readme = WORKSPACE / "business" / "roturn" / "README.md"
    
    if not readme.exists():
        return None
    
    content = readme.read_text(encoding='utf-8')
    
    # Extract key info
    project = {
        'name': '로턴 블로그',
        'id': 'roturn-blog',
        'status': parse_readme_status(readme),
        'progress': 85,  # Can parse from README later
    }
    
    # Find blocker
    if '사진' in content.lower() and '대기' in content.lower():
        project['blocker'] = '사진 필요 (Chris 제공)'
        project['next_action'] = '사진 받으면 첫 글 발행'
    
    return project

def parse_koreacryo_readme():
    """KoreaCryo README 파싱"""
    readme = WORKSPACE / "business" / "koreacryo" / "README.md"
    
    if not readme.exists():
        return None
    
    content = readme.read_text(encoding='utf-8')
    
    project = {
        'name': '웹사이트 리뉴얼',
        'id': 'kcryo-website',
        'status': parse_readme_status(readme),
        'progress': 80,
    }
    
    if '사진' in content.lower():
        project['blocker'] = '사진 품질/방향 결정'
    
    return project

def update_ontology():
    """CHRIS-ONTOLOGY.yml 업데이트"""
    
    # Load current ontology
    with open(ONTOLOGY_FILE, 'r', encoding='utf-8') as f:
        ontology = yaml.safe_load(f)
    
    # Update timestamp
    ontology['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
    
    # Update Roturn project
    roturn_project = parse_roturn_readme()
    if roturn_project:
        for i, proj in enumerate(ontology['companies']['roturn']['current_projects']):
            if proj['id'] == 'roturn-blog':
                ontology['companies']['roturn']['current_projects'][i].update(roturn_project)
    
    # Update KoreaCryo project
    kcryo_project = parse_koreacryo_readme()
    if kcryo_project:
        for i, proj in enumerate(ontology['companies']['koreacryo']['current_projects']):
            if proj['id'] == 'kcryo-website':
                ontology['companies']['koreacryo']['current_projects'][i].update(kcryo_project)
    
    # Count active projects and blockers
    all_projects = []
    all_projects.extend(ontology['companies']['roturn']['current_projects'])
    all_projects.extend(ontology['companies']['koreacryo']['current_projects'])
    
    active_count = len([p for p in all_projects if p.get('status') not in ['completed', 'paused']])
    blocked_count = len([p for p in all_projects if 'blocker' in p])
    
    ontology['active_projects']['count'] = active_count
    ontology['active_projects']['blockers']['count'] = blocked_count
    
    # Save updated ontology
    with open(ONTOLOGY_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(ontology, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Ontology updated: {active_count} active, {blocked_count} blockers")
    print(f"   Timestamp: {ontology['last_updated']}")

if __name__ == '__main__':
    update_ontology()
