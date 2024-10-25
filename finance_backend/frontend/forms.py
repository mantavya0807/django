# frontend/forms.py

from django import forms
from data_fetcher.models import StockPrice

# List of stock symbols
STOCK_CHOICES = [
    ('AAPL', 'Apple (AAPL)'),
    ('GOOGL', 'Alphabet (GOOGL)'),
    ('AMZN', 'Amazon (AMZN)'),
    ('MSFT', 'Microsoft (MSFT)'),
    ('TSLA', 'Tesla (TSLA)'),
    ('FB', 'Meta Platforms (FB)'),
    ('NFLX', 'Netflix (NFLX)'),
    ('NVDA', 'Nvidia (NVDA)'),
    ('INTC', 'Intel (INTC)'),
    ('AMD', 'Advanced Micro Devices (AMD)'),
    ('BABA', 'Alibaba (BABA)'),
    ('CSCO', 'Cisco (CSCO)'),
    ('ORCL', 'Oracle (ORCL)'),
    ('ADBE', 'Adobe (ADBE)'),
    ('CRM', 'Salesforce (CRM)'),
    ('PYPL', 'PayPal (PYPL)'),
    ('SQ', 'Square (SQ)'),
    ('SHOP', 'Shopify (SHOP)'),
    ('UBER', 'Uber Technologies (UBER)'),
    ('LYFT', 'Lyft (LYFT)'),
    ('TWTR', 'Twitter (TWTR)'),
    ('SNAP', 'Snap Inc. (SNAP)'),
    ('ZM', 'Zoom Video (ZM)'),
    ('PLTR', 'Palantir Technologies (PLTR)'),
    ('DIS', 'Walt Disney (DIS)'),
    ('V', 'Visa (V)'),
    ('MA', 'Mastercard (MA)'),
    ('JPM', 'JPMorgan Chase (JPM)'),
    ('GS', 'Goldman Sachs (GS)'),
    ('BAC', 'Bank of America (BAC)'),
    ('C', 'Citigroup (C)'),
    ('WFC', 'Wells Fargo (WFC)'),
    ('AXP', 'American Express (AXP)'),
    ('T', 'AT&T (T)'),
    ('VZ', 'Verizon (VZ)'),
    ('KO', 'Coca-Cola (KO)'),
    ('PEP', 'PepsiCo (PEP)'),
    ('PG', 'Procter & Gamble (PG)'),
    ('JNJ', 'Johnson & Johnson (JNJ)'),
    ('PFE', 'Pfizer (PFE)'),
    ('MRNA', 'Moderna (MRNA)'),
    ('UNH', 'UnitedHealth Group (UNH)'),
    ('CVS', 'CVS Health (CVS)'),
    ('WBA', 'Walgreens Boots Alliance (WBA)'),
    ('LLY', 'Eli Lilly (LLY)'),
    ('AMGN', 'Amgen (AMGN)'),
    ('ABBV', 'AbbVie (ABBV)'),
    ('XOM', 'ExxonMobil (XOM)'),
    ('CVX', 'Chevron (CVX)'),
    ('BP', 'BP (BP)'),
    ('SHEL', 'Shell (SHEL)'),
    ('TOT', 'TotalEnergies (TOT)'),
    ('SLB', 'Schlumberger (SLB)'),
    ('RDS.A', 'Royal Dutch Shell (RDS.A)'),
    ('GE', 'General Electric (GE)'),
    ('GM', 'General Motors (GM)'),
    ('F', 'Ford (F)'),
    ('NIO', 'Nio (NIO)'),
    ('BA', 'Boeing (BA)'),
    ('LMT', 'Lockheed Martin (LMT)'),
    ('RTX', 'Raytheon Technologies (RTX)'),
    ('CAT', 'Caterpillar (CAT)'),
    ('MMM', '3M (MMM)'),
    ('DE', 'Deere & Company (DE)'),
    ('HON', 'Honeywell (HON)'),
    ('IBM', 'IBM (IBM)'),
    ('SPGI', 'S&P Global (SPGI)'),
    ('MO', 'Altria (MO)'),
    ('PM', 'Philip Morris International (PM)'),
    ('MCD', 'McDonald’s (MCD)'),
    ('SBUX', 'Starbucks (SBUX)'),
    ('YUM', 'Yum! Brands (YUM)'),
    ('NKE', 'Nike (NKE)'),
    ('ADDYY', 'Adidas (ADDYY)'),
    ('RL', 'Ralph Lauren (RL)'),
    ('TGT', 'Target (TGT)'),
    ('WMT', 'Walmart (WMT)'),
    ('COST', 'Costco (COST)'),
    ('HD', 'Home Depot (HD)'),
    ('LOW', 'Lowe’s (LOW)'),
    ('BBY', 'Best Buy (BBY)'),
    ('TJX', 'TJX Companies (TJX)'),
    ('KHC', 'Kraft Heinz (KHC)'),
    ('GIS', 'General Mills (GIS)'),
    ('MDLZ', 'Mondelez (MDLZ)'),
    ('K', 'Kellogg (K)'),
    ('CL', 'Colgate-Palmolive (CL)'),
    ('HSY', 'Hershey (HSY)'),
    ('TSM', 'Taiwan Semiconductor (TSM)'),
    ('QCOM', 'Qualcomm (QCOM)'),
    ('MU', 'Micron Technology (MU)'),
    ('NXPI', 'NXP Semiconductors (NXPI)'),
    ('ASML', 'ASML Holding (ASML)'),
    ('LRCX', 'Lam Research (LRCX)'),
    ('AVGO', 'Broadcom (AVGO)'),
    ('TXN', 'Texas Instruments (TXN)'),
    ('ADP', 'Automatic Data Processing (ADP)'),
    ('PAYX', 'Paychex (PAYX)'),
    ('NOW', 'ServiceNow (NOW)'),
    ('INTU', 'Intuit (INTU)'),
    ('DOCU', 'DocuSign (DOCU)'),
    ('FSLY', 'Fastly (FSLY)'),
    ('OKTA', 'Okta (OKTA)'),
    ('MDB', 'MongoDB (MDB)'),
    ('ZS', 'Zscaler (ZS)')
]

