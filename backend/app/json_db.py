from json_db_lite import JSONDatabase


small_db = JSONDatabase(file_path='employees.json')



def json_to_dict_list():
    return small_db.get_all_records()



def add_employee(employee: dict):
    small_db.add_records(employee)
    return True


def upd_employee(upd_filter: dict, new_data: dict):
    small_db.update_record_by_key(upd_filter, new_data)
    return True


def dell_employee(id: int):
    small_db.delete_record_by_key("id", id)
    return True