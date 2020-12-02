library(dplyr, warn.conflicts = FALSE)
library(purrr)

input_dir <- "/home/robinkoch/Documents/AdventOfCode/AoC20/"

#puzzle1.1
inp_file <- "input_1.txt"
fp = paste(input_dir, inp_file, sep = "")
numbers <- read.table(fp)

numbers %>% as_vector() %>%

numbers_t <- t(numbers)

