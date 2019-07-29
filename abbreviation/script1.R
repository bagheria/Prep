### Libraries
library(readxl)
library(tidytext)
library(tidyverse)

### Scripts:
source("rm_tracing_dot.R")

### Functions

# Function to match expansion with abbreviation
expand_abb <- function(word, abb_df) {
  # Check every record in the abbreviation list
  for (i in seq_len(nrow(abb_df))) {
    # If the abbreviation in abbreviation list matches the token from patientrecord:
    if (word == abb_df$abb_cor[i]) {
      # return the the abbreviation's expansion
      result = abb_df$expansion[i]
      return(result)
    }
  }
  # If no match in the abbreviation list, return the original word
  result = word
  return(result)
}

# Function to replace abbreviations in token filled dataframe
replace_abb <- function(token_df, abb_df) {
  new_df <- token_df
  for (i in seq_len(nrow(token_df))) {
    word = token_df$word[i]
    replacement <- expand_abb(word, abb_df)
    new_df$word[i] <- replacement
  }
  return(new_df)
}

# Function to keep token filled dataframe, and add abbreviation expansion information
add_expansion <- function(token_df, abb_df) {
  
  # Copy dataframe to new dataframe which will be function's output
  new_df <- token_df %>% mutate(expansion = NA, abb_cor = NA, converted = NA)
  # Loop through every token generated from patient's token_df
  for (i in seq_len(nrow(token_df))) {
    word = token_df$word[i]
    
    # Get token's expansion, if token is no abbreviation, token itself will be returned
    expansion <- expand_abb(word, abb_df)
    
    if (expansion != word) {
      new_df$expansion[i] <- expansion
      new_df$abb_cor[i] <- word
      new_df$converted[i] <- TRUE
    }
    else {
      new_df$expansion[i] <- word
      new_df$abb_cor[i] <- NA
      new_df$converted[i] <- FALSE
    }
  }
  new_df <- left_join(new_df, abb_df)
  return(new_df)
}

### Import files
records_orig <- read_excel("data/test_record1.xlsx")

abbs <- read_excel("data/Abbreviations list.xlsx") %>% 
  select(1:4) 
colnames(abbs) <- c("abbreviation", "expansion", "explanation", "extra")
# Remove all rows in which the abbreviation has no expansion yet
abbs <- abbs[!is.na(abbs$expansion), ]


# transform text into a dataframe with tokens per word
records <- records_orig %>% unnest_tokens(word, text)  #to_lower = False, can be used to keep capitalization

abbs <- replace_tracing_dot(abbs)

df1 <- replace_abb(records, abbs)

df2 <- add_expansion(records, abbs)

