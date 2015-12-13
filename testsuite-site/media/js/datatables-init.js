
    function initDataTable(fixed,searchable) {
        var tables = document.getElementsByTagName('table');
        
        // add table ids to a non-dynamic list (datatables will grow the # of tables as they're made dynamic)
        var ids = new Array(tables.length-1);
        for (var i = 0; i < tables.length; i++) {
            ids[i] = tables[i].id;
        }
        
        for (var j = 0; j < ids.length; j++) {
            makeDynamic(ids[j], fixed,searchable);
        }
    }
        
    function makeDynamic(tblID, fixed, searchable) {
    
        var isMobile = window.matchMedia("only screen and (max-width: 760px)");
        
        if (isMobile.matches) {
            $('#'+tblID).DataTable({
                "paging":   false,
                "info": false,
                "stateSave": true,
                "responsive": {
                    "details": {
                        "display": $.fn.dataTable.Responsive.display.childRowImmediate,
                        "type": ''
                    }
                },
                "oLanguage": {
                    "sSearch": "Find Reading System(s): ",
                    "sSearchPlaceholder": "Enter a name or operating system"
                }
            });
        }
        else {
            $('#'+tblID).DataTable({
                "paging":   false,
                "info": false,
                "searching": searchable,
                "fixedHeader": !fixed,
                "stateSave": true,
                "autoWidth": false,
                "scrollY": fixed ? "75vh" : false,
                "scrollX": fixed,
                "scrollCollapse": !fixed,
                "fixedColumns": fixed ? {
                    "leftColumns": 1
                } : null,
                "oLanguage": {
                    "sSearch": "Find Reading System(s): ",
                    "sSearchPlaceholder": "Enter a name or operating system"
                }
            });
        }
        
        // dynamically change sorting order so numeric fields are ordered from highest score first
        
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
