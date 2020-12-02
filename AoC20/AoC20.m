%% This is some advent of code fun!

overdir = "/home/robinkoch/Documents/AdventOfCode/AoC20";

%puzzle 1
fp = "input_1.txt";
numbers = csvread(fullfile(overdir, fp));
disp(fun_1_1(numbers));
disp(fun_1_2(numbers));

%puzzle 2
fp = "input_2.txt";
passwords = readtable(fullfile(overdir, fp), 'ReadVariableNames', false);
disp(fun_2_1(passwords));
disp(fun_2_2(passwords));

%puzzle 3



%% Functions

%puzzle 1.1
function res = fun_1_1(numbers)
    mat = numbers+numbers';
    [x, y] = find(mat==2020,1);
    res = (numbers(x)*numbers(y));
end

%puzzle 1.2
function res = fun_1_2(numbers)
    mat = numbers+numbers'+permute(numbers, [2,3,1]);
    [x,y,z] = ind2sub(size(mat),find(mat==2020,1));
    res = (numbers(x)*numbers(y)*numbers(z));
end

%puzzle 2.1
function res = fun_2_1(passwords)
    passwords.Properties.VariableNames{3} = 'PW';
    range = cellfun(@(x) split(x, '-'), passwords{:,1}, 'UniformOutput', false);
    passwords.mins = cellfun(@(x) str2double(x{1}), range);
    passwords.maxs = cellfun(@(x) str2double(x{2}), range);
    passwords.letters = cellfun(@(x) x(1), passwords{:,2}, 'UniformOutput', false);
    occ = rowfun(@count, passwords(:,{'PW','letters'}));
    passwords.occurrences = occ{:,:};
    res = sum(passwords.occurrences >= passwords.mins & passwords.occurrences <= passwords.maxs);
end

%puzzle 2.2
function res = fun_2_2(passwords)
      passwords.Properties.VariableNames{3} = 'PW';
    range = cellfun(@(x) split(x, '-'), passwords{:,1}, 'UniformOutput', false);
    passwords.i1 = cellfun(@(x) str2double(x{1}), range);
    passwords.i2 = cellfun(@(x) str2double(x{2}), range);
    passwords.letters = cellfun(@(x) x(1), passwords{:,2});
    letter_at_i1 = rowfun(@(x,y) x{:}(y), passwords(:,{'PW', 'i1'}));
    letter_at_i2 = rowfun(@(x,y) x{:}(y), passwords(:,{'PW', 'i2'}));
    passwords.l_at_i1 = letter_at_i1{:,:};
    passwords.l_at_i2 = letter_at_i2{:,:};
    res = sum(rowfun(@(x,y,z) xor(x==y, x==z), passwords(:,{'letters','l_at_i1', 'l_at_i2'}),'OutputFormat', 'uniform'));
end


