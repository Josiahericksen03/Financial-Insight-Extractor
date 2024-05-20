from flask import Flask, render_template_string
import yfinance as yf
import fitz  # PyMuPDF
import re
app = Flask(__name__)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

# Function to parse data
def parse_financial_data(text):
    patterns = {

        'total_current_assets': r'Total current assets\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'total_assets': r'Total assets\s+\$\s*(\d{1,3}(?:,\d{3})*)\s+\$\s*(\d{1,3}(?:,\d{3})*)',
        'total_current_liabilities': r'Total current liabilities\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'total_stockholders_equity': r'Total stockholders’ equity\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'total_liabilities_and_stockholders_equity': r'Total liabilities and stockholders’ equity\s+\$\s*(\d{1,3}(?:,\d{3})*)(?:\s+\$\s*)(\d{1,3}(?:,\d{3})*)',

        'cash_beginning': r'CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, BEGINNING OF PERIOD\s+\$\s*(\d{1,3}(?:,\d{3})*)\s+\$\s*(\d{1,3}(?:,\d{3})*)',
        'net_income': r'Net income \(loss\)\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'net_operating_cash': r'Net cash provided by \(used in\) operating activities\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'net_investing_cash': r'Net cash provided by \(used in\) investing activities\s+(\(\d{1,3}(?:,\d{3})*\))\s+(\(\d{1,3}(?:,\d{3})*\))',
        'net_financing_cash': r'Net cash provided by \(used in\) financing activities\s+(-?\$?\d{1,3}(?:,\d{3})*|\(\$?\d{1,3}(?:,\d{3})*\))\s+(-?\$?\d{1,3}(?:,\d{3})*|\(\$?\d{1,3}(?:,\d{3})*\))',
        'cash_end': r'CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, END OF PERIOD\s+\$\s*(\d{1,3}(?:,\d{3})*)\s+\$\s*(\d{1,3}(?:,\d{3})*)',

        'total_net_sales': r'Total net sales\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'total_operating_expenses': r'Total operating expenses\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'net_income': r'Net income \(loss\)\s+(\d{1,3}(?:,\d{3})*)\s+(\d{1,3}(?:,\d{3})*)',
        'weighted_average_shares_basic': r'Basic\s+(\d{1,3}(?:,\d{3})*|\(\d{1,3}(?:,\d{3})*\))\s+(\d{1,3}(?:,\d{3})*|\(\d{1,3}(?:,\d{3})*\))',
        'diluted_average_shares_basic': r'Diluted\s+(\d{1,3}(?:,\d{3})*|\(\d{1,3}(?:,\d{3})*\))\s+(\d{1,3}(?:,\d{3})*|\(\d{1,3}(?:,\d{3})*\))',




    }
    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = {
                '2022': match.group(1), 
                '2023': match.group(2)  
            }
        else:
            data[key] = {
                '2022': "Not found",
                '2023': "Not found"
            }
    return data

@app.route('/report')
def report():
    pdf_path = 'AmazonEarnings.pdf'
    text = extract_text_from_pdf(pdf_path)
    data = parse_financial_data(text)

    tickerSymbol = 'MSFT'
    tickerData = yf.Ticker(tickerSymbol)
    ticker_info = tickerData.info

    market_tickers = {
        'S&P 500': '^GSPC',
        'Dow 30': '^DJI',
        'Nasdaq': '^IXIC',
        'Russell 2000': '^RUT',
        'Crude Oil': 'CL=F',
        'Gold': 'GC=F'
    }

    live_market_data = {}
    for name, ticker in market_tickers.items():
        individual_ticker_info = yf.Ticker(ticker).info 
        live_market_data[name] = individual_ticker_info.get('regularMarketPrice') or individual_ticker_info.get('previousClose', 'N/A')


    other_ticker_data = {
        'ticker': tickerSymbol,
        'current_price': ticker_info['currentPrice'],
        'pe_ratio': ticker_info.get('trailingPE', 'N/A'),
        'week_change': ticker_info.get('52WeekChange', 'N/A'),
        'earnings_growth': ticker_info.get('earningsGrowth', 'N/A'),
    }

    final_data = {
        'data': data,
        'ticker_info': other_ticker_data,
        'live_market_data': live_market_data,
    }

    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .report-container {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: #A9A9A9;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        h1 {
            text-align: center;
        }
    </style>
    <title>Quarterly Earnings Report</title>
</head>
<body>
     <!-- Live Market Data Bar section -->
        <div class="market-data-container">
            <h2>Live Market Data</h2>
            <div style="background-color: #f4f4f4; padding: 10px; margin-bottom: 20px;">
                {% for name, value in live_market_data.items() %}
                <span><strong>{{ name }}</strong>: {{ value }}</span> |
                {% endfor %}
            </div>
        </div>
        
    <h1>Quarterly Earnings Report</h1>
    <div class="report-container">   
        <h2>{{ ticker_info.ticker }} Stock Information</h2>
        <p>Current Price: {{ ticker_info.current_price }}</p>
        <p>P/E Ratio: {{ ticker_info.pe_ratio }}</p>
        <p>52-Week Change: {{ ticker_info.week_change }}</p>
        <p>Earnings Growth: {{ ticker_info.earnings_growth }}</p>
    </div>

    <!-- Consolidated Balance Sheets table -->
