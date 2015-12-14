
    function initDataTable(fixedHeader,fixedCol,searchable,changeDefaultSort,srchLabel,srchPlaceholder) {
        var tables = document.getElementsByTagName('table');
        
        // add table ids to a non-dynamic list (datatables will grow the # of tables as they're made dynamic)
        var ids = new Array(tables.length-1);
        for (var i = 0; i < tables.length; i++) {
            ids[i] = tables[i].id;
        }
        
        for (var j = 0; j < ids.length; j++) {
            makeDynamic(ids[j], fixedHeader, fixedCol, searchable, srchLabel, srchPlaceholder);
            if (changeDefaultSort) {
               chanageSort(ids[j]);
            }
        }
    }
        
    function makeDynamic(tblID, fixedHeader, fixedCol, searchable, srchLabel, srchPlaceholder) {
    
        var sLabel = srchLabel == '' ? 'Find Reading System(s) ' : srchLabel;
        var sPlaceholder = srchPlaceholder == '' ? 'Enter a name or operating system' : srchPlaceholder;
        
        var isMobile = window.matchMedia("only screen and (max-width: 760px)");
        
        var table;
        
        if (isMobile.matches) {
            $('#'+tblID).DataTable({
                "paging": false,
                "info": false,
                "stateSave": true,
                "responsive": {
                    "details": {
                        "display": $.fn.dataTable.Responsive.display.childRowImmediate,
                        "type": ''
                    }
                },
                "oLanguage": {
                    "sSearch": sLabel,
                    "sSearchPlaceholder": sPlaceholder
                }
            });
        }
        else {
            table = $('#'+tblID).DataTable({
                "paging": false,
                "info": false,
                "searching": searchable,
                "stateSave": true,
                "autoWidth": false,
                "scrollY": fixedCol ? "75vh" : false,
                "scrollX": fixedCol,
                "scrollCollapse": !fixedCol,
                "fixedColumns": fixedCol ? {
                    "leftColumns": 1
                } : null,
                "oLanguage": {
                    "sSearch": sLabel,
                    "sSearchPlaceholder": sPlaceholder
                }
            });
        }
        
        if (!isMobile.matches && fixedHeader) {
            new $.fn.dataTable.FixedHeader( table, {
                // options
            });
        }
    }
    
    function changeSort(tblID) {
        var oTable = $('#'+tblID).dataTable();
        var oSettings = oTable.fnSettings();
        var iColumns = oSettings.aoColumns.length - 1;
        
        for (var i = 0; i <= iColumns; i++) {
            var colName = oSettings.aoColumns[i].sTitle.toLowerCase();
            if (colName != '#' && colName != 'name' && colName != 'at' && colName != 'description') {
                oSettings.aoColumns[i].asSorting = ['desc','asc'];
            }
        }
    }
