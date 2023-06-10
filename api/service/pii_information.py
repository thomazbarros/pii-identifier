import json
import re

from model.scan import Scan
from model.schema import Schema
from model.table import Table
from model.tablecolumn import TableColumn
from model.regular_expressions import Regular_Expression
from dto.rule import RuleDTO
import repository.dbcredential as dbcredentialRepository
from repository.scan import ScanRepository
from repository.schema import SchemaRepository
from repository.table import TableRepository
from repository.tablecolumn import TableColumnRepository
from repository.regular_expressions import Regular_Expression_Repository
from service.crypto import CryptoService
from exception.entitynotfoundexception import EntityNotFoundException
from exception.entityalreadyexistsexception import EntityAlreadyExistsException

scanRepository = ScanRepository()
schemaRepository = SchemaRepository()
tableRepository = TableRepository()
tableColumnRepository = TableColumnRepository()
regularExpressionRepository = Regular_Expression_Repository()

crytoService = CryptoService()
internal_schemas = ['information_schema', 'performance_schema', 'mysql', 'sys']

class PIInformation():
    regular_expressions = {
        # "name": re.compile(
        #     "^.*(firstname|fname|lastname|lname|middle|middlename|mname|fullname|maidenname|_name|nickname|name_suffix|name|surname|given|givennane).*$",
        #     re.IGNORECASE),
        "name": re.compile(
            "^(?!.*username)(?=.*(?:firstname|firstname|fname|lastname|lname|middle|middlename|mname|fullname|maidenname|nickname|name_suffix|name|surname|given|givenname)).*$",
            re.IGNORECASE),
        "birthday" : re.compile(
            "^.*(date_of_birth|dateofbirth|dob|birthday|date_of_death|dateofdeath|birthdate).*$",
            re.IGNORECASE,),
        "address" : re.compile(
            "^.*(address|city|state|county|country|borough).*$",
            re.IGNORECASE),
        "zipcode" : re.compile("^.*(zipcode|zip_code|postal|postal_code|zip|po_box|pobox).*$", re.IGNORECASE),
        "country" : re.compile("^.*(country|region|nationality).*$", re.IGNORECASE),
        "gender" : re.compile("^.*(gender|sex).*$", re.IGNORECASE), 
        "email": re.compile("^.*(email|e-mail|mail).*$", re.IGNORECASE),
        "ssn": re.compile("^.*(ssn|social_number|social_security|social_security_number|social_security_no).*$",
            re.IGNORECASE),
        "password": re.compile("^.*pass.*$", re.IGNORECASE),
        "creditcard" : re.compile("^.*(creditcard|credit_card|cc|credit|debitcard|card).*$", re.IGNORECASE),
        "fingerprint" : re.compile("^.*(finger|fingerprint).*$", re.IGNORECASE),
    }

    reg_ex2 = {}

    def is_personal_information(self, string):
        for key, pattern in PIInformation.regular_expressions.items():
            if re.match(pattern, string):
                return key
        return None
    
    def scan(self, dbcredential_id):
        credential = dbcredentialRepository.find_db_by_id(dbcredential_id)
        print(credential.db_username, credential.db_password)
        if credential is None:
            print("Entity not found")
            raise EntityNotFoundException("Credential not found")
        decrypted_password = crytoService.decrypt(credential.db_password)
        schemas=dbcredentialRepository.get_database_schemas(credential.db_username, decrypted_password, credential.db_host, credential.db_port)
        scan_id = self.__buildScan(dbcredential_id)
        for schema in schemas:
            print(schema)
            if schema not in internal_schemas:
                schema_id = self.__buildSchema(scan_id, schema)
                tables = dbcredentialRepository.get_schema_tables(credential.db_username, decrypted_password, credential.db_host, credential.db_port, schema)
                for table in tables:
                    is_pii = False
                    #result = PIInformation.is_personal_information(str(table))
                    #if result is not None:
                    #    is_pii = True
                    table_id = self.__buildTable(schema_id, table, is_pii)
                    columns = dbcredentialRepository.get_table_columns(credential.db_username, decrypted_password, credential.db_host, credential.db_port, schema, table)
                    for column in columns:
                        print(column['name'], column['type'])
                        result = PIInformation.is_personal_information(self, column['name'])
                        is_pii = False
                        if result is not None:
                            print(f"{column['name']} from table {table} is PII. {result} is the key")
                            is_pii = True
                        self.__buildTableColumn(table_id, column['name'], column['type'], is_pii)
        return None

    def __buildScan(self, dbcredential_id):
        scan = Scan(dbcredential_id=dbcredential_id)
        scan_id = scanRepository.save(scan)
        return scan_id
    
    def __buildSchema(self, scan_id, schema_name):
        schema = Schema(scan_id=scan_id,schema_name = schema_name)
        schema_id = schemaRepository.save(schema)
        return schema_id
    
    def __buildTable(self, schema_id, table_name, is_pii):
        table = Table(schema_id=schema_id,table_name = table_name, is_pii = is_pii)
        table_id = tableRepository.save(table)
        return table_id
    
    def __buildTableColumn(self, table_id, column_name, column_type, is_pii):
        table_column = TableColumn(table_id=table_id, column_name = column_name, column_type = column_type, is_pii = is_pii)
        table_column_id = tableColumnRepository.save(table_column)
        return table_column_id
    
    def retrieve_result(self, dbcredential_id):
        #credential = dbcredentialRepository.find_db_by_id(dbcredential_id)
        result = []
        scan_id = ScanRepository.get_last_scan(self, dbcredential_id)
        if scan_id is None:
            raise EntityNotFoundException("DBCredential not found with id " + dbcredential_id)
        print (scan_id)
        schemas = SchemaRepository.find_by_scan_id(self, scan_id)
        for schema in schemas:
            result_schema = {"schema": schema.schema_name, "tables": []}
            result.append(result_schema)
            print("SCHEMA:",schema.schema_name)
            tables = TableRepository.find_by_schema_id(self, schema.schema_id)
            for table in tables:
                result_table = {"table": table.table_name, "isPersonalInfo": table.is_pii, "columns": []}
                result_schema["tables"].append(result_table)
                tablecolumns = TableColumnRepository.find_by_table_id(self, table.table_id)
                for tablecolumn in tablecolumns:
                    result_column = {"column": tablecolumn.column_name, "type": self.__normalize_column_type(tablecolumn.column_type), "isPersonalInfo": tablecolumn.is_pii}
                    result_table["columns"].append(result_column)
                    print("COLUMN:", tablecolumn.column_name, "PII?", tablecolumn.is_pii )
        return result
    
    def __normalize_column_type(self, column_type):
        return column_type.split()[0]
    
    def retrieve_rules(self):
        regexes = {}
        results = regularExpressionRepository.find_all()
        if results is not None:
            for result in results:
                print(result.reg_ex_name)
                regexes[result.reg_ex_name] = result.reg_ex
            return regexes
        else:
            print(":")
            return None
    
    def create_rule(self, name, regex_exp):
        existing = regularExpressionRepository.find(name)
        if existing is not None:
            raise EntityAlreadyExistsException("Rule already exists with name " + name)
        regular_expression = Regular_Expression(reg_ex_name = name, reg_ex = regex_exp)
        regularExpressionRepository.save(regular_expression)

    def find_rule_by_name(self, name):
        reg = regularExpressionRepository.find_by_id(name)
        if reg is None:
            raise EntityNotFoundException("Regular expression not found with name " + name)
        regex = {}
        regex[reg.reg_ex_name] = reg.reg_ex
        return regex
