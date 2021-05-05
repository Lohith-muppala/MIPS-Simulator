register = [0] * 5 
register[2] = int("FA",16)
register[1] = 1 # Let's initialize 32 empty registers
mem = [0] * 259
instr = "01101100"
prog = []
prog.append(instr)
print(prog)
fetch = prog[0]
if fetch[0:3]  == '011':
    mem_loc = 4
    r_1 = int(fetch[3:5],2)
    print(r_1)
    r_2 = int(fetch[5:7],2)
    print(r_2)
    R_1 = register[r_1]
    R_2 = register[r_2]
    print(R_1)
    print(R_2)
    while (R_1 != 255):
        mult_v = R_1 * R_2
        for i in range(4):
            temp_inst = format(mult_v,'016b')
            hi = int(temp_inst[0:8],2)
            lo = int(temp_inst[8:],2)
            xor_v = hi ^ lo
            A5 = xor_v #8bits
            print(A5)
            mult_v = A5 * R_2
        c = format(A5,'08b')
        c1 = int(c[0:4],2)
        c2 = int(c[4:],2)
        c = c1 ^ c2 #4bit num
        c = format(c,'04b')
        c1 = int(c[0:2],2)
        c2 = int(c[2:],2)
        c = c1 ^ c2 #2bit num 
        mem[mem_loc] = c
        mem_loc += 1
        R_1 = R_1 + 1
        
else:
    print('Not implemented')
print('***Simulation finished***')
print('Registers $8 - $23 ', register[0:4])
print('Memory contents 0 - 259 ', mem[0:259])
