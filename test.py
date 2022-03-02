from trees import *
from plot_tree import *

if __name__ == '__main__':
    data_set, labels, labels_full = create_dataset()
    my_tree = create_tree(data_set, labels)
    print(my_tree)

    test_dataset = [['nữ', '1', 'tiêu chuẩn', 'trung bình']]
    test_labels = ['giới tính', 'sở hữu mấy xe', 'chi phí', 'mức thu nhập', 'loại xe']
    test_label_properties = [0, 0, 0, 0, 0, 0]
    for vec in test_dataset:
        test_result = classify(my_tree, test_labels, test_label_properties, vec)
        print("Kết quả người ta đi : ",test_result)

    createPlot(my_tree)

