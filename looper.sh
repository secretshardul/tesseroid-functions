#!/bin/bash -x
string="hin eng"
# IFS=', ' read -r -a array <<< "$string"
# for element in "${array[@]}"
# do
#     echo "$element"
# done
equ="equ"
ind="san hin urd pan mar guj asm ben ori kan tel tam mal sin nep bod dzo"
middle="pus ara fas tur aze aze_cyrl kat kat_old heb"
africa="afr amh swa"
west="eng gle cym fra spa spa_old ita ita_old ell grc por pol deu nld dan nor swe isl rus ukr"
east="chi_sim chi_sim_vert chi_tra chi_tra_vert kor kor_vert jpn jpn_vert"
sea="mya msa ind jav tha lao vie khm tgl"
string="$equ $ind $middle $africa $west $east $sea"
for x in $string 
do
    echo $x
done
# echo "${#string[@]}"