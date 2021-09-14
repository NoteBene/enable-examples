# -*- coding: utf-8 -*
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import hashlib
import requests
from sys import argv


class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):#处理get请求
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))#打印get请求
        if str(self.path) == "/api/explorer":#判断URL的路径
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(a,encoding = "utf8"))#返回验证参数

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))#打印post请求
        if self.path == "/":#判断URL路径
            #处理数据
            self.explorerHandle(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("ok",encoding = "utf8"))#返回验证参数
            return
        data = json.dumps({'code': 404, 'status': 'not found'})
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

    def explorerHandle(self, body):#处理数据函数
        # 设置目标地址
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=*********'
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        d = {
              "msgtype": "text",
              "text": {
                "content": body.decode('utf-8')
              }
            }
        # 转发至目标地址
        r = requests.post(url, headers=headers, data=json.dumps(d))

class MyEncoder(json.JSONEncoder):#将post请求的参数由HTTPMessage转换成json
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)


def run(server_class=HTTPServer, handler_class=Handler, port=80):
    logging.basicConfig(level=logging.INFO)
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
   
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()