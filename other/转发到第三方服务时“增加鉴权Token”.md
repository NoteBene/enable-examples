# **转发到第三方服务时“增加鉴权 Token”**

# **概述**

Token就像是一个暗号，使用它就可以访问一些需要认证的系统或者服务。在物联网开发平台中，用户如果在[转发到第三方服务（Forward）时选择“增加鉴权 Token”](https://cloud.tencent.com/document/product/1081/61105)，则需要经过如下几个步骤对Token进行验证：

- 第 1 步：物联网开发平台根据 Token 等参数计算 Signature，并将其添加到请求头，再发送Get请求至第三方服务。
- 第 2 步：第三方服务校验请求头中的 Signature 是否正确，若正确则返回校验正确的信息。
- 第 3 步：物联网开发平台收到校验信息，确认无误后则继续转发设备数据，

对于用户来讲只需要关注第 2 步，即校验请求头中的 Signature 并返回验证信息。

# **校验 Signature 并返回验证结果**

以下介绍各语言验证并返回验证信息的方法。

验证原理可见“物联网平台增加鉴权Token机制”。

## **PHP**

PHP 示例代码如下：

```php
<?php
ini_set('display_errors',1);            //错误信息  
ini_set('display_startup_errors',1);    //php启动错误信息  
error_reporting(-1);                    //打印出所有的 错误信息  

function microtime_float()
{
        list($usec, $sec) = explode(" ", microtime());
        return ((float)$usec + (float)$sec);
}

function microtime_format($tag, $time)
{
        list($usec, $sec) = explode(".", $time);
        $date = date($tag,$usec);
        return str_replace('x', $sec, $date);
}

function get_AllHeaders(){
    $headers = array();
    foreach($_SERVER as $key=>$value){
        if(substr($key, 0, 5)==='HTTP_'){
            $key = substr($key, 5);
            $key = str_replace('_', ' ', $key);
            $key = str_replace(' ', '-', $key);
            $key = strtolower($key);
            $headers[$key] = $value;
        }
    }
    return $headers;
}
#验签函数
function checkSignature($signature='',$timestamp='',$nonce='')
{
    $postsignature = $signature;
    $posttimestamp = $timestamp;
    $postnonce = $nonce;
    # 用户设置token  在此填入设置的token 
    $token = "test";
    $tmpArr = array($token, $posttimestamp, $postnonce);
    sort($tmpArr, SORT_STRING);
    $tmpStr = implode( $tmpArr );
    $tmpStr = sha1( $tmpStr );
    
    if( $tmpStr == $signature ){
        return true;
    }else{
        return false;
    }
}

$url = $_SERVER["REQUEST_URI"];
$ctype = $_SERVER['CONTENT_TYPE'];
$raw_post_data = file_get_contents('php://input');
if( $_SERVER['REQUEST_METHOD'] === 'GET'){
	
			$header = get_AllHeaders();
			$signature = $header['signature'];
			$timestamp = $header['timestamp'];
			$nonce = $header['nonce'];
			$echostr = $header['echostr'];
			#验签成功与否标志 $flag			
			$flag = checkSignature($signature,$timestamp,$nonce);

			if ($flag === true) {
				header('Content-Type: text/plain; charset=utf-8');
				$len = 'Content-Length: ';
				$len .= strlen($echostr);
				header($len);
				echo $header['echostr'] ;
			}else {
				echo '验签失败',"\r\n";
			}


}else if( $_SERVER['REQUEST_METHOD'] === 'POST') {		
			#echo microtime() ;
			$time = microtime_float();
			$strtime = microtime_format('Ymd-His.x ', $time);
			$ctype = $_SERVER['CONTENT_TYPE'];
			echo $strtime , '#post body:' , $raw_post_data , "\r\n";
			file_put_contents("demo.log" ,"$strtime TYPE:$ctype BODY: $raw_post_data\r\n",FILE_APPEND); 
        }else{
			
		}
?>
```

## **Go**

```go
package main

import (
	"crypto/sha1"
	"encoding/hex"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"sort"
	"strings"
	"time"
)

func jsonReqRsp(w http.ResponseWriter, r *http.Request) {
	var Token string
	var arr []string
	var Signature  string
	var Echostr string
	//用户设置token
	Token = "test"
	arr = append(arr, Token)
	if r.Method =="GET"{
		//解析 header
		if len(r.Header) > 0 {
			for k,v :=range r.Header {
				fmt.Printf("%s=%s\n", k, v[0])
				if k =="Echostr"{
					Echostr = v[0]
				}
				if k== "Signature"{
					Signature = v[0]
				}
				if k=="Timestamp"{
					arr = append(arr,string(v[0]))
				}
				if k=="Nonce"{
					arr = append(arr,string(v[0]))
				}
			}
		}
		//验签
		sort.Slice(arr, func(i, j int) bool {
			return arr[i] < arr[j]
		})
		tmpstr := strings.Join(arr,"")
		h := sha1.New()
		h.Write([]byte(tmpstr))
		tmpsignature := h.Sum(nil)
		result := hex.EncodeToString(tmpsignature)
		fmt.Println("tmpsignature %s: ",result)
		if result == Signature {
			fmt.Println("验签成功")
			// 返回json字符串给客户端
			w.WriteHeader(http.StatusOK)
			w.Header().Set("Content-Type", "application/json")
			io.WriteString(w, Echostr)
		} else {
			fmt.Println("验签失败")
		}


	} else if r.Method=="POST"{
		// 调用json包的解析，解析请求body
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			fmt.Println("解析失败")
			return
		}
		log.Println("req json: ",  string(body))
		//将body写入文件
		fl , err := os.OpenFile("device_report.txt",os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModeAppend)
		if err != nil {
			fmt.Println("失败！！！")
			return
		}
		defer fl.Close()
		n, err := fl.Write(body)
		if err != nil && n < len(body) {
			fmt.Println("失败！！！")
			fmt.Println("err:",err)
		}
	} else {
		w.WriteHeader(404)
	}


}
func main() {
	//设置监听的端口
	http.HandleFunc("/test",jsonReqRsp)
	s := &http.Server{
		Addr:           ":9090",
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	err := s.ListenAndServe()
	if err != nil {
		log.Fatal("listenAndServe: ", err)
	}

}
```



## **Python**

```python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import hashlib
from sys import argv

#用户设置token
token = "test"

class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):#处理get请求
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))#打印get请求
        if str(self.path) == "/":#判断URL的路径
            a = self.checkSignature(token)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(a,encoding = "utf8"))#返回验证参数

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))#打印post请求
        if str(self.path) == "/":#判断URL路径
            self.explorerHandle(post_data)#处理数据
            return
        data = json.dumps({'code': 404, 'status': 'not found'})
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

    def explorerHandle(self, body):#处理数据函数
        # 处理explorer请求
        file = open("device_report.txt", 'w')
        res =json.dumps(json.loads(body),cls=MyEncoder)#转换格式  bytes -> dict
        file.write(res)  # 写入文件

    def checkSignature(self,token):#模拟控制台加密算法生成数字签名与请求中的签名相对比
        signature = self.headers.get_all("signature")[0]
        Echostr = self.headers.get_all("Echostr")
        s = []
        s.append(token)
        s.append(self.headers.get_all("timestamp")[0])
        s.append(self.headers.get_all("nonce")[0])
        s.sort()
        tmpArr = s[0] + s[1] + s[2]
        
        sha1 = hashlib.sha1()
        sha1.update(tmpArr.encode('utf-8'))
        res = sha1.hexdigest()
        
        if res == signature:
            return Echostr[0]
        self.send_response(401)

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
```

# **物联网平台增加鉴权Token机制**

用户如果在转发到第三方服务（Forward）时选择“增加鉴权 Token”，物联网平台将在 HTTPS 请求中头部增加如下字段：

| 参数      | 描述                                                         |
| --------- | ------------------------------------------------------------ |
| Signature | 结合了 Token、 Timestamp、Nonce 并进行字典序排序和 sha1 加密后的结果 |
| Timestamp | 时间戳                                                       |
| Nonce     | 随机数                                                       |

例如用户设置 Token 为 aaa。在某次请求时 Timestamp: 为1604458421，Nonce 为IkOaKMDalrAzUTxC。

则排序后的字符串是 `1604458421IkOaKMDalrAzUTxCaaa`，最终计算 sha1 结果（即Signature）为 `c259ed29ec13ba7c649fe0893007401a36e70453`。

最终物联网平台将向第三方服务发送的报文如下：

```
GET / HTTP/1.1
Host: **.**.**.**:4443
User-Agent: Go-http-client/1.1
Content-Type: application/json
Echostr: UPWIAFASvDUFcTEE
Nonce: testrance
Signature: abb6c316a8134596d825c5a1295bfa6f7657664d
Timestamp: 1623149590
Accept-Encoding: gzip
```

# **服务地址校验机制**

为校验所转发的服务地址是否正确，第三方服务在确认 GET 请求来自物联网平台后，需要在 body 中原样返回 Echostr 参数内容。

回复报文如下：

```
HTTP/1.1 200 OK
Date: Tue, 08 Jun 2021 10:53:10 GMT
Content-Length: 16
Content-Type: text/plain; charset=utf-8

UPWIAFASvDUFcTEE
```

物联网平台通过校验返回的 Echostr 参数内容，便能确认服务器地址 URL 否有效。

# **重发机制**

重发机制用于在消息转发过程中发生失败的情况下，进行再次重发以达到接受消息的目的，具体说明如下：

- 若消息转发失败，系统则会进行转发重试，重试按照1s、3s、10s的时间间隔依次进行，若三次重试均失败，则将消息丢弃掉。
- 若用户配置了“转发错误行为操作”，在三次重试失败后，将按“转发错误行为操作”的配置，再进行一次消息转发，如果仍失败，则将消息丢弃掉。
