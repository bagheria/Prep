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
  cat("\nImport of abbreviation list is completed")
  return(df)
}

### Creates a new column in the abbreviation dataframe
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

  cat("\nDataframe with tokens (words) is being scanned for known abbreviations...\nThis can take some time\n")

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
  # Create an overview of every token with its abbreviation list information if present
  new_df <- left_join(new_df, abb_df)
  # Count the number of conversions: abbreviation -> expansion
  nr_conv <- new_df %>% filter(converted == TRUE) %>% nrow()
  cat("\nScan for abbreviations is completed.\n")
  print(paste("Total number of tokens (words) that have been converted from abbreviated to expanded form is: ", nr_conv))
  return(new_df)
}

# Function to expand abbreviations in the complete unedited patient records
expand_text <- function(pat_records, token_df) {
  mismatch_counter <- 0
  cat("\nReplacement of abbreviations to expansions in patient records is initiaded\n")
  # Check if the number of records between abbreviation dataframe and original records are the same
  if (all.equal(unique(pat_records$record), unique(token_df$record))) {
    cat("\nPatient records and generated abbreviation dataframe are in accordance with each other\n")
  } else {
    cat("\nProblem with number of records between patient records and abbreviation list\n")
    return()
  }

  # Only the abbreviations that were recognized in patient records are necessary to keep in and loop through
  # All tokens that were not recognized as abbreviations can be filtered out:
  token_df <- token_df %>% filter(converted == TRUE)

  # Go over the records one by one to change abbreviations into expansion
  for (i in seq_len(nrow(pat_records))) {

    # Select the abbreviations from the token dataframe for the record that is currently looped over
    record_nr <- pat_records$record[i]
    token_df_rec <- token_df %>% filter(record == record_nr)

    # Select the record from patients record that needs to be changed
    record <- pat_records$text[i]

    # Loop over every known abbreviation from the current patient record, and change it into its expansion
    for (j in seq_len(nrow(token_df_rec))) {

      # Creating a regex pattern to match the current abbreviation that is looked for
      # "(?i)" is case insensitivity flag. (\\W) are non-word character lookarounds (behind and ahead) (\\b) is word bounary
      match <- paste0("(?i)(?<=(\\W)|(\\b))", token_df_rec$word[j], "(?=(\\W)|(\\b))")

      # replacement is the corresponding expansion from the token dataframe
      replacement <- token_df_rec$expansion[j]
      #print(paste("replacement:", replacement))

      # Ignore case since abbreviation capital letter usage can be inconsistent
      change <- str_replace(pattern = match, replacement = replacement, string = record)
      #print(paste("change", change))

      # Report to user if the abbreviation was not recognized in the record during this instance of the loop
      found_match <- str_detect(string = record, pattern = match)
      #print(found_match)
      if (found_match == FALSE) {
        mismatch_counter <- mismatch_counter + 1
        print("This abbreviation was not recognized in the patient record: ")
        print(paste("abb:", token_df_rec$word[j], "to expansion:", replacement, "in record:", token_df_rec$record[j]))
      }

      # Keep change in record variable
      record <- change
    }
    # Put edited record back into dataframe
    pat_records$text[i] <- record
  }

  if (mismatch_counter > 0) {
    cat("\nSome abbreviations could not be replaced:\n")
    print(paste("Number of mismatches:", mismatch_counter))
  }
  else {
    cat("\nAll identified abbreviations were replaced by their abbreviations.\n")

  }
  cat("\nAbbreviation replacement has been completed.\n")
  return(pat_records)
}


# Import patient records
pat_records_orig <- read_excel("data/Datadump_martijnedit.xlsx") %>% na.omit() # %>% filter(record == 490)

# Import abbreviation list
abb_df <- import_abbs("Abbreviations list.xlsx")

# Transform text into a dataframe with tokens per word
token_df <- pat_records_orig %>% unnest_tokens(word, text) #to_lower = False, can be used to keep capitalization

# pat_records[unique(unlist(lapply(pat_records, function(x) which(is.na(x))))), 1]
# pat_records <- pat_records %>% na.omit()

# Creates a column with abbreviations where tracing '.' are removed.
# Necessary since tracing dots were stripped from tokens (words) in unnest_token() function
abb_df <- replace_tracing_dot(abb_df)

# # Creates a dataframe with recordnumber and expanded tokens
# df1 <- replace_abb(pat_records, abbs)

# Creates a dataframe which gives overview of tokens, abbreviations and their expansions for curent dataset
token_df <- add_expansion(token_df, abb_df)

# Replaces abbreviations that have been recognized with their expansions in the original patient records
pat_records_exp <- expand_text(pat_records = pat_records_orig, token_df = token_df)

# Writes token dataframe to an excel file in the output folder
token_df %>% filter(converted == TRUE) %>% as.data.frame() %>%
  write.xlsx(file = "output/attempt1_abbs.xlsx", col.names = T, row.names = F)

# Writes adjusted patient records to an excel file in the output folder
pat_records_exp %>% as.data.frame() %>%
  write.xlsx(file = "output/attempt1_pat_records.xlsx", col.names = T, row.names = F)
