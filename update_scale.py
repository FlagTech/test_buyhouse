import pandas as pd
import numpy as np

def update_scale_data():
    """更新scale.csv資料，使用最新的平均房價和租金"""
    
    # 讀取最新的date_data.csv
    data = pd.read_csv("app/static/assets/date_data.csv", encoding='utf-8-sig')
    
    # 取得最近5個季度來計算平均值
    recent_data = data.tail(5)
    
    # 縣市列表
    cities = ['臺北市', '臺中市', '基隆市', '臺南市', '高雄市', '新北市', '宜蘭縣', '桃園市', 
             '嘉義市', '新竹縣', '苗栗縣', '南投縣', '彰化縣', '新竹市', '雲林縣', '嘉義縣', 
             '屏東縣', '花蓮縣', '金門', '澎湖縣', '臺東縣']
    
    # 薪資資料（基於最新統計資料，這個需要手動更新）
    salary_data = {
        '臺北市': 150000, '臺中市': 115000, '基隆市': 98000, '臺南市': 98000,
        '高雄市': 108000, '新北市': 125000, '宜蘭縣': 100000, '桃園市': 128000,
        '嘉義市': 105000, '新竹縣': 148000, '苗栗縣': 105000, '南投縣': 88000,
        '彰化縣': 95000, '新竹市': 140000, '雲林縣': 90000, '嘉義縣': 82000,
        '屏東縣': 92000, '花蓮縣': 90000, '金門': 85000, '澎湖縣': 75000,
        '臺東縣': 82000
    }
    
    scale_data = []
    
    for city in cities:
        price_col = f'{city}_房價'
        rent_col = f'{city}_租金'
        
        if price_col in recent_data.columns and rent_col in recent_data.columns:
            # 計算近5個季度的平均房價和租金（排除0值）
            price_values = recent_data[price_col][recent_data[price_col] > 0]
            rent_values = recent_data[rent_col][recent_data[rent_col] > 0]
            
            if len(price_values) > 0:
                avg_price = int(price_values.mean())
            else:
                avg_price = 0
                
            if len(rent_values) > 0:
                avg_rent = int(rent_values.mean())
            else:
                avg_rent = 0
            
            # 取得薪資資料
            salary = salary_data.get(city, 100000)
            
            # 計算房價收入比（假設20坪）
            if salary > 0:
                price_income_ratio = round((avg_price * 20) / salary, 2)
            else:
                price_income_ratio = 0
            
            scale_data.append({
                '城市': city,
                '房價': avg_price,
                '租金': avg_rent,
                '月薪': salary,
                '房價收入比(20坪)': price_income_ratio
            })
    
    # 建立DataFrame
    scale_df = pd.DataFrame(scale_data)
    
    # 儲存到scale.csv
    scale_df.to_csv("app/static/assets/scale.csv", encoding='utf-8-sig', index=False)
    print("已更新scale.csv")
    
    return scale_df

if __name__ == "__main__":
    result = update_scale_data()
    print("更新完成！")
    print(result.head())