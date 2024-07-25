#! /usr/bin/env python
"""  
    订阅 turtle1 和 turtle2 的 TF 广播信息，查找并转换时间最近的 TF 信息
    将 turtle1 转换成相对 turtle2 的坐标，在计算线速度和角速度并发布

    实现流程:
        1.导包
        2.初始化 ros 节点
        3.创建 TF 订阅对象
        4.处理订阅到的 TF
            4-1.查找坐标系的相对关系
            4-2.生成速度信息，然后发布
"""
# 1.导包
import rospy
import tf2_ros
from tf2_geometry_msgs import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped, Twist
import math

if __name__ == "__main__":
    # 2.初始化 ros 节点
    rospy.init_node("static_sub_p")
    # 3.创建 TF 订阅对象
    buffer = tf2_ros.Buffer()
    sub = tf2_ros.TransformListener(buffer)
    pub2 = rospy.Publisher("/turtle2/cmd_vel",Twist,queue_size=1000)
    pub3 = rospy.Publisher("/turtle3/cmd_vel",Twist,queue_size=1000)

    # 4.处理订阅到的 TF
    rate = rospy.Rate(100)
    # 创建速度发布对象
    while not rospy.is_shutdown():
        try:
            #def lookup_transform(self, target_frame, source_frame, time, timeout=rospy.Duration(0.0)):
            trans2 = buffer.lookup_transform("turtle2","turtle1",rospy.Time(0))
            rospy.loginfo("相对坐标:(%.2f,%.2f,%.2f)",
                        trans2.transform.translation.x,
                        trans2.transform.translation.y,
                        trans2.transform.translation.z
                        )   
            # 根据转变后的坐标计算出速度和角速度信息
            twist2 = Twist()
            # 線速度 = 係數 * 坐標系原點的間距 = 係數 * （X^2 + Y^2）再開方
            # 角速度 = 係數 * 夾角 = 係數 * atan2（Y,X）
            twist2.linear.x = 0.5 * math.sqrt(math.pow(trans2.transform.translation.x,2) + math.pow(trans2.transform.translation.y,2))
            twist2.angular.z = 4 * math.atan2(trans2.transform.translation.y, trans2.transform.translation.x)

            trans3 = buffer.lookup_transform("turtle3","turtle2",rospy.Time(0))
            rospy.loginfo("相对坐标:(%.2f,%.2f,%.2f)",
                        trans3.transform.translation.x,
                        trans3.transform.translation.y,
                        trans3.transform.translation.z
                        )   
            # 根据转变后的坐标计算出速度和角速度信息
            twist3 = Twist()
            # 線速度 = 係數 * 坐標系原點的間距 = 係數 * （X^2 + Y^2）再開方
            # 角速度 = 係數 * 夾角 = 係數 * atan2（Y,X）
            twist3.linear.x = 0.5 * math.sqrt(math.pow(trans3.transform.translation.x,2) + math.pow(trans3.transform.translation.y,2))
            twist3.angular.z = 4 * math.atan2(trans3.transform.translation.y, trans3.transform.translation.x)

            pub2.publish(twist2)
            pub3.publish(twist3)

        except Exception as e:
            rospy.logwarn("警告:%s",e)
