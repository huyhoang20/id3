import matplotlib.pylab as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.serif'] = ['SimHei']

decisionNode = dict(boxstyle="sawtooth", fc="0.8")

leafNode = dict(boxstyle="round4", fc="0.8")

arrow_args = dict(arrowstyle="<-")

#tạo ra từng node
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

# Xem số lá cuối cùng của cây
def getNumLeafs(myTree):
    numLeafs = 0

    # Lấy khóa đầu tiên hiện tại là node gốc
    firstStr = list(myTree.keys())[0]

    # Nhận nội dung tương ứng với khóa đầu tiên
    secondDict = myTree[firstStr]

    # Đệ quy duyệt qua các node lá
    for key in secondDict.keys():
        # Nếu nó thuộc trong mục thì gọi nó đệ quy
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        # Nếu nó không phải thì là node lá
        else:
            numLeafs += 1
    return numLeafs

#tạo độ sâu của cây
def getTreeDepth(myTree):
    maxDepth = 0

    # Lấy node gốc
    firstStr = list(myTree.keys())[0]

    # Lấy nội dung tương ứng với khóa
    secondDic = myTree[firstStr]

    # Duyệt qua các node con
    for key in secondDic.keys():
        # Nếu nó nằm trong mục thì đệ quy
        if type(secondDic[key]).__name__ == 'dict':
            # Thêm 1 độ sâu vào trong node con
            thisDepth = 1 + getTreeDepth(secondDic[key])

        # Nó là node lá trong thời điểm này
        else:
            thisDepth = 1

        # Thay đổi số lớp tối đa
        if thisDepth > maxDepth:
            maxDepth = thisDepth

    return maxDepth

#vẽ điểm giữa
def plotMidText(cntrPt, parentPt, txtString):

    # Vị trí trục X
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    # Vị trí trục Y
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    # Vẽ
    createPlot.ax1.text(xMid, yMid, txtString)

#Plot vẽ phần cây
def plotTree(myTree, parentPt, nodeTxt):

    # Tính số node lá
    numLeafs = getNumLeafs(myTree=myTree)

    # Tính độ sâu của cây
    depth = getTreeDepth(myTree=myTree)

    # Lấy thông tin của gốc
    firstStr = list(myTree.keys())[0]

    # Tính tọa độ trung tâm
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)

    # Vẽ kết nối giữa node cha với node con
    plotMidText(cntrPt, parentPt, nodeTxt)

    # Vẽ node
    plotNode(firstStr, cntrPt, parentPt, decisionNode)

    # Lấy cây con tương ứng với gốc hiện tại
    secondDict = myTree[firstStr]

    # Tính độ lệch để kéo điểm xuống
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD

    # Vòng qua tất cả các phím
    for key in secondDict.keys():
        # Nếu nó nằm trong khu thì có cây con chạy đệ quy
        if isinstance(secondDict[key], dict):
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            # Tính độ lệch để kéo xuống
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            # Vẽ các node lá
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            # Vẽ nội dung liên kết giữa node lá và node cha
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))

    # Tính độ lệch để kéo điểm xuống
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

#show ra phần hình ảnh cây
def createPlot(inTree):
    # Tạo hình ảnh
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    # Tính tổng chiều rộng của cây quyết định
    plotTree.totalW = float(getNumLeafs(inTree))
    # Tính tổng chiều sâu của cây quyết đinh
    plotTree.totalD = float(getTreeDepth(inTree))
    # Tính độ lệch x để kéo điểm xuống
    plotTree.xOff = -0.5/plotTree.totalW
    # Tính độ lệch y để kéo điểm xuống
    plotTree.yOff = 1.0
    # Gọi hàm vẽ hình node
    plotTree(inTree, (0.5, 1.0), '')
    # Hiển thị
    plt.show()

