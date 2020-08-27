import sheetUpdater


def lambda_handler(event, context):
    from datetime import date
    import time

    epoch_time = int(time.time())

    today = date.today()
    date = today.strftime("%B %d")

    sheetUpdater.updater(epoch_time)

    return {
        'statusCode': 200,
        'body': "Successfully updated spreadsheet on {}".format(date)
    }


lambda_handler("this", "this")