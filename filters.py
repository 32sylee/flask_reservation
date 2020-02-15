from datetime import datetime

# 날짜 형식
def format_datetime(value, format=None):
  if format is None:
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    wd = weekdays[value.weekday()]
    format = "%Y년 %m월 %d일 ({})".format(wd)
    formatted = value.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
  else:
    formatted = value.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
  return formatted