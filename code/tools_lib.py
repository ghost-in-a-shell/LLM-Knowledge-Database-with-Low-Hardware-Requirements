from langchain.tools import BaseTool
from typing import Union,Optional

class FreeFallHeight(BaseTool):
    name="FreeFallHeight Calculator"
    description=("用这个工具来计算一定时间内自由落体的距离"
            "The input to this tool should be a comma separated list of numbers of length two,\
             第一个数是自由落体的秒数，第二个数为单位为米每秒方的重力加速度, 例如, `1,2` 是如果你想要计算重力加速度为2m/s^2时下落1s的距离时的输入."
            )
    
    def _run(self,
        string
        ):
        print('111111111111111111111')
        if ',' in string:
            T_FALL, G = string.split(",")
        else:
            G=10
        
        return 0.5*float(G)*float(T_FALL)*float(T_FALL)