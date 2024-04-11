def format_elapsed_time(elapsed_time):
    # 获取总秒数
    seconds = int(elapsed_time.total_seconds())
    # 提取天数、小时数、分钟数和秒数
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    # 格式化为字符串
    return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"
