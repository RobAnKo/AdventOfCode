%% This is some advent of code fun!

overdir = "/home/robinkoch/Documents/AdventOfCode/AoC20";

% %puzzle 1
% fp = "input_1.txt";
% numbers = csvread(fullfile(overdir, fp));
% disp(fun_1_1(numbers));
% disp(fun_1_2(numbers));
% 
% %puzzle 2
% fp = "input_2.txt";
% passwords = readtable(fullfile(overdir, fp), 'ReadVariableNames', false);
% disp(fun_2_1(passwords));
% disp(fun_2_2(passwords));
% 
% % puzzle 3
% fp = "input_3.txt";
% mountain = read_txt(fullfile(overdir, fp));
% direction = [1,3];
% disp(fun_3_1(mountain,direction));
% disp(fun_3_2(mountain));
% 
% % puzzle 4
% fp = "input_4.txt";
% passport_data = read_txt(fullfile(overdir, fp));
% needed_keys = {'ecl','pid','eyr','hcl','byr','iyr','hgt'};
% disp(fun_4_1(passport_data, needed_keys));
% disp(fun_4_2(passport_data, needed_keys));
% 
% % puzzle 6
% fp = "input_6.txt";
% custom_q_data = read_txt(fullfile(overdir, fp));
% disp(fun_6_1(custom_q_data));
% disp(fun_6_2(custom_q_data));
% 

% %puzzle 11
% fp = "input_11.txt";
% seating = read_txt(fullfile(overdir,fp));
% disp(fun_11_1(seating));
% disp(fun_11_2(seating));

% %puzzle 12
fp = "input_17.txt";
initial_matrix = read_txt(fullfile(overdir,fp));
n = 12;
cw3d = fun_17_1(initial_matrix,n);
cw4d = fun_17_2(initial_matrix,n);



%% Functions

%helper to read text into file
function res = read_txt(fp)
    fid = fopen(fp);
    line1 = fgetl(fid);
    res=line1;
    while ischar(line1) 
        line1 = fgetl(fid);
        if ischar(line1)
            res =char(res,line1);
        end
    end
    fclose(fid);
end




