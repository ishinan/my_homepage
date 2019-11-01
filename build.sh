#!/bin/bash
# Name         : build.sh
# Description  : Make html files from templates(top.html, bottom.html) and contents html
# Author       : Masaaki Yana
# Date         :
# Version      : 
# Usage        : bash build.sh


#cat templates/top.html contents/index.html templates/bottom.html > docs/index.html
#cat templates/top.html contents/blog.html templates/bottom.html > docs/blog.html
#cat templates/top.html contents/projects.html templates/bottom.html > docs/projects.html
#cat templates/top.html contents/contact.html templates/bottom.html > docs/contact.html


# Variables

TEMPLATE_DIR="templates"
CONTENT_DIR="contents"
TARGET_DIR="docs"


# NOTE: html files in the CONTENT_DIR MUST use the same html file name as final file name
for file_html in $( ls ${CONTENT_DIR} );
do
    TARGET_FILE=${TARGET_DIR}/${file_html}
    #echo "TARGET_FILE is ${TARGET_DIR}/${f_html}"
    #echo cat "${TEMPLATE_DIR}/top.html > ${TARGET_FILE}"
    #echo cat "${CONTENT_DIR}/${file_html} >> ${TARGET_FILE}"
    #echo cat "${TEMPLATE_DIR}/bottom.html >> ${TARGET_FILE}"

    cat ${TEMPLATE_DIR}/top.html > ${TARGET_FILE}
    cat ${CONTENT_DIR}/${file_html} >> ${TARGET_FILE}
    cat ${TEMPLATE_DIR}/bottom.html >> ${TARGET_FILE}
done
