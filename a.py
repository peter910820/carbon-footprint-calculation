import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 自訂的時間陣列
x = ['2023-01-01 09:00:00', '2023-01-01 10:00:00', '2023-01-01 11:00:00', '2023-01-01 12:00:00', '2023-01-01 13:00:00']
y = [2, 4, 4, 5, 10]

# 轉換時間格式
x_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in x]

# 設定圖表大小
fig, ax = plt.subplots(figsize=(10, 6))

# 繪製折線圖
plt.plot(x_dates, y, linestyle='solid', marker=None)

# 設定 X 軸刻度間隔和格式
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # 設定刻度間隔為一小時
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  # 設定日期格式

# 設定圖表標題與軸標籤
plt.title("Line Chart")
plt.xlabel("Datetime")
plt.ylabel("Y-axis")

# 儲存圖檔
plt.savefig("line_chart.png")

# 顯示圖表
plt.show()