import pandas as pd
from pathlib import Path
import numpy as np
from statistics import mean

# 縣市代號對應
location = {
    'a': '臺北市', 'b': '臺中市', 'c': '基隆市', 'd': '臺南市',
    'e': '高雄市', 'f': '新北市', 'g': '宜蘭縣', 'h': '桃園市',
    'i': '嘉義市', 'j': '新竹縣', 'k': '苗栗縣', 'm': '南投縣',
    'n': '彰化縣', 'o': '新竹市', 'p': '雲林縣', 'q': '嘉義縣',
    't': '屏東縣', 'u': '花蓮縣', 'w': '金門', 'x': '澎湖縣'
}

def process_quarter_data():
    """處理所有季度資料並更新CSV檔案"""
    
    # 讀取現有的date_data.csv作為基礎
    try:
        existing_data = pd.read_csv("app/static/assets/date_data.csv", encoding='utf-8-sig')
        print(f"現有資料到: {existing_data.iloc[-1, 0]}")
    except:
        existing_data = pd.DataFrame()
    
    # 獲取所有季度目錄
    path = Path.cwd() / "app/static/assets/data"
    quarters = sorted([i for i in path.glob('*') if i.is_dir()])
    
    # 找出需要更新的季度（111Q2之後）
    new_quarters = [q for q in quarters if q.name >= '111Q2']
    
    print(f"需要處理的新季度: {[q.name for q in new_quarters]}")
    
    # 處理每個新季度
    new_rows = []
    
    for quarter_dir in new_quarters:
        quarter_name = quarter_dir.name
        print(f"處理季度: {quarter_name}")
        
        # 初始化該季度的資料
        quarter_data = {'季度': quarter_name}
        
        # 計算整體房價平均
        all_price_data = pd.DataFrame()
        for csv_file in quarter_dir.glob('*_lvr_land_a.csv'):
            try:
                data = pd.read_csv(csv_file, low_memory=False)
                all_price_data = pd.concat([all_price_data, data])
            except Exception as e:
                print(f"讀取檔案 {csv_file} 時出錯: {e}")
                continue
        
        if not all_price_data.empty:
            # 資料清洗 - 房價
            filter_row = (all_price_data['交易標的'] == '房地(土地+建物)') | (all_price_data['交易標的'] == '房地(土地+建物)+車位')
            clean_data = all_price_data[filter_row]
            clean_data = clean_data.dropna(subset=['單價元平方公尺'])
            # 轉換為數值型態並過濾大於0的值
            clean_data = clean_data[pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') > 0]
            
            if not clean_data.empty:
                # 轉換為每坪價格
                clean_data['單價元坪'] = pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') / 0.3025
                avg_price = int(clean_data['單價元坪'].mean())
                quarter_data['房價(元/坪)'] = avg_price
        
        # 計算整體租金平均
        all_rent_data = pd.DataFrame()
        for csv_file in quarter_dir.glob('*_lvr_land_c.csv'):
            try:
                data = pd.read_csv(csv_file, low_memory=False)
                all_rent_data = pd.concat([all_rent_data, data])
            except Exception as e:
                print(f"讀取檔案 {csv_file} 時出錯: {e}")
                continue
        
        if not all_rent_data.empty:
            # 資料清洗 - 租金
            filter_row = (all_rent_data['交易標的'] == '房地(土地+建物)') | (all_rent_data['交易標的'] == '房地(土地+建物)+車位')
            clean_data = all_rent_data[filter_row]
            clean_data = clean_data.dropna(subset=['單價元平方公尺'])
            clean_data = clean_data[pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') > 0]
            
            if not clean_data.empty:
                # 轉換為每坪價格
                clean_data['單價元坪'] = pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') / 0.3025
                avg_rent = int(clean_data['單價元坪'].mean())
                quarter_data['租金(元/坪)'] = avg_rent
        
        # 物價指數 - 先設為空，之後可以手動更新
        quarter_data['物價指數'] = np.nan
        
        # 計算各縣市房價
        for key, city_name in location.items():
            # 房價
            city_price_data = pd.DataFrame()
            for csv_file in quarter_dir.glob(f'{key}_lvr_land_a*.csv'):
                try:
                    data = pd.read_csv(csv_file, low_memory=False)
                    city_price_data = pd.concat([city_price_data, data])
                except:
                    continue
            
            if not city_price_data.empty:
                filter_row = (city_price_data['交易標的'] == '房地(土地+建物)') | (city_price_data['交易標的'] == '房地(土地+建物)+車位')
                clean_data = city_price_data[filter_row]
                clean_data = clean_data.dropna(subset=['單價元平方公尺'])
                clean_data = clean_data[pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') > 0]
                
                if not clean_data.empty:
                    clean_data['單價元坪'] = pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') / 0.3025
                    avg_price = int(clean_data['單價元坪'].mean())
                    quarter_data[f'{city_name}_房價'] = avg_price
                else:
                    quarter_data[f'{city_name}_房價'] = 0
            else:
                quarter_data[f'{city_name}_房價'] = 0
            
            # 租金
            city_rent_data = pd.DataFrame()
            for csv_file in quarter_dir.glob(f'{key}_lvr_land_c*.csv'):
                try:
                    data = pd.read_csv(csv_file, low_memory=False)
                    city_rent_data = pd.concat([city_rent_data, data])
                except:
                    continue
            
            if not city_rent_data.empty:
                filter_row = (city_rent_data['交易標的'] == '房地(土地+建物)') | (city_rent_data['交易標的'] == '房地(土地+建物)+車位')
                clean_data = city_rent_data[filter_row]
                clean_data = clean_data.dropna(subset=['單價元平方公尺'])
                clean_data = clean_data[pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') > 0]
                
                if not clean_data.empty:
                    clean_data['單價元坪'] = pd.to_numeric(clean_data['單價元平方公尺'], errors='coerce') / 0.3025
                    avg_rent = int(clean_data['單價元坪'].mean())
                    quarter_data[f'{city_name}_租金'] = avg_rent
                else:
                    quarter_data[f'{city_name}_租金'] = 0
            else:
                quarter_data[f'{city_name}_租金'] = 0
        
        new_rows.append(quarter_data)
    
    # 建立新的資料框
    if new_rows:
        new_data = pd.DataFrame(new_rows)
        
        # 合併現有資料與新資料
        if not existing_data.empty:
            # 確保欄位順序一致
            for col in existing_data.columns:
                if col not in new_data.columns:
                    new_data[col] = np.nan
            
            new_data = new_data[existing_data.columns]
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data
        
        # 儲存更新後的date_data.csv
        updated_data.to_csv("app/static/assets/date_data.csv", encoding='utf-8-sig', index=False)
        print(f"已更新date_data.csv，新增 {len(new_rows)} 個季度的資料")
        
        # 更新其他檔案
        update_other_files(updated_data)
        
    else:
        print("沒有找到新的資料需要處理")

def update_other_files(updated_data):
    """更新其他相關的CSV檔案"""
    
    # 更新price.csv
    price_data = updated_data[['季度', '房價(元/坪)']].dropna()
    price_transpose = price_data.T
    price_transpose.columns = range(len(price_transpose.columns))
    price_transpose.to_csv("app/static/assets/price.csv", encoding='utf-8-sig', header=False)
    print("已更新price.csv")
    
    # 更新rent.csv
    rent_data = updated_data[['季度', '租金(元/坪)']].dropna()
    rent_transpose = rent_data.T
    rent_transpose.columns = range(len(rent_transpose.columns))
    rent_transpose.to_csv("app/static/assets/rent.csv", encoding='utf-8-sig', header=False)
    print("已更新rent.csv")
    
    # 更新city_p.csv (包含房價和租金)
    city_columns = []
    for city_name in location.values():
        city_columns.extend([f'{city_name}_房價', f'{city_name}_租金'])
    
    if all(col in updated_data.columns for col in city_columns):
        city_p_data = updated_data[city_columns]
        city_p_data.to_csv("app/static/assets/city_p.csv", encoding='utf-8-sig')
        print("已更新city_p.csv")
    
    # 更新city_r.csv (僅租金)
    rent_columns = [f'{city_name}_租金' for city_name in location.values()]
    if all(col in updated_data.columns for col in rent_columns):
        city_r_data = updated_data[rent_columns]
        city_r_data.to_csv("app/static/assets/city_r.csv", encoding='utf-8-sig')
        print("已更新city_r.csv")

if __name__ == "__main__":
    process_quarter_data()
    print("資料更新完成！")