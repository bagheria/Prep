### Libraries
library(readxl)
library(tidytext)
library(tidyverse)

### Scripts:
source("rm_tracing_dot.R")
source("replace_ab_in_text.R")
source("abb_df_functions.R")

### Import files
# Import patien records
pat_records_orig <- read_excel("data/test_record1.xlsx")

# Import abbreviation list
abbs <- read_excel("data/Abbreviations list.xlsx") %>% 
  select(1:4) 
colnames(abbs) <- c("abbreviation", "expansion", "explanation", "extra")
# Rows without a filled in expansion will not be used
abbs <- abbs[!is.na(abbs$expansion), ]

# Transform text into a dataframe with tokens per word
pat_records <- pat_records_orig %>% unnest_tokens(word, text)  #to_lower = False, can be used to keep capitalization

# Creates a column with abbreviations where tracing '.' are removed.
# Necessary since tracing dots were stripped from tokens (words) in unnest_token() function
abbs <- replace_tracing_dot(abbs)

# # Creates a dataframe with recordnumber and expanded tokens
# df1 <- replace_abb(pat_records, abbs)

# Creates a dataframe which gives overview of tokens, abbreviations and their expansions
df2 <- add_expansion(pat_records, abbs)

# Replaces abbreviations that have been recognized with their expansions in the original patient records
pat_recrods_exp <- expand_text(pat_records = pat_records_orig, abb_df = df2)