<div class="report-container">
    <h2>Consolidated Balance Sheets</h2>
    <table>
        <tr>
            <th style="background-color: #337ab7;">Financial Metric</th>
            <th style="background-color: #337ab7;">2022 (in million USD)</th>
            <th style="background-color: #337ab7;">2023 (in million USD)</th>
        </tr>
        <tr>
            <td>Total Current Assets</td>
            <td>{{ data['total_current_assets']['2022']}}</td>
            <td>{{ data['total_current_assets']['2023'] }}</td>
        </tr>
        <tr>
            <td>Total Assets</td>
            <td>{{ data['total_assets']['2022'] }}</td>
            <td>{{ data['total_assets']['2023'] }}</td>
        </tr>
        <tr>
            <td>Total Current Liabilities</td>
            <td>{{ data['total_current_liabilities']['2022'] }}</td>
            <td>{{ data['total_current_liabilities']['2023'] }}</td>
        </tr>
        <tr>
            <td>Total Stockholders' Equity</td>
            <td>{{  data['total_stockholders_equity']['2022'] }}</td>
            <td>{{  data['total_stockholders_equity']['2023'] }}</td>
        </tr>
        <tr>
            <td>Total Liabilities and Stockholders' Equity</td>
            <td>{{ data['total_liabilities_and_stockholders_equity']['2022'] }}</td>
            <td>{{ data['total_liabilities_and_stockholders_equity']['2023'] }}</td>
        </tr>
    </table>
</div>

   <!-- Consolidated Statements of Operations table -->
<div class="report-container">
    <h2>Consolidated Statements of Operations </h2>
    <table>
        <tr>
            <th style="background-color: #ff0000;">Financial Metric</th>
            <th style="background-color: #ff0000;">2022 (in million USD)</th>
            <th style="background-color: #ff0000;">2023 (in million USD)</th>
        </tr>
        <tr>
            <td>CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, BEGINNING OF PERIOD</td>
            <td>{{ data['cash_beginning']['2022'] }}</td>
            <td>{{ data['cash_beginning']['2023'] }}</td>
        </tr>
        <tr>
            <td>Net income (loss)</td>
            <td>{{ data['net_income']['2022'] }}</td>
            <td>{{ data['net_income']['2023'] }}</td>
        </tr>
        <tr>
            <td>Net cash provided by (used in) operating activities</td>
            <td>{{ data['net_operating_cash']['2022'] }}</td>
            <td>{{ data['net_operating_cash']['2023'] }}</td>
        </tr>
        <tr>
            <td>Net cash used in investing activities</td>
            <td>{{ data['net_investing_cash']['2022'] }}</td>
            <td>{{ data['net_investing_cash']['2023'] }}</td>
        </tr>
        <tr>
            <td>Net cash provided by (used in) financing activities</td>
            <td>{{ data['net_financing_cash']['2022'] }}</td>
            <td>{{ data['net_financing_cash']['2023'] }}</td>
        </tr>
        <tr>
            <td>CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, END OF PERIOD</td>
            <td>{{ data['cash_end']['2022'] }}</td>
            <td>{{ data['cash_end']['2023'] }}</td>
        </tr>
    <table>
</div>

    </table>
</div>

    <!-- Consolidated Statements of Cash Flows table -->
<div class="report-container">
    <h2>Consolidated Statements of Cash Flows</h2>
    <table>
        <tr>
            <th style="background-color: #f0ad4e;">Financial Metric</th>
            <th style="background-color: #f0ad4e;">2022 (in million USD)</th>
            <th style="background-color: #f0ad4e;">2023 (in million USD)</th>
        </tr>
        <tr>
            <td>Total Net Sales</td>
            <td>{{ data['total_net_sales']['2022'] }}</td>
            <td>{{ data['total_net_sales']['2023'] }}</td>
        </tr>
        <tr>
            <td>Total Operating Expenses</td>
            <td>{{ data['total_operating_expenses']['2022'] }}</td>
            <td>{{ data['total_operating_expenses']['2023'] }}</td>
        </tr>
        <tr>
            <td>Net income (loss)</td>
            <!-- td>{{ net_operating_cash_2022 }}</td -->
            <td>{{ data['net_income']['2022'] }}</td>
            <td>{{ data['net_income']['2023'] }}</td>
        </tr>
        <tr>
            <td>Weighted Average Shares Basic</td>
            <td>{{ data['weighted_average_shares_basic']['2022'] }}</td>
            <td>{{ data['weighted_average_shares_basic']['2023'] }}</td>
        </tr>
        <tr>
            <td>Diluted Average Shares Basic</td>
            <td>{{ data['diluted_average_shares_basic']['2022'] }}</td>
            <td>{{ data['diluted_average_shares_basic']['2023'] }}</td>
        </tr>
    <table>
</div>
</body>
</html>
"""
    return render_template_string(html_template, **final_data)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
