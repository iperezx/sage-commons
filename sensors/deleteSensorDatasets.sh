endpoint="https://sage-commons.sdsc.edu"
declare -a arr=("xnf-8010rv" "xnv-8080r" "xnv-8082r" "xnv-8081z" "rg-15" "bme680")
apiKey=${CKANAPIKEY}
set -B
for i in "${arr[@]}"
do
   echo -e "$i"
   curl --request POST "${endpoint}/api/3/action/dataset_purge" --header "Authorization: ${apiKey}" --form "id="${i}""
   echo -e "\n"
done