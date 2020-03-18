import xlwt
import datetime


def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    heads = ['itemid', 'time', 'value', 'ns']
    # 将数据写入第 i 行，第 j 列
    i = 0
    for j in range(len(heads)):
        sheet1.write(i, j, heads[j])
    i = 1
    for data in datas:
        for j in range(len(data)):
            if j == 1:
                time = str(datetime.datetime.fromtimestamp(int(data[j])))
                sheet1.write(i, j, time)
            else:
                sheet1.write(i, j, data[j])
            # print(j)
        i = i + 1

    f.save(file_path)  # 保存文件


