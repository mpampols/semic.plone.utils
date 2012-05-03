# -*- coding: utf-8 -*-


def listCarnets(self):
    from Products.CMFCore.utils import getToolByName
    from pyExcelerator import *

    catalog = getToolByName(self, "portal_membership")

    workbook = Workbook()
    worksheet = workbook.add_sheet('CARNETS')

    worksheet.write(0, 0, "MEMBER ID")
    worksheet.write(0, 1, "EMAIL")
    worksheet.write(0, 2, "LAST LOGIN")
    worksheet.write(0, 3, "FULLNAME")
    worksheet.write(0, 4, "LOCATION")
    worksheet.write(0, 5, "DESCRIPTION")
    worksheet.write(0, 6, "LANGUAGE")
    worksheet.write(0, 7, "WYSIWYG EDITOR")

    # starting at row 1
    row = 1
    destination_folder = '/tmp/'

    for memberId in catalog.listMemberIds():
        member = catalog.getMemberById(memberId)

        member_id = str(member)
        email = member.getProperty('email')
        last_login = member.getProperty('last_login')
        fullname = member.getProperty('fullname')
        location = member.getProperty('location')
        description = member.getProperty('description')
        language = member.getProperty('language')
        wysiwyg_editor = member.getProperty('wysiwyg_editor')

        worksheet.write(row, 0, member_id)
        worksheet.write(row, 1, email)
        worksheet.write(row, 2, last_login)
        worksheet.write(row, 3, fullname.decode("utf-8"))
        worksheet.write(row, 4, location.decode("utf-8"))
        worksheet.write(row, 5, description.decode("utf-8"))
        worksheet.write(row, 6, language)
        worksheet.write(row, 7, wysiwyg_editor)

        row += 1

    attch_file_send = 'members.xls'
    w.save(destination_folder + attch_file_send)
    return 1
