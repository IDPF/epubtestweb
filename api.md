Site URIs
========

Manage
/manage

Reading System
/rs/$ID

Edit Reading System
/rs/$ID/edit

New Reading System
/rs/new/

Delete Reading System
/rs/$ID/delete

Web API
=======

Create reading system
POST /rs/

Edit reading system
UPDATE /rs/$ID/

DELETE /rs/$ID/

GET /rs/$ID/

GET (all) /rs/

Get partial evaluation
GET /rs/$ID/category/$ID/


XML Formats
=======
<evaluationRequest
    readingSystem="{ID}"
    testsuite="{ID}"/>


<evaluation id="{ID}">
    <readingSystem id="{ID}">
        <name>{NAME}</name>
        <version>{VERSION}</version>
        ...
    </readingSystem>
    <testsuite id="{ID}" timestamp="{TIMESTAMP}">
    <category id="{ID}">
        <name>{NAME}</name>
        <score passed="{PASSED}" total="{TOTAL}" percent="{PERCENT}"/>
        <result id="{ID}" result="{RESULT}">
            <test originalid="{ID}" required="{REQUIRED}">
                <description>{DESCRIPTION}</description>
            </test>
        </result>
        ...
        <category>
            ...
        </category>
    </category>
</evaluation>
