# Principal Payment = TMP - (OLB * (interest rate / 12))
import datetime as dt
from dateutil.relativedelta import relativedelta
from decimal import Decimal, getcontext, ROUND_HALF_UP
from pprint import pprint
import csv

getcontext().rounding = ROUND_HALF_UP

initDate = dt.date(2024,9,3)
term = 60 # months
loanPrincipal = 50000
annualInterestRate = 4.25
monthlyPaymentAmount = 450
nameOfSchedule = "450perMonth"
amortizationDirectoryPath = "/Users/williamhbelew/Desktop/amortizationSchedules/"

class Payment:
    def __init__(self,date,beginningLoanBalance,paymentAmount,annualInterestRate):
        self.date = date
        self.beginningLoanBalance = Decimal(beginningLoanBalance)
        self.paymentAmount = Decimal(paymentAmount)
        self.annualInterestRate = Decimal(annualInterestRate)
    def calcInterestAndPrincipalPayment(self):
        interest = (self.beginningLoanBalance * (self.annualInterestRate / Decimal(12))).quantize(Decimal('0.01'))
        principal = (self.paymentAmount - interest).quantize(Decimal('0.01'))
        return [interest, principal]
    def calcEndingLoanBalance(self):
        interest, principal = self.calcInterestAndPrincipalPayment()
        return (self.beginningLoanBalance - principal).quantize(Decimal('0.01'))
    def represent(self):
        interest, principal = self.calcInterestAndPrincipalPayment()
        return {
            "date": self.date.strftime("%B %d, %Y"),
            "beginning loan balance": f"${self.beginningLoanBalance:,.2f}",
            "monthly payment amount": f"${self.paymentAmount:,.2f}",
            "interest paid": f"${interest:,.2f}",
            "principal paid": f"${principal:,.2f}",
            "ending loan balance": f"${self.calcEndingLoanBalance():,.2f}"
        }

def createAmortizationSchedule(initDate, termInMonths, loanAmount, annualInterestRate, monthlyPaymentAmount):
    payments = []
    date = initDate
    loanBalance = loanAmount
    for m in range(termInMonths):
        if monthlyPaymentAmount > loanBalance:
            break
        p = Payment(date, loanBalance, monthlyPaymentAmount, Decimal(annualInterestRate)/Decimal(100))
        payments.append(p.represent())
        date = date + relativedelta(months=1)
        loanBalance = p.calcEndingLoanBalance()
    # adding balloon payment at end
    payments.append({"date": date.strftime("%B %d, %Y"),
                "beginning loan balance": "",
                "monthly payment amount": "",
                "interest paid": "",
                "principal paid": "", 
                "ending loan balance": f"${loanBalance:,.2f}", 
                })
    return payments

def saveScheduleToCsv(paymentSchedule, filename="AmortizationSchedule"):
    filepath = f"{amortizationDirectoryPath}{filename}__{dt.date.today().strftime('%m_%d_%Y')}.csv"
    with open(filepath, mode='w', newline='') as csvfile:
        fieldnames = paymentSchedule[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(paymentSchedule)

paymentSchedule = createAmortizationSchedule(
        initDate,
        term,
        loanPrincipal,
        annualInterestRate,
        monthlyPaymentAmount
        )
pprint(paymentSchedule)
saveScheduleToCsv(paymentSchedule, nameOfSchedule if nameOfSchedule else None)
