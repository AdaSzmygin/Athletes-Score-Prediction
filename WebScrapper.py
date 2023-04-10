import requests
from bs4 import BeautifulSoup
import string
years=str(list(range(2001,2018)))

header={
"x-api-key": "da2-ccv5yvixizdjdjtengkq2sbgsm"
}
url="https://v3d2eshxhffjzea4lhqm2i7hfa.appsync-api.eu-west-1.amazonaws.com/graphql"
for x in years:
    payload={"operationName":"GetSingleCompetitorResultsDiscipline","variables":{"resultsByYear":x,"resultsByYearOrderBy":"discipline","id":14201847},"query":"query GetSingleCompetitorResultsDiscipline($id: Int, $resultsByYearOrderBy: String, $resultsByYear: Int) {\n  getSingleCompetitorResultsDiscipline(id: $id, resultsByYear: $resultsByYear, resultsByYearOrderBy: $resultsByYearOrderBy) {\n    parameters {\n      resultsByYear\n      resultsByYearOrderBy\n      __typename\n    }\n    activeYears\n    resultsByEvent {\n      indoor\n      disciplineCode\n      disciplineNameUrlSlug\n      typeNameUrlSlug\n      discipline\n      withWind\n      results {\n        date\n        competition\n        venue\n        country\n        category\n        race\n        place\n        mark\n        wind\n        notLegal\n        resultScore\n        remark\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    response= requests.post(url,headers=header,json=payload) 
    print(response)
#print(response.json()) #PRINTUJE DANE