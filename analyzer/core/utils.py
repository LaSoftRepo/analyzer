def validate_sms_phone(collection):
    for k, phone in collection.phones.items():
        if len(phone) == 10:
            phone = ''.join(('+38', phone))
        if phone:
            return phone
        else:
            collection.phones['error'] = 'ERROR PHONE'
            collection.save()
