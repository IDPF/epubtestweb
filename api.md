Site URIs
========

Manage
/manage/

Reading System
/rs/$ID/

Edit Reading System details
/rs/$ID/edit/

Edit Reading System evaluation
/rs/$ID/eval/

New Reading System
/rs/new/

Delete Reading System
/rs/$ID/delete/

Data export
/export/


Proposed Web API (not implemented yet)
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

For POST/Get
------------

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


For data export
-------------

        <ts:evaluations xmlns:ts="http://idpf.org/ns/testsuite" testsuite="2013-10-01-2">
            <ts:evaluation last_updated="2013-10-01 22:19:34.238928+00:00">
                <ts:readingSystem locale="" sdk_version="" operating_system="c" version="b" name="a"/>
                <ts:results>
                    <ts:category score="100" name="Content Documents">
                        <ts:category score="100" name="EPUB 3.0 Test Suite: Document 0100">
                            <ts:category score="100" name="XHTML Content Documents">
                                <ts:result result="supported">
                                    <ts:test name="Inline Frames" testid="iframe-010"/>
                                </ts:result>
                                ...
                            </ts:category>
                            ...
                        </ts:category>
                        ...
                    </ts:category>
                    ...
                </ts:results>
            </ts:evaluation>
            ...
        </ts:evaluations>