import cv2
import pyrealsense2
import numpy as np

point = (400, 300)


class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = pyrealsense2.pipeline()
        config = pyrealsense2.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = pyrealsense2.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(
            pyrealsense2.camera_info.product_line))

        config.enable_stream(pyrealsense2.stream.depth, 1280, 720, pyrealsense2.format.z16, 6)
        config.enable_stream(pyrealsense2.stream.color, 1280, 720, pyrealsense2.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()


def show_distance(event, x, y, args, params):
    global point
    point = (x, y)
    return(point)
    # print("Points : ", point)

if __name__=="__main__":
    # Initialize Camera Intel Realsense
    dc = DepthCamera()
    
    l=[]
    with open ("test.txt", "rt") as file:
	    for x in file:
		    l.append(x)
    counter = int(l[0])
    # Create mouse event
    cv2.namedWindow("Color frame")
    #cv2.setMouseCallback("Color frame", show_distance)
    

    while True:
        ret, depth_frame, color_frame = dc.get_frame()

        # Show distance for a specific point
        cv2.circle(color_frame, point, 4, (0, 0, 255))
        distance = depth_frame[point[1], point[0]]

        # cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        #cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        #cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)
        k = cv2.waitKey(1)
        
        if(k == ord("s")):
            img_path1 = r"F:\Debabrata_Folder\PROJECT_WORK\TULIP\Tulip Sample Code\Image_Capture\Image_Capture\image\Color_Frame\frame_{}.jpg".format(counter)
            cv2.imwrite(img_path1, color_frame)
            print(" Color frame_{}.jpg image saved".format(counter))
            #img_path2 = r"F:\Debabrata_Folder\PROJECT_WORK\TULIP\Tulip Sample Code\Image_Capture\Image_Capture\image\Depth_Frame\frame_{}.txt".format(counter)
            f = open(r"F:\Debabrata_Folder\PROJECT_WORK\TULIP\Tulip Sample Code\Image_Capture\Image_Capture\image\Depth_Frame\frame_{}.txt".format(counter), "a+")
            np.savetxt(r"F:\Debabrata_Folder\PROJECT_WORK\TULIP\Tulip Sample Code\Image_Capture\Image_Capture\image\Depth_Frame\frame_{}.txt".format(counter),depth_frame)
            #f.write(str(depth_frame))
            f.close()
            print("Depth frame_{}.txt image saved".format(counter))
            counter+=1
            file1= open("test.txt","w")
            file1.write(str(counter))
        elif(k==ord("q")):
            break
       
    cv2.destroyAllWindows()
