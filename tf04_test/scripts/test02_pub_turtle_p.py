#! /usr/bin/env python
"""  
    该文件实现:需要订阅 turtle1 和 turtle2 的 pose，然后广播相对 world 的坐标系信息

    注意: 订阅的两只 turtle,除了命名空间(turtle1 和 turtle2)不同外,
          其他的话题名称和实现逻辑都是一样的，
          所以我们可以将所需的命名空间通过 args 动态传入

    实现流程:
        1.导包
        2.初始化 ros 节点
        3.解析传入的命名空间
        4.创建订阅对象
        5.回调函数处理订阅的 pose 信息
            5-1.创建 TF 广播器
            5-2.将 pose 信息转换成 TransFormStamped
            5-3.发布
        6.spin
"""
# 1.导包
import rospy
import sys
from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
import tf2_ros
import tf_conversions


turtle_name = ""

def doPose(pose):
    # rospy.loginfo("x = %.2f",pose.x)
    #1.创建坐标系广播器
    pub = tf2_ros.TransformBroadcaster()
    #2.将 pose 信息转换成 TransFormStamped
    ts = TransformStamped()
    ts.header.frame_id = "world"
    ts.header.stamp = rospy.Time.now()

    ts.child_frame_id = turtle_name
    #可以在這邊增加烏龜數量
    #子坐標對於父坐標
    ts.transform.translation.x = pose.x
    ts.transform.translation.y = pose.y
    ts.transform.translation.z = 0.0

    qtn = tf_conversions.transformations.quaternion_from_euler(0, 0, pose.theta)
    ts.transform.rotation.x = qtn[0]
    ts.transform.rotation.y = qtn[1]
    ts.transform.rotation.z = qtn[2]
    ts.transform.rotation.w = qtn[3]

    #3.广播器发布 ts
    pub.sendTransform(ts)


if __name__ == "__main__":
    # 2.初始化 ros 节点
    rospy.init_node("dynamic_pub_p")

    # 3.解析传入的命名空间
    rospy.loginfo("-------------------------------%d",len(sys.argv))
    # 文件路徑+ 傳入的參數 +節點名稱+日誌文件路徑
    if len(sys.argv) != 4:
        rospy.loginfo("请传入参数:乌龟的命名空间")
        sys.exit(1)
    else:
        turtle_name = sys.argv[1]

    rospy.loginfo("///////////////////乌龟:%s",turtle_name)

    sub =rospy.Subscriber(turtle_name + "/pose",Pose,doPose,queue_size=100)
    #訂閱turtle1/2/3

    #     6.spin
    rospy.spin()
