from get_txt1 import GroundTruth
from draw_gps import *
import time
import os
import csv
from python.image import load_image



def read_txt(folder_path,key_str='2014-12-02-15-30-08_comp_'):

    new_header='./part_label/'
    dic_map=dict()
    # dic_map2=dict()
    for header,j1,k1 in os.walk(folder_path):
        # print(i,j,k)
        for file_name_ori in k1:
            if ('txt' not in file_name_ori) or (key_str not in file_name_ori) or 'true_mindis' not in file_name_ori:
                continue

            # print(header+file_name_ori)

            csvFile = open(header+file_name_ori, "r")
            reader = csv.reader(csvFile)
            for item in reader:
                to_int =int(item[0].split('/')[-1].split('.')[0])
                # print(to_int,item[1])
                if to_int not in dic_map:
                    dic_map[to_int]=[item[1]]
                else:
                    dic_map[to_int].append(item[1])



    return dic_map

def dataset_to_dict(dataset):
    map_dict=dict()


def read_pic(pic_name):
    model_path='./robotcar-dataset-sdk-master/models'

    pic=load_image(pic_name)
    return pic

def main():
    folder_path='./part_label/'
    main_dataset='2014-12-02-15-30-08'
    dic_map=read_txt(folder_path,key_str=main_dataset+"_comp_")

    data_path='./'+main_dataset
    # main_data_ground_truth=read_image_dataset(data_path)
    # main_data_ground_truth.load_data(data_path)
    save_floder='./comp_imgs/'
    header='./CODE/Downloads/'
    for key in dic_map:
        print(key,dic_map[key])
        pic_day=None
        pic_night=None
        main_pic=read_pic(header + main_dataset + '/stereo/centre/' + str(key) + '.png')
        for name in dic_map[key]:
            if '2014-12' in name:
                pic_night=read_pic(header+name)
            if '2015-11' in name:
                pic_day = read_pic(header+name)
        # print(main_pic)
        plt.figure(num='show dataset',figsize=(40,20))
        plt.subplot(1, 3, 1)
        plt.title('autumn')
        plt.imshow(main_pic)

        if pic_night is not None:
            plt.subplot(1, 3, 2)
            plt.title('night')
            plt.imshow(pic_night)

        if pic_day is not None:
            plt.subplot(1, 3, 3)
            plt.title('day')
            plt.imshow(pic_day)

        plt.savefig(save_floder+str(key) + '_cmp.png')
        # plt.pause(0.01)
        # break

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