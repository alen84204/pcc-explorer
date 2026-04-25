import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 8000

def start_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # 先確認資料是否存在
    if not os.path.exists('data.json'):
        print("尚未有資料，正在呼叫 crawler 抓取...")
        os.system('python pcc_crawler.py')

    # 在背景啟動伺服器
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 等待一秒讓伺服器啟動
    time.sleep(1)
    
    # 自動開啟預設瀏覽器
    url = f"http://localhost:{PORT}/index.html"
    print(f"正在開啟看板: {url}")
    webbrowser.open(url)
    
    # 保持主程式運行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n看板服務已關閉。")
