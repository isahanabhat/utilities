import cv2
import argparse
import os


def check_path(path):
    if os.path.exists(path):
        return True
    return False


class VideoSnip:
    def __init__(self, video_path, dest_path, n):

        self.video_path = video_path
        self.dest_path = dest_path
        self.n = n

    def retrieve_frames(self):
        if not check_path(self.video_path):
            print("Video path does not exist")
            return

        if not check_path(self.dest_path):
            print("Folder path does not exist")
            return

        video = cv2.VideoCapture(self.video_path)

        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

        seconds = frame_count / fps
        milliseconds = round(seconds * 1000)

        start = 0
        count = 1

        # video name
        video_path_list = self.video_path.split("\\")
        video_name = video_path_list[-1].split(".")[0]
        
        while start <= milliseconds:
            video.set(cv2.CAP_PROP_POS_MSEC, start)
            start += self.n

            ret, frame = video.read()
            if ret:
                name = video_name + "_" + str(count).zfill(3)
                save_file = os.path.join(self.dest_path, name + ".jpg")
                count += 1

                cv2.imwrite(save_file, frame)
                # cv2.imshow(winname="Frame", mat=frame)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Video Snip',
        description='Get frames from your video every n milliseconds, and save to your desired path',
        epilog='Goodnight and good luck :)'
    )

    parser.add_argument('-ip', type=str, help='Video Path')
    parser.add_argument('-op', type=str, help='Frames Destination Path')
    parser.add_argument('-td', type=int, help='Time Duration (in ms)')
    args = parser.parse_args()

    if args.ip is None:
        print("-ip mandatory")
        parser.print_help()
        exit()

    if args.op is None:
        print("-op mandatory")
        parser.print_help()
        exit()

    if args.td is None:
        print("-td mandatory")
        parser.print_help()
        exit()

    obj = VideoSnip(args.ip, args.op, args.td)
    obj.retrieve_frames()