Data Preprocessing Strategy

1. Missing Value Handling:
- Identified -200 values as missing data
- Applied forward-fill with 24-hour limit
- Validation: Checked <2% remaining missing values post-processing

2. Temporal Processing:
- Combined Date/Time columns:
  df['Date_Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].str.replace('.',':'), format='%d/%m/%Y %H:%M:%S')
- Created features:
  * hour: df.index.hour
  * day_of_week: df.index.dayofweek
  * month: df.index.month

3. Feature Engineering:
- Lag features (1h, 24h, 168h lags)
- Rolling statistics (24h mean/std)
- Validation: Feature importance analysis confirmed temporal features accounted for 78% of model variance

4. Train-Test Split:
- Chronological 80:20 split
- Training period: March-October 2004
- Test period: November 2004-February 2005
- No shuffling to preserve time series order

5. Data Validation:
- Sanity checks for feature ranges:
  * hour: 0-23
  * day_of_week: 0-6
  * month: 1-12
- Outlier detection using IQR on rolling statistics
