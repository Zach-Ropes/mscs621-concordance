import connexion
import six
import boto3

from swagger_server.models.locate_result_found import LocateResultFound
from swagger_server.models.locate_result import LocateResult  # noqa: E501
from swagger_server import util


def locate_token(body=None, save=None, compute=None):  # noqa: E501
    """Find tokens

    Post text to discover token locations within the string # noqa: E501

    :param body: Text to be analyzed
    :type body: dict | bytes
    :param save:
    :type save: bool
    :param compute:
    :type compute: bool

    :rtype: LocateResult
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

        table = dynamodb.Table('Locate')
        response = table.get_item(
            Key={
                'input': body,
            }
        )
        item = response['Item']
    except:
        item = None

    # If items equivilent to None  or compute is set to true run locate, add to db, and return the result
    if item == None or compute == True:
        # Need a dictionary for word:location index lists
        locateDict = dict()

        # Split body into words that we can loop through and count
        bodyList = body.split()

        for i in range(len(bodyList)):
            # Going to put every word in lower case
            bodyList[i] = bodyList[i].lower()

        # Creates a new list from the first list and puts it in alphabetical order
        alphebetizedBodyList = list(bodyList)
        alphebetizedBodyList.sort()

        # Initizalize the Location dict with the alphebetized list
        for word in alphebetizedBodyList:
            if word not in locateDict:
                locateDict[word] = []

        # Insert the location indexes of the word tokens from the original list
        for i in range(len(bodyList)):
            locateDict[bodyList[i]].append(i)

        # A list for LocateResult objects, created from the filled-in dictionary
        locateResult = []
        for word in locateDict:
            locateResult.append(LocateResultFound(word, locateDict[word]))

        # Put the input and locations results into the db if save is true or hasn't been changed
        if save or save == None:
            table.put_item(
                Item={
                    'input' : body,
                    'locations' : locateDict
                }
            )

        # Return a LocateResult object, providing the list of Locatation Results
        return LocateResult(locateResult)

    # Return the item recieved from the db if it existed in the earlier get
    else:
        return item