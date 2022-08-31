from dataclasses import dataclass


@dataclass
class RuleAccess:
    access_groups: list
    how: str

    def __init__(self, access_groups: list, how: str = 'any'):
        self.access_groups = access_groups
        self.how = how


access_groups = {
    'admin': 'Имеет доступ ко всей системе',
    'administrator': 'Группа доступа для администратора антикафе',
    'super_administrator': 'Группа доступа для главного администратора антикафе'
}

admin_system_page = RuleAccess(['admin'])

administrator_page = RuleAccess(['administrator'])
administrator_loyalty_program_member_extends_funcs = RuleAccess(['super_administrator'])
