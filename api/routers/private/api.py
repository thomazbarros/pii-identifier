from fastapi import Depends, APIRouter, HTTPException, status
from model.apimodel import APIModel
from service.pii_information import PIInformation
from routers.public.login import get_token_header
from service.dbcredential import DBCredentialService
from exception.entitynotfoundexception import EntityNotFoundException
from exception.entityalreadyexistsexception import EntityAlreadyExistsException
from dto.rule import RuleDTO

internal_schemas = ['information_schema', 'performance_schema', 'mysql', 'sys']
pii_information = PIInformation()
dbcredential_service = DBCredentialService()

router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/database/", status_code=status.HTTP_201_CREATED, description="Create a new database configuration to be scanned")
async def create_database(db:APIModel):
    id = dbcredential_service.create(db.host, db.port, db.username, db.password)
    return {'id':id}

@router.post("/database/scan/{id}", status_code=status.HTTP_201_CREATED)
async def scan_db(id:str):
    try: 
        print("starting scanner")
        pii_information.scan(id)
    except EntityNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DBCredential not found with id " + id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. " + str(ex.args))

@router.get("/database/scan/{id}", status_code=status.HTTP_200_OK)
async def get_scan_result(id:str):
    try: 
        return pii_information.retrieve_result(id)
    except EntityNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DBCredential not found with id " + id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

@router.get("/database/rules", status_code=status.HTTP_200_OK, description="List all rules")
async def get_rules():
    return pii_information.retrieve_rules()


@router.post("/database/rules", status_code=status.HTTP_201_CREATED, description="Create a new rule")
async def create_rule(dto: RuleDTO):
    try:
        return pii_information.create_rule(dto.name, dto.regex_exp)
    except EntityAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="DBCredential not found with id " + id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")



@router.get("/database/rules/{name}", status_code=status.HTTP_200_OK, description="Find rule by name")
async def find_rule_by_name(name: str):
    try:
        return pii_information.find_rule_by_name(name)
    except EntityNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found with name " + name)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Reason: " + str(ex.args))

