import sheetUpdater


def lambda_handler(event, context):
    from datetime import date

    today = date.today()
    date = today.strftime("%B %d")

    sheetUpdater.updater(date)

    return {
        'statusCode': 200,
        'body': "Successfully updated spreadsheet on {}".format(date)
    }


lambda_handler("this", "this")