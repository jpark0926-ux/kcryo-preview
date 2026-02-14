# eCount API Integration for KoreaCryo

Python integration with eCount ERP Open API (OAPI) V2 for KoreaCryo's weekly reporting.

## Overview

This script fetches key financial data from eCount ERP:
- **Sales (매출)**: Current month sales transactions
- **Purchases (매입)**: Current month purchase transactions  
- **Receivables (미수금)**: Outstanding customer balances

## Prerequisites

### 1. eCount ERP Account Access

You need access to the KoreaCryo eCount ERP account (**chrispark@koreacryo.com**).

### 2. API Credentials

Obtain the following from eCount ERP:

1. **Log into eCount**: https://login.ecount.com
2. **Navigate to**: Self-Customizing > Information Management > API Certification Key Issuance
3. **Generate/Extend API Key**:
   - Click "Issue API Certification Key"
   - Key is valid for 1 year (can be extended)
   - Copy the `API_CERT_KEY`

4. **Note your credentials**:
   - **Company Code (COM_CODE)**: 6-digit code shown in the API section
   - **User ID**: Your eCount login ID
   - **API Certification Key**: The key generated above
   - **Zone**: Usually "CC" or "KR" (shown in API documentation)

## Setup

### Method 1: Environment Variables (Recommended)

```bash
export ECOUNT_COM_CODE="123456"
export ECOUNT_USER_ID="admin"
export ECOUNT_API_KEY="your_api_cert_key_here"
export ECOUNT_ZONE="CC"
```

Add to your `~/.zshrc` or `~/.bashrc` for persistence.

### Method 2: Direct Configuration

Edit the script and modify the `ECountConfig` defaults:

```python
config = ECountConfig(
    com_code="123456",
    user_id="admin", 
    api_cert_key="your_key",
    zone="CC"
)
```

## Usage

### Run the Script

```bash
python scripts/ecount-api.py
```

### Output

The script generates:
1. **Console output** with formatted summary
2. **JSON file** (`kc_weekly_report_YYYYMMDD.json`) for integration

### JSON Structure

```json
{
  "report_date": "2025-02-13",
  "period": {
    "start": "2025-02-01",
    "end": "2025-02-13"
  },
  "summary": {
    "total_sales": 4950000,
    "total_purchases": 6600000,
    "total_receivables": 15000000
  },
  "details": {
    "sales": [...],
    "purchases": [...],
    "receivables": [...]
  }
}
```

## API Endpoints Used

| Function | eCount Endpoint | Description |
|----------|-----------------|-------------|
| Login | `OAPILogin` | Authenticate and get session |
| Sales | `Sale/GetSaleList` | Fetch sales transactions |
| Purchases | `Purchase/GetPurchaseList` | Fetch purchase transactions |
| Receivables | `Accounting/GetReceivableBalance` | Fetch AR balances |

## Testing

Without valid credentials, the script runs in **demo mode** with sample data:

```
WARNING: Missing API credentials!
Running with sample data for demonstration...
```

This allows testing the data structure and report format before API access.

## Troubleshooting

### Authentication Failed
- Verify API key is valid and not expired
- Check company code, user ID, and zone are correct
- Ensure API access is enabled in eCount settings

### Connection Error
- Check internet connectivity
- Verify eCount API endpoint (zone code)
- eCount API may have maintenance windows

### No Data Returned
- Verify date range covers transactions
- Check user permissions in eCount
- Confirm transactions exist in the period

## eCount API Resources

- **Login Portal**: https://login.ecount.com
- **API Test Page**: https://sboapi.ecount.com/ECERP/OAPI/OAPIView
- **Documentation**: Available after login in eCount portal

## File Structure

```
scripts/
├── ecount-api.py          # Main integration script
├── ecount-api.env.example  # Environment template
└── README.md               # This file
```

## Integration Notes

### For KC Weekly Report

The JSON output is designed for easy integration:

```python
import json

# Load report
with open('kc_weekly_report_20250213.json') as f:
    report = json.load(f)

# Access summary
total_sales = report['summary']['total_sales']
total_receivables = report['summary']['total_receivables']

# Access details
for sale in report['details']['sales']:
    print(f"{sale['cust_des']}: ₩{sale['total_amt']}")
```

## Security Notes

- **Never commit API keys** to version control
- Use environment variables for credentials
- API keys expire annually - set calendar reminder
- Limit API user permissions in eCount to read-only if possible

## Support

For API access issues:
1. Contact eCount support via the portal
2. Check API key expiration
3. Verify user permissions

For script issues:
- Check Python version (3.7+)
- Install requirements: `pip install requests`
