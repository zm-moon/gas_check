import requests
import tkinter as tk
from tkinter import messagebox

# 设置代理地址和端口
proxy_address = '127.0.0.1'  # 代理地址
proxy_port = '3331'  # 代理端口

# 创建一个代理字典
proxies = {
    'http': f'http://{proxy_address}:{proxy_port}',
    'https': f'https://{proxy_address}:{proxy_port}'
}

# 设置提醒的 gas 费用阈值
set_gas_fee = 2  # 设置一个较大的初始值

def get_gas_price():
    url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle'
    response = requests.get(url, proxies=proxies)  # 使用代理进行请求
    data = response.json()
    gas_price = int(data['result']['FastGasPrice'])
    return gas_price

def check_gas_price():
    gas_price = get_gas_price()
    gas_label.config(text=f'Gas Price: {gas_price} Gwei')

    if set_gas_fee is not None and gas_price < set_gas_fee:
        messagebox.showinfo('Gas Price Alert', f'Gas price has dropped below {set_gas_fee} Gwei!')

    root.after(10000, check_gas_price)  # 每 10 秒钟检查一次

# 输入反馈
def gas_seted():
    global set_gas_fee     # global控制外部变量
    gas_already_seted = input_entry.get()
    set_gas_fee = int(gas_already_seted)
    gas_setted.config(text=f"你设定的 gas 提醒值为: {set_gas_fee}")

# 创建主窗口
root = tk.Tk()
root.title('Gas Price Widget')

# 输入框
gas_price_input = tk.Label(root, text='请输入你想要设置的 gas fee', font=('Arial', 18))
gas_price_input.pack(padx=20, pady=20)

input_entry = tk.Entry(root, font=('Arial', 14))
input_entry.pack(padx=20, pady=10)

# 创建一个标签用于显示 gas 费用
gas_label = tk.Label(root, font=('Arial', 18))
gas_label.pack(padx=20, pady=20)

# 用来显示已设置提醒的 gas 值
gas_setted = tk.Label(root, font=('Arial', 18))
gas_setted.pack(padx=10, pady=10)

submit_button = tk.Button(root, text="提交", command=gas_seted)
submit_button.pack(padx=20, pady=10)

# 启动 gas 费用的检查
check_gas_price()

root.focus_force()
root.attributes('-topmost', True)

# 运行主循环
root.mainloop()
