Web API
=======

Create evaluation
POST /evaluations/

Edit evaluation
UPDATE /evaluations/$ID/

DELETE /evaluations/$ID/

GET /evaluations/$ID/

GET /evaluations/

Get partial evaluation
GET /evaluations/$ID/category/$ID/

Edit partial evaluation
UPDATE /evaluations/$ID/category/$ID/


Add reading system
POST /reading-systems/

Edit reading system
UPDATE /reading-systems/$ID/

DELETE /reading-systems/$ID/
GET /reading-systems/$ID/


Process
========
Create and populate evaluation
POST /evaluations/
GET /evaluation/$ID/
UPDATE /evaluation/$ID/


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
