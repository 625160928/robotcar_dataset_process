import csv
import math
import os
import numpy as np
import random
import cv2

class GroundTruth:
    def __init__(self):
        self.dis_list = []
        self.north_list = []
        self.east_list = []
        self.yaw_list = []
        self.csv_name_list = []
        self.match_dis_list = []
        self.match_north_list = []
        self.match_east_list = []
        self.match_yaw_list = []
        self.data_list = []
        self.data_list1 = []
        self.graph_file_name = []

        self.match_filename_list=[]
        self.match_file_list=[]
        self.match_time_range=5000000
        self.csv_res_list=[]
    #加载数据
    def load_data(self,path):
        gps_path=path+'gps/ins.csv'
        img_path=path+'stereo/centre'
        self.read_csv_header_and_res(gps_path)
        # for i in self.csv_name_list:
        #     print(i)
        # return

        self.match_graph_and_gps(img_path)

    def read_csv(self, csvFile_path):
        # csvFile = open("/home/pinoc/Desktop/navigation_data/2015-03-17-11-08-44/2015-03-17-11-08-44_gps/gps/ins.csv",
        #                "r")
        csvFile = open(csvFile_path,"r")
        reader = csv.reader(csvFile)
        # old=0
        # diff_count=0
        for item in reader:
            if reader.line_num == 1:
                continue
            ts=int(item[0].rstrip(' '))
            # print(ts,item,type(item))
            dis = self.cal_dis(float(item[5]), float(item[6]))
            self.dis_list.append(dis)
            self.north_list.append(float(item[5]))
            self.east_list.append(float(item[6]))
            self.yaw_list.append(float(item[14]))
            self.csv_name_list.append(ts)

        self.data_list = list(zip(self.csv_name_list, self.north_list, self.east_list, self.dis_list, self.yaw_list))

    def read_csv_header_and_res(self, csvFile_path):
        csvFile = open(csvFile_path,"r")
        reader = csv.reader(csvFile)
        # old=0
        # diff_count=0
        for item in reader:
            if reader.line_num == 1:
                # print(item)
                continue
            ts=int(item[0].rstrip(' '))
            res=item[1:]
            # print(ts,res,type(item))
            self.csv_name_list.append(ts)
            self.csv_res_list.append(res)
            # dis = self.cal_dis(float(item[5]), float(item[6]))
            # self.dis_list.append(dis)
            # self.north_list.append(float(item[5]))
            # self.east_list.append(float(item[6]))
            # self.yaw_list.append(float(item[14]))
            # self.csv_name_list.append(ts)

    def read_graph(self, path):
        # 获取所有图片的名字
        # path = "/home/pinoc/Desktop/navigation_data/2015-03-17-11-08-44/2015-03-17-11-08-44_01/stereo/centre"
        file_name_list = os.listdir(path)
        file_name = str(file_name_list)
        file_name = file_name.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        file_name = file_name.split('.png,')[:-2]
        return file_name
        # print(file_name) #['1426590796320640', '1426590753451643', '1426590907305488'...]

    def align(self, path):
        self.graph_file_name = self.read_graph(path)
        min_diff_ts=99999999999999
        for i in range(len(self.graph_file_name)):
            print(i,len(self.graph_file_name),'----------',100*i/len(self.graph_file_name))
            file=self.graph_file_name[i]
            file_ts = int(file)
            diff_list = np.array(self.csv_name_list) - np.ones_like(np.array(self.csv_name_list)) * file_ts
            # print(np.min(np.abs(diff_list)), np.argmin(np.abs(diff_list)))
            idx = np.argmin(np.abs(diff_list))
            # print(file,self.csv_name_list[idx],'---',idx,diff_list[idx])
            # if diff_list[idx]<min_diff_ts:
            #     min_diff_ts=diff_list[idx]
            # if diff_list[idx]<0:
            #     print('-----')
            #     for i in range(idx+110):
            #
            #         print(diff_list[i])
            #     break
            if abs(diff_list[idx])<self.match_time_range:
                self.match_filename_list.append(file)
                self.match_dis_list.append(self.dis_list[idx])
                self.match_yaw_list.append(self.yaw_list[idx])
                self.match_north_list.append(self.north_list[idx])
                self.match_east_list.append(self.east_list[idx])
                # break
            if i>200:
                break
        # self.data_list1 = list(zip(self.match_yaw_list))  # [('1426590796320640', 5768992.580767565, 2.762767), ('1426590753451643', 5769227.829803004, 2.342556)]
        # print('min diff ts = ',min_diff_ts)
    def match_graph_and_gps(self, path):
        self.graph_file_name = self.read_graph(path)
        for i in range(len(self.graph_file_name)):
            # if i%100==0:
            #     print(i,len(self.graph_file_name),'----------',100*i/len(self.graph_file_name))
            file=self.graph_file_name[i]
            file_ts = int(file)
            diff_list = np.array(self.csv_name_list) - np.ones_like(np.array(self.csv_name_list)) * file_ts
            idx = np.argmin(np.abs(diff_list))

            new_file=[file_ts,self.csv_name_list[idx],diff_list[idx]]+self.csv_res_list[idx]
            # print(new_file)
            self.match_file_list.append(new_file)


            # if i>200:
            #     break
    def cal_dis(self, north_value, east_value):
        dis = math.sqrt(north_value ** 2 + east_value ** 2)
        return dis

    def save_match_file_list(self,listpath):
        header=['image_name','gpstimestamp','time_diff', 'ins_status', 'latitude', 'longitude', 'altitude', 'northing', 'easting', 'down', 'utm_zone', 'velocity_north', 'velocity_east', 'velocity_down', 'roll', 'pitch', 'yaw']

        with open(listpath, 'w', newline='') as student_file:
            writer = csv.writer(student_file)
            writer.writerow(header)
            for f in self.match_file_list:
                writer.writerow(f)
