#-*-coding:utf8-*-

'''
	Настройки
'''
test_order_link = 'www.ivi.ru/watch/7029?adr_order_id={{ test_order }}'
test_placement_link = 'http://special.ivi.ru/vast/production/{{ xml_name }}.xml?r=%%RANDOM%%'
order = {'1' : 246157, '2' : 246158, '3' : 246159, '4' : 246160, '5' : 246161, '6' : 246162} # соответствие РЗ слотам (потом убрать в файл настроек)
template = { 'Web WOW-roll': 'web_wow_roll_vast', 'Web': None , 'Mobile':   'mobile_vast'  }