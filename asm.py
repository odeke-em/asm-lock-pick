#!/usr/bin/python

import sys

class Executer():
    def __init__(self):
        self.memory_size = 0xff + 1
        self.memory = [0 for i in xrange(self.memory_size)]

        self.regs = {
            'a' : 0,
            'b' : 0,
            'c' : 0,
            'x' : 0,
            'y' : 0,
            'z' : 0,
            'i' : 0,
            'j' : 0,
            'rv' : 0,
            'sp' : self.memory_size - 1,
        }

        self.next_cmd = 0
        self.execute_next = True

        def execute_mov(cmd):
            self.regs[cmd[1]] = self.get_value(cmd[2])

        def execute_add(cmd):
            self.regs[cmd[1]] += self.get_value(cmd[2])

        def execute_sub(cmd):
            self.regs[cmd[1]] -= self.get_value(cmd[2])

        def execute_mul(cmd):
            self.regs[cmd[1]] *= self.get_value(cmd[2])

        def execute_div(cmd):
            self.regs[cmd[1]] /= self.get_value(cmd[2])

        def execute_inc(cmd):
            self.regs[cmd[1]] += 1

        def execute_dec(cmd):
            self.regs[cmd[1]] -= 1

        def execute_ret(cmd):
            print self.regs['rv']

        def execute_push(cmd):
            self.memory[self.regs['sp']] = self.get_value(cmd[1])
            self.regs['sp'] -= 1

        def execute_pop(cmd):
            self.regs['sp'] += 1
            self.regs[cmd[1]] = self.memory[self.regs['sp']]

        def execute_ife(cmd):
            if not(self.get_value(cmd[1]) == self.get_value(cmd[2])):
                self.execute_next = False

        def execute_ifn(cmd):
            if not(self.get_value(cmd[1]) != self.get_value(cmd[2])):
                self.execute_next = False

        def execute_ifg(cmd):
            if not(self.get_value(cmd[1]) > self.get_value(cmd[2])):
                self.execute_next = False

        def execute_ifl(cmd):
            if not(self.get_value(cmd[1]) < self.get_value(cmd[2])):
                self.execute_next = False

        def execute_ifge(cmd):
            if not(self.get_value(cmd[1]) >= self.get_value(cmd[2])):
                self.execute_next = False

        def execute_ifle(cmd):
            if not(self.get_value(cmd[1]) <= self.get_value(cmd[2])):
                self.execute_next = False

        def execute_load(cmd):
            self.regs[cmd[1]] = self.memory[self.get_value(cmd[2])]

        def execute_save(cmd):
            self.memory[self.get_value(cmd[1])] = self.get_value(cmd[2])

        self.protos = [
            ['mov',  ['reg', 'reg|num'],     execute_mov],
            ['add',  ['reg', 'reg|num'],     execute_add],
            ['sub',  ['reg', 'reg|num'],     execute_sub],
            ['mul',  ['reg', 'reg|num'],     execute_mul],
            ['div',  ['reg', 'reg|num'],     execute_div],
            ['inc',  ['reg'],                execute_inc],
            ['dec',  ['reg'],                execute_dec],
            ['ret',  [],                     execute_ret],
            ['push', ['reg|num'],            execute_push],
            ['pop',  ['reg'],                execute_pop],
            ['ife',  ['reg|num', 'reg|num'], execute_ife],
            ['ifn',  ['reg|num', 'reg|num'], execute_ifn],
            ['ifg',  ['reg|num', 'reg|num'], execute_ifg],
            ['ifl',  ['reg|num', 'reg|num'], execute_ifl],
            ['ifge', ['reg|num', 'reg|num'], execute_ifge],
            ['ifle', ['reg|num', 'reg|num'], execute_ifle],
            ['load', ['reg', 'reg|num'],     execute_load],
            ['save', ['reg|num', 'reg|num'], execute_save],
        ]

    def is_reg(self, arg):
        return arg in self.regs.keys()

    def is_num(self, arg):
        try:
            arg = int(arg, 0)
            return 0 <= arg <= 255
        except ValueError:
            return False

    def get_value(self, arg):
        if self.is_num(arg):
            return int(arg, 0)
        elif self.is_reg(arg):
            return self.regs[arg]
        assert False

    def validate(self, proto, cmd):
        if proto[0] != cmd[0]:
            return False
        if len(proto[1]) + 1 != len(cmd):
            return False
        for i, types in enumerate(proto[1]):
            types = types.split('|')
            acceptable = False
            for type in types:
                if type == 'reg' and self.is_reg(cmd[i + 1]):
                    acceptable = True
                if type == 'num' and self.is_num(cmd[i + 1]):
                    acceptable = True
            if not(acceptable):
                return False
        return True 

    def execute_command(self, cmd):
        if not(self.execute_next):
            self.execute_next = True
            return
        for proto in self.protos:
            if self.validate(proto, cmd):
                proto[2](cmd)
                return
        print cmd
        assert False

    def execute(self, cmds):
        while self.next_cmd < len(cmds):
            self.execute_command(cmds[self.next_cmd])
            self.next_cmd += 1

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s <file>' % (sys.argv[0],)
        return
    with open(sys.argv[1], 'r+') as file:
        cmds = []
        for line in file:
            if line.lstrip()[0] == '#':
                continue
            cmd = line.split()
            cmds.append(cmd)
        executer = Executer()
        executer.execute(cmds)

if __name__ == '__main__':
    main()
