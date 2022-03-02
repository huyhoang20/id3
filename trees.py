import collections
from math import pow
import operator


#tạo dữ liệu đầu vào
def create_dataset():
    dataset = [['nam', '0', 'rẻ', 'thấp', 'bus'],
               ['nam', '1', 'rẻ', 'trung bình', 'bus'],
               ['nữ', '0', 'rẻ', 'thấp', 'bus'],
               ['nam', '1', 'rẻ', 'trung bình', 'bus'],
               ['nữ', '1', 'đắt', 'cao', 'oto'],
               ['nam', '2', 'đắt', 'trung bình', 'oto'],
               ['nữ', '2', 'đắt', 'cao', 'oto'],
               ['nữ', '1', 'rẻ', 'trung bình', 'tàu'],
               ['nam', '0', 'tiêu chuẩn', 'trung bình', 'tàu']]

    labels = ['giới tính', 'sở hữu mấy xe', 'chi phí', 'mức thu nhập', 'loại xe']

    labels_full = {}

    for i in range(len(labels)):
        label_list = [example[i] for example in dataset] # Đếm các dữ liệu chuẩn đầu ra
        unique_label = set(label_list) # chia kết quả nó ra thành mảng ko trùng lặp
        labels_full[labels[i]] = unique_label #tổng quát tất cả mảng chia nó ra

    return dataset, labels, labels_full

#Tính phần hệ số gini
def calc_gini_index(dataset):
    num_entries = len(dataset) # đếm số dữ liệu đầu vào
    label_counts = collections.defaultdict(int)  # đếm số dữ liệu đầu vào những tách độ giống nhau

    for feature_vec in dataset:
        current_label = feature_vec[-1] #dữ liệu cuối cùng của kết quả
        label_counts[current_label] += 1 #đếm dữ liệu cuối cùng

    gini_index = 1.0

    for key in label_counts:
        prob = float(label_counts[key]) / num_entries #Tính tỉ lệ của từng phần trong dữ liệu
        gini_index -= pow(prob, 2)

    return gini_index

#tính phần hệ số gini
def calc_delta_gini(dataset, feature_list, i, base_gini):
    unique_values = set(feature_list) # Lấy dữ liệu đầu vào đầu tiên
    new_gini = 1.0

    for value in unique_values:
        sub_dataset = split_dataset(dataset=dataset, axis=i, value=value) # cắt phần dữ liệu chia nó thành 4 mảng
        prob = len(sub_dataset) / float(len(dataset)) # tỉ lệ của số lượng dữ liệu chia mảng với tổng số lượng data
        new_gini -= prob * calc_gini_index(sub_dataset)

    delta_gini = base_gini - new_gini

    return delta_gini





#tính phần hệ số gini với mỗi thuộc tính
def calc_gini_gain_for_series(dataset, i, base_gini):
    best_delta_gini = 0.0
    best_split_point = -1

    feature_list = [example[i] for example in dataset] # Lấy dữ liệu đầu tiên của cột data
    class_list = [example[-1] for example in dataset] # Lấy dữ liệu cuối của cột data
    dict_list = dict(zip(feature_list, class_list)) #Thêm nó vào dạng thư viện

    sorted_feature_list = sorted(dict_list.items(), key=operator.itemgetter(0)) #Cho vào trong các tập
    num_feature_list = len(sorted_feature_list) # đếm số lượng các tập
    split_point_list = [round((sorted_feature_list[i][0] + sorted_feature_list[i + 1][0]) / 2.0, 3) for i in
                        range(num_feature_list - 1)]

    # tính toán mức tăng thông tin của mỗi điểm phân chia
    for split_point in split_point_list:
        elt_dataset, gt_dataset = split_dataset_for_series(dataset, i, split_point)
        #Tính số lượng của từng tệp đã nhận
        new_gini = len(elt_dataset) / len(sorted_feature_list) * calc_gini_index(elt_dataset) \
            + len(gt_dataset) / len(sorted_feature_list) * calc_gini_index(gt_dataset)

        delta_gini = base_gini - new_gini
        if delta_gini < best_delta_gini:
            best_split_point = split_point
            best_delta_gini = delta_gini

    return best_delta_gini, best_split_point




#chọn ra hàm tối ưu
def choose_best_feature_to_split(dataset):
    num_features = len(dataset[0]) - 1
    base_gini = calc_gini_index(dataset)
    best_delta_gini = 1.0
    best_feature = -1
    flag_series = 0
    best_split_point = 0.0
    new_split_point = 0.0

    for i in range(num_features):
        feature_list = [example[i] for example in dataset] #Lấy dữ liệu của phần 3
        if isinstance(feature_list[0], str):
            delta_gini = calc_delta_gini(dataset, feature_list, i, base_gini)
        else:
            delta_gini, new_split_point = calc_gini_gain_for_series(dataset, i, base_gini)

        if delta_gini < best_delta_gini:
            best_delta_gini = delta_gini
            best_feature = i
            flag_series = 0

            if not isinstance(dataset[0][best_feature], str):
                flag_series = 1
                best_split_point = new_split_point

    if flag_series:
        return best_feature, best_split_point
    else:
        return best_feature



