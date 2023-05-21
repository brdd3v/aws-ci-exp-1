resource "aws_sns_topic" "sns_topic" {
  name = "sns-topic"
}

resource "aws_sns_topic_subscription" "sqs_sns_subscription" {
  protocol             = "sqs"
  raw_message_delivery = true
  topic_arn            = aws_sns_topic.sns_topic.arn
  endpoint             = aws_sqs_queue.sqs_queue.arn
}

