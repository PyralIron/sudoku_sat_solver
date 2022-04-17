import os, io
import subprocess, sys

def main():
    CNF_FILENAME = "sudoku.txt"
    RESULT_FILENAME = "results.txt"
    f = open(CNF_FILENAME,"w")
    f2 = open("prefilled.txt","r")
    size = 3
    def output_line(literals):
        s = ""
        for i in literals: s += str(i) + " "
        s += "0\n"
        f.write(s)
    def only_1(vars):
        case0 = [i for i in vars]
        output_line(case0)
        for i in range(len(vars)):
            for j in range(i+1,len(vars)):
                output_line([-vars[i],-vars[j]])
    def get_var_num(row,col,num):
        return row*81+col*9+num+1
    def unique_column(num,col):
        vars = [get_var_num(i,col,num) for i in range(9)]
        only_1(vars)
    def unique_row(num,row):
        vars = [get_var_num(row,i,num) for i in range(9)]
        only_1(vars)
    def unique_3b3(num,srow,scol):
        vars = [get_var_num(i,j,num) for i in range(srow*3,srow*3+3)
                                     for j in range(scol*3,scol*3+3)]
        only_1(vars)
    def unique_square(row,col):
        vars = [get_var_num(row,col,i) for i in range(9)]
        only_1(vars)
    def add_prefilled(row,col,num):
        output_line([get_var_num(row,col,num)])
    def read_prefilled():
        l = f2.readlines()
        l2 = [[int(j) for j in i.replace("\n","").split(" ")] for i in l]
        pfmap = {}
        for i in l2:
            pfmap[i[0]*9+i[1]] = i[2]
            add_prefilled(i[0],i[1],i[2]-1)
        for i in range(9):
            for j in range(9):
                if (i*9+j) in pfmap:
                    print(pfmap[i*9+j],end=' ')
                else:
                    print('-',end=' ')
            print("")


    def run_sat():
        prog = "cat .\\"+CNF_FILENAME +" | docker run --rm -i msoos/cryptominisat > "+RESULT_FILENAME
        subprocess.run(["powershell", "-Command", prog], capture_output=True)
        f_res = open(RESULT_FILENAME,"r",encoding="utf-16-le")
        lines = list(map(lambda x: x.replace("s","").replace("v","").replace("\n","").replace(" 0","").strip(),
                list(filter(lambda x: (x[0] == 's' or x[0] == 'v'),f_res.readlines()))))
        true_map = {}
        count = 0
        for i in lines[1:]:
            k = [int(j) for j in i.split(" ")]
            for j in k:
                if j > 0:
                    j -= 1
                    true_map[(j//9)] = j % 9
                    count += 1
        print("="*18)
        for i in range(9):
            for j in range(9):
                if (i*9+j) in true_map:
                    print(true_map[i*9+j]+1,end=' ')
                else:
                    print("_",end=" ")
            print("")

    read_prefilled()

    for i in range(9):
        for j in range(9):
            unique_column(i,j)
            unique_row(i,j)
            unique_square(i,j)
    for i in range(3):
        for j in range(3):
            for k in range(9):
                unique_3b3(k,i,j)
    run_sat()
if __name__ == '__main__':
    main()
