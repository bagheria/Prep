# Function to replace abbreviation with tracing dots in string
# Necessary since 'unnest_token()' will strip tracing dots, 
# which makes matching of tokens to abbreviations impossible otherwise.
rm_tracing_dot <- function(x){
  string <- x
  # Regex: matches entire string which ends with a '.'
  pattern <- pattern <- "^.*\\.$"
  # Replaces matches with same string but last character stripped
  replacement <- substr(string, 1, nchar(string)-1)
  result <- sub(pattern = pattern, replacement = replacement, x = string)
  return(result)
}

replace_tracing_dot <- function(abb_df) {
  # Initialize counter to keep track of number of changes
  counter <- 0
  new_df <- abb_df
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

