library(tidyverse)
library(magrittr)


#input_dir <- "/home/robinkoch/Documents/AdventOfCode/AoC20/"
input_dir <- "/home/karlchen/Documents/AdventOfCode/AoC20/"

#puzzle 1
inp_file <- "input_1.txt"
fp = paste(input_dir, inp_file, sep = "")
numbers = read.table(fp)

# puzzle 1.1
# which 2 numbers add up to 2020?
nums <- numbers %>%
  mutate(V2 = V1) %>% 
  expand(V1,V2) %>%
  filter(V1+V2==2020) %>%
  use_series(V1) %>%
  unique()

# answer
nums[1]*nums[2]


# puzzle 1.2
nums <- numbers %>% 
  as_tibble() %>% 
  mutate(V2 = V1) %>% 
  mutate(V3 = V1) %>% 
  expand(V1, V2, V3) %>%
  filter(V1+V2+V3 == 2020) %>%
  use_series(V1) %>% 
  unique()

# answer
nums[1]*nums[2]*nums[3]

# puzzle 2
inp_file = "input_2.txt"
fp = paste(input_dir, inp_file, sep = "")
pws = read.table(fp)

df <- pws %>%
  mutate(letter= str_remove(V2, ':')) %>%
  mutate(V1= strsplit(V1, '-')) %>%
  mutate(i1 = map(V1, ~.[1])) %>%
  mutate(i2 = map(V1, ~.[2])) %>%
  mutate_at(vars(i1,i2), ~as.numeric(.)) %>%
  mutate(count = map2_dbl(V3, letter, ~str_count(.x,.y))) %>%
  select(-c(V1,V2))


# puzzle 2.1
df %>%
  mutate(right = (count >= i1) & (count <= i2)) %>%
  use_series(right) %>%
  sum


# puzzle 2.2
df %>%
  mutate(l_at_i1 = map2_chr(V3,i1, ~substr(.x,.y,.y))) %>%
  mutate(l_at_i2 = map2_chr(V3,i2, ~substr(.x,.y,.y))) %>%
  mutate(hit1 = map2_lgl(letter, l_at_i1, ~(.x ==.y))) %>%
  mutate(hit2 = map2_lgl(letter, l_at_i2, ~(.x ==.y))) %>%
  filter(xor(hit1,hit2)) %>%
  use_series(V3) %>%
  length

# puzzle 3

inp_file = "input_3.txt"
fp = paste(input_dir, inp_file, sep = "")
x = read.table(fp)

# puzzle 3.1

# puzzle 3.2



