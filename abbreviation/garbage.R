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
