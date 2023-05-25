from get_txt1 import GroundTruth
import time

def main():
    # data_path='./CODE/Downloads/2014-05-06-12-54-54/'
    files_path=[]
    header='./CODE/Downloads/'
    files_path.append('2014-12-02-15-30-08')
    files_path.append('2014-12-10-18-10-50')
    files_path.append('2015-11-13-10-28-08')
    for data_path_ori in files_path:
        data_path=header+data_path_ori+'/'
        print('processing ',data_path)
        data1_ground_truth=GroundTruth()
        data1_ground_truth.load_data(data_path)
        data1_ground_truth.save_match_file_list('./'+data_path_ori+'.csv')
        # print(data1_ground_truth.data_list1)
        print('number of useful data is',len(data1_ground_truth.match_file_list))

if __name__ == '__main__':
    start_time=time.time()
    main()
    end_time=time.time()
    print('花费时间 ',(end_time-start_time),'s')