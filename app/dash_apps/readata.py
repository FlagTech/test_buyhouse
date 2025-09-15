from statistics import mean
import pandas as pd 
from pathlib import Path

##縣市名稱
location = { 'a' : '臺北市', 'b' : '臺中市' ,
                'c' : '基隆市', 'd' : '臺南市' ,
                'e' : '高雄市', 'f' : '新北市' ,
                'g' : '宜蘭縣', 'h' : '桃園市' ,
                'i' : '嘉義市', 'j' : '新竹縣' ,
                'k' : '苗栗縣', 'm' : '南投縣' ,
                'n' : '彰化縣', 'o' : '新竹市' ,
                'p' : '雲林縣', 'q' : '嘉義縣' ,
                't' : '屏東縣', 'u' : '花蓮縣' ,
                'v' : '臺東縣', 'w' : '金門'  ,
                'x' : '澎湖縣'  }
##資料路徑


price_data = pd.DataFrame()
#尋找路徑
path = Path.cwd() / "app/static/assets/data"
for i in list(path.glob('*')):

    print(i.name)

    df_all = pd.DataFrame()
    for x in list(i.glob('*a.csv')):
        data = pd.read_csv(x , low_memory=False)
        df_all = pd.concat([df_all,data])

    ##資料清洗
    filter_row = (df_all['交易標的'] == '房地(土地+建物)' ) | (df_all['交易標的'] == '房地(土地+建物)+車位' )
    filter_col = ['鄉鎮市區' , '交易標的' , '交易年月日','移轉層次' ,'總樓層數' , '建物型態','建築完成年月' , '總價元' ,'單價元平方公尺']

    f_df = df_all.loc[filter_row, filter_col]
    f_df = f_df.dropna(subset=['單價元平方公尺'])
    f_df['單價元坪'] = f_df['單價元平方公尺'].apply(int) / 0.3025
    f_df = f_df.loc[(f_df['單價元平方公尺'] != 0),: ]
    f_df['單價元坪'] = f_df['單價元坪'].apply(int)

    price = f_df['單價元坪'].mean()
    if pd.isna(price):
        price = 0  # or use a default value
    else:
        price = int(price)

    df_date = pd.DataFrame([i.name,price])

    price_data = pd.concat([price_data, df_date] ,axis=1)



price_data.to_csv("app/static/assets/price.csv")


########租金
price_data = pd.DataFrame()
#尋找路徑
path = Path.cwd() / "app/static/assets/data"
for i in list(path.glob('*')):

    print(i.name)

    df_all = pd.DataFrame()
    for x in list(i.glob('*c.csv')):
        data = pd.read_csv(x , low_memory=False)
        df_all = pd.concat([df_all,data])

    ##資料清洗
    if '交易標的' in df_all.columns:
        df_all['交易標的'] = df_all['交易標的'].replace('租賃房屋', '建物')
    filter_row = (df_all['交易標的'] == '建物' ) | (df_all['交易標的'] == '房地(土地+建物)' )
    filter_col = ['鄉鎮市區' , '交易標的'  ,'總樓層數' , '建物型態','建築完成年月'  ,'單價元平方公尺']

    f_df = df_all.loc[filter_row, filter_col]
    f_df = f_df.dropna(subset=['單價元平方公尺'])
    f_df['單價元坪'] = f_df['單價元平方公尺'].apply(int) / 0.3025
    f_df = f_df.loc[(f_df['單價元平方公尺'] != 0),: ]
    f_df['單價元坪'] = f_df['單價元坪'].apply(int)

    price = f_df['單價元坪'].mean()
    if pd.isna(price):
        price = 0  # or use a default value
    else:
        price = int(price)

    df_date = pd.DataFrame([i.name,price])

    price_data = pd.concat([price_data, df_date] ,axis=1)


price_data.to_csv("app/static/assets/rent.csv")




#########各縣市房價資料


ALLL_data =  pd.DataFrame()