class FetchStockForm(forms.Form):
    symbol = forms.ChoiceField(choices=STOCK_CHOICES, label='Stock Symbol', widget=forms.Select(attrs={'class': 'form-control'}))


class BacktestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BacktestForm, self).__init__(*args, **kwargs)

        # Get unique stock symbols from the StockPrice model
        fetched_symbols = StockPrice.objects.values_list('symbol', flat=True).distinct()

        # Combine initial predefined choices and fetched symbols
        all_choices =[(symbol, symbol) for symbol in fetched_symbols]

        # Set up the symbol field with the combined choices
        self.fields['symbol'] = forms.ChoiceField(choices=all_choices, label='Stock Symbol', widget=forms.Select(attrs={'class': 'form-control'}))

    initial_investment = forms.FloatField(label='Initial Investment ($)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10000'}))
    buy_moving_average = forms.IntegerField(label='Buy Moving Average (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50'}))
    sell_moving_average = forms.IntegerField(label='Sell Moving Average (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 200'}))

class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)

        # Get unique stock symbols from the StockPrice model
        fetched_symbols = StockPrice.objects.values_list('symbol', flat=True).distinct()

        # Combine initial predefined choices and fetched symbols
        all_choices =[(symbol, symbol) for symbol in fetched_symbols]

        # Set up the symbol field with the combined choices
        self.fields['symbol'] = forms.ChoiceField(choices=all_choices, label='Stock Symbol', widget=forms.Select(attrs={'class': 'form-control'}))
    days = forms.IntegerField(label='Number of Days to Predict', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 30'}))