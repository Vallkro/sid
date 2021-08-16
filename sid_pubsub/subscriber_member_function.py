import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
import json
import os

class MinimalSubscriber(Node):

    def __init__(self):
        # Load json config
        #absolute_path = os.path.dirname(os.path.abspath(__file__))
        #file_path = os.path.join(absolute_path, 'config.json')
        homedir = os.environ['HOME']
        file_path = homedir + '/dev_ws/src/sid_pubsub/sid_pubsub/config.json'
        f =open(file_path) 
        config = json.load(f)
        f.close()
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            config['robot_command_topic'],
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()