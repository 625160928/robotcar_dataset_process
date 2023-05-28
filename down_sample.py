from get_txt1 import GroundTruth
import time
import os
import csv

def down_sample_txt(folder_path,down_sample_rate=0.1):

    new_header='./part_label/'

    skip_number=int(1/down_sample_rate)
    for header,j1,k1 in os.walk(folder_path):
        # print(i,j,k)
        for file_name_ori in k1:
            if 'csv' not in file_name_ori:
                continue
            content=[]
            print(header+file_name_ori)

            csvFile = open(header+file_name_ori, "r")
            reader = csv.reader(csvFile)
            count=0
            for item in reader:
                count+=1
                # if reader.line_num == 1:
                #     continue
                if count%skip_number==0:
                    # print(count,item,type(item))
                    content.append(item)
            name=new_header+file_name_ori.split('.')[0]
            print(name)
            with open(name + '.txt', 'w') as f:
                for l in content:
                    f.write(str(l[0]) + ',' + str(l[1]) + ',' + str(l[2]) + '\n')
            # break
def main():
    folder_path='./label/'
    down_sample_txt(folder_path)
    # data_path='./CODE/Downloads/2014-05-06-12-54-54/'
    # files_path=[]
    # header='./CODE/Downloads/'
    # files_path.append('2014-12-02-15-30-08')
    # files_path.append('2014-12-10-18-10-50')
    # files_path.append('2015-11-13-10-28-08')
    # for data_path_ori in files_path:
    #     data_path=header+data_path_ori+'/'
    #     print('processing ',data_path)
    #     data1_ground_truth=GroundTruth()
    #     data1_ground_truth.load_data(data_path)
    #     data1_ground_truth.save_match_file_list('./'+data_path_ori+'.csv')
    #     # print(data1_ground_truth.data_list1)
    #     print('number of useful data is',len(data1_ground_truth.match_file_list))

if __name__ == '__main__':
    start_time=time.time()
    main()
    end_time=time.time()
    print('花费时间 ',(end_time-start_time),'s')