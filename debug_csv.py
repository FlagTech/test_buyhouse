import pandas as pd

# 讀取CSV文件
df = pd.read_csv('app/static/assets/date_data.csv', encoding='utf-8-sig')

print("CSV檔案列名檢查:")
print("總共有", len(df.columns), "個欄位")
print()

# 列出所有欄位名稱並使用repr來顯示真實內容
print("所有欄位名稱:")
for i, col in enumerate(df.columns):
    print(f"  {i+1}: {repr(col)}")
print()

# 檢查基本欄位
base_columns = ['季度', '房價(元/坪)', '租金(元/坪)', '物價指數']
print("基本欄位檢查:")
for col in base_columns:
    exists = col in df.columns
    print(f"  '{col}': {exists}")
    if not exists:
        # 找相似的
        similar = [c for c in df.columns if col.split('(')[0] in c]
        if similar:
            print(f"    可能的替代: {similar}")
print()

# 檢查臺北市相關欄位
taipei_price = '臺北市_房價'
taipei_rent = '臺北市_租金'

print(f"'{taipei_price}' 是否存在:", taipei_price in df.columns)
print(f"'{taipei_rent}' 是否存在:", taipei_rent in df.columns)

# 顯示資料樣本
print("\n前3行數據:")
print(df.head(3))