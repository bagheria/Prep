# # Function to replace abbreviation in complete records with its expansion
# replace_abb_in_text <- function(x){
#   string <- x
#   # Regex: matches all words or abbreviations separated by whitespaces
#   pattern <- "(\\b[\\w|\\.]+(?=[\\s]))|(\\b[\\w|\\.]+$)"
#   # Replaces matches with same string but last character stripped
#   replacement <- substr(string, 1, nchar(string)-1)
#   result <- sub(pattern = pattern, replacement = replacement, x = string)
#   return(result)
# }

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




## Regex code to try out stuff:

# string <- "test1. ab.c. test1 def ghk. test1blabla test1."
# pattern <- "(?<=\\b)test1(?=\\b)"
# str_extract_all(pattern = pattern, string = string)
# sub(pattern = "asdbds", replacement = "x", x = string, perl = T)
# 
# 
# str_split(string = string, pattern = "\\s")
# 
# 
# 
# string <- "test1. ab.c. def ghk."
# pattern <- "(\\b[\\w|\\.]+(?=[\\s]))|(\\b[\\w|\\.]+$)"
# matches <- str_extract_all(pattern = pattern, string = string)
# 
# 
# str_split(string = string, pattern = "\\s")
