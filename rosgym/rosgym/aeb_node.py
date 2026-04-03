import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class AEBNode(Node):
    def __init__(self):
        super().__init__("aeb_node")

        # I've just copied these from gym_bridge.py for now
        # TODO: there should probably be a single source of truth.
        self.declare_parameter("ego_namespace", "ego_racecar")
        self.declare_parameter("ego_odom_topic", "odom")
        self.declare_parameter("ego_opp_odom_topic", "opp_odom")
        self.declare_parameter("ego_scan_topic", "scan")
        self.declare_parameter("ego_drive_topic", "opp_drive")

        self.get_logger().info("Hello world from AEB node")

        ego_scan_topic = (
            self.get_parameter("ego_namespace").value
            + "/"
            + self.get_parameter("ego_scan_topic").value
        )
        ego_odom_topic = (
            self.get_parameter("ego_namespace").value
            + "/"
            + self.get_parameter("ego_odom_topic").value
        )
        self.odom_sub = self.create_subscription(
            Odometry, ego_odom_topic, self.odom_callback, 10
        )
        # self.scan_sub = self.create_subscription(
        #     LaserScan, ego_scan_topic, self.scan_callback, 10
        # )

    def odom_callback(self, msg):
        # Should be the "forwards" velocity.
        # linear.y would be lateral "slip" which isn't taken into account here.
        self.current_velocity = msg.twist.twist.linear.x
        self.get_logger().info(self.current_velocity)


def main(args=None):
    rclpy.init(args=args)
    node = AEBNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
