# Bigtime_Space_CrackedHourGlass_spawn_time_calculator

BIGTIME空间破碎沙漏生成时间计算器

用于自动计算空间中的沙漏时区和可掉落时间

详细教程请阅读 [YiJer](https://github.com/YiJer) 的 [給一般使用者的說明](https://github.com/pyDraco9/Bigtime_Space_CrackedHourGlass_spawn_time_calculator/issues/1)

使用方法: 请访问在任意有鉴权的接口(如: https://openloot.com/collection )时按F12获取 `cookie`, `X-Device-Id` 和 `X-Session-Id`.

如果不会可以谷歌搜索 "chrome如何获取cookie", 其他两个参数也在同一个页面可以找到.

将这些值写入.env文件后(用文本编辑器编辑)运行 `space_check.py` 或 [下载编译好的exe](https://github.com/pyDraco9/Bigtime_Space_CrackedHourGlass_spawn_time_calculator/releases/)

补充: 可以直接修改 `calculate_time_difference` 函数 中 `timestamp = timestamp + timedelta(hours=8)` 实现自定义时区. 当前源码中时区为UTC+8.

效果图:

![20240316202931](https://github.com/pyDraco9/Bigtime_Space_CrackedHourGlass_spawn_time_calculator/assets/11333467/82ab176c-ae82-49a1-84d4-456993add5af)