% % puzzle 1.1
% function res = fun_1_1(numbers)
%     mat = numbers+numbers';
%     [x, y] = find(mat==2020,1);
%     res = (numbers(x)*numbers(y));
% end
% 
% % puzzle 1.2
% function res = fun_1_2(numbers)
%     mat = numbers+numbers'+permute(numbers, [2,3,1]);
%     [x,y,z] = ind2sub(size(mat),find(mat==2020,1));
%     res = (numbers(x)*numbers(y)*numbers(z));
% end
% 
% % puzzle 2.1
% function res = fun_2_1(passwords)
%     passwords.Properties.VariableNames{3} = 'PW';
%     range = cellfun(@(x) split(x, '-'), passwords{:,1}, 'UniformOutput', false);
%     passwords.mins = cellfun(@(x) str2double(x{1}), range);
%     passwords.maxs = cellfun(@(x) str2double(x{2}), range);
%     passwords.letters = cellfun(@(x) x(1), passwords{:,2}, 'UniformOutput', false);
%     occ = rowfun(@count, passwords(:,{'PW','letters'}));
%     passwords.occurrences = occ{:,:};
%     res = sum(passwords.occurrences >= passwords.mins & passwords.occurrences <= passwords.maxs);
% end
% 
% % puzzle 2.2
% function res = fun_2_2(passwords)
%       passwords.Properties.VariableNames{3} = 'PW';
%     range = cellfun(@(x) split(x, '-'), passwords{:,1}, 'UniformOutput', false);
%     passwords.i1 = cellfun(@(x) str2double(x{1}), range);
%     passwords.i2 = cellfun(@(x) str2double(x{2}), range);
%     passwords.letters = cellfun(@(x) x(1), passwords{:,2});
%     letter_at_i1 = rowfun(@(x,y) x{:}(y), passwords(:,{'PW', 'i1'}));
%     letter_at_i2 = rowfun(@(x,y) x{:}(y), passwords(:,{'PW', 'i2'}));
%     passwords.l_at_i1 = letter_at_i1{:,:};
%     passwords.l_at_i2 = letter_at_i2{:,:};
%     res = sum(rowfun(@(x,y,z) xor(x==y, x==z), passwords(:,{'letters','l_at_i1', 'l_at_i2'}),'OutputFormat', 'uniform'));
% end
% 
% 
% % puzzle 3.1
% function res = fun_3_1(mountain, direction)
%     path = "";
%     posy = 1 + direction(1);
%     posx = 1 + direction(2);
%     [h,w] = size(mountain);
%     while posy <= h
%         path=path+string(mountain(posy, posx));
%         posy = posy+direction(1);
%         posx = posx+direction(2);
%         if posx>w
%             posx = posx-w;
%         end
%     end
%     res = count(path, '#');
% end
% 
% % puzzle 3.2
% function res = fun_3_2(mountain)
%     directions = {[1,1],[1,3],[1,5],[1,7],[2,1]};
%     res = 1;
%     for i =1:length(directions)
%         res = res * fun_3_1(mountain, directions{i});
%     end
% end
% 
% 
% % puzzle 4.1
% function res = fun_4_1(passport_data, needed_keys)
%     res = 0;
%     ppd = string(passport_data);
%     splits = arrayfun(@(x) isempty(regexp(x, '\w', 'once')), ppd);
%     pp_string = "";
%     for i = 1:length(splits)
%         if ~splits(i)
%             pp_string = pp_string + ppd(i);
%         else
%             res = res + pp_keys_are_valid(pp_string, needed_keys);
%             pp_string = "";
%         end
%     end
% end
% 
% function valid = pp_keys_are_valid(pp_string, needed_keys)
%     valid = 0;
%     sp = split(pp_string, " ");
%     sp = arrayfun(@(x) split(x, ":"), sp(~(sp=="")), 'UniformOutput', false);
%     keys = cellfun(@(x) x{1},sp, 'UniformOutput', false);
%     if all(contains(needed_keys, keys))
%         valid = 1;
%     end
% end
% 
% 
% % puzzle 4.2
% function res = fun_4_2(passport_data, needed_keys)
%     res = 0;
%     ppd = string(passport_data);
%     splits = arrayfun(@(x) isempty(regexp(x, '\w', 'once')), ppd);
%     pp_string = "";
%     for i = 1:length(splits)
%         if ~splits(i)
%             pp_string = pp_string + ppd(i);
%         else
%             res = res + (pp_keys_are_valid(pp_string, needed_keys) & pp_values_are_valid(pp_string));
%             pp_string = "";
%         end
%     end
% end
% 
% 
% 
% function valid = pp_values_are_valid(pp_string)
%     valid = 0;
%     sp = split(pp_string, " ");
%     sp = arrayfun(@(x) split(x, ":"), sp(~(sp=="")), 'UniformOutput', false);
%     keys = cellfun(@(x) x{1}, sp, 'UniformOutput', false);
%     values = cellfun(@(x) x{2}, sp, 'UniformOutput', false);
%     valids = zeros(length(keys),1);
%     for i = 1:length(keys)
%         valids(i) = rule_function(keys{i}, values{i});
%     end
%     if all(valids)
%         valid = 1;
%     end
% end
%     
% function valid = rule_function(key, value)
%     switch key
%         case 'byr'
%             num =str2double(value);
%             valid = (length(value)==4) && (1920 <= num) && (num <= 2002);  
%         case 'iyr'
%             num =str2double(value);
%             valid = (length(value)==4) && (2010 <= num) && (num <= 2020);
%         case 'eyr'
%             num =str2double(value);
%             valid = (length(value)==4) && (2020 <= num) && (num <= 2030);
%         case 'hgt'
%             unit = regexp(value, "[a-z]*" ,'match');
%             hgt = str2double(regexp(value, "\d*", 'match'));
%             if ~isempty(unit)
%                 switch unit{:}
%                     case "cm"
%                         valid = (150 <= hgt) && (hgt <= 193);
%                     case "in"
%                         valid = (59 <= hgt) && (hgt <= 76);
%                     otherwise
%                         valid = 0;
%                 end
%             else
%                 valid = 0;
%             end
%         case 'hcl'
%             valid = startsWith(value, "#") & length(value)==7 & isempty(regexp(value(2:end), "[^0-9a-f]", 'once'));
%         case 'ecl'
%             colors = {'amb' 'blu' 'brn' 'gry' 'grn' 'hzl' 'oth'};
%             valid = length(value)==3 && any(cellfun(@(x) all(x == value), colors));
%         case 'pid'
%             valid = length(value)==9 && ~isnan(str2double(value));
%         case 'cid'
%             valid = 1;
%     end            
% end
% 
% 
% % puzzle 6.1
% 
% function res = fun_6_1(custom_q_data)
%     res = 0;
%     cqd = string(custom_q_data);
%     splits = arrayfun(@(x) isempty(regexp(x, '\w', 'once')), cqd);
%     answers = {};
%     ai = 1;
%     for i = 1:length(splits)
%         if ~splits(i)
%             answers{ai} = char(regexp(cqd(i), "\w+", 'match'));
%             ai = ai+1;
%         else
%             res = res + length(munion(answers{:}));
%             answers = {};
%             ai = 1;
%         end
%     end
% end
% 
% function U = munion(varargin)
%     % MUNION - union of multiple sets
%     % U = UNION(S1,S2,S3, ..., Sn) returns the union of sets S1 to Sn
%     U = varargin{1} ;
%     for k=2:nargin
%        U = union(U, varargin{k});
%     end
% end
% 
% % puzzle 6.2
% function res = fun_6_2(custom_q_data)
%     res = 0;
%     cqd = string(custom_q_data);
%     splits = arrayfun(@(x) isempty(regexp(x, '\w', 'once')), cqd);
%     answers = {};
%     ai = 1;
%     for i = 1:length(splits)
%         if ~splits(i)
%             answers{ai} = char(regexp(cqd(i), "\w+", 'match'));
%             ai = ai+1;
%         else
%             res = res + length(mintersect(answers{:}));
%             answers = {};
%             ai = 1;
%         end
%     end
% end
% 
% 
% 
% function I = mintersect(varargin)
%     % mintersect - intersection of multiple sets
%     % I = intersect(S1,S2,S3, ..., Sn) returns the intersect of sets S1 to Sn
%     I = varargin{1} ;
%     for k=2:nargin
%        I = intersect(I, varargin{k});
%     end
% end
% 
% 
% %puzzle 11.1
% 
% function res = fun_11_1(seating)
%     seat_matrix = seating == 'L';
%     seat_idxs = find(seat_matrix)';
%     occupation_matrix = zeros(size(seat_matrix));
%     earlier_occupation_matrix = ones(size(seat_matrix));
%     n_updates = 0;
%     while any(occupation_matrix ~= earlier_occupation_matrix,'all')
%         earlier_occupation_matrix = occupation_matrix;
%         occupation_matrix = update_occ_matrix(occupation_matrix, seat_idxs, "direct");
%         n_updates = n_updates + 1;
%     end
%     res = sum(occupation_matrix, 'all');
%     disp("We had "+n_updates+" update cycles.");
% end
% 
% function updated_occ_mat = update_occ_matrix(occ_mat, seat_idxs, type_of)
%     updated_occ_mat = occ_mat;
%     if type_of == "direct"
%         for i = seat_idxs
%             if occ_mat(i)
%                 if count_neighbours(occ_mat,i) >= 4
%                     updated_occ_mat(i) = 0;
%                 end
%             else
%                 if count_neighbours(occ_mat,i) == 0
%                     updated_occ_mat(i) = 1;
%                 end
%             end
%         end
%     elseif type_of == "sight"
%         seat_mat = zeros(size(occ_mat));
%         seat_mat(seat_idxs) = 1;
%         for i = seat_idxs
%             if occ_mat(i)
%                 if count_neighbours_sight(occ_mat,seat_mat,i) >= 5
%                     updated_occ_mat(i) = 0;
%                 end
%             else
%                 if count_neighbours_sight(occ_mat,seat_mat,i) == 0
%                     updated_occ_mat(i) = 1;
%                 end
%             end
%         end
%     end
%         
% end
% 
%     
% function n = count_neighbours(mat, i)
% %disp("count "+i+"!");
% sz = size(mat);
% [y,x] = ind2sub(size(mat),i);
% xs = (max(1,x-1):min(x+1,sz(2)));
% ys = (max(1,y-1):min(y+1,sz(1)));
% n = sum(mat(ys,xs),'all')-mat(i);
% end
% 
% 
% %puzzle 11.2
% %Basically identical to 11.1, but counting neighbours is a bit more
% %complicated
% 
% function res = fun_11_2(seating)
%     seat_matrix = seating == 'L';
%     seat_idxs = find(seat_matrix)';
%     occupation_matrix = zeros(size(seat_matrix));
%     earlier_occupation_matrix = ones(size(seat_matrix));
%     n_updates = 0;
%     while any(occupation_matrix ~= earlier_occupation_matrix,'all')
%         earlier_occupation_matrix = occupation_matrix;
%         occupation_matrix = update_occ_matrix(occupation_matrix, seat_idxs, "sight");
%         n_updates = n_updates + 1;
%     end
%     res = sum(occupation_matrix, 'all');
%     disp("We had "+n_updates+" update cycles.");
% end
% 
% 
% function n = count_neighbours_sight(occ_mat, seat_mat, i)
% %disp("count "+i+"!");
% n = 0;
% sz = size(occ_mat);
% [y,x] = ind2sub(sz,i);
% directions = {[1 0],[0 1],[-1 0],[0 -1],[1 1],[-1 -1],[1 -1],[-1 1]};
% for direction = directions
%     n = n + sight(occ_mat, seat_mat, direction{:}, [y x], sz);
% end
% end
% 
% function sighted = sight(occ_mat, seat_mat, direction, pos, mat_size)
%     sighted = 0;
%     found = 0;
%     test_pos = pos + direction;
%     while all(test_pos <= mat_size) && all(test_pos > [0,0]) && ~found
%         if seat_mat(test_pos(1),test_pos(2))
%             if occ_mat(test_pos(1),test_pos(2))
%                 sighted = 1;
%                 found = 1;
%             else
%                 sighted = 0;
%                 found = 1;
%             end
%         end
%         test_pos = test_pos + direction;
%     end
% end


%puzzle 17.1
function res = fun_17_1(initial_matrix,n)
    cw3d = Conway3D(initial_matrix);
    res = cw3d.update(n);
end


%puzzle 17.2
function res2 = fun_17_2(initial_matrix,n)
    cw4d = Conway4D(initial_matrix);
    res2 = cw4d.update(n);
end