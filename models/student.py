
class Student:
    def __init__(self, name, mobile_number, joining_date,
                  application_number,
                    amount, discount, amount_paid, settle_amount, 
                    course,
                    training_days=10, notes=''
                    ):
        self.name = name
        self.mobile_number = mobile_number
        self.joining_date = joining_date
        self.application_number = application_number
        self.amount = amount
        self.discount = discount
        self.amount_paid = amount_paid
        self.settle_amount = settle_amount
        self.course = course
        self.training_days = training_days
        self.notes = notes
