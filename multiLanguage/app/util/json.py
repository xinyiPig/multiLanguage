from datetime import datetime,date

def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    json = {}
    # json['fields'] = {}
    # json['pk'] = getattr(model, 'id')
   
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        # json['fields'][col.name] = getattr(model, col.name)
        value = getattr(model, col.name)
        # print(value)
        if isinstance(value, datetime):
          json[col.name] = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
          json[col.name] =  value.strftime('%Y-%m-%d')
        else:
          json[col.name] = value
       

    # return dumps([json])
    return json

def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list

