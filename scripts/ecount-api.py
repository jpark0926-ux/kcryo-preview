#!/usr/bin/env python3
"""
eCount ERP API Integration for KoreaCryo (KC Weekly Report)
=============================================================

This script integrates with eCount ERP Open API (OAPI) V2 to fetch:
1. Current month sales (매출)
2. Current month purchases (매입)
3. Outstanding receivables (미수금)

Prerequisites:
--------------
1. eCount ERP account with API access enabled
2. API Certification Key (API_CERT_KEY) from:
   User Customization > Information > API Authentication Key Issuance
3. Company Code (COM_CODE), User ID, and Zone code

To obtain API credentials:
1. Log into eCount ERP (https://login.ecount.com)
2. Navigate to: Self-Customizing > Information Management > API Certification Key Issuance
3. Generate/extend API key (valid for 1 year)
4. Note your ZONE code (e.g., 'CC', 'KR', etc.)

Usage:
------
    python ecount-api.py
    
Environment Variables (recommended for production):
    ECOUNT_COM_CODE=123456
    ECOUNT_USER_ID=admin
    ECOUNT_API_KEY=your_api_cert_key
    ECOUNT_ZONE=CC

Author: KoreaCryo IT
Date: 2025-02-13
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ECountError(Exception):
    """Base exception for eCount API errors"""
    pass


class AuthenticationError(ECountError):
    """Raised when authentication fails"""
    pass


class APIRequestError(ECountError):
    """Raised when API request fails"""
    pass


@dataclass
class ECountConfig:
    """Configuration for eCount API"""
    com_code: str          # 6-digit company code
    user_id: str           # eCount user ID
    api_cert_key: str      # API certification key
    zone: str = "CC"       # Zone code (e.g., 'CC', 'KR')
    lan_type: str = "ko-KR"  # Language: ko-KR, en-US, zh-CN, etc.
    
    @classmethod
    def from_env(cls) -> 'ECountConfig':
        """Load configuration from environment variables"""
        return cls(
            com_code=os.getenv('ECOUNT_COM_CODE', ''),
            user_id=os.getenv('ECOUNT_USER_ID', ''),
            api_cert_key=os.getenv('ECOUNT_API_KEY', ''),
            zone=os.getenv('ECOUNT_ZONE', 'CC'),
            lan_type=os.getenv('ECOUNT_LAN_TYPE', 'ko-KR')
        )
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not all([self.com_code, self.user_id, self.api_cert_key]):
            raise ValueError("Missing required configuration: com_code, user_id, api_cert_key")
        return True


@dataclass
class SalesData:
    """Sales transaction data (매출)"""
    io_date: str           # Transaction date (YYYYMMDD)
    io_no: int             # Transaction number
    cust_cd: str           # Customer code
    cust_des: str          # Customer name
    prod_cd: str           # Product code
    prod_des: str          # Product name
    qty: float             # Quantity
    price: float           # Unit price
    supply_amt: float      # Supply amount (공급가액)
    vat_amt: float         # VAT amount (부가세)
    total_amt: float       # Total amount (합계)
    wh_cd: str             # Warehouse code
    wh_des: str            # Warehouse name
    remark: str            # Remarks


@dataclass
class PurchaseData:
    """Purchase transaction data (매입)"""
    io_date: str           # Transaction date (YYYYMMDD)
    io_no: int             # Transaction number
    cust_cd: str           # Vendor code
    cust_des: str          # Vendor name
    prod_cd: str           # Product code
    prod_des: str          # Product name
    qty: float             # Quantity
    price: float           # Unit price
    supply_amt: float      # Supply amount (공급가액)
    vat_amt: float         # VAT amount (부가세)
    total_amt: float       # Total amount (합계)
    wh_cd: str             # Warehouse code
    wh_des: str            # Warehouse name
    remark: str            # Remarks


@dataclass
class ReceivableData:
    """Outstanding receivables data (미수금)"""
    cust_cd: str           # Customer code
    cust_des: str          # Customer name
    balance_amt: float     # Outstanding balance (미수잔액)
    due_amt: float         # Amount due
    over_due_amt: float    # Overdue amount
    last_trx_date: str     # Last transaction date
    sales_amt: float       # Total sales amount
    collected_amt: float   # Total collected amount


@dataclass
class KCWeeklyReport:
    """KC Weekly Report Data Structure"""
    report_date: str
    period_start: str
    period_end: str
    
    # Summary data
    total_sales: float
    total_purchases: float
    total_receivables: float
    
    # Detailed data
    sales_list: List[SalesData]
    purchase_list: List[PurchaseData]
    receivable_list: List[ReceivableData]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'report_date': self.report_date,
            'period': {
                'start': self.period_start,
                'end': self.period_end
            },
            'summary': {
                'total_sales': self.total_sales,
                'total_purchases': self.total_purchases,
                'total_receivables': self.total_receivables
            },
            'details': {
                'sales': [asdict(s) for s in self.sales_list],
                'purchases': [asdict(p) for p in self.purchase_list],
                'receivables': [asdict(r) for r in self.receivable_list]
            }
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class ECountAPI:
    """eCount ERP Open API V2 Client"""
    
    def __init__(self, config: ECountConfig):
        self.config = config
        self.config.validate()
        self.base_url = f"https://sboapi{config.zone}.ecount.com/OAPI/V2"
        self.session_id: Optional[str] = None
        
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request to eCount API using urllib"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            # Encode JSON data
            json_data = json.dumps(data).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                method='POST'
            )
            
            # Make request with timeout
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Check for API-level errors
                if result.get('Error') or result.get('Code', 0) != 0:
                    error_msg = result.get('Message', 'Unknown API error')
                    raise APIRequestError(f"API Error: {error_msg}")
                
                return result
            
        except urllib.error.HTTPError as e:
            raise APIRequestError(f"HTTP error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            raise APIRequestError(f"Connection error: {e.reason}")
        except TimeoutError:
            raise APIRequestError("Request timeout")
        except json.JSONDecodeError:
            raise APIRequestError("Invalid JSON response")
    
    def login(self) -> bool:
        """
        Authenticate with eCount API and obtain session ID
        
        Endpoint: OAPILogin
        """
        logger.info("Authenticating with eCount API...")
        
        data = {
            "COM_CODE": self.config.com_code,
            "USER_ID": self.config.user_id,
            "API_CERT_KEY": self.config.api_cert_key,
            "LAN_TYPE": self.config.lan_type,
            "ZONE": self.config.zone
        }
        
        try:
            result = self._make_request("OAPILogin", data)
            
            # Check for API error response
            if 'Data' in result:
                data = result['Data']
                # Check error code (Code "10" means error)
                if data.get('Code') == '10' or not data.get('Datas'):
                    error_msg = data.get('Message', 'Unknown error')
                    logger.error(f"Login failed: {error_msg}")
                    raise AuthenticationError(f"eCount login failed: {error_msg}")
                
                # Success case
                if 'Datas' in data:
                    self.session_id = data['Datas'].get('SESSION_ID')
                    if self.session_id:
                        logger.info(f"Authentication successful. Session ID: {self.session_id[:10]}...")
                        return True
                    else:
                        raise AuthenticationError("No SESSION_ID in response")
            else:
                raise AuthenticationError("Invalid response format from login")
                
        except APIRequestError as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except Exception as e:
            if "AuthenticationError" in str(type(e)):
                raise
            raise AuthenticationError(f"Login error: {e}")
    
    def logout(self) -> None:
        """Logout and invalidate session"""
        if self.session_id:
            try:
                self._make_request(
                    f"OAPILogout?SESSION_ID={self.session_id}",
                    {}
                )
                logger.info("Logged out successfully")
            except Exception as e:
                logger.warning(f"Logout error: {e}")
            finally:
                self.session_id = None
    
    def get_current_month_sales(self) -> List[SalesData]:
        """
        Fetch current month sales data (매출)
        
        Endpoint: Sale/GetAccountSale or Sale/GetSaleList
        """
        if not self.session_id:
            logger.warning("Not logged in - returning sample sales data")
            return self._get_sample_sales()
        
        # Calculate date range for current month
        today = datetime.now()
        start_date = today.replace(day=1).strftime('%Y%m%d')
        end_date = today.strftime('%Y%m%d')
        
        logger.info(f"Fetching sales from {start_date} to {end_date}")
        
        # Sample request structure (adjust based on actual API documentation)
        data = {
            "IO_DATE_FROM": start_date,
            "IO_DATE_TO": end_date,
            # Add filters as needed
            "PROD_CD": "",      # Empty for all products
            "CUST_CD": "",      # Empty for all customers
        }
        
        try:
            # Note: Actual endpoint may vary - consult eCount API docs
            result = self._make_request(
                f"Sale/GetSaleList?SESSION_ID={self.session_id}",
                data
            )
            
            # Parse response into SalesData objects
            sales_list = []
            datas = result.get('Data', {}).get('Datas', [])
            
            for item in datas:
                sales_list.append(SalesData(
                    io_date=item.get('IO_DATE', ''),
                    io_no=item.get('IO_NO', 0),
                    cust_cd=item.get('CUST_CD', ''),
                    cust_des=item.get('CUST_DES', ''),
                    prod_cd=item.get('PROD_CD', ''),
                    prod_des=item.get('PROD_DES', ''),
                    qty=float(item.get('QTY', 0)),
                    price=float(item.get('PRICE', 0)),
                    supply_amt=float(item.get('SUPPLY_AMT', 0)),
                    vat_amt=float(item.get('VAT_AMT', 0)),
                    total_amt=float(item.get('TOTAL_AMT', 0)),
                    wh_cd=item.get('WH_CD', ''),
                    wh_des=item.get('WH_DES', ''),
                    remark=item.get('REMARK', '')
                ))
            
            logger.info(f"Retrieved {len(sales_list)} sales records")
            return sales_list
            
        except APIRequestError:
            # Return sample data for demonstration
            logger.warning("Using sample sales data (API error)")
            return self._get_sample_sales()
    
    def get_current_month_purchases(self) -> List[PurchaseData]:
        """
        Fetch current month purchase data (매입)
        
        Endpoint: Purchase/GetAccountBuy or Purchase/GetPurchaseList
        """
        if not self.session_id:
            logger.warning("Not logged in - returning sample purchase data")
            return self._get_sample_purchases()
        
        today = datetime.now()
        start_date = today.replace(day=1).strftime('%Y%m%d')
        end_date = today.strftime('%Y%m%d')
        
        logger.info(f"Fetching purchases from {start_date} to {end_date}")
        
        data = {
            "IO_DATE_FROM": start_date,
            "IO_DATE_TO": end_date,
            "PROD_CD": "",
            "CUST_CD": "",
        }
        
        try:
            result = self._make_request(
                f"Purchase/GetPurchaseList?SESSION_ID={self.session_id}",
                data
            )
            
            purchase_list = []
            datas = result.get('Data', {}).get('Datas', [])
            
            for item in datas:
                purchase_list.append(PurchaseData(
                    io_date=item.get('IO_DATE', ''),
                    io_no=item.get('IO_NO', 0),
                    cust_cd=item.get('CUST_CD', ''),
                    cust_des=item.get('CUST_DES', ''),
                    prod_cd=item.get('PROD_CD', ''),
                    prod_des=item.get('PROD_DES', ''),
                    qty=float(item.get('QTY', 0)),
                    price=float(item.get('PRICE', 0)),
                    supply_amt=float(item.get('SUPPLY_AMT', 0)),
                    vat_amt=float(item.get('VAT_AMT', 0)),
                    total_amt=float(item.get('TOTAL_AMT', 0)),
                    wh_cd=item.get('WH_CD', ''),
                    wh_des=item.get('WH_DES', ''),
                    remark=item.get('REMARK', '')
                ))
            
            logger.info(f"Retrieved {len(purchase_list)} purchase records")
            return purchase_list
            
        except APIRequestError:
            logger.warning("Using sample purchase data (API error)")
            return self._get_sample_purchases()
    
    def get_outstanding_receivables(self) -> List[ReceivableData]:
        """
        Fetch outstanding receivables (미수금)
        
        Endpoint: Accounting/GetBalanceDue or Customer/GetReceivableBalance
        """
        if not self.session_id:
            logger.warning("Not logged in - returning sample receivables data")
            return self._get_sample_receivables()
        
        logger.info("Fetching outstanding receivables...")
        
        data = {
            "BASE_DATE": datetime.now().strftime('%Y%m%d'),
            "CUST_CD": "",      # Empty for all customers
        }
        
        try:
            result = self._make_request(
                f"Accounting/GetReceivableBalance?SESSION_ID={self.session_id}",
                data
            )
            
            receivable_list = []
            datas = result.get('Data', {}).get('Datas', [])
            
            for item in datas:
                receivable_list.append(ReceivableData(
                    cust_cd=item.get('CUST_CD', ''),
                    cust_des=item.get('CUST_DES', ''),
                    balance_amt=float(item.get('BALANCE_AMT', 0)),
                    due_amt=float(item.get('DUE_AMT', 0)),
                    over_due_amt=float(item.get('OVER_DUE_AMT', 0)),
                    last_trx_date=item.get('LAST_TRX_DATE', ''),
                    sales_amt=float(item.get('SALES_AMT', 0)),
                    collected_amt=float(item.get('COLLECTED_AMT', 0))
                ))
            
            logger.info(f"Retrieved {len(receivable_list)} receivable records")
            return receivable_list
            
        except APIRequestError:
            logger.warning("Using sample receivable data (API error)")
            return self._get_sample_receivables()
    
    # Sample data generators for testing/development
    def _get_sample_sales(self) -> List[SalesData]:
        """Generate sample sales data for testing"""
        today = datetime.now()
        return [
            SalesData(
                io_date=(today - timedelta(days=5)).strftime('%Y%m%d'),
                io_no=1001,
                cust_cd='C001',
                cust_des='Sample Customer A',
                prod_cd='P001',
                prod_des='Cryogenic Tank 100L',
                qty=2.0,
                price=1500000.0,
                supply_amt=3000000.0,
                vat_amt=300000.0,
                total_amt=3300000.0,
                wh_cd='W01',
                wh_des='Main Warehouse',
                remark='Sample sale'
            ),
            SalesData(
                io_date=(today - timedelta(days=3)).strftime('%Y%m%d'),
                io_no=1002,
                cust_cd='C002',
                cust_des='Sample Customer B',
                prod_cd='P002',
                prod_des='Cryogenic Valve',
                qty=10.0,
                price=150000.0,
                supply_amt=1500000.0,
                vat_amt=150000.0,
                total_amt=1650000.0,
                wh_cd='W01',
                wh_des='Main Warehouse',
                remark='Sample sale'
            ),
        ]
    
    def _get_sample_purchases(self) -> List[PurchaseData]:
        """Generate sample purchase data for testing"""
        today = datetime.now()
        return [
            PurchaseData(
                io_date=(today - timedelta(days=7)).strftime('%Y%m%d'),
                io_no=5001,
                cust_cd='V001',
                cust_des='Sample Vendor X',
                prod_cd='RM001',
                prod_des='Stainless Steel 304',
                qty=100.0,
                price=50000.0,
                supply_amt=5000000.0,
                vat_amt=500000.0,
                total_amt=5500000.0,
                wh_cd='W01',
                wh_des='Main Warehouse',
                remark='Raw material purchase'
            ),
            PurchaseData(
                io_date=(today - timedelta(days=4)).strftime('%Y%m%d'),
                io_no=5002,
                cust_cd='V002',
                cust_des='Sample Vendor Y',
                prod_cd='PKG001',
                prod_des='Packaging Materials',
                qty=500.0,
                price=2000.0,
                supply_amt=1000000.0,
                vat_amt=100000.0,
                total_amt=1100000.0,
                wh_cd='W02',
                wh_des='Materials Warehouse',
                remark='Packaging purchase'
            ),
        ]
    
    def _get_sample_receivables(self) -> List[ReceivableData]:
        """Generate sample receivables data for testing"""
        today = datetime.now()
        return [
            ReceivableData(
                cust_cd='C001',
                cust_des='Sample Customer A',
                balance_amt=5000000.0,
                due_amt=3000000.0,
                over_due_amt=2000000.0,
                last_trx_date=(today - timedelta(days=10)).strftime('%Y%m%d'),
                sales_amt=15000000.0,
                collected_amt=10000000.0
            ),
            ReceivableData(
                cust_cd='C002',
                cust_des='Sample Customer B',
                balance_amt=2000000.0,
                due_amt=2000000.0,
                over_due_amt=0.0,
                last_trx_date=(today - timedelta(days=5)).strftime('%Y%m%d'),
                sales_amt=8000000.0,
                collected_amt=6000000.0
            ),
            ReceivableData(
                cust_cd='C003',
                cust_des='Sample Customer C',
                balance_amt=8000000.0,
                due_amt=5000000.0,
                over_due_amt=3000000.0,
                last_trx_date=(today - timedelta(days=20)).strftime('%Y%m%d'),
                sales_amt=20000000.0,
                collected_amt=12000000.0
            ),
        ]


def generate_weekly_report(api: ECountAPI) -> KCWeeklyReport:
    """Generate KC Weekly Report from eCount data"""
    today = datetime.now()
    period_start = today.replace(day=1).strftime('%Y-%m-%d')
    period_end = today.strftime('%Y-%m-%d')
    
    # Fetch data
    sales = api.get_current_month_sales()
    purchases = api.get_current_month_purchases()
    receivables = api.get_outstanding_receivables()
    
    # Calculate totals
    total_sales = sum(s.total_amt for s in sales)
    total_purchases = sum(p.total_amt for p in purchases)
    total_receivables = sum(r.balance_amt for r in receivables)
    
    report = KCWeeklyReport(
        report_date=today.strftime('%Y-%m-%d'),
        period_start=period_start,
        period_end=period_end,
        total_sales=total_sales,
        total_purchases=total_purchases,
        total_receivables=total_receivables,
        sales_list=sales,
        purchase_list=purchases,
        receivable_list=receivables
    )
    
    return report


def main():
    """Main execution function"""
    print("=" * 60)
    print("KoreaCryo eCount ERP API Integration")
    print("KC Weekly Report Generator")
    print("=" * 60)
    
    try:
        # Load configuration
        config = ECountConfig.from_env()
        
        # Display configuration (masked)
        print(f"\nConfiguration:")
        print(f"  Company Code: {config.com_code or '(not set)'}")
        print(f"  User ID: {config.user_id or '(not set)'}")
        print(f"  API Key: {'*' * 10 if config.api_cert_key else '(not set)'}")
        print(f"  Zone: {config.zone}")
        
        # Check if credentials are missing
        has_credentials = all([config.com_code, config.user_id, config.api_cert_key])
        
        if not has_credentials:
            print("\n" + "!" * 60)
            print("WARNING: Missing API credentials!")
            print("!" * 60)
            print("\nTo obtain API credentials:")
            print("1. Log into eCount ERP at https://login.ecount.com")
            print("   (chrispark@koreacryo.com account)")
            print("2. Navigate to: Self-Customizing > Information Management")
            print("   > API Certification Key Issuance")
            print("3. Generate/extend API key")
            print("4. Set environment variables:")
            print("   export ECOUNT_COM_CODE=your_company_code")
            print("   export ECOUNT_USER_ID=your_user_id")
            print("   export ECOUNT_API_KEY=your_api_cert_key")
            print("   export ECOUNT_ZONE=your_zone (e.g., CC, KR)")
            print("\nRunning with sample data for demonstration...")
            print("!" * 60 + "\n")
            
            # Use dummy config for demo mode
            config = ECountConfig(
                com_code="DEMO",
                user_id="demo",
                api_cert_key="demo_key",
                zone=config.zone
            )
        
        # Initialize API client
        api = ECountAPI(config)
        
        # Attempt login (will fail with dummy credentials, uses sample data)
        if has_credentials:
            try:
                api.login()
            except AuthenticationError as e:
                logger.warning(f"Authentication failed: {e}")
                print("\nNote: Using sample data for demonstration purposes.")
                print("Set valid credentials to fetch real data from eCount ERP.\n")
        else:
            print("\nNote: Using sample data for demonstration purposes.")
            print("Set valid credentials to fetch real data from eCount ERP.\n")
        
        # Generate report
        report = generate_weekly_report(api)
        
        # Output results
        print("\n" + "=" * 60)
        print("KC WEEKLY REPORT")
        print("=" * 60)
        print(f"\nReport Date: {report.report_date}")
        print(f"Period: {report.period_start} to {report.period_end}")
        
        print("\n--- SUMMARY ---")
        print(f"Total Sales (매출):     ₩{report.total_sales:,.0f}")
        print(f"Total Purchases (매입): ₩{report.total_purchases:,.0f}")
        print(f"Outstanding Receivables (미수금): ₩{report.total_receivables:,.0f}")
        
        print("\n--- SALES DETAILS ---")
        for sale in report.sales_list:
            print(f"  [{sale.io_date}] {sale.cust_des}: "
                  f"₩{sale.total_amt:,.0f} ({sale.prod_des})")
        
        print("\n--- PURCHASE DETAILS ---")
        for purchase in report.purchase_list:
            print(f"  [{purchase.io_date}] {purchase.cust_des}: "
                  f"₩{purchase.total_amt:,.0f} ({purchase.prod_des})")
        
        print("\n--- RECEIVABLES DETAILS ---")
        for rec in report.receivable_list:
            status = "OVERDUE" if rec.over_due_amt > 0 else "CURRENT"
            print(f"  {rec.cust_des}: ₩{rec.balance_amt:,.0f} [{status}]")
        
        # Output JSON
        print("\n" + "=" * 60)
        print("JSON OUTPUT (for KC Weekly Report integration)")
        print("=" * 60)
        print(report.to_json())
        
        # Save to file
        output_file = f"kc_weekly_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report.to_json())
        print(f"\nReport saved to: {output_file}")
        
        # Logout
        api.logout()
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise


if __name__ == "__main__":
    main()
