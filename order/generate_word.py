from docxtpl import DocxTemplate


def basic(num_list):
    exp_list = ['拾', '佰', '仟', '万']
    lst = []
    lth = len(num_list)
    for i in range(lth - 1):
        lst.append(num_list[lth - i - 1])
        lst.append(exp_list[i])
    lst.append(num_list[0])
    return lst


def writeNumber(num):
    s = str(num)
    num2pinin = {'1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖', '0': '零'}
    sum_of_number = str(num)
    num_list = list(map(lambda x: num2pinin[x], sum_of_number))
    lth = len(num_list)

    yi_lst = []
    wan_lst = []
    lst = []
    if lth > 9:
        yi_lst = ['亿'] + basic(num_list[:-8])
        wan_lst = ['万'] + basic(num_list[-8:-4])
        lst = basic(num_list[-4:])
    elif lth > 5:
        wan_lst = ['万'] + basic(num_list[:-4])
        lst = basic(num_list[-4:])
    else:
        lst = basic(num_list)
    result = lst + wan_lst + yi_lst
    result.reverse()
    # 去掉〇后面相邻字符
    for i in range(len(result) - 1):
        if result[i] == '〇':
            result[i + 1] = ''

    # 去掉空字符串
    result = list(''.join(result))
    print(result)
    # 去掉相邻的〇
    for i in range(len(result) - 1):
        if result[i] == '〇':
            j = i + 1
            while result[j] == '〇':
                result[j] = ''
                j = j + 1
    if result[-1] == '〇':
        result.pop(-1)
    return ''.join(result)


def generate_word(order):
    mat_set = order.mat_set.all()
    big_sum = sum((mat.material_price * mat.material_num for mat in mat_set.all()))
    big_sum = int(big_sum)
    chinese_sum = writeNumber(big_sum)
    doc = DocxTemplate('word_files/template.docx')
    items = []
    for i in range(len(mat_set)):
        items.append({
            'idx': i+1,
            'cols': [
                mat_set[i].material_name,
                mat_set[i].material_spec,
                mat_set[i].material_unit,
                mat_set[i].material_num,
                mat_set[i].material_price,
                mat_set[i].material_num*mat_set[i].material_price,
                mat_set[i].material_date,
                mat_set[i].material_expl,
            ]
        })
    context = {
        'buyer': order.buyer.comp_name,
        'seller': order.seller.comp_name,
        'order_code': order.order_code,
        'order_place': order.order_place,
        'items': items,
        'big_sum': big_sum,
        'chinese_sum': chinese_sum,
        'deposit_percent':order.deposit_percent,
        'deposit':order.deposit_percent*order.get_sum()/100,
        'comp_addr': order.buyer.comp_addr,
        'comp_addr_': order.seller.comp_addr,
        'comp_legal_person': order.buyer.comp_legal_person,
        'comp_legal_person_': order.seller.comp_legal_person,
        'comp_agent_person': order.buyer.comp_agent_person,
        'comp_agent_person_': order.seller.comp_agent_person,
        'comp_phone': order.buyer.comp_phone,
        'comp_phone_': order.seller.comp_phone,
        'comp_bank_name': order.buyer.comp_bank_name,
        'comp_bank_name_': order.seller.comp_bank_name,
        'comp_bank_account': order.buyer.comp_bank_account,
        'comp_bank_account_': order.seller.comp_bank_account,
        'comp_tax_account': order.buyer.comp_tax_account,
        'comp_tax_account_': order.seller.comp_tax_account,
        'comp_contact_person': order.buyer.comp_contact_person,
        'comp_contact_person_': order.seller.comp_contact_person,
    }
    doc.render(context)
    word_name=order.order_date.strftime('%Y-%m-%d')+f'甲方：{order.buyer.comp_name}'
    doc.save(f'word_files/{word_name}.docx')
    return word_name
