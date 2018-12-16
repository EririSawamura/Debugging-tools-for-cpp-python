# This is for one problem and one answer mode
# The file of input: ".in"
# The file of answer: ".ans"
# The file of output: ".out"
# The name of input should be the same as the name of answer
import os


def judge_result(currect_result, user_result):
    '''对输出数据进行评测'''
    # currect_result = os.path.join("./ans.out")
    # user_result = os.path.join("./main.out")
    try:
        curr = open(currect_result).read().replace('\r','').rstrip()#删除\r,删除行末的空格和换行  
        # print(curr)
        user = open(user_result).read().replace('\r','').rstrip()  #python2中使用file函数
        # print(user)
    except:
        return False
    if curr == user:       #完全相同:AC
        return "Accepted"
    if curr.split() == user.split(): #除去空格,tab,换行相同:PE
        return "Presentation Error"
    if curr in user:  #输出多了
        return "Output limit"
    return "Wrong Answer"  #其他WA

def check(inputpath, outputpath):
    if inputpath.endswith('.in'):
        answer = inputpath.split(".")
        answer[-1] = "ans"
        answerpath = '.'.join(answer)
        if judge_result(answerpath, outputpath) == 'Accepted':
                return True
        else:
                return False
        #return filecmp.cmp(answerpath, outputpath)

def main():
    inn = input("A path end with .in: ")
    out = input("A path end with .out: ")
    print(check(inn, out))

if __name__ == "__main__":
    main()
