"""
All the variables related to instamojo

Author: Himanshu Shankar (https://himanshus.com)
"""
PENDING = "Pending"
SENT = "Sent"
FAILED = "Failed"
COMPLETED = "Completed"
NULL = "Null"

CREDIT = "Credit"

STATUS_CHOICES = (
    (PENDING, "PENDING"),
    (SENT, "SENT"),
    (FAILED, "FAILED"),
    (COMPLETED, "COMPLETED"),
)

SENT_STATUS_CHOICES = (
    (PENDING, "PENDING"),
    (SENT, "SENT"),
    (FAILED, "FAILED"),
    (NULL, "NULL")
)

PAYMENT_STATUS_CHOICES = (
    (CREDIT, "CREDIT"),
    (FAILED, "FAILED")
)

CREATE_REQUEST = "payment-requests/"
LIST_REQUEST = "payment-requests/"
RETRIEVE_REQUEST = "payment-requests/{id}/"
DISABLE_REQUEST = "payment-requests/{id}/disable/"
ENABLE_REQUEST = "payment-requests/{id}/enable/"
