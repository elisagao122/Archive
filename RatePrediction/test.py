# encoding=utf-8
import os
import numpy as np
from db_preprocess import db_result
from db_preprocess import get_column_statistic
from db_preprocess import feature_extraction
from db_preprocess import get_db_list
from rate_prediction import rate_predict
from log_preprocess import walk_dir
from export_pay_rej import pay_rej
from log_feature import get_log_list
from log_feature import single_log_feature
from log_feature import log_feature_discretize
from log_feature import log_feature_walk_dir
from match_db_log import match_feature
#from cross_validation import stat_ida_before_date

# step 1:
# 订单信息
db_path = 'data/research_refuse.gorders'
# 订单信息从db_path里面export部分信息
pay_rej_path = 'parsing/db_pay_rej.txt'
# no??
pay_rej(db_path, pay_rej_path, 'no')
print '(1/6) Finished export the database log with label buy and reject'

# step 2:
# db_list = db_result(pay_rej_path)
# print get_column_statistic(db_path, 2)
# convert db file to nest lists
db_list = get_db_list(pay_rej_path)
feature_list = feature_extraction(db_list)
print '(2/6) Finished extract database feature'


# step 3:
log_path = 'data/nginx_logs/'
#walk_dir(log_path)
print '(3/6) Finished parsing raw log'

# step 4:
parsing_result_path = 'parsing/'
#log_feature_walk_dir(parsing_result_path)
print '(4/6) Finished extract log feature'

# step 5:
log_feature_path = 'log_feature/'
#final_feature = match_feature(feature_list, log_feature_path)
#np.savetxt('final_feature_with_cancel.txt', np.array(final_feature), delimiter = ',', fmt = '%s')
print '(5/6) Finished match log and databese feature'

# step 6:

# Debug:
final_feature = get_db_list('final_feature_with_cancel.txt')
#print final_feature
train = []
train_label = []
test = []
test_label = []
for i in range(len(final_feature)):
    if i < len(final_feature) * 2 / 3:
        train_label.append(int(final_feature[i][0]))
        #train.append(final_feature[i][3:])
        train.append([float(m) for m in final_feature[i][3:]])
    elif i >= len(final_feature) * 2 / 3 and final_feature[i][0] in ['0', '1']:
        test_label.append(int(final_feature[i][0]))
        #test.append(final_feature[i][3:])
        test.append([float(m) for m in final_feature[i][3:]])

rate_predict(train, train_label, test, test_label)
print '(6/6) Job done!'





