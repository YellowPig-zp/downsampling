
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import threading
import settings 

cores = input()
cores = cores.split(",")
cores = [int(c) for c in cores]

def resize(img, sizd=(64,64)):
	if len(img.shape) == 3:
		img = img.transpose((1,2,0))
	img = cv.resize(img, (64,64))
	if len(img.shape) == 3:
		img = img.transpose((2,0,1))
	return img

class myThread(threading.Thread):
    def __init__(self, thread_name, images, start_index, end_index):
      threading.Thread.__init__(self)
      self.thread_name = thread_name
      self.thread_images = images[start_index:end_index]


    def run(self):
        thread_resized_imgs = []
        for i in range(len(self.thread_images)):
            img = self.thread_images[i]
            img = self.resize(img)
            thread_resized_imgs.append(edge_map)
            if i%20==0:
                print(i, len(self.thread_images), self.thread_name)
        self._return = thread_resized_imgs

    def join(self):
        threading.Thread.join(self)
        return self._return



if __name__ == "__main__":
    for batch_name in os.listdir(settings.IMAGE_PATH):
        if batch_name in os.listdir(settings.SAVED_PATH):
            print("{} already done!".format(batch_name))
            continue
        print("{} starts:".format(batch_name))
        full_filename = settings.IMAGE_PATH + batch_name
        images = np.load(full_filename)
        num_size = len(images)

        num_threads = len(cores)

        my_threads = []
        for i in range(num_threads):
            if not i == num_threads - 1:
                tmp_thread = myThread("Thread-{}".format(i+1), \
                    images, num_size//num_threads*i, num_size//num_threads*(i+1))
            else:
                tmp_thread = myThread("Thread-{}".format(i+1), \
                    images, num_size//num_threads*i, num_size)
            my_threads.append(tmp_thread)
        for idx, t in zip(cores, my_threads):
            os.system("taskset -p -c %d %d" % (idx, os.getpid()))
            t.start()

        my_thread_results = []
        for t in my_threads:
            my_thread_results.append(t.join())

        print("Exiting Main Thread")
        
        imgs_batch = []
        for result in my_thread_results:
            imgs_batch.extend(result)
        imgs_batch = np.array(imgs_batch)
        np.save(saved_directory+batch_name, imgs_batch)

        

