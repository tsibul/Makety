from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from salesreport.models import CustomerPeriodsYear, CustomerPeriodsQuarter, CustomerPeriodsMonth, CustomerPeriodsWeek, \
    GoodsPeriodsWeek, GoodsPeriodsMonth, GoodsPeriodsQuarter, GoodsPeriodsYear


def customer_import_compare(row, customer):
    return customer.name == row[1] and \
           customer.form == row[2] and \
           customer.inn == row[3] and \
           customer.address == row[5] and \
           customer.phone == row[6] and \
           customer.mail == row[7] and \
           customer.comment == row[8] and \
           customer.all_phones == row[13] and \
           customer.all_mails == row[12]


def customer_check_row(row):
    result = (len(row) == 14)
    empty = True
    for i in range(2, len(row)):
        empty = empty and (row[i] == '' or row[i] == '0')
    return result and not empty


def customer_type_chose(type, region):
    if 'Конечник' in type and (region == '77' or region == '50'):
        type_obj = Customer_types.objects.get(type_name='Конечник Москва')
    elif 'Конечник' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Конечник Регион')
    elif 'рекламщик' in type and region == '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Рекламщик Москва')
    elif 'рекламщик' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Рекламщик Регион')
    elif 'Агентство' in type and region == '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Агентство Москва')
    elif 'Агентство' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Агентство Регион')
    elif 'Дилер' in type and region == '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Дилер Москва')
    elif 'Дилер' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Дилер Регион')
    elif 'точка' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Розничная Точка')
    else:
        type_obj = ''
    return type_obj


def set_inn(customer):
    cust_all = Customer_all.objects.filter(inn=customer.inn).order_by('frigat_id').last()
    customer.customer_all = cust_all
    customer.frigat_id = cust_all.frigat_id
    customer.save()


def check_class(period):
    if period == 'WK':
        return CustomerPeriodsWeek
    elif period == 'MT':
        return CustomerPeriodsMonth
    elif period == 'QT':
        return CustomerPeriodsQuarter
    else:
        return CustomerPeriodsYear


def check_goods_class(period):
    if period == 'WK':
        return GoodsPeriodsWeek
    elif period == 'MT':
        return GoodsPeriodsMonth
    elif period == 'QT':
        return GoodsPeriodsQuarter
    else:
        return GoodsPeriodsYear
