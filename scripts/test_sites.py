#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/roturnjarvis/.openclaw/workspace/scripts')

# 수동 임포트
import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

def test_clien():
    print("=== 클리앙 테스트 ===")
    try:
        url = "https://www.clien.net/service/board/park?&od=T33"
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('div', class_='list_item')
        print(f"Found items: {len(items)}")
        
        for item in items[:2]:
            title = item.find('span', class_='subject_fixed')
            if title:
                print(f"  - {title.get_text(strip=True)[:40]}")
    except Exception as e:
        print(f"Error: {e}")

def test_ppomppu():
    print("\n=== 뽐뿔 테스트 ===")
    try:
        url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=freeboard&sort=read_num&how=desc"
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        
        all_tr = soup.find_all('tr')
        print(f"Total tr: {len(all_tr)}")
        
        found = 0
        for tr in all_tr:
            tds = tr.find_all('td')
            if len(tds) >= 5:
                views_text = tds[-1].get_text(strip=True).replace(',', '')
                if views_text.isdigit() and int(views_text) > 500:
                    title = tds[1].get_text(strip=True)[:40]
                    print(f"  - {title} ({views_text} views)")
                    found += 1
                    if found >= 2:
                        break
    except Exception as e:
        print(f"Error: {e}")

def test_theqoo():
    print("\n=== 더쿠 테스트 ===")
    try:
        url = "https://theqoo.net/hot"
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        
        tables = soup.find_all('table')
        if tables:
            trs = tables[0].find_all('tr')
            print(f"Table rows: {len(trs)}")
            
            found = 0
            for tr in trs:
                tds = tr.find_all('td')
                if len(tds) >= 5:
                    no = tds[0].get_text(strip=True)
                    if no.isdigit():
                        title = tds[2].get_text(strip=True)[:40]
                        views = tds[4].get_text(strip=True)
                        print(f"  - {title} ({views} views)")
                        found += 1
                        if found >= 2:
                            break
    except Exception as e:
        print(f"Error: {e}")

def test_ddanzi():
    print("\n=== 딴지 테스트 ===")
    try:
        url = "https://www.ddanzi.com/free?sort_index=readed_count"
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        
        board = soup.find('section', {'class': 'board_content'})
        if board:
            items = board.find_all('li')
            print(f"Board items: {len(items)}")
            
            for item in items[:2]:
                link = item.find('a')
                if link:
                    print(f"  - {link.get_text(strip=True)[:40]}")
        else:
            print("Board section not found")
            # 대체 방식
            links = soup.find_all('a')
            print(f"Total links: {len(links)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_clien()
    test_ppomppu()
    test_theqoo()
    test_ddanzi()
