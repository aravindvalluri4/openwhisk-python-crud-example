#/bin/bash

info()
{
    [ -n "$@" ] && echo -e "\n \e[93m INFO: $*  \e[39m" >&2
}


info "################ BUILD ZIP ####################"
sh ./build_zip.sh
info "################ Done BUILD ####################"

POSTGRES_HOST=$(kubectl get svc --namespace postgres postgres-postgresql -o jsonpath="{.spec.clusterIP}")
POSTGRES_DB_NAME=postgres
POSTGRES_PASSWORD=$(kubectl get secret --namespace postgres postgres-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode)

echo ""
info "IDENTIFIED POSTGRES PARAMETERS"
info "host: $POSTGRES_HOST, database:$POSTGRES_DB_NAME password:$POSTGRES_PASSWORD"
echo ""

info "################ WSK Deploy ####################"

# create package
wsk package update schema_faas \
-a description "This package manages the library API of schema actions" \
-p db_url "$POSTGRES_HOST" \
-p db_name "$POSTGRES_DB_NAME" \
-p db_pass "$POSTGRES_PASSWORD" -i

# create actions
wsk action update schema_faas/db_init build/schema_actions.zip --main init --web true -i --kind python:2
wsk action update schema_faas/get_schema build/schema_actions.zip --main get --web true -i --kind python:2
wsk action update schema_faas/post_schema build/schema_actions.zip --main post --web true -i --kind python:2
wsk action update schema_faas/delete_schema build/schema_actions.zip --main delete --web true -i --kind python:2

wsk package get --summary schema_faas -i

# create API's
 # get
wsk api create -n "smAPI" /sm /schemas get schema_faas/get_schema --response-type http -i
wsk api create -n "smAPI" /sm /schemas/{schemaName} get schema_faas/get_schema --response-type http -i

wsk api create -n "smAPI" /sm /schemas/{schemaName} delete schema_faas/delete_schema --response-type http -i
wsk api create -n "smAPI" /sm /schemas post schema_faas/post_schema --response-type http -i

info "################ Done WSK Deploy ####################"

info "################ Initialize the Database ####################"
wsk action invoke schema_faas/db_init -i -r

info "################ Schema Management REST API INFO ####################"
wsk api list smAPI -i -f
info "################ Instalation Done ####################"
