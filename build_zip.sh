rm -rf ./build
mkdir -p ./build

cp -r ./src/schema_actions build/
cd build/schema_actions
mv psycopg2_ow_build psycopg2
zip -r ../schema_actions.zip *
cd -