for key,value in location.items():
    print(key)
    print(value)

    price_data = pd.DataFrame()
    #尋找路徑
    path = Path.cwd() / "app/static/assets/data"
    for i in list(path.glob('*')):

        print(i.name)

        df_all = pd.DataFrame()
        city = 'a'
        csv_files = list(i.glob(key + '*a.csv'))
        
        # Skip if no files found
        if not csv_files:
            print(f"No {key}*a.csv files found in {i.name}, skipping...")
            continue
            
        for x in csv_files:
            data = pd.read_csv(x , low_memory=False)
            df_all = pd.concat([df_all,data])

        # Skip if no data
        if df_all.empty:
            print(f"No data loaded for {key} in {i.name}, skipping...")
            continue

        ##資料清洗
        filter_row = (df_all['交易標的'] == '房地(土地+建物)' ) | (df_all['交易標的'] == '房地(土地+建物)+車位' )
        filter_col = ['鄉鎮市區' , '交易標的' , '交易年月日','移轉層次' ,'總樓層數' , '建物型態','建築完成年月' , '總價元' ,'單價元平方公尺']

        f_df = df_all.loc[filter_row, filter_col]
        f_df = f_df.dropna(subset=['單價元平方公尺'])
        f_df['單價元坪'] = f_df['單價元平方公尺'].apply(int) / 0.3025
        f_df = f_df.loc[(f_df['單價元平方公尺'] != 0),: ]
        f_df['單價元坪'] = f_df['單價元坪'].apply(int)

        price = f_df['單價元坪'].mean()
        price = int(price)

        df_date = pd.DataFrame([price])

        price_data = pd.concat([price_data, df_date])

    # Only process if price_data is not empty
    if not price_data.empty:
        price_data.columns = [value + "_房價"]
        price_data.reset_index(drop=True, inplace=True)  # Reset index to avoid duplicates
        
        if ALLL_data.empty:
            ALLL_data = price_data
        else:
            # Reset index for ALLL_data as well to ensure proper concatenation
            ALLL_data.reset_index(drop=True, inplace=True)
            ALLL_data = pd.concat([ALLL_data, price_data], axis=1)
    else:
        print(f"No data for {value}, skipping...")

ALLL_data.to_csv("app/static/assets/city_p.csv" , encoding="utf_8_sig")

######各縣市租金資料

ALLL_data =  pd.DataFrame()
# Dictionary to store previous prices for forward filling
previous_prices = {}

for key,value in location.items():
    print(key)
    print(value)

    price_data = pd.DataFrame()
    #尋找路徑
    path = Path.cwd() / "app/static/assets/data"
    for i in list(path.glob('*')):

        print(i.name)

        df_all = pd.DataFrame()
        city = 'a'
        csv_files = list(i.glob(key + '*c.csv'))
        
        # Skip if no files found
        if not csv_files:
            print(f"No {key}*c.csv files found in {i.name}, skipping...")
            continue
            
        for x in csv_files:
            data = pd.read_csv(x , low_memory=False)
            df_all = pd.concat([df_all,data])

        # Skip if no data
        if df_all.empty:
            print(f"No data loaded for {key} in {i.name}, skipping...")
            continue

        ##資料清洗
        # Replace '租賃房屋' with '建物' to match old format
        if '交易標的' in df_all.columns:
            df_all['交易標的'] = df_all['交易標的'].replace('租賃房屋', '建物')
        filter_row = (df_all['交易標的'] == '建物' ) | (df_all['交易標的'] == '房地(土地+建物)' )
        filter_col = ['鄉鎮市區' , '交易標的'  ,'總樓層數'  ,'單價元平方公尺']

        f_df = df_all.loc[filter_row, filter_col]
        f_df = f_df.dropna(subset=['單價元平方公尺'])
        f_df['單價元坪'] = f_df['單價元平方公尺'].apply(int) / 0.3025
        f_df = f_df.loc[(f_df['單價元平方公尺'] != 0),: ]
        f_df['單價元坪'] = f_df['單價元坪'].apply(int)

        price = f_df['單價元坪'].mean()
        if pd.isna(price) or price <= 0:
            # Use previous price if available for forward filling
            if key in previous_prices:
                price = previous_prices[key]
                print(f"Using previous price {price} for {key} in {i.name}")
            else:
                price = 0
        else:
            price = int(price)
            # Store current price for future forward filling
            previous_prices[key] = price

        df_date = pd.DataFrame([price])

        price_data = pd.concat([price_data, df_date])

    # Only process if price_data is not empty
    if not price_data.empty:
        price_data.columns = [value + "_租金"]
        price_data.reset_index(drop=True, inplace=True)  # Reset index to avoid duplicates
        
        if ALLL_data.empty:
            ALLL_data = price_data
        else:
            # Reset index for ALLL_data as well to ensure proper concatenation
            ALLL_data.reset_index(drop=True, inplace=True)
            ALLL_data = pd.concat([ALLL_data, price_data], axis=1)
    else:
        print(f"No data for {value}, skipping...")


ALLL_data.to_csv("app/static/assets/city_r.csv" , encoding="utf_8_sig")
