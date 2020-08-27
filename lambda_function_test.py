import time
import sheetUpdater
import json


def lambda_handler(event, context):
    epoch_time = int(time.time())

    worksheet = sheetUpdater.get_sheet(str(epoch_time))
    worksheet.append_row(["This is a test",
                          epoch_time,
                          "ahhhhh"])

    epoch_time = int(time.time())

    worksheet.append_row(["This is a test",
                          epoch_time,
                          "ahhhhh"])
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
