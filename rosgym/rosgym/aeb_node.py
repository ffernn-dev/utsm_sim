import rclpy
from rclpy.node import Node


class AEBNode(Node):
    def __init__(self):
        super().__init__("aeb_node")
        self.get_logger().info("Hello world from AEB node")


def main(args=None):
    rclpy.init(args=args)
    node = AEBNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
