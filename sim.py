def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)        
    return val       
def sim(program):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 4   # Let's initialize 32 empty registers
    mem = [0] * 260    # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
    DIC = 0 # Dynamic Instr Count
    spl_reg = [0] * 4 # like LO and HI they are special registers that incerement the count
    Count = 0
    while(not(finished)):
        if PC == 0:
            fetch = program[PC]
            register[2] = int(fetch,2)
            PC += 1
        if PC == len(program) - 1: 
            finished = True
        fetch = program[PC]
        DIC += 1
        #print(hex(int(fetch,2)), PC)
        
        if ((fetch[0:2]  == '11')&(fetch[2:4] != '00')): #11011011
            r_1 = int(fetch[2:4],2)
            r_2 = int(fetch[4:6],2)
            r_3 = int(fetch[6:],2)
            R_1 = register[r_1]
            R_2 = register[r_2]
            mem_loc = register[r_3]
            mult_v = R_1 * R_2
            temp_inst = format(mult_v,'016b')
            hi = int(temp_inst[0:8],2)
            lo = int(temp_inst[8:],2)
            xor_v = hi ^ lo
            A5 = xor_v #8bits
            for i in range(4):
                mult_v = A5 * R_2
                temp_inst = format(mult_v,'016b')
                hi = int(temp_inst[0:8],2)
                lo = int(temp_inst[8:],2)
                xor_v = hi ^ lo
                A5 = xor_v #8bits            print(A5)
            c = format(A5,'08b')
            c1 = int(c[0:4],2)
            c2 = int(c[4:],2)
            c = c1 ^ c2 #4bit num
            c = format(c,'04b')
            c1 = int(c[0:2],2)
            c2 = int(c[2:],2)
            c = c1 ^ c2 #2bit num 
            mem[mem_loc] = c
            PC += 1
            
        elif(fetch[0:2] == '01'): #load into 01 01(mem index) 10(stored in to the reg) XX
            #print("Load")
            r_1 = int(fetch[2:4],2)
            r_2 = int(fetch[4:6],2)
            register[r_2] = mem[register[r_1]]
            PC += 1
        
        elif (fetch[0:4] == "0000"):# loop index
            L_pc = PC
            L_Val = int(fetch[4:],2)
            #print(L_pc)
            PC += 1
        
        elif (fetch[0:2] == '00'): # 00 11 XXXX
            #match 
            r_1 = int(fetch[2:4],2)
            val = register[r_1] #start location
            if(val == 0):
                spl_reg[0] += 1
            elif(val == 1):
                spl_reg[1] += 1
            elif(val == 2):
                spl_reg[2] += 1
            elif(val == 3):
                spl_reg[3] += 1
            mem[0] = spl_reg[0]
            mem[1] = spl_reg[1]
            mem[2] = spl_reg[2]
            mem[3] = spl_reg[3]
            PC += 1
        
        elif (fetch[0:4] == "1100"): #BNZ
            #print("BNZ")
            r_1 = int(fetch[4:6],2)
            if( register[r_1] != 4):
                PC = L_pc + 1
                #print(PC)
            else:
                PC += 1
                
        elif (fetch[0:2] == "10"): #addi 10 R1 imm
            r_1 = int(fetch[2:4],2)
            sign_check = fetch[4:]
            if(sign_check[0] == "1"):
                imm = twos_comp(int(sign_check,2), len(sign_check))
            else:
                imm = int(sign_check,2)
            register[r_1] = register[r_1] + imm 
            PC += 1
            
        else:
            # This is not implemented on purpose
            print('Not implemented')

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')
    print('Registers $0 - $3 ', register[0:4])
    print('Special Registers $0 - $3 ', spl_reg[0:4])
    print('Dynamic Instr Count ', DIC)
    for i in range(260):
        print('Memory contents M['+ str(i) +'] = '+ str (mem[i]))
    

def main():
    read_f = open('mc.txt','r')
    file = read_f.readlines()
    program = []
    for line in file:
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)
        if line[0] == '\n':
            continue
        line = line.replace('\n','')
        instr = line[2:]
        instr = int(instr,16)
        instr = format(instr,'08b')
        program.append(instr)       
    sim(program)     

if __name__ == '__main__':
    main()