### Libraries
library(readxl)
library(tidytext)
library(tidyverse)
library(xlsx)


# Import abbreviation list
import_abbs <- function(filename) {
  df <- read_excel(paste0("data/", filename)) %>% 
    select(1:4) 
  colnames(df) <- c("abbreviation", "expansion", "explanation", "extra")
  # Rows without a present expansion will not be used for replacement
  df <- df[!is.na(df$expansion), ]
  return(df)
}

### Creates a new column in the abbreviation dataframe; 'abb_cor'
### This column coppies the abbreviations but strips them from a tracing '.'

# Sub function to actually remove the '.' from the string.
rm_tracing_dot <- function(x){
  string <- x
  # Regex: matches entire string which ends with a '.'
  pattern <- pattern <- "^.*\\.$"
  # Replaces matches with same string but last character stripped
  replacement <- substr(string, 1, nchar(string)-1)
  result <- sub(pattern = pattern, replacement = replacement, x = string)
  return(result)
}

# Function to replace abbreviation with tracing dots in string
# Necessary since 'unnest_token()' will strip tracing dots, 
# which makes matching of tokens to abbreviations impossible otherwise.
replace_tracing_dot <- function(abb_df) {
  # Initialize counter to keep track of number of changes
  counter <- 0
  new_df <- abb_df
  new_df$abb_cor <- NA
  cat("\nReplacement of tracing '.' in abbreviations dataframa has been initiated: \n\n")
  for (i in seq_len(nrow(abb_df))) {
    abb <- abb_df$abbreviation[i]
    result <- rm_tracing_dot(abb)
    if (result != abb) {
      print(paste(abb, "has been replaced to", result))
      counter <- counter + 1
    }
    new_df$abb_cor[i] <- result
  }
  cat("\n")
  cat(paste("A total number of", counter, "replacements for tracing '.' has been made.\n\n"))
  return(new_df)
}

# # Redundant:
# # Function to replace abbreviations in token filled dataframe
# replace_abb <- function(token_df, abb_df) {
#   new_df <- token_df
#   for (i in seq_len(nrow(token_df))) {
#     word = token_df$word[i]
#     replacement <- expand_abb(word, abb_df)
#     new_df$word[i] <- replacement
#   }
#   return(new_df)
# }

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

# Function to expand abbreviations in the complete unedited patient records
expand_text <- function(pat_records, abb_df) {
  # Check if the number of records between abbreviation dataframe and original records are the same
  if (all.equal(unique(pat_records$record), unique(abb_df$record))) {
    print("Patient records and abbreviation list are in accordance with each other")
  } else {
    print("Problem with number of records between patient records and abbreviation list")
    return()
  }
  
  # Only the abbreviations that were recognized in patient records are necessary to keep in and loop through
  abb_df <- abb_df %>% filter(converted == TRUE)
  
  # Go over the records one by one to change abbreviations into expansion
  for (i in seq_len(nrow(pat_records))) {
    abb_df_rec <- abb_df %>% filter(record == i)
    record <- pat_records$text[i]
    # Catch every abbreviation in the text and change it into its expansion
    for (j in seq_len(nrow(abb_df_rec))) {
      # Looking for every abbreviation in the text
      match <- paste0("(?<=\\b)", abb_df_rec$word[j], "(?=\\b)")
      match2 <- abb_df_rec$word[j]
      # replace it with the corresponding expansion
      replacement <- abb_df_rec$expansion[j]
      
      # Ignore case since abbreviation capital letter usage can be inconsistent
      change <- sub(pattern = match, replacement = replacement, x = record, ignore.case = TRUE, perl = T)
      
      # Report to user of abbreviation is not recognized in patient record
      if (change == record) {
        print("This abbreviation was not recognized:")
        print(abb_df_rec$word[j])
      }
      
      # Keep change in record variable
      record <- change
    }
    # Put edited record back into dataframe
    pat_records$text[i] <- record
  }
  return(pat_records)
}


# Import patient records
pat_records_orig <- read_excel("data/test_record1.xlsx")

# Import abbreviation list
abbs <- import_abbs("Abbreviations list.xlsx")

# Transform text into a dataframe with tokens per word
pat_records <- pat_records_orig %>% unnest_tokens(word, text)  #to_lower = False, can be used to keep capitalization

# Creates a column with abbreviations where tracing '.' are removed.
# Necessary since tracing dots were stripped from tokens (words) in unnest_token() function
abbs <- replace_tracing_dot(abbs)

# # Creates a dataframe with recordnumber and expanded tokens
# df1 <- replace_abb(pat_records, abbs)

# Creates a dataframe which gives overview of tokens, abbreviations and their expansions for curent dataset
df2 <- add_expansion(pat_records, abbs)

# Replaces abbreviations that have been recognized with their expansions in the original patient records
pat_records_exp <- expand_text(pat_records = pat_records_orig, abb_df = df2)


df2 %>% filter(converted == TRUE) %>% as.data.frame() %>% 
  write.xlsx(file = "output/attempt1_abbs.xlsx", col.names = T, row.names = F)

pat_records_exp %>% as.data.frame() %>% 
  write.xlsx(file = "output/attempt1_pat_records.xlsx", col.names = T, row.names = F)
