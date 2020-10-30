import connexion
import six
import boto3


from swagger_server.models.result import Result  # noqa: E501
from swagger_server.models.result import ResultConcordance
from swagger_server import util


def get_concordance(body=None, save=None, compute=None):  # noqa: E501
    """Calculate

    Post text to generate concordance # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes
    :param save:
    :type save: bool
    :param compute:
    :type compute: bool

    :rtype: Result
    """
    

    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501


    # Body was in bytes, decoding into a string
    body = body.decode('UTF-8')

   

    # Check if input is in database already, if so initialize item with response
    # if not just set item to None to be checked in the if right after
    try:
         # Connect to dynamoDB
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('Analyze')
        response = table.get_item(
            Key={
                'input': body,
            }
        )
        item = response['Item']
    except:
        item = None

    # If items equivilent to None  or compute is set to true run concordance and add to db and return the result
    if item == None or compute:
        # Need a dictionary for word:occurrence pairs
        concordanceDict = dict()

        # Split body into words that we can loop through and count
        bodyList = body.split()

        for i in range(len(bodyList)):
            # Going to put every word in lower case
            bodyList[i] = bodyList[i].lower()

        # Sorts the list in alphabetical order
        bodyList.sort()

        for word in bodyList:
            # Add the word to the dict if it isn't there, otherwise increment the occurrences
            if word not in concordanceDict:
                concordanceDict[word] = 1
            elif word in concordanceDict:
                concordanceDict[word] = concordanceDict[word] + 1

        # A list for ResultConcordance objects, created from the filled-in dictionary
        concordanceResult = []
        for word in concordanceDict:
            concordanceResult.append(ResultConcordance(word, concordanceDict[word]))

         # Put the input and result of concordance into the db if save is true or hasn't been changed
        if save or save == None:
            table.put_item(
                Item={
                    'input' : body,
                    'concordance' : concordanceDict
                },
            )

        # Return a Result object, providing the list of ResultConcordance objects and the original message
        return Result(concordanceResult, body)

    # Return the item recieved from the db if it existed in the earlier get
    else:
        return item