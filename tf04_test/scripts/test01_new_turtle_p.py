#! /usr/bin/env python
#1.导包
import rospy
from turtlesim.srv import Spawn, SpawnRequest, SpawnResponse

if __name__ == "__main__":
    # 2.初始化 ros 节点
    rospy.init_node("service_call_p")
    # 3.创建服务客户端
    client = rospy.ServiceProxy("/spawn",Spawn)
    # 4.組織數據發送請求

    req = SpawnRequest()
    req.x = 4.5
    req.y = 2.0
    req.theta = -3
    req.name = "turtle2"

    req3 = SpawnRequest()
    req3.x = 2.5
    req3.y = 2.0
    req3.theta = -3
    req3.name = "turtle3"

    # 6.发送请求并处理响应
    client.wait_for_service()
  
    try:
        response = client.call(req)
        rospy.loginfo("乌龟创建成功，名字是:%s",response.name)
        response3 = client.call(req3)
        rospy.loginfo("乌龟创建成功，名字是:%s",response3.name)

    except Exception as e:
        rospy.loginfo("服务调用失败....")
"""  
    调用 service 服务在窗体指定位置生成一只乌龟
    流程:
        1.导包
        2.初始化 ros 节点
        3.创建服务客户端
        4.等待服务启动
        5.创建请求数据
        6.发送请求并处理响应
"""