# cắt các dữ liệu theo cột
def split_dataset_for_series(dataset, axis, value):
    elt_dataset = []
    gt_dataset = []

    for feature in dataset:
        if feature[axis] <= value:
            elt_dataset.append(feature)
        else:
            gt_dataset.append(feature)

    return elt_dataset, gt_dataset

# cắt dữ liệu theo data
def split_dataset(dataset, axis, value):
    ret_dataset = []

    for feature_vec in dataset:
        if feature_vec[axis] == value:
            reduced_vec = feature_vec[:axis]
            reduced_vec.extend(feature_vec[axis + 1:])
            ret_dataset.append(reduced_vec)

    return ret_dataset


#tìm ra nhánh chính
def majority_count(class_list):
    class_count = collections.defaultdict(int)

    for vote in class_list:
        class_count[vote] += 1

    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_class_count[0][0]



#tạo ra cây
def create_tree(dataset, labels):
    class_list = [example[-1] for example in dataset]

    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    # Nếu cây chỉ có 1 nhánh duy nhất
    if len(dataset[0]) == 1:
        return majority_count(class_list)

    best_feature = choose_best_feature_to_split(dataset=dataset)

    split_point = 0.0

    # Nếu nó là mức tối ưu nhất thì cứ tiếp tục
    if isinstance(best_feature, tuple):
        best_feature_label = str(labels[best_feature[0]]) + '<' + str(best_feature[1])
        split_point = best_feature[1]
        best_feature = best_feature[0]
        flag_series = 1
    else:
        best_feature_label = labels[best_feature]
        flag_series = 0

    my_tree = {best_feature_label: {}}

    feature_values = [example[best_feature] for example in dataset]

    # Xử lí giá trị liên tục
    if flag_series:
        elt_dataset, gt_dataset = split_dataset_for_series(dataset, best_feature, split_point)
        sub_labels = labels[:]
        sub_tree = create_tree(elt_dataset, sub_labels)
        my_tree[best_feature_label]['<'] = sub_tree

        sub_tree = create_tree(gt_dataset, sub_labels)
        my_tree[best_feature_label]['>'] = sub_tree

        return my_tree

    # Xử lí giá trị rời rạc
    else:
        del (labels[best_feature])
        unique_values = set(feature_values)
        for value in unique_values:
            sub_labels = labels[:]
            sub_tree = create_tree(split_dataset(dataset=dataset, axis=best_feature, value=value), sub_labels)
            my_tree[best_feature_label][value] = sub_tree
        return my_tree



#giải phần cần tìm trong đầu tìm
def classify(input_tree, feature_labels, feature_label_properties, test_vec):
    first_str = list(input_tree.keys())[0]
    first_label = first_str
    less_index = str(first_str).find('<')
    # print(less_index)
    if less_index > -1:  # Nếu nó là 1 tính năng liên tục
        first_label = str(first_str)[:less_index]
        # print("first_label", first_label)
    second_dict = input_tree[first_str]
    feature_index = feature_labels.index(first_label)  # Các tính năng ứng với các node
    # print(second_dict)
    class_label = None
    for key in second_dict.keys():  # Vòng lặp cho mỗi nhánh
        if feature_label_properties[feature_index] == 0:  # Các tính năng rời rạc
            if test_vec[feature_index] == key:  # Các mẫu thử nghiệm tính năng rời rạc nhập vào 1 nhánh
                if type(second_dict[key]).__name__ == 'dict':  # Nhánh không phải node lá thì đệ quy
                    class_label = classify(second_dict[key], feature_labels, feature_label_properties, test_vec)
                else:  # Nếu là node lá thì trả về kết quả
                    class_label = second_dict[key]
        else:
            split_point = float(str(first_str)[less_index + 1:])
            if test_vec[feature_index] < split_point:  # Nhập cây con phía bên trái
                if type(second_dict['<']).__name__ == 'dict':  # Nhánh không phải node lá thì đệ quy
                    class_label = classify(second_dict['<'], feature_labels, feature_label_properties, test_vec)
                else:  # Nếu là node thì trả về kết quả
                    class_label = second_dict['<']
            else:
                if type(second_dict['>']).__name__ == 'dict':  # Nhánh không phải node lá thì đệ quy
                    class_label = classify(second_dict['>'], feature_labels, feature_label_properties, test_vec)
                else:  # Nếu là lá thì trả về kết quả
                    class_label = second_dict['>']

    return class_label
