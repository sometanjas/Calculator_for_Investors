# write your code here
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import desc, func
import csv


file_1 = '/Users/vitaly/IdeaProjects/Calculator for Investors/Calculator for Investors/companies.csv'
file_2 = '/Users/vitaly/IdeaProjects/Calculator for Investors/Calculator for Investors/financial.csv'

with open(file_1) as companies_file:
    reader = csv.reader(companies_file)
    headers_one = next(reader)  # skip headers
    data_one = [[cell if cell != '' else None for cell in row] for row in reader]

with open(file_2) as financial_file:
    reader = csv.reader(financial_file)
    headers_two = next(reader)  # skip headers
    data_two = [[cell if cell != '' else None for cell in row] for row in reader]

Base = declarative_base()
engine = create_engine('sqlite:///investor.db', echo=False, connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()


class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


Base.metadata.create_all(engine)

any_company = session.query(Companies).first()
if not any_company:
    for row in data_one:
        # if row[0] != 'MOON':
        company = Companies(ticker=row[0], name=row[1], sector=row[2])
        session.add(company)
        session.commit()
    for row in data_two:
        financial = Financial(ticker=row[0], ebitda=row[1], sales=row[2], net_profit=row[3], market_price=row[4],
                              net_debt=row[5], assets=row[6], equity=row[7], cash_equivalents=row[8], liabilities=row[9])
        session.add(financial)
        session.commit()


def main_menu():
    print("MAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria")
    print("Enter an option:")
    return input()


def crud_menu():
    print("CRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a company\n"
          "5 List all companies\n")
    print("Enter an option:")
    return input()


def top_ten_menu():
    print("TOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA\n")
    print("Enter an option:")
    return input()


def create_company():
    ticker = input("Enter ticker (in the format 'MOON'):")
    enter_company = input("Enter company (in the format 'Moon Corp'):")
    codd_corp = input("Enter industries (in the format 'Technology'):")
    ebitda = int(input("Enter ebitda (in the format '987654321'):"))
    sales = int(input("Enter sales (in the format '987654321'):"))
    net_profit = int(input("Enter net profit (in the format '987654321'):"))
    market_price = int(input("Enter market price (in the format '987654321'):"))
    net_debt = int(input("Enter net debt (in the format '987654321'):"))
    assets = int(input("Enter assets (in the format '987654321'):"))
    equity = int(input("Enter equity (in the format '987654321'):"))
    cash_equivalents = int(input("Enter cash equivalents (in the format '987654321'):"))
    liabilities = int(input("Enter liabilities (in the format '987654321'):"))
    add_info = Companies(ticker=ticker, name=enter_company, sector=codd_corp)
    session.add(add_info)
    session.commit()
    add_data = Financial(ticker=ticker, ebitda=ebitda, sales=sales, net_profit=net_profit, market_price=market_price, net_debt=net_debt, assets=assets, equity=equity, cash_equivalents=cash_equivalents, liabilities=liabilities)
    session.add(add_data)
    session.commit()
    print("Company created successfully!")


def read_company():
    company_name = input("Enter company name: \n")
    result = session.query(Companies).filter(Companies.name.ilike(f'%{company_name}%')).all()
    # assert isinstance(result, Companies)
    if result:
        for index, line in enumerate(result):
            print(f'{index} {line.name}')
        company_number = int(input("Enter company number: "))
        financial_indicators(result[company_number])
    else:
        print("Company not found!")


def financial_indicators(company: Companies):
    table = session.query(Financial)
    query = table.filter(Financial.ticker == company.ticker)
    result = query.first()
    assert isinstance(result, Financial)
    print(company.ticker, company.name)
    p_e = division(result.market_price, result.net_profit)
    print("P/E =", p_e)
    p_s = division(result.market_price, result.sales)
    print("P/S =", p_s)
    p_b = division(result.market_price, result.assets)
    print("P/B =", p_b)
    nd_ebitda = division(result.net_debt, result.ebitda)
    print("ND/EBITDA =", nd_ebitda)
    roe = division(result.net_profit, result.equity)
    print("ROE =", roe)
    roa = division(result.net_profit, result.assets)
    print("ROA =", roa)
    l_a = division(result.liabilities, result.assets)
    print("L/A =", l_a)


def division(x, y):
    if x is None or y is None:
        return None
    else:
        return round(x / y, 2)


def update_company():
    company_name = input("Enter company name: ")
    result = session.query(Companies).filter(Companies.name.ilike(f'%{company_name}%')).all()
    if result:
        if result:
            for index, line in enumerate(result):
                print(f'{index} {line.name}\n')
        company_number = int(input("Enter company number: "))
        sub_update(result[company_number])
    else:
        print("Company not found!")


def sub_update(company):
    ebitda = int(input("Enter ebitda (in the format '987654321'): "))
    sales = int(input("Enter sales (in the format '987654321'): "))
    net_profit = int(input("Enter net profit (in the format '987654321'): "))
    market_price = int(input("Enter market price (in the format '987654321'): "))
    net_debt = int(input("Enter net debt (in the format '987654321'): "))
    assets = int(input("Enter assets (in the format '987654321'): "))
    equity = int(input("Enter equity (in the format '987654321'): "))
    cash_equivalents = int(input("Enter cash equivalents (in the format '987654321'): "))
    liabilities = int(input("Enter liabilities (in the format '987654321'): "))
    print("Company updated successfully!")
    company = session.query(Companies).filter_by(ticker=company.ticker).first()
    if company:
        financial = session.query(Financial).filter_by(ticker=company.ticker).first()
        if financial:
            financial.ebitda = ebitda
            financial.sales = sales
            financial.net_profit = net_profit
            financial.market_price = market_price
            financial.net_debt = net_debt
            financial.assets = assets
            financial.equity = equity
            financial.cash_equivalents = cash_equivalents
            financial.liabilities = liabilities
            session.commit()
    else:
        print("Company not found")


def delete_company():
    company_name = input("Enter company name: ")
    result = session.query(Companies).filter(Companies.name.ilike(f'%{company_name}%')).all()
    if result:
        if result:
            for index, line in enumerate(result):
                print(f'{index} {line.name}\n')
        company_number = int(input("Enter company number: "))
        sub_delete(result[company_number])
        print("Company deleted successfully!\n")
    else:
        print("Company not found!\n")


def sub_delete(company):
    session.query(Financial).filter(Financial.ticker == company.ticker).delete()
    session.commit()
    session.query(Companies).filter(Companies.ticker == company.ticker).delete()
    session.commit()


def list_all_companies():
    print("COMPANY LIST")
    result = session.query(Companies.ticker, Companies.name, Companies.sector).order_by(Companies.ticker).all()
    for row in result:
        print(f'{row[0]} {row[1]} {row[2]}')


def list_by_nd_ebitda():
    print("TICKER ND/EBITDA")
    top_10_query = session.query(Companies.ticker, (Financial.net_debt / Financial.ebitda).label('nd_ebitda')) \
        .join(Financial, Financial.ticker == Companies.ticker) \
        .order_by(desc('nd_ebitda'), desc(Companies.ticker)) \
        .limit(10)
    for result in top_10_query.all():
        print(result.ticker, round(result.nd_ebitda, 2))


def list_by_roe():
    print("TICKER ROE")
    top_10_query = session.query(Companies.ticker, (Financial.net_profit / Financial.equity).label('roe')) \
        .join(Financial, Financial.ticker == Companies.ticker) \
        .order_by(desc('roe'), desc(Companies.ticker)) \
        .limit(10)
    for result in top_10_query.all():
        print(result.ticker, round(result.roe, 2))


def list_by_roa():
    print("TICKER ROA")
    top_10_query = session.query(Companies.ticker, func.round((Financial.net_profit / Financial.assets), 2).label('roa')) \
        .join(Financial, Financial.ticker == Companies.ticker) \
        .order_by(desc('roa'), desc(Companies.ticker)) \
        .limit(10)
    for result in top_10_query:
        cname = result.ticker
        print(cname, round(result.roa, 2))


def main():
    print("Welcome to the Investor Program!\n")
    while True:
        answer = main_menu()
        validated_answer = is_answer_valid(answer, {0, 1, 2})
        if validated_answer == -1:
            print("Invalid option!\n")
            continue
        if validated_answer == 0:
            print("Have a nice day!\n")
            break
        if validated_answer == 1:
            answer = crud_menu()
            validated_answer = is_answer_valid(answer, {0, 1, 2, 3, 4, 5})
            if validated_answer == 1:
                create_company()
                continue
            if validated_answer == 2:
                read_company()
                continue
            if validated_answer == 3:
                update_company()
                continue
            if validated_answer == 4:
                delete_company()
                continue
            if validated_answer == 5:
                list_all_companies()
                continue
        if validated_answer == 2:
            answer = top_ten_menu()
            validated_answer = is_answer_valid(answer, {0, 1, 2, 3})
            if validated_answer == -1:
                print("Invalid option!\n")
            if validated_answer == 0:
                continue
            if validated_answer == 1:
                list_by_nd_ebitda()
            if validated_answer == 2:
                list_by_roe()
            if validated_answer == 3:
                list_by_roa()


def is_answer_valid(input_value, valid_options):
    result = -1
    try:
        result = int(input_value)
    except ValueError:
        return -1
        # print("Invalid option!")
    if result not in valid_options:
        return -1
    return result


main()