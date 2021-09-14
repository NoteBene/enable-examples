<!DOCTYPE html>
<html>
<body>

<h1>接收Post数据</h1>

<?php
date_default_timezone_set("PRC");

// 接收Post数据
$raw_post_data = file_get_contents('php://input');
// 获取当前时间
$time = date("Y-m-d H:i:s");
// 输出数据
echo $time , '#post body:' , $raw_post_data , "\r\n";
// 记录信息
file_put_contents("raw_post_data.txt", "$time DATA: $raw_post_data\r\n", FILE_APPEND | LOCK_EX);
?>


</body>
</html>
