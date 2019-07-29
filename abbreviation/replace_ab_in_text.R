# Function to replace abbreviation in complete records with its expansion
replace_abb_in_text <- function(x){
  string <- x
  # Regex: matches all words or abbreviations separated by whitespaces
  pattern <- "(\\b[\\w|\\.]+(?=[\\s]))|(\\b[\\w|\\.]+$)"
  # Replaces matches with same string but last character stripped
  replacement <- substr(string, 1, nchar(string)-1)
  result <- sub(pattern = pattern, replacement = replacement, x = string)
  return(result)
}

string <- "test1. ab.c. def ghk."
pattern <- "(\\b[\\w|\\.]+(?=[\\s]))|(\\b[\\w|\\.]+$)"
matches <- str_extract_all(pattern = pattern, string = string)


str_split(string = string, pattern = "\\s")
