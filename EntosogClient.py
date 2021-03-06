
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

URL = "https://transparency.entsog.eu/api/v1/"

class EntsogClient:
    """
    Client inspired by the enstoe package, used to extract pipe flows of the European gas network.
    This Client pulls in .xml format
    areas to develop:
        - .csv pull
        - not limited to tsoEicCodes
    """

    def __init__(self, tsoID):

        opUrl = URL + "operationaldatas.csv?tsoItemIdentifier=" + tsoID

        self.operatorDataOut = pd.read_csv(opUrl)

    def capacityRequest(self, tsoID, capType, directionKey, operatorKey, pointKey):
        """
        First we need to check whether the capacity request type exists in the operational data.
        Options for the operational data:
           1. 'Firm Technical'
           2. 'Firm Available'
           3. 'Firm Booked'
        """
        if len(operatorKey) == 0:
            operatorKey = self.operatorDataOut.operatorKey.unique()[0].lower()
        if len(pointKey) == 0:
            pointKey = self.operatorDataOut.pointKey.unique()[0].lower()
        if len(directionKey) == 0:
            directionKey = self.operatorDataOut.directionKey.unique()[0].lower()

        keyElement = operatorKey + pointKey + directionKey

        validTypes = ["Firm Technical", "Firm Available", "Firm Booked"]

        startDate = datetime.now() - timedelta(weeks=1)
        endDate = datetime.now()

        if type(startDate) is datetime:
            startDate = startDate.strftime("%Y-%m-%d")
        elif not type(startDate) is datetime:
            return print("End date not in datetime format")

        if type(endDate) is datetime:
            endDate = endDate.strftime("%Y-%m-%d")
        elif not type(endDate) is datetime:
            return print("End date not in datetime format")

        if capType in validTypes:

            if capType == "Firm Technical":
                indicator = "&indicator=Firm%20Technical"
            elif capType == "Firm Available":
                indicator = "&indicator=Firm%20Available"
            elif capType == "Firm Booked":
                indicator = "&indicator=Firm%20Booked"

            opData = (
                URL
                + "operationaldata.csv?pointDirection="
                + keyElement
                + indicator
                + "&from="
                + startDate
                + "&to="
                + endDate
            )
            return pd.read_csv(opData)[
                {
                    "operatorLabel",
                    "periodFrom",
                    "periodTo",
                    "value",
                    "unit",
                    "pointLabel",
                    "directionKey",
                }
            ]

            if capType in opData.indicator.values:
                opData = opData[opData["indicator"] == capType]
                return opData
            else:
                print(
                    "The Type is not found on Entsog for TSO: "
                    + self.operatorDataOut.tsoItemIdentifier[0]
                )

        else:
            print("This is not a valid Type")

    def physicalFlow(self, startDate, endDate, directionKey, operatorKey, pointKey):
        """
        Request to the API for the physical flow. key elements:
            1. operatorKey+pointKey+directionKey
            2. start and end date (YYYY-mm-dd)
            3. indicator = Physical%20Flow
            4. periodType = day
            
        """

        if len(operatorKey) == 0:
            operatorKey = self.operatorDataOut.operatorKey.unique()[0].lower()
        if len(pointKey) == 0:
            pointKey = self.operatorDataOut.pointKey.unique()[0].lower()

        indicator = "&indicator=Physical%20Flow"

        if len(directionKey) == 0:
            directionKey = self.operatorDataOut.directionKey.unique()[0].lower()

        keyElement = operatorKey + pointKey + directionKey

        if type(startDate) is datetime:
            startDate = startDate.strftime("%Y-%m-%d")
        elif not type(startDate) is datetime:
            return print("End date not in datetime format")

        if type(endDate) is datetime:
            endDate = endDate.strftime("%Y-%m-%d")
        elif not type(endDate) is datetime:
            return print("End date not in datetime format")

        physicalFlowURL = (
            URL
            + "operationaldata.csv?pointDirection="
            + keyElement
            + "&from="
            + startDate
            + "&to="
            + endDate
            + indicator
        )

        return pd.read_csv(physicalFlowURL)[
            {
                "operatorLabel",
                "periodFrom",
                "periodTo",
                "value",
                "unit",
                "pointLabel",
                "directionKey",
            }
        ]
    
    def physicalFlowHour2D(self, directionKey, operatorKey, pointKey):
        """
        Request to the API for the physical flow. key elements:
            1. operatorKey+pointKey+directionKey
            2. start and end date (YYYY-mm-dd)
            3. indicator = Physical%20Flow
            4. periodType = hour
            
        """

        if len(operatorKey) == 0:
            operatorKey = self.operatorDataOut.operatorKey.unique()[0].lower()
        if len(pointKey) == 0:
            pointKey = self.operatorDataOut.pointKey.unique()[0].lower()

        indicator = "&indicator=Physical%20Flow"
        periodType = "&periodType=hour"

        startDate = datetime.now() - timedelta(days=2)
        endDate = datetime.now()

        if len(directionKey) == 0:
            directionKey = self.operatorDataOut.directionKey.unique()[0].lower()

        keyElement = operatorKey + pointKey + directionKey

        if type(startDate) is datetime:
            startDate = startDate.strftime("%Y-%m-%d")
        elif not type(startDate) is datetime:
            return print("End date not in datetime format")

        if type(endDate) is datetime:
            endDate = endDate.strftime("%Y-%m-%d")
        elif not type(endDate) is datetime:
            return print("End date not in datetime format")

        physicalFlowURL = (
            URL
            + "operationaldata.csv?pointDirection="
            + keyElement
            + "&from="
            + startDate
            + "&to="
            + endDate
            + indicator
            + periodType
        )

        return pd.read_csv(physicalFlowURL)[
            {
                "operatorLabel",
                "periodFrom",
                "periodTo",
                "value",
                "unit",
                "pointLabel",
                "directionKey",
            }
        ]
