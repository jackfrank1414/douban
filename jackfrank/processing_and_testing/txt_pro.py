from jackfrank.utils.txt_utils import reserve_chinese
from jackfrank.utils.txt_utils import read_name

def clear_txt(list):
    for i in range(10):
        name = list[i]
        path = './t/' + str(name) + '.txt'
        fp1 = open('./coms/' + str(name) + '.txt','r',encoding='utf-8')
        lines = fp1.readlines()
        with open('./t/' + str(name) + '.txt','a',encoding='utf-8') as fp2:
            for line in lines:
                if line !='\n':
                    line = reserve_chinese(line)
                    fp2.write(line + '\n')
            print(name)
            fp1.close()
            fp2.close()

if __name__ == '__main__':
    list = read_name()
    clear_txt(list)
    print("success!")
