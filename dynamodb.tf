resource "aws_dynamodb_table" "dynamodb_table" {
  name           = "DynamoDB-Table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 2
  write_capacity = 2
  hash_key       = "MessageId"

  attribute {
    name = "MessageId"
    type = "S"
  }
}

