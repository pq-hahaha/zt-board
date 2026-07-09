# -*- coding: utf-8 -*-
"""本地HTTP服务器 - no-cache响应头, 防止浏览器缓存HTML/JSON
用法: python serve.py
替代: python -m http.server 8765 --bind 127.0.0.1 --directory "..."
"""
import http.server
import socketserver
import os
import sys

PORT = 8765
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """所有响应加no-cache头, 浏览器每次都从服务器拉最新文件"""

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # 简化日志, 只打印状态码和路径
        sys.stdout.write("[%s] %s\n" % (self.log_date_time_string(), format % args))


class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    os.chdir(DIRECTORY)
    try:
        with ReusableServer(("127.0.0.1", PORT), NoCacheHandler) as httpd:
            print("[serve.py] Serving: " + DIRECTORY)
            print("[serve.py] URL: http://127.0.0.1:" + str(PORT))
            print("[serve.py] Cache-Control: no-cache (all responses)")
            print("[serve.py] Press Ctrl+C to stop")
            print("---")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98 or 'Address already in use' in str(e):
            print("[serve.py] ERROR: Port " + str(PORT) + " already in use.")
            print("[serve.py] Run: taskkill /F /IM python.exe  (or find the PID using the port)")
        else:
            print("[serve.py] ERROR: " + str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[serve.py] Stopped")
