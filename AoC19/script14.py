from collections import defaultdict
import fileinput
import re

PATTERN = re.compile(r'(\d+) (\w+)')
MAX = 1_000_000_000_000


def parse(lines):
    rules = {}
    for line in lines:
        srcs, last = {}, None
        for match in PATTERN.finditer(line):
            if last is not None:
                key, n = last
                srcs[key] = n
            last = match.group(2), int(match.group(1))
        key, n = last
        rules[key] = n, srcs
    return rules


def produce(rules, quantity):
    mats = defaultdict(int)
    mats['FUEL'] = quantity
    runs = 0
    try:
        while True:
            key, n = next(
                #find stuff to produce if it is not ORE and needed (n>0)
                (key, n) for key, n in mats.items() if key != 'ORE' and n > 0) 
            m, srcs = rules[key]
            x = (n + m - 1) // m            #is equivalent to ceil(n/m)
            mats[key] -= m * x    #we just produced material <key> so we can remove it from the list of needs
            for k, v in srcs.items(): #but now we have to add the needs of the reactions below
                mats[k] += x * v
    except StopIteration as e:
        pass
    return mats['ORE']



def part2(lines):
    '''
    >>> part2("157 ORE => 5 NZVS;165 ORE => 6 DCFZ;44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL;12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ;179 ORE => 7 PSHF;177 ORE => 5 HKGWZ;7 DCFZ, 7 PSHF => 2 XJWVT;165 ORE => 2 GPVTF;3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT".split(";"))
    82892753
    >>> part2("2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG;17 NVRVD, 3 JNWZP => 8 VPVL;53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL;22 VJHF, 37 MNCFX => 5 FWMGM;139 ORE => 4 NVRVD;144 ORE => 7 JNWZP;5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC;5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV;145 ORE => 6 MNCFX;1 NVRVD => 8 CXFTF;1 VJHF, 6 MNCFX => 4 RFSQX;176 ORE => 6 VJHF".split(";"))
    5586022
    >>> part2("171 ORE => 8 CNZTR;7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL;114 ORE => 4 BHXH;14 VRPVC => 6 BMBT;6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL;6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT;15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW;13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW;5 BMBT => 4 WPTQ;189 ORE => 9 KTJDG;1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP;12 VRPVC, 27 CNZTR => 2 XDBXC;15 KTJDG, 12 BHXH => 5 XCVML;3 BHXH, 2 VRPVC => 7 MZWV;121 ORE => 7 VRPVC;7 XCVML => 6 RJRHP;5 BHXH, 4 VRPVC => 5 LTCX".split(";"))
    460664
    '''
    rules = parse(lines)
    #how many runs of production can we do 
    #given the price calculated in 1 and the maximum amount of ore we have
    good, bad = MAX // produce(rules, 1), None 
    #binary search
    while bad is None or good < bad - 1:
        #try twice the amount 
        if bad is None:
            quantity = 2 * good 
        #then try the middle between what works and what doesnt work
        else:
            quantity = (good + bad) // 2
        ores = produce(rules, quantity)
        if ores < MAX: #works -> we can shift the working amount up to quantity
            good = quantity
        elif ores > MAX: #too much -> reduce the upper limit down to this quantity
            bad = quantity
        else:
            return mid
    return good


inputfile = "Input_14.txt"
lines = open(inputfile).readlines()
rules = parse(lines)
production = produce(rules,1)
part2_ = part2(lines)
print(f"Solution to puzzle 14.1:\n {production}")
