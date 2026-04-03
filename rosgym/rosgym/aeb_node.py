import numpy as np
import rclpy
from ackermann_msgs.msg import AckermannDriveStamped
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

        self.ttc_threshold = 0.7
        self.current_velocity = 0.0

        ego_scan_topic = self.get_parameter("ego_scan_topic").value
        ego_drive_topic = self.get_parameter("ego_drive_topic").value
        ego_odom_topic = (
            self.get_parameter("ego_namespace").value
            + "/"
            + self.get_parameter("ego_odom_topic").value
        )
        self.odom_sub = self.create_subscription(
            Odometry, ego_odom_topic, self.odom_callback, 10
        )
        self.scan_sub = self.create_subscription(
            LaserScan, ego_scan_topic, self.scan_callback, 10
        )
        self.drive_pub = self.create_publisher(
            AckermannDriveStamped, ego_drive_topic, 10
        )

    def odom_callback(self, msg):
        # should be the "forwards" velocity.
        # linear.y would be lateral "slip" which isn't taken into account here.
        self.current_velocity = msg.twist.twist.linear.x

    def scan_callback(self, msg):
        if self.current_velocity <= 0:
            return

        ranges = np.array(msg.ranges)
        angles = np.arange(msg.angle_min, msg.angle_max, msg.angle_increment)

        # an object at angle theta is closing at v * cos(theta) per second.
        # objects are approaching if their radial velocity is positive.
        v_radial = self.current_velocity * np.cos(angles)

        # only consider beams where the object is coming
        # towards us (and avoid division by zero ofc)
        mask = v_radial > 0

        ittc = np.full_like(ranges, np.inf)
        ittc[mask] = ranges[mask] / v_radial[mask]

        if np.min(ittc) < self.ttc_threshold:
            self.apply_brakes()

    def apply_brakes(self):
        msg = AckermannDriveStamped()
        msg.drive.speed = 0.0
        self.drive_pub.publish(msg)
        self.get_logger().warn("!!! EMERGENCY BRAKE APPLIED !!!")


def main(args=None):
    rclpy.init(args=args)
    node = AEBNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
